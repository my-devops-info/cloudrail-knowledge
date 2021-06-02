from typing import Optional, List
from cloudrail.knowledge.context.azure.azure_resources.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.azure_resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.azure_resources.web_app.auth_settings import AuthSettings


class AzureFunctionApp(AzureResource):

    def __init__(self, subscription_id: str, resource_group_name: str, location: str, name: str,
                 app_service_plan_id: str, storage_account_name: str, storage_account_access_key: str,
                 auth_settings: AuthSettings) -> None:
        super().__init__(subscription_id, resource_group_name, location,
                         'Microsoft.Web', AzureResourceType.AZURERM_FUNCTION_APP)
        self.name = name
        self.app_service_plan_id: str = app_service_plan_id
        self.storage_account_name: str = storage_account_name
        self.storage_account_access_key: str = storage_account_access_key
        self.auth_settings: AuthSettings = auth_settings
        self.with_aliases(name)

    def get_keys(self) -> List[str]:
        return [self.subscription_id, self.name, self.location]

    def get_name(self) -> str:
        return self.name

    def get_cloud_resource_url(self) -> Optional[str]:
        pass

    def get_friendly_name(self) -> str:
        return self.get_name()

    @property
    def is_tagable(self) -> bool:
        return True
