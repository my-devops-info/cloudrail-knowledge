from typing import Dict, List

from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.base_rule import BaseRule, Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class IamNoHumanUsersRule(BaseRule):

    def execute(self, env_context: EnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues_list: List[Issue] = []
        users_login_list = [user_name.name for user_name in env_context.users_login_profile]
        for user in env_context.users:
            if user.name in users_login_list:
                issues_list.append(Issue(f'The {user.get_type()} `{user.get_friendly_name()}` has console access, '
                                         f'and so is considered human', user, user))
        return issues_list

    def get_id(self) -> str:
        return "non_car_iam_no_human_users"

    def get_needed_parameters(self) -> List[ParameterType]:
        return []

    def should_run_rule(self, environment_context: EnvironmentContext) -> bool:
        return bool(environment_context.users)
