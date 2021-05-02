from typing import List, Optional

from cloudrail.knowledge.context.aws.ecs.ecs_target import EcsTarget
from cloudrail.knowledge.context.aws.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.service_name import AwsServiceName


class CloudWatchEventTarget(AwsResource):

    def __init__(self,
                 account: str,
                 region: str,
                 name: str,
                 rule_name: str,
                 target_id: str,
                 role_arn: str,
                 cluster_arn: str,
                 ecs_target_list: List[EcsTarget]) -> None:
        super().__init__(account, region, AwsServiceName.AWS_CLOUD_WATCH_EVENT_TARGET)
        self.name: str = name
        self.rule_name: str = rule_name
        self.target_id: str = target_id
        self.role_arn: str = role_arn
        self.cluster_arn: str = cluster_arn
        self.ecs_target_list: List[EcsTarget] = ecs_target_list

    def get_keys(self) -> List[str]:
        return [self.rule_name, self.cluster_arn]

    def get_type(self, is_plural: bool = False) -> str:
        if is_plural:
            return 'CloudWatch Event Target'
        else:
            return "CloudWatch Event Targets"

    def get_arn(self) -> str:
        return self.cluster_arn

    def get_cloud_resource_url(self) -> Optional[str]:
        return '{0}cloudwatch/home?{1}#rules:name={2}'\
            .format(self.AWS_CONSOLE_URL, self.region, self.rule_name)

    @property
    def is_tagable(self) -> bool:
        return False
