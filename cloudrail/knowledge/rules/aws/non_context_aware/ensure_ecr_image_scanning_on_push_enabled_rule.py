from typing import List, Dict
from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureEcrImageScanningOnPushEnabledRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_ecr_image_scanning_on_push_enabled'

    def execute(self, env_context: EnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for ecr in env_context.ecr_repositories:
            if not ecr.is_image_scan_on_push:
                issues.append(
                    Issue(
                        f'The {ecr.get_type()} `{ecr.get_friendly_name()}` is not configured to perform image scan on push', ecr, ecr))
            return issues

    def should_run_rule(self, environment_context: EnvironmentContext) -> bool:
        return bool(environment_context.ecr_repositories)
