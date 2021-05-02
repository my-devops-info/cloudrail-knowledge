from typing import List, Dict
from cloudrail.knowledge.context.aws.kms.kms_key_manager import KeyManager

from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.base_rule import BaseRule, Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureXrayEncryptionCmkRule(BaseRule):

    def get_id(self) -> str:
        return 'non_car_xray_encryption_config_encrypt_at_rest_with_customer_managed_CMK'

    def execute(self, env_context: EnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for xray in env_context.xray_encryption_configurations:
            if (xray.key_id and xray.kms_data.key_manager != KeyManager.CUSTOMER) \
                 or not xray.key_id:
                issues.append(
                    Issue(f'The {xray.get_type()} config is not set to encrypt at rest using customer-managed CMK',\
                        xray, xray))
        return issues

    def get_needed_parameters(self) -> List[ParameterType]:
        return []

    def should_run_rule(self, environment_context: EnvironmentContext) -> bool:
        return bool(environment_context.xray_encryption_configurations)
