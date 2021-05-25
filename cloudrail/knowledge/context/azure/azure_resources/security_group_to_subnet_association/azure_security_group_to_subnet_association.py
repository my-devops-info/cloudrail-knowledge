from typing import List, Optional

from cloudrail.knowledge.context.azure.azure_resources.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.azure_resources.constants.azure_resource_type import AzureResourceType


class AzureSecurityGroupToSubnetAssociation(AzureResource):

    def __init__(self, subscription_id: str, subnet_id: str, security_group_id: str):
        super().__init__(subscription_id, None, None, AzureResourceType.AZURERM_SUBNET_NETWORK_SECURITY_GROUP_ASSOCIATION)
        self.subscription_id: str = subscription_id
        self.subnet_id: str = subnet_id
        self.security_group_id = security_group_id

    def get_cloud_resource_url(self) -> Optional[str]:
        pass

    def get_friendly_name(self) -> str:
        pass

    @property
    def is_tagable(self) -> bool:
        return False

    def get_keys(self) -> List[str]:
        return [self.subscription_id, self.subnet_id, self.security_group_id]
