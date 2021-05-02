from enum import Enum


class TransitGatewayResourceType(Enum):
    vpc = 'vpc'
    vpn = 'vpn'
    peering = 'peering'
