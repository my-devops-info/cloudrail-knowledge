import unittest

from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.aws.iam.policy import Policy, S3Policy
from cloudrail.knowledge.context.aws.iam.policy_statement import PolicyStatement, StatementEffect
from cloudrail.knowledge.context.aws.iam.principal import Principal, PrincipalType
from cloudrail.knowledge.context.aws.kms.kms_key import KmsKey
from cloudrail.knowledge.context.aws.kms.kms_key_manager import KeyManager
from cloudrail.knowledge.context.aws.kms.kms_key_policy import KmsKeyPolicy
from cloudrail.knowledge.context.aws.lambda_.lambda_function import LambdaFunction
from cloudrail.knowledge.context.aws.s3.s3_bucket import S3Bucket
from cloudrail.knowledge.context.aws.secretsmanager.secrets_manager_secret import SecretsManagerSecret
from cloudrail.knowledge.context.aws.secretsmanager.secrets_manager_secret_policy import SecretsManagerSecretPolicy
from cloudrail.knowledge.context.aws.sqs.sqs_queue import SqsQueue
from cloudrail.knowledge.context.aws.sqs.sqs_queue_policy import SqsQueuePolicy
from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.policy_wildcard_violation.ensure_policy_not_use_wildcard_actions_rules import \
    EnsureKmsKeyPolicyNotUseWildcard, EnsureLambdaFunctionPolicyNotUseWildcard, EnsureS3BucketPolicyNotUseWildcard, \
    EnsureSecretsManagerSecretPolicyNotUseWildcard, \
    EnsureSqsQueuePolicyNotUseWildcard
from cloudrail.knowledge.rules.base_rule import RuleResultType
from tests.rule_test_utils import create_empty_entity


class TestEnsureLambdaFunctionPolicyNotUseWildcard(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureLambdaFunctionPolicyNotUseWildcard()

    def test_non_car_aws_lambda_func_policy_wildcard_fail(self):
        # Arrange
        lambda_func: LambdaFunction = create_empty_entity(LambdaFunction)
        lambda_func.resource_based_policy = Policy('account', [PolicyStatement(StatementEffect.ALLOW,
                                                                               ['lambda:*'], ['*'], Principal(PrincipalType.PUBLIC, ['*']))])
        context = EnvironmentContext(lambda_function_list=[lambda_func])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("is using wildcard action `lambda:*`, and principal `AWS: *`, without any condition" in result.issues[0].evidence)

    def test_non_car_aws_lambda_func_policy_wildcard__only_action__fail(self):
        # Arrange
        lambda_func: LambdaFunction = create_empty_entity(LambdaFunction)
        lambda_func.resource_based_policy = Policy('account', [PolicyStatement(StatementEffect.ALLOW,
                                                                               ['lambda:*'], ['*'],
                                                                               Principal(PrincipalType.AWS, ['arn:aws:iam::123456789012:root']))])
        context = EnvironmentContext(lambda_function_list=[lambda_func])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("is using wildcard action `lambda:*`, without any condition" in result.issues[0].evidence)

    def test_non_car_aws_lambda_func_policy_wildcard__only_principal__fail(self):
        # Arrange
        lambda_func: LambdaFunction = create_empty_entity(LambdaFunction)
        lambda_func.resource_based_policy = Policy('account', [PolicyStatement(StatementEffect.ALLOW,
                                                                               ['lambda:GetLogs'], ['*'],
                                                                               Principal(PrincipalType.PUBLIC, ['*']))])
        context = EnvironmentContext(lambda_function_list=[lambda_func])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("is using principal `AWS: *`, without any condition" in result.issues[0].evidence)

    def test_non_car_aws_lambda_func_policy_wildcard__no_policy__fail(self):
        # Arrange
        lambda_func: LambdaFunction = create_empty_entity(LambdaFunction)
        context = EnvironmentContext(lambda_function_list=[lambda_func])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("There is no resource policy or no statements attached to" in result.issues[0].evidence)

    def test_non_car_aws_lambda_func_policy_wildcard_pass(self):
        # Arrange
        lambda_func: LambdaFunction = create_empty_entity(LambdaFunction)
        lambda_func.resource_based_policy = Policy('account', [PolicyStatement(StatementEffect.ALLOW,
                                                                               ['lambda:GetLogs'], ['*'],
                                                                               Principal(PrincipalType.AWS, ['arn:aws:iam::123456789012:root']))])
        context = EnvironmentContext(lambda_function_list=[lambda_func])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))


