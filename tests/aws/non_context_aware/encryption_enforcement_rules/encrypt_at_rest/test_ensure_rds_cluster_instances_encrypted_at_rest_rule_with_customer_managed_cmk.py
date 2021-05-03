
# import unittest
#
# from cloudrail.knowledge.context.environment_context import EnvironmentContext
# from cloudrail.knowledge.rules.base_rule import RuleResultType
# from cloudrail.dev_tools.rule_test_utils import create_empty_entity
#
#
# class TestEnsureRdsInstancesEncryptedAtRestWithCustomerManagedCmkRule(unittest.TestCase):
#     def setUp(self):
#         self.rule = EnsureRdsInstancesEncryptedAtRestWithCustomerManagedCmkRule()
#
#     def test_non_car_rds_cluster_instance_encrypt_performance_insights_with_customer_managed_cmk_creating_fail(self):
#         # Arrange
#         context = EnvironmentContext()
#         # Act
#         result = self.rule.run(context, {})
#         # Assert
#         self.assertEqual(RuleResultType.FAILED, result.status)
#         self.assertEqual(1, len(result.issues))
#
#     def test_non_car_rds_cluster_instance_encrypt_performance_insights_with_customer_managed_cmk_creating_pass(self):
#         # Arrange
#         context = EnvironmentContext()
#         # Act
#         result = self.rule.run(context, {})
#         # Assert
#         self.assertEqual(RuleResultType.SUCCESS, result.status)
#         self.assertEqual(0, len(result.issues))
