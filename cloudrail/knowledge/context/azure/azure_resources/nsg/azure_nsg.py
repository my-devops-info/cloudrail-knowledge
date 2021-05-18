from typing import Optional, List
from cloudrail.knowledge.context.azure.azure_resources.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.azure_resources.constants.azure_resource_type import AzureResourceType

class AzureNetworkSecurityGroup(AzureResource):

    def __init__(self, subscription_id: str, resource_group_name: str, location: str, name: str,
                network_interfaces=None,
                subnets=None) -> None:
        super().__init__(subscription_id, resource_group_name, location,
                         'Microsoft.Network/networkSecurityGroups', AzureResourceType.AZURERM_NETWORK_SECURITY_GROUP)
        self.name = name
        self.with_aliases(name)
        self.subnets = subnets or []
        self.network_interfaces = network_interfaces or []

    def get_keys(self) -> List[str]:
        return [self.get_name()]

    def get_name(self) -> str:
        return self.name

    def get_cloud_resource_url(self) -> Optional[str]:
        pass

    def get_friendly_name(self) -> str:
        return self.get_name()

    @property
    def is_tagable(self) -> bool:
        return True
