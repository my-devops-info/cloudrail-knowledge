from typing import List, Dict
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureApiGwXrayTracingEnabledRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_api_gateway_xray_tracing_enabled'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for api_gw in env_context.rest_api_gw:
            for stage in api_gw.api_gw_stages:
                if not stage.xray_tracing_enabled:
                    issues.append(
                        Issue(
                            f'The {api_gw.get_type()} `{api_gw.get_friendly_name()}` has'
                            f' X-Ray tracing disabled for stage {stage.get_friendly_name()}', api_gw, stage))
        return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.rest_api_gw and environment_context.rest_api_stages)
