from typing import List, Dict
from cloudrail.knowledge.context.aws.kms.kms_key_manager import KeyManager

from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.base_rule import BaseRule, Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureSecretsManagersSecretsEncryptedAtRestWithCustomerManagedCmkRule(BaseRule):

    def get_id(self) -> str:
        return 'non_car_secrets_manager_secrets_encrypted_at_rest_with_customer_managed_cmk'

    def execute(self, env_context: EnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for secrets_manager in env_context.secrets_manager_secrets:
            if (secrets_manager.kms_data is None) or (secrets_manager.kms_data.key_manager != KeyManager.CUSTOMER):
                issues.append(
                    Issue(
                        f'The Secrets Manager secret `{secrets_manager.get_name()}` is not set '
                        f'to be encrypted at rest using customer-managed CMK', secrets_manager, secrets_manager))
        return issues

    def get_needed_parameters(self) -> List[ParameterType]:
        return []

    def should_run_rule(self, environment_context: EnvironmentContext) -> bool:
        return bool(environment_context.secrets_manager_secrets)
