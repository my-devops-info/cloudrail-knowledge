from abc import abstractmethod
from typing import List, Dict
from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class SampleCustomRule(AwsBaseRule):
    @abstractmethod
    def get_id(self) -> str:
        return 'my_sample_rule'

    def execute(self, env_context: EnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues = []
        for entity in env_context.vpcs:
            issues.append(
                Issue(
                    f"Vpc exists `{entity.get_friendly_name()}`", entity, entity))
        return issues

    def should_run_rule(self, environment_context: EnvironmentContext) -> bool:
        return True
