from enum import IntEnum
from typing import List


class KnownPorts(IntEnum):
    SSH: int = 22
    RDP: int = 3389
    ORACLE_DB_DEFAULT: int = 1521
    ORACLE_DB: int = 2483
    ORACLE_DB_SSL: int = 2484
    MYSQL: int = 3306
    POSTGRES: int = 5432
    REDIS: int = 6379
    MONGODB: int = 27017
    MONGODB_SHARD_CLUSTER: int = 27018
    CASSANDRA: int = 7199
    CASSANDRA_THRIFT: int = 9160
    CASSANDRA_MNG: int = 8888
    MEMCACHED: int = 11211
    ELASTICSEARCH_NODES: int = 9300
    ELASTICSEARCH: int = 9200
    KIBANA: int = 5601
    ALL: int = -1


def get_values() -> List[KnownPorts]:
    return list(KnownPorts)
