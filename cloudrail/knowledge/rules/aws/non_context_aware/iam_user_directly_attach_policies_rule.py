from typing import Dict, List

from cloudrail.knowledge.context.aws.iam.policy import ManagedPolicy, InlinePolicy
from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.base_rule import BaseRule, Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class IAMUserDirectlyAttachPoliciesRule(BaseRule):

    def execute(self, env_context: EnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues_list: List[Issue] = []
        for user in env_context.users:
            for policy in user.permissions_policies:
                if isinstance(policy, (InlinePolicy, ManagedPolicy)):
                    issues_list.append(Issue(f"The user `{user.get_friendly_name()}` has the policy `{policy.get_friendly_name()}"
                                             f"`  attached directly to it",
                                             user, policy))
        return issues_list

    def get_id(self) -> str:
        return "non_car_iam_no_permissions_directly_to_user"

    def get_needed_parameters(self) -> List[ParameterType]:
        return []

    def should_run_rule(self, environment_context: EnvironmentContext) -> bool:
        return bool(environment_context.users)
