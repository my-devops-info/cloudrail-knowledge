import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.lambda_.lambda_function import LambdaFunction
from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_lambda_function_xray_tracing_enabled_rule import \
    EnsureLambdaFunctionXrayTracingEnabledRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureLambdaFunctionXrayTracingEnabledRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureLambdaFunctionXrayTracingEnabledRule()

    def test_non_car_lambda_function_xray_tracing_enabled_fail(self):
        # Arrange
        lambda_func: LambdaFunction = create_empty_entity(LambdaFunction)
        lambda_func.xray_tracing_enabled = False
        context = EnvironmentContext(lambda_function_list=[lambda_func])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_lambda_function_xray_tracing_enabled_pass(self):
        # Arrange
        lambda_func: LambdaFunction = create_empty_entity(LambdaFunction)
        lambda_func.xray_tracing_enabled = True
        context = EnvironmentContext(lambda_function_list=[lambda_func])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
