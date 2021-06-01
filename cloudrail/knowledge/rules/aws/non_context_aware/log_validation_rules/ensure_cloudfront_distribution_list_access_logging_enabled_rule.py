from typing import List, Dict

from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureCloudfrontDistributionListAccessLoggingEnabledRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_cloudfront_distribution_access_logging_enabled'

    def execute(self, env_context: EnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for cloudfront in env_context.cloudfront_distribution_list:
            if not cloudfront.logs_settings or not cloudfront.logs_settings.logging_enabled:
                issues.append(
                    Issue(
                        f'The {cloudfront.get_type()} `{cloudfront.get_friendly_name()}` has access logging disabled', cloudfront, cloudfront))
        return issues

    def should_run_rule(self, environment_context: EnvironmentContext) -> bool:
        return bool(environment_context.cloudfront_distribution_list)
