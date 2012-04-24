import pycassa
import time
import datetime
import json
import uuid

KEYSPACE = "perfbucket"

cassandra_pool = None
def _get_cassandra_connection():
    global cassandra_pool
    if cassandra_pool is None:
        cassandra_pool = pycassa.pool.ConnectionPool(KEYSPACE)
    return cassandra_pool

def _jsonify(fields):
    jsonified = {}
    for key, value in fields.items():
        jsonified[key] = json.dumps(value)
    return jsonified

def _unjsonify(fields):
    unjsonified = {}
    for key, value in fields.items():
        unjsonified[key] = json.loads(value)
    return unjsonified

def get_time_uuids(now=None):
    if now is None:
        now = time.time()
  
    result = {}
    result["unique"] = pycassa.util.convert_time_to_uuid(now, randomize=True)
    result["hour"] = pycassa.util.convert_time_to_uuid(int(now) / 60 / 60)
    
    return result
    
def get_worst(timestamp, minimum=5000000, max_count=100):
    pool = _get_cassandra_connection()
    data_cf = pycassa.ColumnFamily(pool, "profiling_data")
    metadata_cf = pycassa.ColumnFamily(pool, "profiling_metadata")
    worst_cf = pycassa.ColumnFamily(pool, "profiling_worst_by_hour")

    minimum_column = (minimum, "")
    hour_uuid = get_time_uuids(timestamp)["hour"]
    
    results = {}
    try:
        results = _unjsonify(worst_cf.get(hour_uuid, column_finish=minimum_column, column_count=max_count))
        for name, value in results.iteritems():
            results[name]["run_uuid"] = uuid.UUID(value["run_uuid"])
    except pycassa.cassandra.ttypes.NotFoundException:
        pass
    
    return results
    
def get_profiling_details(run_uuid):
    pool = _get_cassandra_connection()
    data_cf = pycassa.ColumnFamily(pool, "profiling_data")
    metadata_cf = pycassa.ColumnFamily(pool, "profiling_metadata")
    
    data = dict(_unjsonify(data_cf.get(run_uuid)))
    metadata = dict(_unjsonify(metadata_cf.get(run_uuid)))
    
    return {"data": data, "metadata": metadata}

def get_page_from_metadata(metadata):
    return "{0}?{1}".format(metadata["SERVER"]["SCRIPT_NAME"], metadata["SERVER"]["QUERY_STRING"])

def get_duration_from_data(data):
    return int(data["main()"]["wt"])

def save_profiling_result(data, metadata):
    pool = _get_cassandra_connection()
    data_cf = pycassa.ColumnFamily(pool, "profiling_data")
    metadata_cf = pycassa.ColumnFamily(pool, "profiling_metadata")
    worst_cf = pycassa.ColumnFamily(pool, "profiling_worst_by_hour")

    uuids = get_time_uuids()
    data_cf.insert(uuids["unique"], _jsonify(data))
    metadata_cf.insert(uuids["unique"], _jsonify(metadata))

    duration = get_duration_from_data(data)
    value = {"run_uuid": str(uuids["unique"]),
             "page": get_page_from_metadata(metadata),
             "duration": duration}
    worst_data = {(duration, str(uuids["unique"])): value}
    worst_cf.insert(uuids["hour"], _jsonify(worst_data))
