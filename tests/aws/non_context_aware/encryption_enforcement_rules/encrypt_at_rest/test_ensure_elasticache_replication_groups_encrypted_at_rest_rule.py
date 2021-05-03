import unittest

from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.knowledge.context.aws.elasticache.elasti_cache_replication_group import ElastiCacheReplicationGroup
from cloudrail.knowledge.context.terraform_state import TerraformState
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_elasticache_replication_groups_encrypted_at_rest_rule import \
    EnsureElasticacheReplicationGroupsEncryptedAtRestRule
from cloudrail.dev_tools.rule_test_utils import create_empty_entity


class TestEnsureElasticacheReplicationGroupsEncryptedAtRestRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureElasticacheReplicationGroupsEncryptedAtRestRule()

    def test_non_car_elasticache_replication_group_encrypt_at_rest_creating_fail(self):
        # Arrange
        elasti_cache_replication_group: ElastiCacheReplicationGroup = create_empty_entity(ElastiCacheReplicationGroup)
        terraform_state = create_empty_entity(TerraformState)
        elasti_cache_replication_group.terraform_state = terraform_state
        elasti_cache_replication_group.terraform_state.is_new = True
        elasti_cache_replication_group.encrypted_at_rest = False
        context = EnvironmentContext(elasti_cache_replication_groups=[elasti_cache_replication_group])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_elasticache_replication_group_encrypt_at_rest_creating__is_encrypted_at_rest_pass(self):
        # Arrange
        elasti_cache_replication_group: ElastiCacheReplicationGroup = create_empty_entity(ElastiCacheReplicationGroup)
        terraform_state = create_empty_entity(TerraformState)
        elasti_cache_replication_group.terraform_state = terraform_state
        elasti_cache_replication_group.terraform_state.is_new = True
        elasti_cache_replication_group.encrypted_at_rest = True
        context = EnvironmentContext(elasti_cache_replication_groups=[elasti_cache_replication_group])

        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_elasticache_replication_group_encrypt_at_rest_creating__not_new_tf_resource__pass(self):
        # Arrange
        elasti_cache_replication_group: ElastiCacheReplicationGroup = create_empty_entity(ElastiCacheReplicationGroup)
        terraform_state = create_empty_entity(TerraformState)
        elasti_cache_replication_group.terraform_state = terraform_state
        elasti_cache_replication_group.terraform_state.is_new = False
        elasti_cache_replication_group.encrypted_at_rest = False
        context = EnvironmentContext(elasti_cache_replication_groups=[elasti_cache_replication_group])

        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
