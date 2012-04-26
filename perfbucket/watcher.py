# This file is part of perfbucket.
#
# perfbucket is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# perfbucket is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with perfbucket.  If not, see <http://www.gnu.org/licenses/>.

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
