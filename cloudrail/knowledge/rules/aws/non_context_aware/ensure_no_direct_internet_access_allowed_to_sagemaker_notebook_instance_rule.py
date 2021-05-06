from typing import List, Dict
from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureNoDirectInternetAccessAllowedToSagemakerNotebookInstanceRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_no_direct_internet_access_allowed_from_sagemaker_notebook_instance_rule'

    def execute(self, env_context: EnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for sagemaker_instance in env_context.sagemaker_notebook_instances:
            if sagemaker_instance.direct_internet_access:
                issues.append(
                    Issue(
                        f'The {sagemaker_instance.get_type()} `{sagemaker_instance.get_friendly_name()}` uses '
                        f'direct internet access', sagemaker_instance, sagemaker_instance))
            return issues

    def should_run_rule(self, environment_context: EnvironmentContext) -> bool:
        return bool(environment_context.sagemaker_notebook_instances)
