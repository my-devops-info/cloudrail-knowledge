from typing import List, Dict

from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.base_rule import BaseRule, Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureSqsQueuesEncryptedAtRestRule(BaseRule):

    def get_id(self) -> str:
        return 'non_car_sqs_queue_encrypt_at_rest'

    def execute(self, env_context: EnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for sqs_queue in env_context.sqs_queues:
            if not sqs_queue.encrypted_at_rest:
                issues.append(
                    Issue(
                        f'The {sqs_queue.get_type()} `{sqs_queue.get_friendly_name()}` \
                            is not set to use encryption at rest', sqs_queue, sqs_queue))
        return issues

    def get_needed_parameters(self) -> List[ParameterType]:
        return []

    def should_run_rule(self, environment_context: EnvironmentContext) -> bool:
        return bool(environment_context.sqs_queues)
