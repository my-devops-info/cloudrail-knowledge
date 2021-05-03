from typing import List, Dict

from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class RdsEncryptAtRestRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'not_car_rds_instances_encrypted_at_rest'

    def execute(self, env_context: EnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for rds_instance in env_context.rds_instances:
            if rds_instance.is_new_resource():
                if not rds_instance.encrypted_at_rest:
                    issues.append(
                        Issue(
                            f"~{rds_instance.get_type()}~. {rds_instance.get_type()} "
                            f"`{rds_instance.get_friendly_name()}` "
                            f"is not set to use encrypt at rest", rds_instance, rds_instance))

        for rds_cluster in env_context.rds_clusters:
            if rds_cluster.is_new_resource():
                if not rds_cluster.encrypted_at_rest:
                    issues.append(
                        Issue(
                            f"~{rds_cluster.get_type()}~. {rds_cluster.get_type()} "
                            f"`{rds_cluster.get_friendly_name()}` "
                            f"is not set to use encrypt at rest", rds_cluster, rds_cluster))

        for rds_global_cluster in env_context.rds_global_clusters:
            if rds_global_cluster.is_new_resource():
                if not rds_global_cluster.encrypted_at_rest:
                    issues.append(
                        Issue(
                            f"~{rds_global_cluster.get_type()}~. {rds_global_cluster.get_type()} "
                            f"`{rds_global_cluster.get_friendly_name()}` is not set to use encrypt at rest",
                            rds_global_cluster, rds_global_cluster))

        return issues

    def should_run_rule(self, environment_context: EnvironmentContext) -> bool:
        return bool(environment_context.rds_instances or environment_context.rds_clusters or environment_context.rds_global_clusters)
