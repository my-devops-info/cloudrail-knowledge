from typing import List, Dict

from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.base_rule import BaseRule, Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureNeptuneClusterEncryptedAtRestRule(BaseRule):

    def get_id(self) -> str:
        return 'non_car_neptune_cluster_encrypt_at_rest_creating'

    def execute(self, env_context: EnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for neptune_cluster in env_context.neptune_clusters:
            if neptune_cluster.is_new_resource() and not neptune_cluster.encrypted_at_rest:
                issues.append(
                    Issue(
                        f'The {neptune_cluster.get_type()} `{neptune_cluster.get_friendly_name()}` '
                        f'is not set to use encryption at rest', neptune_cluster, neptune_cluster))
        return issues

    def get_needed_parameters(self) -> List[ParameterType]:
        return []

    def should_run_rule(self, environment_context: EnvironmentContext) -> bool:
        return bool(environment_context.neptune_clusters)
