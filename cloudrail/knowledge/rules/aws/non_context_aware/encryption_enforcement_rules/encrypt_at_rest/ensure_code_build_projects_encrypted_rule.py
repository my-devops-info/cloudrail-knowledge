from typing import List, Dict

from cloudrail.knowledge.context.aws.kms.kms_key_manager import KeyManager
from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.base_rule import BaseRule, Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureCodeBuildProjectsEncryptedRule(BaseRule):

    def get_id(self) -> str:
        return 'not_car_codebuild_projects_encrypted_at_rest_with_customer_managed_CMK'

    def execute(self, env_context: EnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for project in env_context.codebuild_projects:
            if project.kms_data.key_manager != KeyManager.CUSTOMER:
                issues.append(
                    Issue(
                        f'The {project.get_type()} project `{project.get_friendly_name()}` '
                        f'is not set to use encryption at rest '
                        f'with customer-managed CMK', project, project))
        return issues

    def get_needed_parameters(self) -> List[ParameterType]:
        return []

    def should_run_rule(self, environment_context: EnvironmentContext) -> bool:
        return bool(environment_context.codebuild_projects)
