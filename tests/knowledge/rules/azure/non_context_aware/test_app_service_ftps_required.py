import unittest

from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.aws.iam.iam_user import IamUser
from cloudrail.knowledge.context.aws.iam.iam_users_login_profile import IamUsersLoginProfile
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.azure_resources.app_service.azure_app_service import AzureAppService
from cloudrail.knowledge.context.azure.azure_resources.app_service.azure_ftps_state import FtpsState
from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.iam_no_human_users_rule import IamNoHumanUsersRule
from cloudrail.knowledge.rules.azure.app_service_ftps_required import AppServiceFtpsRequired
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.dev_tools.rule_test_utils import create_empty_entity


class TestAppServiceFtpsRequired(unittest.TestCase):
    def setUp(self):
        self.rule = AppServiceFtpsRequired()

    def test_all_allowed_state(self):
        # Arrange
        app_service: AzureAppService = create_empty_entity(AzureAppService)
        app_service.name = 'tmp-name'
        app_service.ftps_state = FtpsState.ALL_ALLOWED
        context = AzureEnvironmentContext(app_services=AliasesDict(app_service))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_disabled_state(self):
        # Arrange
        app_service: AzureAppService = create_empty_entity(AzureAppService)
        app_service.name = 'tmp-name'
        app_service.ftps_state = FtpsState.DISABLED
        context = AzureEnvironmentContext(app_services=AliasesDict(app_service))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)

    def test_ftps_only_state(self):
        # Arrange
        app_service: AzureAppService = create_empty_entity(AzureAppService)
        app_service.name = 'tmp-name'
        app_service.ftps_state = FtpsState.FTPS_ONLY
        context = AzureEnvironmentContext(app_services=AliasesDict(app_service))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
