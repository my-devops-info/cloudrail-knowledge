from typing import List, Dict

from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureLoadBalancerLoggingEnabledRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_elb_logging_enabled'

    def execute(self, env_context: EnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for load_balancer in env_context.load_balancers:
            if load_balancer.load_balancer_attributes:
                if not load_balancer.load_balancer_attributes.access_logs or not load_balancer.load_balancer_attributes.access_logs.enabled:
                    issues.append(
                        Issue(
                            f'The {load_balancer.get_type()} `{load_balancer.get_friendly_name()}` does not have logging enabled',
                            load_balancer, load_balancer))
        return issues

    def should_run_rule(self, environment_context: EnvironmentContext) -> bool:
        return bool(environment_context.load_balancers)
