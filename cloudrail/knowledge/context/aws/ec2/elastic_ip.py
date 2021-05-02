from typing import List, Optional

from cloudrail.knowledge.context.aws.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.aws_resource import AwsResource


class ElasticIp(AwsResource):

    def __init__(self, allocation_id: str, public_ip: Optional[str], private_ip: Optional[str], region: str, account: str):
        super().__init__(account, region, AwsServiceName.AWS_ELASTIC_IP)
        self.allocation_id: str = allocation_id
        self.public_ip: str = public_ip or "0.0.0.0"
        self.private_ip: Optional[str] = private_ip

    def get_keys(self) -> List[str]:
        return [self.allocation_id]

    def get_id(self) -> str:
        return self.allocation_id

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'Elastic IP address'
        else:
            return 'Elastic IP addresses'

    def get_cloud_resource_url(self) -> str:
        return '{0}vpc/home?region={1}#Addresses:public-ip={2}'\
            .format(self.AWS_CONSOLE_URL, self.region, self.public_ip)

    def get_arn(self) -> str:
        pass

    @property
    def is_tagable(self) -> bool:
        return True
