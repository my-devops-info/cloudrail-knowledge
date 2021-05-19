import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.ec2.ec2_image import Ec2Image
from cloudrail.knowledge.context.aws.ec2.ebs_snapshot import EBSSnapshot
from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest \
    .ensure_ec2_image_encrypted_rule import EnsureAmiSnapshotEncryptedRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureAmiSnapshotEncryptedRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureAmiSnapshotEncryptedRule()

    def test_non_car_ec2_image_encrypted_fail(self):
        # Arrange
        ec2_image: Ec2Image = create_empty_entity(Ec2Image)
        snap_data: EBSSnapshot = create_empty_entity(EBSSnapshot)
        snap_data.is_encrypted = False
        ec2_image.snap_id = 'snap-id'
        ec2_image.snap_data = snap_data
        context = EnvironmentContext(ec2_images=[ec2_image])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_ec2_image_encrypted_pass(self):
        # Arrange
        ec2_image: Ec2Image = create_empty_entity(Ec2Image)
        snap_data: EBSSnapshot = create_empty_entity(EBSSnapshot)
        snap_data.is_encrypted = True
        ec2_image.snap_id = 'snap-id'
        ec2_image.snap_data = snap_data
        context = EnvironmentContext(ec2_images=[ec2_image])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
