from typing import List, Dict

from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureRdsResourceLoggingEnabledRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_rds_instance_and_cluster_logging_enabled'

    def execute(self, env_context: EnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        rds_resources = env_context.rds_clusters + env_context.rds_instances
        for resource in rds_resources:
            if not resource.cloudwatch_logs_exports:
                issues.append(
                    Issue(
                        f'The {resource.get_type()} `{resource.get_friendly_name()}` does not have Cloudwatch log export enabled',
                        resource, resource))
            return issues

    def should_run_rule(self, environment_context: EnvironmentContext) -> bool:
        return bool(environment_context.rds_clusters or environment_context.rds_instances)
