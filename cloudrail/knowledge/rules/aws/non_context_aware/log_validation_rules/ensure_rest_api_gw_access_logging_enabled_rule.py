from typing import List, Dict

from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureRestApiGwAccessLoggingEnabledRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_rest_api_gateway_access_logging_enabled'

    def execute(self, env_context: EnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for api_gw in env_context.rest_api_gw:
            for stage in api_gw.api_gw_stages:
                if not stage.access_logs:
                    issues.append(
                        Issue(
                            f'The {api_gw.get_type()} `{api_gw.get_friendly_name()}` does not have access logging enabled '
                            f'for stage {stage.get_friendly_name()}', api_gw, stage))
        return issues

    def should_run_rule(self, environment_context: EnvironmentContext) -> bool:
        return bool(environment_context.rest_api_gw and environment_context.rest_api_stages)