class TestEnsureKmsKeyPolicyNotUseWildcard(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureKmsKeyPolicyNotUseWildcard()

    def test_non_car_aws_kms_key_policy_wildcard_fail(self):
        # Arrange
        kms_key: KmsKey = create_empty_entity(KmsKey)
        kms_key.policy = KmsKeyPolicy('kms_key', [PolicyStatement(StatementEffect.ALLOW,
                                                                  ['kms:*'], ['*'], Principal(PrincipalType.PUBLIC, ['*']))],
                                      'raw_doc_string', 'account')
        kms_key.key_manager = KeyManager.CUSTOMER
        context = EnvironmentContext(kms_keys=[kms_key])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("is using wildcard action `kms:*`, and principal `AWS: *`, without any condition" in result.issues[0].evidence)

    def test_non_car_aws_kms_key_policy_wildcard__only_action__fail(self):
        # Arrange
        kms_key: KmsKey = create_empty_entity(KmsKey)
        kms_key.policy = KmsKeyPolicy('kms_key', [PolicyStatement(StatementEffect.ALLOW,
                                                                  ['kms:*'], ['*'],
                                                                  Principal(PrincipalType.PUBLIC, ['arn:aws:iam::123456789012:root']))],
                                      'raw_doc_string', 'account')
        kms_key.key_manager = KeyManager.CUSTOMER
        context = EnvironmentContext(kms_keys=[kms_key])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("is using wildcard action `kms:*`, without any condition" in result.issues[0].evidence)

    def test_non_car_aws_kms_key_policy_wildcard__only_principal__fail(self):
        # Arrange
        kms_key: KmsKey = create_empty_entity(KmsKey)
        kms_key.policy = KmsKeyPolicy('kms_key', [PolicyStatement(StatementEffect.ALLOW,
                                                                  ['kms:GetLogs'], ['*'],
                                                                  Principal(PrincipalType.PUBLIC, ['*']))],
                                      'raw_doc_string', 'account')
        kms_key.key_manager = KeyManager.CUSTOMER
        context = EnvironmentContext(kms_keys=[kms_key])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("is using principal `AWS: *`, without any condition" in result.issues[0].evidence)

    def test_non_car_aws_kms_key_policy_wildcard__no_policy__fail(self):
        # Arrange
        kms_key: KmsKey = create_empty_entity(KmsKey)
        kms_key.key_manager = KeyManager.CUSTOMER
        context = EnvironmentContext(kms_keys=[kms_key])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("There is no resource policy or no statements attached to" in result.issues[0].evidence)

    def test_non_car_aws_kms_key_policy_wildcard_pass(self):
        # Arrange
        kms_key: KmsKey = create_empty_entity(KmsKey)
        kms_key.policy = KmsKeyPolicy('kms_key', [PolicyStatement(StatementEffect.ALLOW,
                                                                  ['kms:GetLogs'], ['*'],
                                                                  Principal(PrincipalType.PUBLIC, ['arn:aws:iam::123456789012:root']))],
                                      'raw_doc_string', 'account')
        kms_key.key_manager = KeyManager.CUSTOMER
        context = EnvironmentContext(kms_keys=[kms_key])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_aws_kms_key_policy_wildcard__no_customer_key__skip(self):
        # Arrange
        kms_key: KmsKey = create_empty_entity(KmsKey)
        kms_key.policy = KmsKeyPolicy('kms_key', [PolicyStatement(StatementEffect.ALLOW,
                                                                  ['kms:*'], ['*'], Principal(PrincipalType.PUBLIC, ['*']))],
                                      'raw_doc_string', 'account')
        kms_key.key_manager = KeyManager.AWS
        context = EnvironmentContext(kms_keys=[kms_key])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SKIPPED, result.status)
        self.assertEqual(0, len(result.issues))


