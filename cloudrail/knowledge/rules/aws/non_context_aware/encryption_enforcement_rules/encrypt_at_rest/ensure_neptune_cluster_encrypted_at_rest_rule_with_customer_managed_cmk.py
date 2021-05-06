from typing import List, Dict
from cloudrail.knowledge.context.aws.kms.kms_key_manager import KeyManager

from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureNeptuneClusterEncryptedAtRestWithCustomerManagedCmkRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_neptune_cluster_encrypt_at_rest_with_customer_managed_cmk'

    def execute(self, env_context: EnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for neptune_cluster in env_context.neptune_clusters:
            if neptune_cluster.is_new_resource() and neptune_cluster.encrypted_at_rest:
                if not neptune_cluster.kms_data or neptune_cluster.kms_data.key_manager != KeyManager.CUSTOMER:
                    issues.append(
                        Issue(
                            f'The Neptune cluster `{neptune_cluster.get_friendly_name()}` '
                            f'is not set to be encrypted at rest using customer-managed CMK', neptune_cluster, neptune_cluster))
        return issues

    def should_run_rule(self, environment_context: EnvironmentContext) -> bool:
        return bool(environment_context.neptune_clusters)
