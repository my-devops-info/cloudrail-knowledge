from typing import List, Dict

from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.base_rule import BaseRule, Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureDaxClustersEncryptedRule(BaseRule):

    def get_id(self) -> str:
        return 'not_car_dynamodb_dax_clusters_encrypted_at_rest'

    def execute(self, env_context: EnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for dax_cluster in env_context.dax_cluster:
            if dax_cluster.is_new_resource():
                if not dax_cluster.server_side_encryption:
                    issues.append(
                        Issue(
                            f'The {dax_cluster.get_type()} `{dax_cluster.get_friendly_name()}` is not set '
                            f'to be encrypted at rest', dax_cluster, dax_cluster))
        return issues

    def get_needed_parameters(self) -> List[ParameterType]:
        return []

    def should_run_rule(self, environment_context: EnvironmentContext) -> bool:
        return bool(environment_context.dax_cluster)
