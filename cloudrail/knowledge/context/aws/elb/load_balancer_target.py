from typing import List, Optional

from cloudrail.knowledge.context.aws.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.aws_resource import AwsResource


class LoadBalancerTarget(AwsResource):

    def __init__(self, target_group_arn: str, target_health, target_id: str, port: int, account: str, region: str):
        super().__init__(account, region, AwsServiceName.AWS_LOAD_BALANCER_TARGET_GROUP_ATTACHMENT)
        self.target_group_arn: str = target_group_arn
        self.target_health = target_health
        self.target_id: str = target_id
        self.port: int = port
        self.target_instance = None

    def get_keys(self) -> List[str]:
        return [self.target_group_arn, self.target_id]

    def get_cloud_resource_url(self) -> Optional[str]:
        return '{0}ec2/v2/home?region={1}#TargetGroup:targetGroupArn={2}'\
            .format(self.AWS_CONSOLE_URL, self.region, self.target_group_arn)

    def get_arn(self) -> str:
        return self.target_group_arn

    @property
    def is_tagable(self) -> bool:
        return False
