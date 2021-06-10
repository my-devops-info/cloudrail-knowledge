from typing import List, Dict
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureEc2InstanceEbsOptimizedRule(AwsBaseRule):

    def get_id(self) -> str:
        return 'non_car_ec2_instance_is_ebs_optimized'

    def execute(self, env_context: AwsEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        instance_types_default_optimized = env_context.get_all_ec2_instance_types_with_default_ebs_optimization()
        instance_types = [ec2_inst_type.instance_type for ec2_inst_type in instance_types_default_optimized]
        for instance in env_context.ec2s:
            if (instance_types_default_optimized and instance.instance_type not in instance_types and not instance.ebs_optimized)\
                    or (not instance_types_default_optimized and not instance.ebs_optimized):
                issues.append(
                    Issue(
                        f'The {instance.get_type()} `{instance.get_friendly_name()}` is not EBS optimized', instance, instance))
        return issues

    def should_run_rule(self, environment_context: AwsEnvironmentContext) -> bool:
        return bool(environment_context.ec2s)
