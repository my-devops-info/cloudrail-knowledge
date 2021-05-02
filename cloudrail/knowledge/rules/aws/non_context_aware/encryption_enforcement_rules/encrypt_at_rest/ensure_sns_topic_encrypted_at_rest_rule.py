from typing import List, Dict

from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.base_rule import BaseRule, Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureSnsTopicEncryptedAtRestRule(BaseRule):

    def get_id(self) -> str:
        return 'non_car_sns_topic_encrypt_at_rest'

    def execute(self, env_context: EnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for sns_topic in env_context.sns_topics:
            if not sns_topic.encrypted_at_rest:
                issues.append(
                    Issue(
                        f'The {sns_topic.get_type()} `{sns_topic.get_friendly_name()}` '
                        f'is not set to use encryption at rest', sns_topic, sns_topic))
        return issues

    def get_needed_parameters(self) -> List[ParameterType]:
        return []

    def should_run_rule(self, environment_context: EnvironmentContext) -> bool:
        return bool(environment_context.sns_topics)
