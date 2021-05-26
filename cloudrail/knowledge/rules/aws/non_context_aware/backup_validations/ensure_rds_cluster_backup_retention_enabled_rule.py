from typing import List, Dict
from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureRdsClusterBackupRetentionEnabledRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_rds_clusters_backup_retention_policy'

    def execute(self, env_context: EnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for rds_cluster in env_context.rds_clusters:
            if rds_cluster.backup_retention_period == 0:
                issues.append(
                    Issue(
                        f'The {rds_cluster.get_type()} `{rds_cluster.get_friendly_name()}` does not have a backup retention policy configured',
                        rds_cluster, rds_cluster))
            return issues

    def should_run_rule(self, environment_context: EnvironmentContext) -> bool:
        return bool(environment_context.rds_clusters)
