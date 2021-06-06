from typing import List, Dict, Union
from packaging import version

from cloudrail.knowledge.context.aws.rds.rds_cluster import RdsCluster
from cloudrail.knowledge.context.aws.rds.rds_instance import RdsInstance
from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureRdsResourceIamAuthenticationEnabledRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_rds_database_iam_authentication_enabled'

    def execute(self, env_context: EnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        rds_resources = env_context.rds_clusters + env_context.rds_instances
        for resource in rds_resources:
            if self._supported_rds_versions(resource) and not resource.iam_database_authentication_enabled:
                issues.append(
                    Issue(
                        f'The {resource.get_type()} `{resource.get_friendly_name()}` has IAM database authentication disabled', resource, resource))
            return issues

    def should_run_rule(self, environment_context: EnvironmentContext) -> bool:
        return bool(environment_context.rds_clusters or environment_context.rds_instances)

    def _supported_rds_versions(self, rds_resource: Union[RdsCluster, RdsInstance]) -> bool:
        supported_mysql_versions = ['5.6.34', '5.7.16', '8.0.16']
        supported_postgres_versions = ['9.5.15', '9.6.11', '10.6', '11', '12', '13']
        if isinstance(rds_resource, RdsCluster):
            return True
        else:
            if not rds_resource.engine_version:
                return True
            elif 'mysql' in rds_resource.engine_type.lower():
                return self._check_version(rds_resource.engine_version, supported_mysql_versions, 'mysql')
            elif 'postgresql' in rds_resource.engine_type.lower():
                return self._check_version(rds_resource.engine_version, supported_postgres_versions, 'postgresql')
            else:
                return False

    def _check_version(self, rds_ver: str, supported_ver_list: list, engine_type: str) -> bool:
        if version.parse(rds_ver) < version.parse(supported_ver_list[0]):
            return False
        elif version.parse(rds_ver) > version.parse(supported_ver_list[-1]):
            return True
        else:
            if engine_type == 'mysql':
                return any((version.parse(rds_ver) >= version.parse(ver)) for ver in supported_ver_list[1:-1]
                           if self._mysql_condition(rds_ver, ver))
            else:
                return any((version.parse(rds_ver) >= version.parse(ver)) for ver in supported_ver_list[1:-1]
                           if self._postgresql_condition(rds_ver, ver))

    @staticmethod
    def _mysql_condition(rds_ver: str, supported_ver: str) -> bool:
        return (version.parse(rds_ver).major, version.parse(rds_ver).minor) == \
               (version.parse(supported_ver).major, version.parse(supported_ver).minor)

    @staticmethod
    def _postgresql_condition(rds_ver: str, supported_ver: str) -> bool:
        return version.parse(rds_ver).major == version.parse(supported_ver).major
