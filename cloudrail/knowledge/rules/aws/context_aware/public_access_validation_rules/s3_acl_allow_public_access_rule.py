from typing import List, Dict

from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.utils.policy_utils import is_any_resource_based_action_allowed
from cloudrail.knowledge.utils.s3_public_access_evaluator import S3PublicAccessEvaluator, PublicAccessResults
from cloudrail.knowledge.utils.policy_evaluator import PolicyEvaluation
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType
from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.context.aws.aws_resource import AwsResource


class S3AclAllowPublicAccessRule(AwsBaseRule):
    # Notice:
    # - this rule don't issue on violation on the bucket object level
    def execute(self, env_context: EnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues_list: List[Issue] = []
        for bucket in env_context.s3_buckets:
            evaluator: S3PublicAccessEvaluator = S3PublicAccessEvaluator(bucket, True)
            results_map: Dict[AwsResource, PublicAccessResults] = evaluator.evaluate()
            for resource, results in results_map.items():
                if is_any_resource_based_action_allowed(PolicyEvaluation(resource_allowed_actions=results.allowed_actions,
                                                                         resource_denied_actions=results.denied_actions)):
                    issues_list.append(Issue(f"~The {bucket.get_type()}~. `{bucket.get_friendly_name()}` is publicly exposed through"
                                             f" the `{resource.get_type()}` with identifier `{resource.get_friendly_name()}`.",
                                             bucket, resource))
        return issues_list

    def get_id(self) -> str:
        return "s3_acl_disallow_public_and_cross_account"

    def should_run_rule(self, environment_context: EnvironmentContext) -> bool:
        return bool(environment_context.s3_buckets)
