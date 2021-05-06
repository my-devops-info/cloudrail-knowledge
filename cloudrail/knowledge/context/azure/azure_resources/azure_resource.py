from abc import abstractmethod
from typing import Optional, List
from cloudrail.knowledge.context.mergeable import Mergeable

from cloudrail.knowledge.context.azure.azure_resources.constants.azure_resource_type import AzureResourceType


class AzureResource(Mergeable):

    def __init__(self, subscription_id: str, resource_group_name: str, location: str,
                 azure_resource_type: str, resource_type: AzureResourceType):
        super().__init__()
        self.subscription_id: str = subscription_id
        self.resource_group_name: str = resource_group_name
        self.location: str = location
        self.azure_resource_type: str = azure_resource_type
        self.tf_resource_type: AzureResourceType = resource_type

    @abstractmethod
    def get_keys(self) -> List[str]:
        pass

    @abstractmethod
    def get_cloud_resource_url(self) -> Optional[str]:
        pass

    @abstractmethod
    def get_friendly_name(self) -> str:
        pass

    @property
    @abstractmethod
    def is_tagable(self) -> bool:
        pass
