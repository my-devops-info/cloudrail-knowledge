from typing import List, Dict

from cloudrail.knowledge.context.aws.kms.kms_key_manager import KeyManager
from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.base_rule import BaseRule, Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureCodeBuildReportGroupEncryptedWithCustomerManagedCmkRule(BaseRule):

    def get_id(self) -> str:
        return 'not_car_codebuild_report_groups_encrypted_at_rest_with_customer_managed_cmk'

    def execute(self, env_context: EnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for report_group in env_context.codebuild_report_groups:
            if report_group.export_config_s3_destination_kms_data is None \
                    or report_group.export_config_s3_destination_kms_data.key_manager != KeyManager.CUSTOMER:
                issues.append(
                    Issue(
                        f'The {report_group.get_type()} `{report_group.get_friendly_name()}` '
                        f'is not set to use encryption at rest '
                        f'with customer-managed CMK', report_group, report_group))
        return issues

    def get_needed_parameters(self) -> List[ParameterType]:
        return []

    def should_run_rule(self, environment_context: EnvironmentContext) -> bool:
        return bool(environment_context.codebuild_report_groups)
