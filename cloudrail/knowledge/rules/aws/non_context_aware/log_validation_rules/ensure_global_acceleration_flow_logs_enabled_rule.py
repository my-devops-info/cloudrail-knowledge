from typing import List, Dict

from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureGlobalAccelerationFlowLogsEnabledRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_global_accelerator_flow_logs_enabled'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for gac in env_context.global_accelerators:
            if not gac.attributes or not gac.attributes.flow_logs_enabled:
                issues.append(
                    Issue(
                        f'The {gac.get_type()} `{gac.get_friendly_name()}` does not have flow logs enabled', gac, gac))
        return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.global_accelerators)
