from typing import List

from cloudrail.knowledge.context.aws.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.service_name import AwsServiceName


class ElastiCacheReplicationGroup(AwsResource):

    def __init__(self,
                 replication_group_id: str,
                 encrypted_at_rest: bool,
                 encrypted_in_transit: bool,
                 region: str,
                 account: str):
        super().__init__(account, region, AwsServiceName.AWS_ELASTICACHE_REPLICATION_GROUP)
        self.replication_group_id: str = replication_group_id
        self.encrypted_at_rest: bool = encrypted_at_rest
        self.encrypted_in_transit: bool = encrypted_in_transit

    def get_keys(self) -> List[str]:
        return [self.replication_group_id]

    def get_name(self) -> str:
        return self.replication_group_id

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'ElastiCache Replication Group'
        else:
            return 'ElastiCache Replication Groups'

    def get_cloud_resource_url(self) -> str:
        return '{0}elasticache/home?region={1}#redis-group-nodes:id={2};clusters'\
            .format(self.AWS_CONSOLE_URL, self.region, self.replication_group_id)

    def get_arn(self) -> str:
        pass

    @property
    def is_tagable(self) -> bool:
        return False
