import storage
import uuid
import phpserialize
import sys

def get_xhprof_data(request_uuid):
    details = storage.get_profiling_details(request_uuid)
    return phpserialize.dumps(details["data"])

print(get_xhprof_data(uuid.UUID(sys.argv[1])))
