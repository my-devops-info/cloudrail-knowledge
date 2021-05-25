from typing import List, Dict
from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureCloudtrailMultiregionEnabledRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_cloudtrail_is_enabled_in_all_regions'

    def execute(self, env_context: EnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for cloudtrail in env_context.cloudtrail:
            if not cloudtrail.is_multi_region_trail:
                issues.append(
                    Issue(
                        f'The {cloudtrail.get_type()} `{cloudtrail.get_friendly_name()}` is not enabled in all regions', cloudtrail, cloudtrail))
            return issues

    def should_run_rule(self, environment_context: EnvironmentContext) -> bool:
        return bool(environment_context.cloudtrail)
