from typing import List, Dict

from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.base_rule import BaseRule, Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureElasticacheReplicationGroupsEncryptedInTransitRule(BaseRule):

    def get_id(self) -> str:
        return 'non_car_elasticache_replication_group_encrypt_in_transit_creating'

    def execute(self, env_context: EnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for elasticache_replication_group in env_context.elasti_cache_replication_groups:
            if elasticache_replication_group.is_new_resource():
                if not elasticache_replication_group.encrypted_in_transit:
                    issues.append(
                        Issue(
                            f'The {elasticache_replication_group.get_type()} `{elasticache_replication_group.get_friendly_name()}` is '
                            f'not set to use encryption in transit', elasticache_replication_group, elasticache_replication_group))
        return issues

    def get_needed_parameters(self) -> List[ParameterType]:
        return []

    def should_run_rule(self, environment_context: EnvironmentContext) -> bool:
        return bool(environment_context.elasti_cache_replication_groups)
