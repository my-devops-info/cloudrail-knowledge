from typing import List, Dict

from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureLoadBalancerDropsInvalidHttpHeadersRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_alb_drops_invalid_http_headers'

    def execute(self, env_context: EnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for lb in env_context.load_balancers:
            if lb.load_balancer_attributes and not lb.load_balancer_attributes.drop_invalid_header_fields:
                issues.append(
                    Issue(
                        f'The {lb.get_type()} `{lb.get_friendly_name()}` does not drop invalid HTTP headers', lb, lb))
        return issues

    def should_run_rule(self, environment_context: EnvironmentContext) -> bool:
        return bool(environment_context.load_balancers)
