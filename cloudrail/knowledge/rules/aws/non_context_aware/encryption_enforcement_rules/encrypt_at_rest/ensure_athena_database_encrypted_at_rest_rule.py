from typing import List, Dict

from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureAthenaDatabaseEncryptedAtRestRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_athena_database_encrypted_at_rest'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for database in env_context.athena_databases:
            if not database.encryption_option:
                issues.append(
                    Issue(
                        f'The {database.get_type()} `{database.get_friendly_name()}` is not encrypted at rest', database, database))
        return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.athena_databases)
