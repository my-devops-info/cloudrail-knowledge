from abc import abstractmethod
from typing import List, Dict
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.rules.base_rule import BaseRule, Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class AzureBaseRule(BaseRule[AzureEnvironmentContext]):

    @abstractmethod
    def execute(self, env_context: AzureEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        pass

    @abstractmethod
    def get_id(self) -> str:
        pass

    @abstractmethod
    def should_run_rule(self, environment_context: AzureEnvironmentContext) -> bool:
        pass

    def get_needed_parameters(self) -> List[ParameterType]:
        return []
