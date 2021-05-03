from abc import abstractmethod
from typing import List, Dict

from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.base_rule import BaseRule, Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class AwsBaseRule(BaseRule[EnvironmentContext]):

    @abstractmethod
    def execute(self, env_context: EnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        pass

    @abstractmethod
    def get_id(self) -> str:
        pass

    @abstractmethod
    def should_run_rule(self, environment_context: EnvironmentContext) -> bool:
        pass

    def get_needed_parameters(self) -> List[ParameterType]:
        return []
