import pycassa
import storage

def _create_cf(sm, keyspace_name, cf, comparator_type, default_validation_class, key_validation_class):
    try:
        sm.create_column_family(keyspace_name, cf,
                   comparator_type=comparator_type,
                   default_validation_class=default_validation_class,
                   key_validation_class=key_validation_class)
    except pycassa.cassandra.ttypes.InvalidRequestException as e:
        print e.why
        pass

def _create_index(sm, keyspace_name, cf, column, type):
    try:
        sm.create_index(keyspace_name, cf, column, type)

    except pycassa.cassandra.c10.ttypes.InvalidRequestException as e:
        print e.why
        pass

def install(keyspace_name, update=False, drop_first=False, rf=1):
    """Function to install or update the keyspace.

    update      If true, doesn't try to recreate the keyspace, meaning you can
                safely ignore the rf variable.
    drop_first  Drop the schema and reinstall.
    rf          The replication factor for new or reinstalled schemas.
    """

    sm = pycassa.system_manager.SystemManager("127.0.0.1:9160")

    # Drop the keyspaces first, if requested.
    if drop_first:
        props = None
        try:
            props = sm.get_keyspace_properties(keyspace_name)
        except pycassa.cassandra.ttypes.NotFoundException:
            pass
        if props is not None:
            sm.drop_keyspace(keyspace_name)

    if drop_first or not update:
        sm.create_keyspace(keyspace_name, pycassa.system_manager.SIMPLE_STRATEGY, {'replication_factor': str(rf)})

    _create_cf(sm, keyspace_name, "profiling_data",
               comparator_type=pycassa.types.UTF8Type(),
               key_validation_class=pycassa.types.TimeUUIDType(),
               default_validation_class=pycassa.types.UTF8Type())

    _create_cf(sm, keyspace_name, "profiling_metadata",
               comparator_type=pycassa.types.UTF8Type(),
               key_validation_class=pycassa.types.TimeUUIDType(),
               default_validation_class=pycassa.types.UTF8Type())

    t = pycassa.types.CompositeType(pycassa.types.IntegerType(reversed=True), pycassa.types.UTF8Type())
    _create_cf(sm, keyspace_name, "profiling_worst_by_hour",
               comparator_type=t,
               key_validation_class=pycassa.types.TimeUUIDType(),
               default_validation_class=pycassa.types.UTF8Type())

if __name__ == '__main__':
    install(storage.KEYSPACE, drop_first=True)
