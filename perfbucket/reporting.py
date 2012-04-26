import storage
import pprint
import time
import datetime

def print_hour(timestamp):
    print("")
    rounded_to_hour = int(timestamp / 60 / 60) * 60 * 60
    print(datetime.datetime.utcfromtimestamp(rounded_to_hour).isoformat())

# All paths slower than "N" (5000 milliseconds)

def slowest_requests_by_hour(begin=None, hours=24, verbose=False):
    print("Slowest Requests by Hour")

    if begin is None:
        begin = time.time()
    for hours_ago in range(0, hours):
        timestamp = begin - hours_ago * 60 * 60
        results = storage.get_worst(timestamp)
        if len(results) > 0:
            print_hour(timestamp)
            for name, value in results.iteritems():
                request_uuid = value["request_uuid"]
                print("  Request UUID: %s" % request_uuid)
                print("    Duration: {0} milliseconds".format(value["duration"] / 1000))
                print("    Page: {0}".format(value["page"]))

# Top 20 slowest by average wall time (weighted by popularity?)

def _slowest_pages_on_average_for_hour(timestamp, top, min_count, verbose):
    pages = {}
    results = storage.get_worst(timestamp, max_count=10000)
    for name, value in results.iteritems():
        current = pages.get(value["page"], {"count": 0, "duration": 0, "requests": {}})
        current["requests"][value["duration"]] = str(value["request_uuid"])
        pages[value["page"]] = {"count": current["count"] + 1,
                                "duration": current["count"] + value["duration"],
                                "requests": current["requests"]}

    ordered_pages = {}
    for page, data in pages.iteritems():
        if data["count"] >= min_count:
            ordered_pages[(data["duration"], page)] = data

    if len(ordered_pages) == 0:
        return
    print_hour(timestamp)

    displayed = 0
    for key in reversed(sorted(ordered_pages.keys())):
        (average_duration, page) = key
        value = pages[page]
        print("  Page: {0}".format(page))
        print("    Count: {0}".format(value["count"]))
        print("    Average duration: {0} milliseconds".format(average_duration / 1000))
        if verbose:
            print("    Worst requests (showing up to ten):")

            requests_displayed = 0
            for duration in reversed(sorted(value["requests"].keys())):
                print("      {0}".format(value["requests"][duration]))
                requests_displayed += 1
                if requests_displayed == 10:
                    break

            displayed += 1
            if displayed == top:
                break

def slowest_pages_on_average_by_hour(begin=None, hours=24, top=50, min_count=2, verbose=False):
    print("Slowest Pages on Average by Hour")
    if begin is None:
        begin = time.time()
    for hours_ago in range(0, hours):
        timestamp = begin - hours_ago * 60 * 60
        _slowest_pages_on_average_for_hour(timestamp, top, min_count, verbose)

if __name__ == '__main__':
    slowest_requests_by_hour()
    print("")
    slowest_pages_on_average_by_hour()
