from typing import Optional, TypeVar, Type

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.ec2.network_acl import NetworkAcl
from cloudrail.knowledge.context.aws.ec2.network_interface import NetworkInterface
from cloudrail.knowledge.context.aws.ec2.subnet import Subnet
from cloudrail.knowledge.context.aws.ec2.vpc import Vpc
from cloudrail.knowledge.context.aws.networking_config.network_entity import NetworkEntity


_T = TypeVar('_T', bound=NetworkEntity)


def create_network_entity(_type: Type[_T], subnet: Optional[Subnet] = None) -> _T:
    instance: NetworkEntity = create_empty_entity(_type)
    if not subnet:
        subnet = create_empty_entity(Subnet)
        subnet.name = 'subnet-name'
    if not subnet.vpc:
        vpc = create_empty_entity(Vpc)
        subnet.vpc = vpc
    if not subnet.network_acl:
        nacl = create_empty_entity(NetworkAcl)
        nacl.name = 'network-acl-name'
        subnet.network_acl = nacl
    eni = create_empty_entity(NetworkInterface)
    eni.owner = instance
    eni.subnet = subnet
    instance.network_resource.add_interface(eni)
    return instance
