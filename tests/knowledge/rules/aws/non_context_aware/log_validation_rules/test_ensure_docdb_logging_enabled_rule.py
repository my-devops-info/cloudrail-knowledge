import unittest

from cloudrail.knowledge.context.aws.docdb.docdb_cluster import DocumentDbCluster
from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_docdb_logging_enabled_rule import EnsureDocdbLoggingEnabledRule
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.dev_tools.rule_test_utils import create_empty_entity


class TestEnsureDocdbLoggingEnabledRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureDocdbLoggingEnabledRule()

    def test_not_car_docdb_cluster_encrypted_at_rest__empty_list__fail(self):
        # Arrange
        docdb_cluster: DocumentDbCluster = create_empty_entity(DocumentDbCluster)
        docdb_cluster.enabled_cloudwatch_logs_exports = []
        context = EnvironmentContext(docdb_cluster=[docdb_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_not_car_docdb_cluster_encrypted_at_rest__one_item__fail(self):
        # Arrange
        docdb_cluster: DocumentDbCluster = create_empty_entity(DocumentDbCluster)
        docdb_cluster.enabled_cloudwatch_logs_exports = ["audit"]
        context = EnvironmentContext(docdb_cluster=[docdb_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_not_car_docdb_cluster_encrypted_at_rest_pass(self):
        # Arrange
        docdb_cluster: DocumentDbCluster = create_empty_entity(DocumentDbCluster)
        docdb_cluster.enabled_cloudwatch_logs_exports = ["profiler", "audit"]
        context = EnvironmentContext(docdb_cluster=[docdb_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
