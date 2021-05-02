from typing import List, Optional

from cloudrail.knowledge.context.aws.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.aws_resource import AwsResource


class LoadBalancerTargetGroupAssociation(AwsResource):

    def __init__(self, target_group_arns: List[str], load_balancer_arn: str, port: int, account: str, region: str):
        super().__init__(account, region, AwsServiceName.AWS_LOAD_BALANCER_LISTENER)
        self.target_group_arns: List[str] = target_group_arns
        self.load_balancer_arn: str = load_balancer_arn
        self.port: int = port

    def get_keys(self) -> List[str]:
        return self.target_group_arns + [self.load_balancer_arn]

    def get_cloud_resource_url(self) -> Optional[str]:
        return '{0}ec2/v2/home?region={1}#LoadBalancers:type=application'\
            .format(self.AWS_CONSOLE_URL, self.region)

    def get_arn(self) -> str:
        pass

    @property
    def is_tagable(self) -> bool:
        return False
