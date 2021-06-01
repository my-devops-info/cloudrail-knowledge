import unittest

from parameterized import parameterized

from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.azure_resources.app_service.azure_app_service import AzureAppService
from cloudrail.knowledge.context.azure.azure_resources.app_service.azure_ftps_state import FtpsState
from cloudrail.knowledge.rules.azure.app_service_ftps_required import AppServiceFtpsRequired
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.dev_tools.rule_test_utils import create_empty_entity


class TestAppServiceFtpsRequired(unittest.TestCase):
    def setUp(self):
        self.rule = AppServiceFtpsRequired()

    @parameterized.expand(
        [
            [FtpsState.ALL_ALLOWED, True],
            [FtpsState.DISABLED, False],
            [FtpsState.FTPS_ONLY, False]
        ]
    )
    def test_states(self, ftps_state: FtpsState, should_alert: bool):
        # Arrange
        app_service: AzureAppService = create_empty_entity(AzureAppService)
        app_service.name = 'tmp-name'
        app_service.ftps_state = ftps_state
        context = AzureEnvironmentContext(app_services=AliasesDict(app_service))
        # Act
        result = self.rule.run(context, {})
        # Assert
        if should_alert:
            self.assertEqual(RuleResultType.FAILED, result.status)
            self.assertEqual(1, len(result.issues))
        else:
            self.assertEqual(RuleResultType.SUCCESS, result.status)
