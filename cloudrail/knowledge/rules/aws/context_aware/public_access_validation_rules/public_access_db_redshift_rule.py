from typing import List, Dict

from cloudrail.knowledge.utils.connection_utils import ConnectionUtils
from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.base_rule import BaseRule, Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class PublicAccessDbRedshiftRule(BaseRule):

    def get_id(self) -> str:
        return 'public_access_db_redshift_rule'

    def execute(self, env_context: EnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for redshift in env_context.redshift_clusters:
            violating_security_group = ConnectionUtils.get_allowing_public_access_on_ports(redshift, [redshift.port])
            if violating_security_group:
                issues.append(Issue(
                    f'~Internet~. '
                    f"{redshift.get_type()}: `{redshift.get_friendly_name()}` "
                    f"is on {redshift.network_resource.vpc.get_type()}"
                    f" `{redshift.network_resource.vpc.get_friendly_name()}`. "
                    f"{redshift.get_type()} uses security groups "
                    f"`{', '.join([x.get_friendly_name() for x in redshift.network_resource.security_groups])}`. "
                    f"Security group(s) allow Redshift associated port. "
                    f"{redshift.get_type()} is on subnets:"
                    f" `{', '.join([x.get_friendly_name() for x in redshift.network_resource.subnets])}`. "
                    f"Subnets rely on Network ACL's "
                    f"`{', '.join([x.network_acl.get_friendly_name() for x in redshift.network_resource.subnets])}`. "
                    f"{redshift.get_type()} is capable of traversing to the internet via Redshift associated port. "
                    f"~{redshift.get_type()} `{redshift.get_friendly_name()}`~",
                    redshift,
                    violating_security_group))

        return issues

    def get_needed_parameters(self) -> List[ParameterType]:
        return []

    def should_run_rule(self, environment_context: EnvironmentContext) -> bool:
        return bool(environment_context.redshift_clusters)
