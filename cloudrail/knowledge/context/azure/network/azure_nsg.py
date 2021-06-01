from typing import Optional, List
from cloudrail.knowledge.context.azure.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.network.azure_nic import AzureNic
from cloudrail.knowledge.context.azure.network.azure_subnet import AzureSubnet


class AzureNetworkSecurityGroup(AzureResource):
    """
        Attributes:
            security_group_id: The network security group id.
            name: The NSG name
            network_interfaces: List of network interfaces which the NSG connected to (if any)
            subnets: List of subnets which the NSG connected to (if any)
    """

    def __init__(self, security_group_id: str,
                 name: str,
                 network_interfaces: AzureNic = None,
                 subnets: AzureSubnet = None) -> None:
        super().__init__(AzureResourceType.AZURERM_NETWORK_SECURITY_GROUP)
        self.security_group_id: str = security_group_id
        self.name: str = name
        self.with_aliases(security_group_id)
        self.subnets = subnets or []
        self.network_interfaces = network_interfaces or []

    def get_keys(self) -> List[str]:
        return [self.security_group_id]

    def get_id(self) -> str:
        return self.security_group_id

    def get_name(self) -> str:
        return self.name

    def get_cloud_resource_url(self) -> Optional[str]:
        pass

    def get_friendly_name(self) -> str:
        return self.get_name()

    @property
    def is_tagable(self) -> bool:
        return True
