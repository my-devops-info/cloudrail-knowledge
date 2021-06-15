from typing import List, Dict
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.rules.azure.azure_base_rule import AzureBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class FunctionAppUseLatestHttpVersionRule(AzureBaseRule):

    def get_id(self) -> str:
        return 'non_car_http_latest_in_function_app'

    def execute(self, env_context: AzureEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for func_app in env_context.function_apps:
            if not func_app.site_config.http2_enabled:
                issues.append(
                    Issue(
                        f'The {func_app.get_type()} `{func_app.get_friendly_name()}` does not use the latest HTTP version.',
                        func_app,
                        func_app))
        return issues

    def should_run_rule(self, environment_context: AzureEnvironmentContext) -> bool:
        return bool(environment_context.function_apps)