class TestEnsureSqsQueuePolicyNotUseWildcard(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureSqsQueuePolicyNotUseWildcard()

    def test_non_car_aws_sqs_policy_wildcard_fail(self):
        # Arrange
        sqs_queue: SqsQueue = create_empty_entity(SqsQueue)
        sqs_queue.policy = SqsQueuePolicy('queue_name', [PolicyStatement(StatementEffect.ALLOW,
                                                                         ['sqs:*'], ['*'], Principal(PrincipalType.PUBLIC, ['*']))],
                                          'raw_doc_string', 'account')
        context = EnvironmentContext(sqs_queues=[sqs_queue])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("is using wildcard action `sqs:*`, and principal `AWS: *`, without any condition" in result.issues[0].evidence)

    def test_non_car_aws_sqs_policy_wildcard__only_action__fail(self):
        # Arrange
        sqs_queue: SqsQueue = create_empty_entity(SqsQueue)
        sqs_queue.policy = SqsQueuePolicy('queue_name', [PolicyStatement(StatementEffect.ALLOW,
                                                                         ['sqs:*'], ['*'],
                                                                         Principal(PrincipalType.AWS, ['arn:aws:iam::123456789012:root']))],
                                          'raw_doc_string', 'account')
        context = EnvironmentContext(sqs_queues=[sqs_queue])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("is using wildcard action `sqs:*`, without any condition" in result.issues[0].evidence)

    def test_non_car_aws_sqs_policy_wildcard__only_principal__fail(self):
        # Arrange
        sqs_queue: SqsQueue = create_empty_entity(SqsQueue)
        sqs_queue.policy = SqsQueuePolicy('queue_name', [PolicyStatement(StatementEffect.ALLOW,
                                                                         ['sqs:GetLogs'], ['*'],
                                                                         Principal(PrincipalType.PUBLIC, ['*']))],
                                          'raw_doc_string', 'account')
        context = EnvironmentContext(sqs_queues=[sqs_queue])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("is using principal `AWS: *`, without any condition" in result.issues[0].evidence)

    def test_non_car_aws_sqs_policy_wildcard__no_policy__fail(self):
        # Arrange
        sqs_queue: SqsQueue = create_empty_entity(SqsQueue)
        context = EnvironmentContext(sqs_queues=[sqs_queue])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("There is no resource policy or no statements attached to" in result.issues[0].evidence)

    def test_non_car_aws_sqs_policy_wildcard_pass(self):
        # Arrange
        sqs_queue: SqsQueue = create_empty_entity(SqsQueue)
        sqs_queue.policy = SqsQueuePolicy('queue_name', [PolicyStatement(StatementEffect.ALLOW,
                                                                         ['sqs:GetLogs'], ['*'],
                                                                         Principal(PrincipalType.PUBLIC, ['arn:aws:iam::123456789012:root']))],
                                          'raw_doc_string', 'account')
        context = EnvironmentContext(sqs_queues=[sqs_queue])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))


class TestEnsureSecretsManagerSecretPolicyNotUseWildcard(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureSecretsManagerSecretPolicyNotUseWildcard()

    def test_non_car_aws_secrets_manager_secret_policy_wildcard_fail(self):
        # Arrange
        secret_manager: SecretsManagerSecret = create_empty_entity(SecretsManagerSecret)
        secret_manager.policy = SecretsManagerSecretPolicy('secret_arn', [PolicyStatement(StatementEffect.ALLOW,
                                                                                          ['secretsmanager:*'],
                                                                                          ['*'], Principal(PrincipalType.PUBLIC, ['*']))],
                                                           'raw_doc_string', 'account')
        context = EnvironmentContext(secrets_manager_secrets=[secret_manager])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("is using wildcard action `secretsmanager:*`, and principal `AWS: *`, without any condition" in result.issues[0].evidence)

    def test_non_car_aws_secrets_manager_secret_policy_wildcard__only_action__fail(self):
        # Arrange
        secret_manager: SecretsManagerSecret = create_empty_entity(SecretsManagerSecret)
        secret_manager.policy = SecretsManagerSecretPolicy('secret_arn', [PolicyStatement(StatementEffect.ALLOW,
                                                                                          ['secretsmanager:*'],
                                                                                          ['*'],
                                                                                          Principal(PrincipalType.PUBLIC,
                                                                                                    ['arn:aws:iam::123456789012:root']))],
                                                           'raw_doc_string', 'account')
        context = EnvironmentContext(secrets_manager_secrets=[secret_manager])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("is using wildcard action `secretsmanager:*`, without any condition" in result.issues[0].evidence)

    def test_non_car_aws_secrets_manager_secret_policy_wildcard__only_principal__fail(self):
        # Arrange
        secret_manager: SecretsManagerSecret = create_empty_entity(SecretsManagerSecret)
        secret_manager.policy = SecretsManagerSecretPolicy('secret_arn', [PolicyStatement(StatementEffect.ALLOW,
                                                                                          ['secretsmanager:GetLogs'],
                                                                                          ['*'],
                                                                                          Principal(PrincipalType.PUBLIC, ['*']))],
                                                           'raw_doc_string', 'account')
        context = EnvironmentContext(secrets_manager_secrets=[secret_manager])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("is using principal `AWS: *`, without any condition" in result.issues[0].evidence)

    def test_non_car_aws_secrets_manager_secret_policy_wildcard__no_policy__fail(self):
        # Arrange
        secret_manager: SecretsManagerSecret = create_empty_entity(SecretsManagerSecret)
        context = EnvironmentContext(secrets_manager_secrets=[secret_manager])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("There is no resource policy or no statements attached to" in result.issues[0].evidence)

    def test_non_car_aws_secrets_manager_secret_policy_wildcard_pass(self):
        # Arrange
        secret_manager: SecretsManagerSecret = create_empty_entity(SecretsManagerSecret)
        secret_manager.policy = SecretsManagerSecretPolicy('secret_arn', [PolicyStatement(StatementEffect.ALLOW,
                                                                                          ['secretsmanager:GetLogs'],
                                                                                          ['*'],
                                                                                          Principal(PrincipalType.PUBLIC,
                                                                                                    ['arn:aws:iam::123456789012:root']))],
                                                           'raw_doc_string', 'account')
        context = EnvironmentContext(secrets_manager_secrets=[secret_manager])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))


