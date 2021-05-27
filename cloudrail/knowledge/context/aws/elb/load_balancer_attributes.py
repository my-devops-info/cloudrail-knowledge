from typing import List

from cloudrail.knowledge.context.aws.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.service_name import AwsServiceName


class LoadBalancerAttributes(AwsResource):
    """
        Attributes:
            load_balancer_arn: The ARN of the load balancer.
            drop_invalid_header_fields: An indication if the application load balancer remove invalid http headers or send to the targets as is.
    """
    def __init__(self,
                 account: str,
                 region: str,
                 load_balancer_arn: str,
                 drop_invalid_header_fields: bool):
        super().__init__(account, region, AwsServiceName.AWS_LOAD_BALANCER)
        self.load_balancer_arn: str = load_balancer_arn
        self.drop_invalid_header_fields: bool = drop_invalid_header_fields

    def get_keys(self) -> List[str]:
        return [self.load_balancer_arn, 'attributes']

    def get_arn(self) -> str:
        pass

    def get_cloud_resource_url(self) -> str:
        return '{0}ec2/v2/home?region={1}#LoadBalancers' \
            .format(self.AWS_CONSOLE_URL, self.region)

    @property
    def is_tagable(self) -> bool:
        return False
