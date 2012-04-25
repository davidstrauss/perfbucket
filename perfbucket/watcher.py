import os
import sys
import pyinotify
import analyzer

class ProcessProfilerEvent(pyinotify.ProcessEvent):
    def process_IN_CLOSE_WRITE(self, event):
        if event.name.endswith(".json"):
            base = os.path.splitext(os.path.join(event.path, event.name))[0]
            analyzer.analyze_profiling_result(base)

def monitor(directory):
    wm = pyinotify.WatchManager()
    notifier = pyinotify.Notifier(wm, ProcessProfilerEvent())
    mask = pyinotify.IN_CLOSE_WRITE  # Watched events
    wdd = wm.add_watch(directory, mask)
    
    while True:
        try:
            # process the queue of events as explained above
            notifier.process_events()
            if notifier.check_events():
                # read notified events and enqeue them
                notifier.read_events()
            # you can do some tasks here...
        except KeyboardInterrupt:
            # destroy the inotify's instance on this interrupt (stop monitoring)
            notifier.stop()
            break

if __name__ == '__main__':
    monitor(sys.argv[1])
