
# import unittest
#
# from cloudrail.knowledge.context.environment_context import EnvironmentContext
# from cloudrail.knowledge.rules.base_rule import RuleResultType
# from tests.rule_test_utils import create_empty_entity
#
#
# class TestAccessAnalyzerValidationWarningAndSuggestionRule(unittest.TestCase):
#     def setUp(self):
#         self.rule = AccessAnalyzerValidationWarningAndSuggestionRule()
#
#     def test_not_car_access_analyzer_validation_warning_and_suggestion_fail(self):
#         # Arrange
#         context = EnvironmentContext()
#         # Act
#         result = self.rule.run(context, {})
#         # Assert
#         self.assertEqual(RuleResultType.FAILED, result.status)
#         self.assertEqual(1, len(result.issues))
#
#     def test_not_car_access_analyzer_validation_warning_and_suggestion_pass(self):
#         # Arrange
#         context = EnvironmentContext()
#         # Act
#         result = self.rule.run(context, {})
#         # Assert
#         self.assertEqual(RuleResultType.SUCCESS, result.status)
#         self.assertEqual(0, len(result.issues))
