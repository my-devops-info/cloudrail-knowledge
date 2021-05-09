# import unittest
#
# from cloudrail.knowledge.context.aliases_dict import AliasesDict
# from cloudrail.knowledge.context.aws.apigateway.api_gateway_integration import ApiGatewayIntegration
# from cloudrail.knowledge.context.aws.apigateway.api_gateway_method import ApiGatewayMethod
# from cloudrail.knowledge.context.aws.apigateway.api_gateway_method_settings import ApiGatewayMethodSettings, RestApiMethods
# from cloudrail.knowledge.context.aws.apigateway.rest_api_gw import RestApiGw
# from cloudrail.knowledge.context.aws.aws_connection import PolicyEvaluation
# from cloudrail.knowledge.context.aws.iam.policy import AssumeRolePolicy, Policy, S3Policy
# from cloudrail.knowledge.context.aws.iam.policy_statement import PolicyStatement, StatementCondition, StatementEffect
# from cloudrail.knowledge.context.aws.iam.principal import Principal, PrincipalType
# from cloudrail.knowledge.context.aws.iam.role import Role
# from cloudrail.knowledge.context.aws.lambda_.lambda_function import LambdaFunction
# from cloudrail.knowledge.context.aws.s3.s3_bucket import S3Bucket
# from cloudrail.knowledge.context.environment_context import EnvironmentContext
# from cloudrail.knowledge.rules.aws.context_aware.indirect_public_access_rules.s3_bucket_lambda_indirect_exposure_rule import \
#     S3BucketLambdaIndirectExposureRule
# from cloudrail.knowledge.rules.base_rule import RuleResultType
# from cloudrail.dev_tools.rule_test_utils import create_empty_entity
#
#
# class TestS3BucketLambdaIndirectExposureRule(unittest.TestCase):
#     def setUp(self):
#         self.rule = S3BucketLambdaIndirectExposureRule()
#
#     def test_s3_lambda_indirect_exposure_fail(self):
#         # Arrange
#         s3_bucket = S3Bucket('111111', 's3_bucket_name', 's3_bucket_arn')
#         rest_api_gw: RestApiGw = create_empty_entity(RestApiGw)
#         api_gw_method: ApiGatewayMethod = create_empty_entity(ApiGatewayMethod)
#         method_settings: ApiGatewayMethodSettings = create_empty_entity(ApiGatewayMethodSettings)
#         gw_integration: ApiGatewayIntegration = create_empty_entity(ApiGatewayIntegration)
#         role: Role = create_empty_entity(Role)
#         policy_eval: PolicyEvaluation = create_empty_entity(PolicyEvaluation)
#         policy_condition = [StatementCondition(operator='BOOL', key='aws:SecureTransport', values=['false'])]
#         s3_bucket.resource_based_policy = S3Policy('account', 'bucket_name', [PolicyStatement(StatementEffect.DENY, ['s3:*'],
#                                                                                               ['*'], Principal(PrincipalType.PUBLIC, ['*']),
#                                                                                               'statement_id', policy_condition)],
#                                                    'raw_doc')
#         lambda_func: LambdaFunction = create_empty_entity(LambdaFunction)
#         lambda_func.resource_based_policy = Policy('account', [PolicyStatement(StatementEffect.ALLOW,
#                                                                                ['lambda:*'], ['*'], Principal(PrincipalType.PUBLIC, ['*']))])
#         assume_role_policy = AssumeRolePolicy('111111111', 'test-role', 'arn:aws:iam::123456789:role/test-role',
#                                               [PolicyStatement(StatementEffect.ALLOW,
#                                                                ['sts:AssumeRole'],
#                                                                ['*'],
#                                                                Principal(PrincipalType.PUBLIC, ['*']))], 'state_id')
#         role.assume_role_policy = assume_role_policy
#         policy_eval.resource_denied_actions = {'s3:PutObject'}
#         policy_eval.resource_allowed_actions = set()
#         role.policy_evaluation_result_map = {'something', policy_eval}
#         method_settings.http_method = RestApiMethods.HEAD
#         method_settings.stage_name = 'method_tests'
#         rest_api_gw.method_settings = method_settings
#         rest_api_gw.rest_api_gw_id = 'rest_api_id'
#         api_gw_method.rest_api_id = 'rest_api_id'
#         gw_integration.lambda_func_integration = lambda_func
#         gw_integration.lambda_func_integration.iam_role = role
#         api_gw_method.integration = gw_integration
#         context = EnvironmentContext(s3_buckets=AliasesDict(*[s3_bucket]), lambda_function_list=[lambda_func], rest_api_gw=[rest_api_gw],
#                                      api_gateway_methods=[api_gw_method])
#         # Act
#         result = self.rule.run(context, {})
#         # Assert
#         self.assertEqual(RuleResultType.FAILED, result.status)
#         self.assertEqual(1, len(result.issues))
#
#     def test_s3_lambda_indirect_exposure_pass(self):
#         # Arrange
#         context = EnvironmentContext()
#         # Act
#         result = self.rule.run(context, {})
#         # Assert
#         self.assertEqual(RuleResultType.SUCCESS, result.status)
#         self.assertEqual(0, len(result.issues))
