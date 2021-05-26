import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.rds.rds_cluster import RdsCluster
from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.backup_validations.ensure_rds_cluster_backup_retention_enabled_rule import \
    EnsureRdsClusterBackupRetentionEnabledRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureRdsClusterBackupRetentionEnabledRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureRdsClusterBackupRetentionEnabledRule()

    def test_non_car_rds_clusters_backup_retention_policy_fail(self):
        # Arrange
        rds_cluster: RdsCluster = create_empty_entity(RdsCluster)
        rds_cluster.backup_retention_period = 0
        context = EnvironmentContext(rds_clusters=[rds_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_rds_clusters_backup_retention_policy_pass(self):
        # Arrange
        rds_cluster: RdsCluster = create_empty_entity(RdsCluster)
        rds_cluster.backup_retention_period = 1
        context = EnvironmentContext(rds_clusters=[rds_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
