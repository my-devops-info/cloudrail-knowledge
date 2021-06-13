from typing import List, Dict
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureEcsClusterEnableContainerInsightsRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_ecs_cluster_container_insights_enabled'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for cluster in env_context.ecs_cluster_list:
            if not cluster.is_container_insights_enabled:
                issues.append(
                    Issue(
                        f'The {cluster.get_type()} `{cluster.get_friendly_name()}` has container insights disabled', cluster, cluster))
            return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.ecs_cluster_list)
