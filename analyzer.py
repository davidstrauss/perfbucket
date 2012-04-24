import phpserialize
import json
import storage

import sys
import pprint

def analyze_profiling_result(base_name):
    data = None
    with open(base_name + ".xhprof_testing") as f:
        data = phpserialize.load(f)

    metadata = None
    with open(base_name + ".json") as f:
        metadata = json.load(f)

    storage.save_profiling_result(data, metadata)

    pprint.pprint(data)
    pprint.pprint(metadata)

if __name__ == '__main__':
    analyze_profiling_result(sys.argv[1])
