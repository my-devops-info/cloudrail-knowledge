from abc import abstractmethod
from typing import Callable, List, Dict, Tuple
from cloudrail.knowledge.context.aws.account.account import Account
from cloudrail.knowledge.context.aws.iam.iam_password_policy import IamPasswordPolicy
from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule

from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class AbstractIamAccountPasswordPolicy(AwsBaseRule):

    @abstractmethod
    def get_id(self) -> str:
        pass

    @abstractmethod
    def execute(self, env_context: EnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        pass

    @staticmethod
    def _check_users(env_context: EnvironmentContext) -> bool:
        users_login_list = [user_name.name for user_name in env_context.users_login_profile]
        return any(user.name in users_login_list for user in env_context.users)

    def _get_entities_list(self, env_context: EnvironmentContext, policy_condition: Callable[[IamPasswordPolicy], bool]) \
            -> List[Tuple[Account, IamPasswordPolicy]]:
        issues = []
        if self._check_users(env_context):
            for account in env_context.accounts:
                policy = next((policy for policy in env_context.iam_account_pass_policies if policy.account == account.account), None)
                if policy:
                    if policy_condition(policy):
                        issues.append((account, policy))
        return issues

    def should_run_rule(self, environment_context: EnvironmentContext) -> bool:
        return bool(environment_context.accounts)
