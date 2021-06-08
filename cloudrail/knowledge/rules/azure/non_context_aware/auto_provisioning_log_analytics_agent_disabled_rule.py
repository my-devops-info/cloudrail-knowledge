from typing import List, Dict

from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.rules.azure.azure_base_rule import AzureBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class AutoProvisioningLogAnalyticsAgentDisabledRule(AzureBaseRule):
    def get_id(self) -> str:
        return 'non_car_auto_provisioning_log_analytics_agent_enabled'

    def execute(self, env_context: AzureEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for security_center_auto_provisioning in env_context.security_center_auto_provisioning:
            if not security_center_auto_provisioning.auto_provision_is_on:
                issues.append(
                    Issue(f'The auto provisioning of the Log Analytics agent is not enabled for the '
                          f'subscription `{security_center_auto_provisioning.subscription_id}`.',
                          security_center_auto_provisioning,
                          security_center_auto_provisioning))
        return issues

    def should_run_rule(self, environment_context: AzureEnvironmentContext) -> bool:
        return bool(environment_context.security_center_auto_provisioning)
