from typing import List, Dict

from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureElasticsearchDomainLoggingEnabledRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_elasticsearch_domain_logging_enabled'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for es_domain in env_context.elastic_search_domains:
            if not es_domain.log_publishing_options:
                issues.append(
                    Issue(
                        f'The {es_domain.get_type()} `{es_domain.get_friendly_name()}` does not have'
                        f' logging configured at all', es_domain, es_domain))
            else:
                for log in es_domain.log_publishing_options:
                    if not log.enabled:
                        issues.append(
                            Issue(
                                f'The {es_domain.get_type()} `{es_domain.get_friendly_name()}` does not have '
                                f'logging enabled for log type: {log.log_type}', es_domain, es_domain))
        return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.elastic_search_domains)
