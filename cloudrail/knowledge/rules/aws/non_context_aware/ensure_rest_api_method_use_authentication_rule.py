from typing import List, Dict
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureRestApiMethodUseAuthenticationRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_api_gateway_methods_use_authentication'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for rest_api in env_context.rest_api_gw:
            for method in rest_api.api_gateway_methods:
                if method.authorization == 'NONE':
                    issues.append(
                        Issue(
                            f'The {rest_api.get_type()} `{rest_api.get_friendly_name()}` is not requiring authorization for the method '
                            f'`{method.get_friendly_name()}`', rest_api, method))
        return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.rest_api_gw and environment_context.api_gateway_methods)
