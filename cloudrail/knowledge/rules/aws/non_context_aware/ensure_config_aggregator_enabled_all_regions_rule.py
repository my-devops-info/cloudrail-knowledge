from typing import List, Dict
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureConfigAggregatorEnabledAllRegionsRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_config_aggregator_is_enabled_in_all_regions'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for aggregator in env_context.aws_config_aggregators:
            if not aggregator.is_enabled_all_regions:
                issues.append(
                    Issue(
                        f'The {aggregator.get_type()} `{aggregator.get_friendly_name()}` is not enabled in all regions', aggregator, aggregator))
            return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.aws_config_aggregators)
