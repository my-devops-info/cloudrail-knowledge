from typing import List, Optional

from cloudrail.knowledge.context.azure.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.constants.azure_resource_type import AzureResourceType


class AzureNic(AzureResource):
    """
        Attributes:
            subscription_id: The subscription id.
            nic_id: The network interface id.
            resource_group_name: Resource group name whcih the NIC belongs to.
            location: Azure location.
    """

    def __init__(self, subscription_id: str, nic_id: str, resource_group_name: str, location: str):
        super().__init__(subscription_id, resource_group_name, location, AzureResourceType.AZURERM_NETWORK_INTERFACE)
        self.subscription_id: str = subscription_id
        self.nic_id: str = nic_id
        self.resource_group_name = resource_group_name
        self.with_aliases(nic_id)

    def get_cloud_resource_url(self) -> Optional[str]:
        pass

    @property
    def is_tagable(self) -> bool:
        return False

    def get_keys(self) -> List[str]:
        return [self.nic_id]

    def get_id(self) -> str:
        return self.nic_id
