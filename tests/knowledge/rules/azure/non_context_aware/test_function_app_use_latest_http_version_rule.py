from unittest import TestCase
from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.webapp.azure_function_app import AzureFunctionApp
from cloudrail.knowledge.rules.azure.non_context_aware.function_app_use_latest_http_version_rule import FunctionAppUseLatestHttpVersionRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestFunctionAppUseLatestHttpVersionRule(TestCase):

    def setUp(self):
        self.rule = FunctionAppUseLatestHttpVersionRule()

    def test_non_car_http_latest_in_function_app_fail(self):
        # Arrange
        func_app: AzureFunctionApp = create_empty_entity(AzureFunctionApp)
        func_app.http2_enabled = False
        context = AzureEnvironmentContext(function_apps=AliasesDict(func_app))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_client_cert_optional(self):
        # Arrange
        func_app: AzureFunctionApp = create_empty_entity(AzureFunctionApp)
        func_app.http2_enabled = True
        context = AzureEnvironmentContext(function_apps=AliasesDict(func_app))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
