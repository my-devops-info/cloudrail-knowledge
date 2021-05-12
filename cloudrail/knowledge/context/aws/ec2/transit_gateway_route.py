from enum import Enum
from typing import List

from cloudrail.knowledge.context.aws.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.ec2.transit_gateway_vpc_attachment import TransitGatewayVpcAttachment


class TransitGatewayRouteState(Enum):
    ACTIVE = 'active'
    BLACKHOLE = 'blackhole'


class TransitGatewayRouteType(Enum):
    STATIC = "static"
    PROPAGATED = "propagated"


class TransitGatewayRoute(AwsResource):

    def __init__(self,
                 destination_cidr_block: str,
                 state: TransitGatewayRouteState,
                 route_type: TransitGatewayRouteType,
                 attachment_ids: List[str],
                 route_table_id: str,
                 region: str,
                 account: str):
        super().__init__(account, region, AwsServiceName.AWS_TRANSIT_GATEWAY_ROUTE)
        self.destination_cidr_block: str = destination_cidr_block
        self.state: TransitGatewayRouteState = state
        self.route_type: TransitGatewayRouteType = route_type
        self.attachment_ids: List[str] = attachment_ids
        self.route_table_id: str = route_table_id
        self.vpc_attachment: TransitGatewayVpcAttachment = None

    def get_keys(self) -> List[str]:
        return [self.route_table_id,
                self.destination_cidr_block,
                self.attachment_ids]

    def get_extra_data(self) -> str:
        destination_cidr_block = 'destination_cidr_block: {}'.format(self.destination_cidr_block) if self.destination_cidr_block else ''
        attachment_ids = 'attachment_ids: {}'.format(self.attachment_ids) if self.attachment_ids else ''
        route_table_id = 'route_table_id: {}'.format(self.route_table_id) if self.route_table_id else ''

        return ', '.join([destination_cidr_block, attachment_ids, route_table_id])

    def get_cloud_resource_url(self) -> str:
        return '{0}vpc/home?region={1}#TransitGatewayRouteTables:transitGatewayRouteTableId={2}'\
            .format(self.AWS_CONSOLE_URL, self.region, self.route_table_id)

    def get_arn(self) -> str:
        pass

    @property
    def is_tagable(self) -> bool:
        return False
