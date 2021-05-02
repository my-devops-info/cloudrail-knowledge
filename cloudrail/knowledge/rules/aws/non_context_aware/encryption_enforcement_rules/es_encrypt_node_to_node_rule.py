from typing import List, Dict

from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.base_rule import BaseRule, Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EsEncryptNodeToNodeRule(BaseRule):

    def get_id(self) -> str:
        return 'not_car_elasticsearch_domains_encrypted_note_to_node'

    def execute(self, env_context: EnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for es_domain in env_context.elastic_search_domains:
            if es_domain.is_new_resource():
                if not es_domain.encrypt_node_to_node_state:
                    issues.append(
                        Issue(
                            f"~{es_domain.get_type()}~. {es_domain.get_type()} `{es_domain.get_friendly_name()}`. "
                            f"is not set to use encrypt node-to-node", es_domain, es_domain))
        return issues

    def get_needed_parameters(self) -> List[ParameterType]:
        return []

    def should_run_rule(self, environment_context: EnvironmentContext) -> bool:
        return bool(environment_context.elastic_search_domains)
