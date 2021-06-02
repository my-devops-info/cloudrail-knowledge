from typing import List, Dict

from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureEc2InstanceDetailedMonitoringEnabledRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_ec2_instance_detailed_monitoring_enabled'

    def execute(self, env_context: EnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for ec2 in env_context.ec2s:
            if not ec2.monitoring_enabled:
                issues.append(
                    Issue(
                        f'The {ec2.get_type()} `{ec2.get_friendly_name()}` has detailed monitoring disabled', ec2, ec2))
        return issues

    def should_run_rule(self, environment_context: EnvironmentContext) -> bool:
        return bool(environment_context.ec2s)
