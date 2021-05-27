import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.rules.azure.non_context_aware.unused_network_security_group_rule import UnusedNetworkSecurityGroupRule
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.network.azure_nsg import AzureNetworkSecurityGroup


class TestUnusedNetworkSecurityGroupRuleAz(unittest.TestCase):
    def setUp(self):
        self.rule = UnusedNetworkSecurityGroupRule()

    def test_non_car_unused_network_security_group_fail(self):
        # Arrange
        nsg = AzureNetworkSecurityGroup("subscr", "nsg-id", "rg", "westeu", "mynsg")
        context = AzureEnvironmentContext(net_security_groups=AliasesDict(*[nsg]))
        #context = AzureEnvironmentContext(net_security_groups=[nsg])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_unused_network_security_group_pass_with_nic(self):
        # Arrange
        nsg = AzureNetworkSecurityGroup("subscr", "nsg-id", "rg", "westeu", "mynsg")
        nsg.network_interfaces=["mynic"]
        context = AzureEnvironmentContext(net_security_groups=AliasesDict(*[nsg]))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_unused_network_security_group_pass_with_snet(self):
        # Arrange
        nsg = AzureNetworkSecurityGroup("subscr", "nsg-id", "rg", "westeu", "mynsg")
        nsg.subnets=["mysubnet"]
        context = AzureEnvironmentContext(net_security_groups=AliasesDict(*[nsg]))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
        
    def test_non_car_unused_network_security_group_pass_with_nic_snet(self):
        # Arrange
        nsg = AzureNetworkSecurityGroup("subscr", "nsg-id", "rg", "westeu", "mynsg")
        nsg.network_interfaces=["mynic"]
        nsg.subnets=["mysubnet"]
        context = AzureEnvironmentContext(net_security_groups=AliasesDict(*[nsg]))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
