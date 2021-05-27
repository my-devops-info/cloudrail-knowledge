from typing import List, Optional

from cloudrail.knowledge.context.azure.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.constants.azure_resource_type import AzureResourceType


class AzureSubnet(AzureResource):
    """
        Attributes:
            subscription_id: The subscription id.
            subnet_id: The subnet id.
            resource_group: Resource group name whcih the NSG belongs to.
    """

    def __init__(self, subscription_id: str, subnet_id: str, resource_group: str):
        super().__init__(subscription_id, resource_group, None, AzureResourceType.AZURERM_NETWORK_SECURITY_GROUP)
        self.subscription_id: str = subscription_id
        self.subnet_id: str = subnet_id
        self.resource_group = resource_group
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
