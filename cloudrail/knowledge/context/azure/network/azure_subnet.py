from typing import List, Optional

from cloudrail.knowledge.context.azure.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.constants.azure_resource_type import AzureResourceType


class AzureSubnet(AzureResource):
    """
        Attributes:
            subnet_id: The subnet id.
    """

    def __init__(self, subnet_id: str):
        super().__init__(AzureResourceType.AZURERM_NETWORK_SECURITY_GROUP)
        self.subnet_id: str = subnet_id
        self.with_aliases(subnet_id)

    def get_cloud_resource_url(self) -> Optional[str]:
        pass

    @property
    def is_tagable(self) -> bool:
        return False

    def get_keys(self) -> List[str]:
        return [self.subnet_id]

    def get_id(self) -> str:
        return self.subnet_id
