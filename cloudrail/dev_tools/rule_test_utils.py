import inspect
from typing import TypeVar, Type

from cloudrail.knowledge.context.mergeable import Mergeable
from cloudrail.knowledge.context.terraform_action_type import TerraformActionType
from cloudrail.knowledge.context.terraform_state import TerraformState


_T = TypeVar('_T', bound=Mergeable)


def create_empty_entity(class_type: Type[_T], **kwargs) -> _T:
    """
    A test auxiliary function that creates a new instance of type `class_type` and initializes it with the values of kwargs or None
    Args:
        class_type: The instance's `class_type` to create.
        **kwargs: The parameters that will be passed to the instance's __init__ method.

    Returns:
        An instance of type `class_type`, initialized with the parameters in `kwargs`.
    """
    signature = inspect.signature(class_type.__init__)
    params = {}
    for param in list(signature.parameters)[1:]:
        params[param] = None
    params.update(kwargs)
    return class_type(**params)


def as_new_resource(resource: Mergeable, friendly_name: str):
    resource.terraform_state = TerraformState(friendly_name, TerraformActionType.CREATE, None, True)
