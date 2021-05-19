from typing import List, Dict

from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureAmiSnapshotEncryptedRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_ami_encrypt_snapshots_at_rest_creating'

    def execute(self, env_context: EnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for image in env_context.ec2_images:
            if image.snap_data.is_new_resource and not image.snap_data.is_encrypted:
                issues.append(
                    Issue(
                        f'The {image.get_type()} `{image.get_friendly_name()}` uses snapshot '
                        f'`{image.snap_id}`, which is not encrypted', image, image.snap_data))
        return issues

    def should_run_rule(self, environment_context: EnvironmentContext) -> bool:
        return bool(environment_context.ec2_images)
