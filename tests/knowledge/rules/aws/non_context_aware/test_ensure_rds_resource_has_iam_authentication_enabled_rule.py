import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.rds.rds_cluster import RdsCluster
from cloudrail.knowledge.context.aws.rds.rds_instance import RdsInstance
from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.ensure_rds_resource_has_iam_authentication_enabled_rule import \
    EnsureRdsResourceIamAuthenticationEnabledRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureRdsResourceIamAuthenticationEnabledRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureRdsResourceIamAuthenticationEnabledRule()

    def test_non_car_rds_database_iam_authentication_enabled__supported_ver_no_auth__fail(self):
        # Arrange
        rds_instance: RdsInstance = create_empty_entity(RdsInstance)
        rds_instance.engine_type = 'mysql'
        rds_instance.engine_version = '5.7.16'
        rds_instance.iam_database_authentication_enabled = False
        context = EnvironmentContext(rds_instances=[rds_instance])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_rds_database_iam_authentication_enabled__unsupported_version__pass(self):
        # Arrange
        rds_instance: RdsInstance = create_empty_entity(RdsInstance)
        rds_instance.engine_type = 'mysql'
        rds_instance.engine_version = '5.7.15'
        rds_instance.iam_database_authentication_enabled = False
        context = EnvironmentContext(rds_instances=[rds_instance])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_rds_database_iam_authentication_enabled__supported_version_auth_disabled__pass(self):
        # Arrange
        rds_instance: RdsInstance = create_empty_entity(RdsInstance)
        rds_instance.engine_type = 'mysql'
        rds_instance.engine_version = '5.7'
        rds_instance.iam_database_authentication_enabled = True
        context = EnvironmentContext(rds_instances=[rds_instance])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_rds_database_iam_authentication_enabled__rds_cluster__fail(self):
        # Arrange
        rds_cluster: RdsCluster = create_empty_entity(RdsCluster)
        rds_cluster.engine_type = 'mysql'
        rds_cluster.engine_version = '5.7.mysql_aurora.2.03.2'
        rds_cluster.iam_database_authentication_enabled = False
        context = EnvironmentContext(rds_clusters=[rds_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_rds_database_iam_authentication_enabled__rds_cluster__pass(self):
        # Arrange
        rds_cluster: RdsCluster = create_empty_entity(RdsCluster)
        rds_cluster.engine_type = 'mysql'
        rds_cluster.engine_version = '5.7.mysql_aurora.2.03.2'
        rds_cluster.iam_database_authentication_enabled = True
        context = EnvironmentContext(rds_clusters=[rds_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
