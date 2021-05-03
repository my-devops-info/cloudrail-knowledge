from typing import Optional, List
from cloudrail.knowledge.context.azure.azure_resources.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.azure_resources.constants.azure_resource_type import AzureResourceType


class AzureSqlServer(AzureResource):

    def __init__(self, subscription_id: str, resource_group_name: str, location: str,
                 server_name: str, public_network_access_enable: bool) -> None:
        super().__init__(subscription_id, resource_group_name, location,
                         'Microsoft.Sql/servers', AzureResourceType.AZURERM_SQL_SERVER)
        self.server_name: str = server_name
        self.with_aliases(server_name)
        self.public_network_access_enable: bool = public_network_access_enable

    def get_keys(self) -> List[str]:
        return [self.get_name()]

    def get_name(self) -> str:
        return self.server_name

    def get_cloud_resource_url(self) -> Optional[str]:
        pass

    def get_friendly_name(self) -> str:
        return self.get_name()

    @property
    def is_tagable(self) -> bool:
        return True
