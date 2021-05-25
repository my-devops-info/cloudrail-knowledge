from abc import abstractmethod
from typing import Optional, List
from cloudrail.knowledge.context.mergeable import Mergeable

from cloudrail.knowledge.context.azure.azure_resources.constants.azure_resource_type import AzureResourceType


class AzureResource(Mergeable):

    def __init__(self, subscription_id: str, resource_group_name: Optional[str], location: str, resource_type: AzureResourceType):
        super().__init__()
        self.subscription_id: str = subscription_id
        self.resource_group_name: Optional[str] = resource_group_name
        self.location: str = location
        self.tf_resource_type: AzureResourceType = resource_type

    @abstractmethod
    def get_keys(self) -> List[str]:
        pass

    @abstractmethod
    def get_cloud_resource_url(self) -> Optional[str]:
        pass

    def get_friendly_name(self) -> str:
        if self.terraform_state:
            return self.terraform_state.address
        return self.get_name() or self.get_id()

    @property
    @abstractmethod
    def is_tagable(self) -> bool:
        pass
