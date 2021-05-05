import unittest

from cloudrail.knowledge.context.aws.cloudwatch.cloud_watch_log_group import CloudWatchLogGroup
from cloudrail.knowledge.context.aws.lambda_.lambda_function import LambdaFunction
from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_lambda_function_has_non_infinite_log_retention_rule import \
    EnsureLambdaFunctionHasNonInfiniteLogRetentionRule
from cloudrail.knowledge.rules.base_rule import RuleResultType
from tests.rule_test_utils import create_empty_entity


class TestEnsureLambdaFunctionHasNonInfiniteLogRetentionRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureLambdaFunctionHasNonInfiniteLogRetentionRule()

    def test_non_car_lambda_logging_not_infnite_fail(self):
        # Arrange
        lambda_func: LambdaFunction = create_empty_entity(LambdaFunction)
        log_group: CloudWatchLogGroup = create_empty_entity(CloudWatchLogGroup)
        lambda_func.log_group = log_group
        lambda_func.log_group.retention_in_days = 0
        context = EnvironmentContext(lambda_function_list=[lambda_func])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_lambda_logging_not_infnite__no_retention__fail(self):
        # Arrange
        lambda_func: LambdaFunction = create_empty_entity(LambdaFunction)
        log_group: CloudWatchLogGroup = create_empty_entity(CloudWatchLogGroup)
        lambda_func.log_group = log_group
        lambda_func.log_group.retention_in_days = None
        context = EnvironmentContext(lambda_function_list=[lambda_func])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue('Upon creation' not in result.issues[0].evidence)

    def test_non_car_lambda_logging_not_infnite__no_retention_and_pseudo___fail(self):
        # Arrange
        lambda_func: LambdaFunction = create_empty_entity(LambdaFunction)
        log_group: CloudWatchLogGroup = create_empty_entity(CloudWatchLogGroup)
        lambda_func.log_group = log_group
        lambda_func.log_group.retention_in_days = None
        lambda_func.log_group.is_pseudo = True
        context = EnvironmentContext(lambda_function_list=[lambda_func])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue('Upon creation' in result.issues[0].evidence)

    def test_non_car_lambda_logging_not_infnite_pass(self):
        # Arrange
        lambda_func: LambdaFunction = create_empty_entity(LambdaFunction)
        log_group: CloudWatchLogGroup = create_empty_entity(CloudWatchLogGroup)
        lambda_func.log_group = log_group
        lambda_func.log_group.retention_in_days = 10
        context = EnvironmentContext(lambda_function_list=[lambda_func])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
