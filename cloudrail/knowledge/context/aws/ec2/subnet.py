from typing import List

from cloudrail.knowledge.context.aws.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.ec2.network_acl import NetworkAcl
from cloudrail.knowledge.context.aws.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.ec2.route_table import RouteTable


class Subnet(AwsResource):

    def __init__(self,
                 subnet_id: str,
                 vpc_id: str,
                 cidr_block: str,
                 name: str,
                 availability_zone: str,
                 map_public_ip_on_launch: bool,
                 region: str,
                 account: str,
                 is_default: bool = False,
                 tf_resource_type: AwsServiceName = AwsServiceName.AWS_SUBNET):
        super().__init__(account, region, tf_resource_type)
        self.subnet_id: str = subnet_id
        self.map_public_ip_on_launch = map_public_ip_on_launch
        self.vpc_id: str = vpc_id
        self.cidr_block: str = cidr_block
        self.name: str = name
        self.availability_zone: str = availability_zone
        self.is_default: bool = is_default

        self.route_table: RouteTable = None
        self.network_acl: NetworkAcl = None
        self.vpc: 'Vpc' = None
        self.aliases.add(subnet_id)

    def get_keys(self) -> List[str]:
        return [self.subnet_id]

    def get_id(self) -> str:
        return self.subnet_id

    def get_extra_data(self) -> str:
        vpc = 'vpc: {}'.format(self.vpc.get_friendly_name()) if self.vpc else ''
        network_acl = 'network_acl: {}'.format(self.network_acl.get_friendly_name()) if self.network_acl else ''
        return ', '.join([vpc, network_acl])

    def get_cloud_resource_url(self) -> str:
        return '{0}vpc/home?region={1}#SubnetDetails:subnetId={2}'\
            .format(self.AWS_CONSOLE_URL, self.region, self.subnet_id)

    def get_arn(self) -> str:
        pass

    @property
    def is_tagable(self) -> bool:
        return True
