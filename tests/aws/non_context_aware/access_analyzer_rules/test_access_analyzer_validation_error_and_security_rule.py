# import unittest
#
# from cloudrail.knowledge.context.aws.iam.policy import Policy
# from cloudrail.knowledge.context.environment_context import EnvironmentContext
# from cloudrail.knowledge.context.mergeable import EntityOrigin
# from cloudrail.knowledge.rules.aws.non_context_aware.access_analyzer_rules.access_analyzer_validation_error_and_security_rule import \
#     AccessAnalyzerValidationErrorAndSecurityRule
# from cloudrail.knowledge.rules.base_rule import RuleResultType
# from cloudrail.dev_tools.rule_test_utils import create_empty_entity
#
#
# class TestAccessAnalyzerValidationErrorAndSecurityRule(unittest.TestCase):
#     def setUp(self):
#         self.rule = AccessAnalyzerValidationErrorAndSecurityRule()
#
#     def test_not_car_access_analyzer_validation_error_and_security_fail(self):
#         # Arrange
#         policy: Policy = Policy(account='account',
#                                 statements= [])
#         policy.origin == EntityOrigin.TERRAFORM
#         policy.access_analyzer_findings = [{
#             "findingDetails": "Add a value to the empty string in the Sid element.",
#             "findingType": "SUGGESTION",
#             "issueCode": "EMPTY_SID_VALUE",
#             "learnMoreLink": "https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-reference-policy-checks.html",
#             "locations": [
#                 {
#                     "path": [
#                         {
#                             "value": "Statement"
#                         },
#                         {
#                             "index": 0
#                         },
#                         {
#                             "value": "Sid"
#                         }
#                     ],
#                     "span": {
#                         "end": {
#                             "column": 19,
#                             "line": 10,
#                             "offset": 235
#                         },
#                         "start": {
#                             "column": 17,
#                             "line": 10,
#                             "offset": 233
#                         }
#                     }
#                 }
#             ]
#         }]
#
#         context = EnvironmentContext(policies=[policy])
#         # Act
#         result = self.rule.run(context, {})
#         # Assert
#         self.assertEqual(RuleResultType.FAILED, result.status)
#         self.assertEqual(1, len(result.issues))
#
#     def test_not_car_access_analyzer_validation_error_and_security_pass(self):
#         # Arrange
#         context = EnvironmentContext()
#         # Act
#         result = self.rule.run(context, {})
#         # Assert
#         self.assertEqual(RuleResultType.SUCCESS, result.status)
#         self.assertEqual(0, len(result.issues))
