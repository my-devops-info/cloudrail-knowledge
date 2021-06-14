from typing import List, Dict

from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.rules.azure.azure_base_rule import AzureBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EmailNotificationHighSeverityAlertsEnabledRule(AzureBaseRule):
    def get_id(self) -> str:
        return 'non_car_email_notification_high_severity_alerts_enabled'

    def execute(self, env_context: AzureEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for security_center_contact in env_context.security_center_contacts:
            if not security_center_contact.alert_notifications:
                issues.append(
                    Issue(
                        f'The email notification for high severity alerts is not enabled for '
                        f'the subscription {security_center_contact.subscription_id}',
                        security_center_contact,
                        security_center_contact))
        return issues

    def should_run_rule(self, environment_context: AzureEnvironmentContext) -> bool:
        return bool(environment_context.security_center_contacts)
