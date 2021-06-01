from typing import List, Optional

from cloudrail.knowledge.context.azure.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.constants.azure_resource_type import AzureResourceType


class AzureNic(AzureResource):
    """
        Attributes:
            nic_id: The network interface id.
    """

    def __init__(self, nic_id: str):
        super().__init__(AzureResourceType.AZURERM_NETWORK_INTERFACE)
        self.nic_id: str = nic_id
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
