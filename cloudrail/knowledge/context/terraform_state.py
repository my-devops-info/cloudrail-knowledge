from dataclasses import dataclass
from typing import Optional

from cloudrail.knowledge.context.terraform_action_type import TerraformActionType
from cloudrail.knowledge.context.terraform_resource_metadata import TerraformResourceMetadata


@dataclass
class TerraformState:
    address: str
    action: TerraformActionType
    resource_metadata: Optional[TerraformResourceMetadata]
    is_new: bool