class TestEnsureS3BucketPolicyNotUseWildcard(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureS3BucketPolicyNotUseWildcard()

    def test_non_car_aws_s3_bucket_policy_wildcard_fail(self):
        # Arrange
        s3_bucket = S3Bucket('111111', 's3_bucket_name', 's3_bucket_arn')
        s3_bucket.resource_based_policy = S3Policy('account', 'bucket_name', [PolicyStatement(StatementEffect.ALLOW, ['s3:*'],
                                                                                              ['*'], Principal(PrincipalType.PUBLIC, ['*']))],
                                                   'raw_doc')
        context = EnvironmentContext(s3_buckets=AliasesDict(*[s3_bucket]))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("is using wildcard action `s3:*`, and principal `AWS: *`, without any condition" in result.issues[0].evidence)

    def test_non_car_aws_s3_bucket_policy_wildcard__only_action__fail(self):
        # Arrange
        s3_bucket = S3Bucket('111111', 's3_bucket_name', 's3_bucket_arn')
        s3_bucket.resource_based_policy = S3Policy('account', 'bucket_name', [PolicyStatement(StatementEffect.ALLOW, ['s3:*'],
                                                                                              ['*'], Principal(PrincipalType.PUBLIC,
                                                                                                               ['arn:aws:iam::123456789012:root']))],
                                                   'raw_doc')
        context = EnvironmentContext(s3_buckets=AliasesDict(*[s3_bucket]))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("is using wildcard action `s3:*`, without any condition" in result.issues[0].evidence)

    def test_non_car_aws_s3_bucket_policy_wildcard__only_principal__fail(self):
        # Arrange
        s3_bucket = S3Bucket('111111', 's3_bucket_name', 's3_bucket_arn')
        s3_bucket.resource_based_policy = S3Policy('account', 'bucket_name', [PolicyStatement(StatementEffect.ALLOW, ['s3:GetLogs'],
                                                                                              ['*'], Principal(PrincipalType.PUBLIC, ['*']))],
                                                   'raw_doc')
        context = EnvironmentContext(s3_buckets=AliasesDict(*[s3_bucket]))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("is using principal `AWS: *`, without any condition" in result.issues[0].evidence)

    def test_non_car_aws_s3_bucket_policy_wildcard__no_policy__fail(self):
        # Arrange
        s3_bucket = S3Bucket('111111', 's3_bucket_name', 's3_bucket_arn')
        context = EnvironmentContext(s3_buckets=AliasesDict(*[s3_bucket]))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue("There is no resource policy or no statements attached to" in result.issues[0].evidence)

    def test_non_car_aws_s3_bucket_policy_wildcard_wildcard_pass(self):
        # Arrange
        s3_bucket = S3Bucket('111111', 's3_bucket_name', 's3_bucket_arn')
        s3_bucket.resource_based_policy = S3Policy('account', 'bucket_name', [PolicyStatement(StatementEffect.ALLOW, ['s3:GetLogs'],
                                                                                              ['*'], Principal(PrincipalType.PUBLIC,
                                                                                                               ['arn:aws:iam::123456789012:root']))],
                                                   'raw_doc')
        context = EnvironmentContext(s3_buckets=AliasesDict(*[s3_bucket]))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
