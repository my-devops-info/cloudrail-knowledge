from typing import List, Dict

from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.base_rule import BaseRule, Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class AllowOnlyPrivateAmisRule(BaseRule):

    def get_id(self) -> str:
        return 'non_car_ec2_amis_private_only'

    def execute(self, env_context: EnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for ec2 in env_context.ec2s:
            if ec2.image_data and ec2.image_data.is_public:
                issues.append(
                    Issue(
                        f'The {ec2.get_type()} `{ec2.get_friendly_name()}` uses AMI '
                        f'`{ec2.image_id}`, which is public', ec2, ec2.image_data))
        return issues

    def get_needed_parameters(self) -> List[ParameterType]:
        return []

    def should_run_rule(self, environment_context: EnvironmentContext) -> bool:
        return bool(environment_context.ec2s)
