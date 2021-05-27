from typing import Optional, List
from cloudrail.knowledge.context.azure.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.constants.azure_resource_type import AzureResourceType


class AzureNetworkSecurityGroup(AzureResource):
    """
        Attributes:
            subscription_id: The subscription id.
            security_group_id: The network security group id.
            resource_group_name: Resource group name whcih the NSG belongs to.
            location: Azure location.
            name: The NSG name
            network_interfaces: List of network interfaces which the NSG connected to (if any)
            subnets: List of subnets which the NSG connected to (if any)
    """

    def __init__(self, subscription_id: str, security_group_id: str, resource_group_name: str, location: str, name: str,
                network_interfaces=None,
                subnets=None) -> None:
        super().__init__(subscription_id, resource_group_name, location, AzureResourceType.AZURERM_NETWORK_SECURITY_GROUP)
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
