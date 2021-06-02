from typing import Optional, List
from cloudrail.knowledge.context.azure.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.constants.azure_resource_type import AzureResourceType


class AzureNetworkSecurityGroup(AzureResource):
    """
        Attributes:
            name: The NSG name
            network_interface_ids: List of network interface ids which the NSG connected to (if any)
            subnet_ids: List of subnet ids which the NSG connected to (if any)
    """

    def __init__(self,
                 name: str,
                 network_interface_ids: Optional[List[str]] = None,
                 subnet_ids: Optional[List[str]] = None) -> None:
        super().__init__(AzureResourceType.AZURERM_NETWORK_SECURITY_GROUP)
        self.name: str = name

        self.network_interface_ids: List[str] = network_interface_ids or []
        self.subnet_ids: List[str] = subnet_ids or []

        self.subnets: List['AzureSubnet'] = []
        self.network_interfaces: List['AzureNic'] = []

    def get_keys(self) -> List[str]:
        return [self.get_id()]

    def get_name(self) -> str:
        return self.name

    def get_cloud_resource_url(self) -> Optional[str]:
        pass

    def get_friendly_name(self) -> str:
        return self.get_name()

    @property
    def is_tagable(self) -> bool:
        return True

    def exclude_from_invalidation(self) -> list:
        return [self.subnets, self.network_interfaces]
