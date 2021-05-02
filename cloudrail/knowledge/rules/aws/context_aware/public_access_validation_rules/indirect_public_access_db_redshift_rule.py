from typing import List, Dict, Optional

from cloudrail.knowledge.utils.connection_utils import ConnectionData, ConnectionUtils
from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.base_rule import BaseRule, Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class IndirectPublicAccessDbRedshift(BaseRule):

    def get_id(self) -> str:
        return 'indirect_public_access_db_redshift'

    def execute(self, env_context: EnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        for redshift in env_context.redshift_clusters:
            violation_data: Optional[ConnectionData] = ConnectionUtils.get_allowing_indirect_public_access_on_ports(redshift, [redshift.port])
            if violation_data:
                issues.append(
                    Issue(
                        f'~Internet~. '
                        f"Instance `{violation_data.target_instance.owner.get_friendly_name()}"
                        f"` resides in subnet(s) that are routable to internet gateway. "
                        f'Instance has public IP address. '
                        f'Instance accepts incoming traffic on port 443. '
                        f"~Instance `{violation_data.target_instance.owner.get_friendly_name()}`~. "
                        f"Redshift Database: `{redshift.get_friendly_name()}` does not have a public IP address. "
                        f"{redshift.get_type()} is on subnets:"
                        f" `{', '.join([x.get_friendly_name() for x in redshift.network_resource.subnets])}`. "
                        f"Redshift resides in same subnet as Instance `{violation_data.target_instance.owner.get_friendly_name()}`. "
                        f"Redshift Database uses Network ACL's "
                        f"`{', '.join([x.network_acl.get_friendly_name() for x in redshift.network_resource.subnets])}`. "
                        f'{redshift.get_type()} is accessible from instance within public subnet. '
                        f"~{redshift.get_type()} `{redshift.get_friendly_name()}`~",
                        redshift,
                        violation_data.security_group))

        return issues

    def get_needed_parameters(self) -> List[ParameterType]:
        return []

    def should_run_rule(self, environment_context: EnvironmentContext) -> bool:
        return bool(environment_context.redshift_clusters)
