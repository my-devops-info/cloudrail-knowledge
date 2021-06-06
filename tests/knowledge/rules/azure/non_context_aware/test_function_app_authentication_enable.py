from unittest import TestCase

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.webapp.auth_settings import AuthSettings
from cloudrail.knowledge.context.azure.webapp.azure_function_app import AzureFunctionApp
from cloudrail.knowledge.rules.azure.non_context_aware.function_app_authentication_enable_rule import FunctionAppAuthenticationEnableRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestFunctionAppAuthenticationEnable(TestCase):

    def setUp(self):
        self.rule = FunctionAppAuthenticationEnableRule()

    def test_ftps_enabled(self):
        # Arrange
        auth_settings: AuthSettings = AuthSettings(True)
        func_app: AzureFunctionApp = create_empty_entity(AzureFunctionApp)
        func_app.auth_settings = auth_settings
        func_app.name = 'my-func-app'
        context = AzureEnvironmentContext(function_apps=AliasesDict(func_app))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_ftps_disabled(self):
        # Arrange
        auth_settings: AuthSettings = AuthSettings(False)
        func_app: AzureFunctionApp = create_empty_entity(AzureFunctionApp)
        func_app.auth_settings = auth_settings
        func_app.name = 'my-func-app'
        context = AzureEnvironmentContext(function_apps=AliasesDict(func_app))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
