from typing import List, Dict
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureLambdaFunctionXrayTracingEnabledRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_lambda_function_xray_tracing_enabled'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for lambda_func in env_context.lambda_function_list:
            if not lambda_func.xray_tracing_enabled:
                issues.append(
                    Issue(
                        f'The {lambda_func.get_type()} `{lambda_func.get_friendly_name()}` does not have X-Ray tracing enabled',
                        lambda_func, lambda_func))
        return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.lambda_function_list)
