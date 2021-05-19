from typing import List, Dict

from cloudrail.knowledge.context.aws.aws_connection import PolicyEvaluation
from cloudrail.knowledge.context.aws.iam.policy import Policy
from cloudrail.knowledge.context.aws.s3.s3_bucket import S3Bucket
from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.aws.aws_base_rule import AwsBaseRule
from cloudrail.knowledge.rules.base_rule import Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType
from cloudrail.knowledge.utils.policy_evaluator import is_action_subset_allowed


class S3BucketLambdaIndirectExposureRule(AwsBaseRule):

    def get_id(self) -> str:
        return 's3_lambda_indirect_exposure'

    def execute(self, env_context: EnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for api_gateway in env_context.rest_api_gw:
            if not api_gateway.is_public:
                continue
            for agw_method in api_gateway.api_gateway_methods:
                for resource_arn, evaluation_results in agw_method.integration.lambda_func_integration.iam_role.policy_evaluation_result_map.items():
                    s3_bucket: S3Bucket = env_context.s3_buckets.get(resource_arn)
                    if s3_bucket and \
                            self._allows_access_to_buckets(evaluation_results,
                                                           agw_method.integration.lambda_func_integration.iam_role.permissions_policies):

                        issues.append(Issue(evidence=f"The S3 Bucket `{s3_bucket.get_friendly_name()}`. is exposed via the execution role in "
                                                     f"Lambda Function `{agw_method.integration.lambda_func_integration.get_friendly_name()}`. "
                                                     f"which can be invoked by public API Gateway `{agw_method.get_friendly_name()}`",
                                            exposed=s3_bucket,
                                            violating=agw_method.integration.lambda_func_integration))
        return issues

    def should_run_rule(self, environment_context: EnvironmentContext) -> bool:
        return bool(environment_context.s3_buckets
                    and environment_context.lambda_function_list
                    and environment_context.api_gateway_methods)

    @staticmethod
    def _allows_access_to_buckets(results: PolicyEvaluation, policies: List[Policy]):
        if is_action_subset_allowed(results, 's3:*'):
            for statement in [statement for policy in policies for statement in policy.statements]:
                if any(resource == '*' for resource in statement.resources) and \
                        any(action.startswith('s3:') or action == '*' for action in statement.actions):
                    return True
        return False
