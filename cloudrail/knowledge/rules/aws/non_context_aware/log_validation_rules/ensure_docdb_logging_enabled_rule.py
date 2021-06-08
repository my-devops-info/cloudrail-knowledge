from typing import List, Dict

from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureDocdbLoggingEnabledRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_docdb_logging_enabled'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for cluster in env_context.docdb_cluster:
            if not all(item in cluster.enabled_cloudwatch_logs_exports for item in ["audit", "profiler"]):
                issues.append(
                    Issue(
                        f'The {cluster.get_type()} `{cluster.get_friendly_name()}` has logging disabled', cluster, cluster))
        return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.docdb_cluster)
