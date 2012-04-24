import pycassa
import time
import datetime
import json

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
    
def get_worst(timestamp, minimum_ms=5000):
    pool = _get_cassandra_connection()
    data_cf = pycassa.ColumnFamily(pool, "profiling_data")
    metadata_cf = pycassa.ColumnFamily(pool, "profiling_metadata")
    worst_cf = pycassa.ColumnFamily(pool, "profiling_worst_by_hour")

    minimum_column = (minimum_ms * 1000, "")
    hour_uuid = get_time_uuids(timestamp)["hour"]
    
    results = {}
    try:
        results = worst_cf.get(hour_uuid, column_finish=minimum_column, column_count=100)
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

def save_profiling_result(data, metadata):
    pool = _get_cassandra_connection()
    data_cf = pycassa.ColumnFamily(pool, "profiling_data")
    metadata_cf = pycassa.ColumnFamily(pool, "profiling_metadata")
    worst_cf = pycassa.ColumnFamily(pool, "profiling_worst_by_hour")

    uuids = get_time_uuids()
    data_cf.insert(uuids["unique"], _jsonify(data))
    metadata_cf.insert(uuids["unique"], _jsonify(metadata))

    duration = int(data["main()"]["wt"])
    worst_data = {(duration, str(uuids["unique"])): uuids["unique"]}
    worst_cf.insert(uuids["hour"], worst_data)
