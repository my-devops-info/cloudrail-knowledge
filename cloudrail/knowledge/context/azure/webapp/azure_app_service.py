from typing import Optional, List
from cloudrail.knowledge.context.azure.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.webapp.constants import FtpsState


class AzureAppService(AzureResource):
    """
        Attributes:
            name: The name of this AppService
            ftps_state: The FTPS state of this AppService config. Either AllAllowed, FTPSOnly or Disabled
    """
    def __init__(self, name: str, ftps_state: FtpsState) -> None:
        super().__init__(AzureResourceType.AZURERM_APP_SERVICE)
        self.name: str = name
        self.ftps_state: FtpsState = ftps_state

    def get_keys(self) -> List[str]:
        return [self.get_name()]

    def get_name(self) -> str:
        return self.name

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'https://portal.azure.com/#@{self.tenant_id}/resource/subscriptions/{self.subscription_id}/resourceGroups/' \
               f'{self.resource_group_name}/providers/Microsoft.Web/sites/{self.name}/appServices'

    @property
    def is_tagable(self) -> bool:
        return True
