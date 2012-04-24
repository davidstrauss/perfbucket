import storage
import pprint
import time
import datetime

def print_profiling_details(run_uuid):
    run = storage.get_profiling_details(run_uuid)
    duration = int(run["data"]["main()"]["wt"]) / 1000
    page = "{0}?{1}".format(run["metadata"]["SERVER"]["SCRIPT_NAME"], run["metadata"]["SERVER"]["QUERY_STRING"])
    print("    Duration: {0} milliseconds".format(duration))
    print("    Page: {0}".format(page))

def print_hour(timestamp):
    rounded_to_hour = int(timestamp / 60 / 60) * 60 * 60
    print(datetime.datetime.utcfromtimestamp(rounded_to_hour).isoformat())  

# All paths slower than "N" (5000 milliseconds)

def hourly_report(begin=None):
    if begin is None:
        begin = time.time()
    for hours_ago in range(0, 24):
        timestamp = begin - hours_ago * 60 * 60
        print_hour(timestamp)
        results = storage.get_worst(timestamp)
        for key, value in results.iteritems():
            print("  Run ID: %s" % value)
            print_profiling_details(value)
            #pprint.pprint(result)

# Top 20 slowest by average wall time (weighted by popularity?)



if __name__ == '__main__':
    hourly_report()
