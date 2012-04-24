import storage
import pprint
import time
import datetime

def print_hour(timestamp):
    rounded_to_hour = int(timestamp / 60 / 60) * 60 * 60
    print(datetime.datetime.utcfromtimestamp(rounded_to_hour).isoformat())  

# All paths slower than "N" (5000 milliseconds)

def slowest_requests_by_hour(begin=None, hours=24):
    print("Slowest Requests by Hour")
  
    if begin is None:
        begin = time.time()
    for hours_ago in range(0, hours):
        timestamp = begin - hours_ago * 60 * 60
        print_hour(timestamp)
        results = storage.get_worst(timestamp)
        for name, value in results.iteritems():
            run_uuid = value["run_uuid"]
            print("  Run ID: %s" % run_uuid)
            print("    Duration: {0} milliseconds".format(value["duration"] / 1000))
            print("    Page: {0}".format(value["page"]))

# Top 20 slowest by average wall time (weighted by popularity?)

def _slowest_pages_on_average_for_hour(timestamp, top=50):
    pages = {}
    results = storage.get_worst(timestamp, max_count=10000)
    for name, value in results.iteritems():
        current = pages.get(value["page"], {"count": 0, "duration": 0})
        pages[value["page"]] = {"count": current["count"] + 1,
                                "duration": current["count"] + value["duration"]}
                                    
    ordered_pages = {}
    for page, data in pages.iteritems():
        ordered_pages[(data["duration"], page)] = data

    displayed = 0
    for key in reversed(sorted(ordered_pages.keys())):
        (average_duration, page) = key
        value = pages[page]
        print("  Page: {0}".format(page))
        print("    Count: {0}".format(value["count"]))
        print("    Average duration: {0} milliseconds".format(average_duration / 1000))
        displayed += 1
        if displayed == top:
            return

def slowest_pages_on_average_by_hour(begin=None, hours=24, top=50):
    print("Slowest Pages on Average by Hour")
    if begin is None:
        begin = time.time()
    for hours_ago in range(0, hours):
        timestamp = begin - hours_ago * 60 * 60
        print_hour(timestamp)
        _slowest_pages_on_average_for_hour(timestamp, top)

if __name__ == '__main__':
    slowest_requests_by_hour()
    print("")
    slowest_pages_on_average_by_hour()
