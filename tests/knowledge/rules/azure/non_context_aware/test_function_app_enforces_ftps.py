from unittest import TestCase
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.webapp.azure_function_app import AzureFunctionApp
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.azure.webapp.site_config import SiteConfig
from cloudrail.knowledge.context.azure.webapp.constants import FtpsState
from cloudrail.knowledge.rules.azure.non_context_aware.function_app_enforces_ftps_only_rule import FunctionAppEnforcesFtpsOnlyRule


class TestFunctionAppEnforcesFtps(TestCase):

    def setUp(self):
        self.rule = FunctionAppEnforcesFtpsOnlyRule()

    def test_ftps_enabled(self):
        # Arrange
        site_config: SiteConfig = SiteConfig(FtpsState.FTPS_ONLY, True)
        app: AzureFunctionApp = create_empty_entity(AzureFunctionApp)
        app.site_config = site_config
        app.name = 'my-app'
        app.with_aliases(app.name)
        context = AzureEnvironmentContext(function_apps=AliasesDict(app))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_ftps_disabled(self):
        # Arrange
        app: AzureFunctionApp = create_empty_entity(AzureFunctionApp)
        app.name = 'my-app'
        app.with_aliases(app.name)
        context = AzureEnvironmentContext(function_apps=AliasesDict(app))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
