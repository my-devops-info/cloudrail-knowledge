from typing import List, Dict

from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureNeptuneClusterLoggingEnabledRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_neptune_cluster_logging_enabled'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for neptune_cluster in env_context.neptune_clusters:
            if not neptune_cluster.cloudwatch_logs_exports or 'audit' not in neptune_cluster.cloudwatch_logs_exports:
                issues.append(
                    Issue(
                        f'The {neptune_cluster.get_type()} `{neptune_cluster.get_friendly_name()}` does not have Cloudwatch log export enabled',
                        neptune_cluster, neptune_cluster))
        return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.neptune_clusters)
