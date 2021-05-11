from typing import List, Optional
from cloudrail.knowledge.context.aws.networking_config.network_configuration import NetworkConfiguration
from cloudrail.knowledge.context.aws.networking_config.network_entity import NetworkEntity
from cloudrail.knowledge.context.aws.service_name import AwsServiceName


class BatchComputeEnvironment(NetworkEntity):

    def __init__(self,
                 compute_name: str,
                 arn: str,
                 account: str,
                 region: str,
                 vpc_config: NetworkConfiguration):
        super().__init__(compute_name, account, region, AwsServiceName.AWS_BATCH_COMPUTE_ENVIRONMENT)
        self.compute_name: str = compute_name
        self.arn: str = arn
        self.vpc_config: NetworkConfiguration = vpc_config

    def get_keys(self) -> List[str]:
        return [self.arn]

    def get_name(self) -> str:
        return self.compute_name

    def get_arn(self) -> str:
        return self.arn

    def get_all_network_configurations(self) -> Optional[List[NetworkConfiguration]]:
        if self.vpc_config:
            return [NetworkConfiguration(False,
                                         self.vpc_config.security_groups_ids,
                                         self.vpc_config.subnet_list_ids)]
        else:
            return []

    def get_cloud_resource_url(self) -> str:
        return '{0}batch/v2/home?region={1}#compute-environments/detail/{2}'\
            .format(self.AWS_CONSOLE_URL, self.region, self.arn)

    @property
    def is_tagable(self) -> bool:
        return True
