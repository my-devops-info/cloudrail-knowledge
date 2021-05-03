import unittest

from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.aws.s3.s3_bucket import S3Bucket
from cloudrail.knowledge.context.aws.s3.s3_bucket_encryption import S3BucketEncryption
from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.context.terraform_state import TerraformState
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_s3_buckets_encrypted_rule import \
    EnsureS3BucketsEncryptedRule
from cloudrail.knowledge.rules.base_rule import RuleResultType
from tests.rule_test_utils import create_empty_entity


class TestEnsureS3BucketsEncryptedRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureS3BucketsEncryptedRule()

    def test_not_car_s3_buckets_encrypted_at_rest_fail(self):
        # Arrange
        s3_bucket: S3Bucket = create_empty_entity(S3Bucket)
        terraform_state = create_empty_entity(TerraformState)
        s3_bucket.terraform_state = terraform_state
        s3_bucket.terraform_state.is_new = True
        s3_bucket.encryption_data = S3BucketEncryption(bucket_name='s3_bucket', encrypted=False, region='us-east-1', account='111111')
        context = EnvironmentContext(s3_buckets=AliasesDict(s3_bucket))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_not_car_s3_buckets_encrypted_at_rest_pass(self):
        # Arrange
        context = EnvironmentContext()
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
