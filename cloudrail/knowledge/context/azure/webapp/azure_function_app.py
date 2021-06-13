from typing import Optional, List

from cloudrail.knowledge.context.azure.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.webapp.auth_settings import AuthSettings
from cloudrail.knowledge.context.azure.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.webapp.constants import FieldMode


class AzureFunctionApp(AzureResource):
    """
        Attributes:
            name: Function app resource name.
            auth_settings: Function app authentication settings.
    """
    def __init__(self, name: str, auth_settings: AuthSettings, client_cert_mode: FieldMode = None) -> None:
        super().__init__(AzureResourceType.AZURERM_FUNCTION_APP)
        self.name = name
        self.auth_settings: AuthSettings = auth_settings
        self.client_cert_mode: FieldMode = client_cert_mode
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
