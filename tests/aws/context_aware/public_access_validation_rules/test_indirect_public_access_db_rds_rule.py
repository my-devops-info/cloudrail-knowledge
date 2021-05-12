# import unittest
#
# from cloudrail.knowledge.context.aws.aws_connection import ConnectionDirectionType, ConnectionInstance, PolicyConnectionProperty, \
#     PortConnectionProperty, PrivateConnectionDetail, \
#     PublicConnectionDetail
# from cloudrail.knowledge.context.aws.ec2.network_acl import NetworkAcl
# from cloudrail.knowledge.context.aws.ec2.network_interface import NetworkInterface
# from cloudrail.knowledge.context.aws.ec2.security_group import SecurityGroup
# from cloudrail.knowledge.context.aws.ec2.security_group_rule import ConnectionType, SecurityGroupRule, SecurityGroupRulePropertyType
# from cloudrail.knowledge.context.aws.ec2.subnet import Subnet
# from cloudrail.knowledge.context.aws.networking_config.network_resource import NetworkResource
# from cloudrail.knowledge.context.aws.rds.rds_cluster import RdsCluster
# from cloudrail.knowledge.context.aws.rds.rds_instance import RdsInstance
# from cloudrail.knowledge.context.environment_context import EnvironmentContext
# from cloudrail.knowledge.rules.aws.context_aware.indirect_public_access_rules.indirect_public_access_db_rds_rule import IndirectPublicAccessDbRds
# from cloudrail.knowledge.rules.base_rule import RuleResultType
# from cloudrail.dev_tools.rule_test_utils import create_empty_entity
#
#
# class TestIndirectPublicAccessDbRds(unittest.TestCase):
#     def setUp(self):
#         self.rule = IndirectPublicAccessDbRds()
#
#     def test_indirect_public_access_db_rds__rds_cluster__fail(self):
#         # Arrange
#         rds_cluster: RdsCluster = create_empty_entity(RdsCluster)
#         network_resource: NetworkResource = create_empty_entity(NetworkResource)
#         network_interface = create_empty_entity(NetworkInterface)
#         security_group: SecurityGroup = create_empty_entity(SecurityGroup)
#         rds_instance: RdsInstance = create_empty_entity(RdsInstance)
#         subnet: Subnet = create_empty_entity(Subnet)
#         network_acl: NetworkAcl = create_empty_entity(NetworkAcl)
#         network_acl.name = 'subnet_network_acl_name'
#         subnet.name = 'subnet_testing_name'
#         subnet.subnet_id = 'subnet_testing_id'
#         subnet.network_acl = network_acl
#         inbound_permissions = [SecurityGroupRule(0, 65535, '-1', SecurityGroupRulePropertyType.IP_RANGES,
#                                                  '0.0.0.0/0', False, ConnectionType.Inbound,
#                                                  'AllInclusiveSecurityGroup', 'us-east-1', '1111111')]
#         outbound_permissions = [SecurityGroupRule(0, 65535, '-1',
#                                                   SecurityGroupRulePropertyType.IP_RANGES, '10.10.10.0/24', False,
#                                                   ConnectionType.Outbound, 'AllInclusiveSecurityGroup', 'us-east-1', '1111111')]
#         security_group.security_group_id = 'sg-pseudo-some-id'
#         security_group.inbound_permissions = inbound_permissions
#         security_group.outbound_permissions = outbound_permissions
#         network_interface.security_groups.append(security_group)
#         connection_detail = PublicConnectionDetail(PolicyConnectionProperty([]), ConnectionDirectionType.INBOUND)
#         network_interface.inbound_connections.add(connection_detail)
#         network_resource.network_interfaces.append(network_interface)
#         rds_instance.publicly_accessible = True
#         rds_instance.security_group_ids = [security_group]
#         rds_instance.name = 'rds_instance_name'
#         rds_instance.network_resource = network_resource
#         rds_instance.network_resource.network_interfaces[0].add_private_inbound_conn(PortConnectionProperty(ports=[(443, 443)],
#                                                                                                             cidr_block='0.0.0.0/0',
#                                                                                                             ip_protocol_type='tcp'),
#                                                                                      rds_instance.network_resource.network_interfaces[0])
#         rds_instance.network_resource.network_interfaces[0].secondary_ip_addresses = ['10.10.10.16/24']
#         rds_instance.network_resource.network_interfaces[0].primary_ip_address = '10.10.10.10/24'
#         rds_instance.network_resource.network_interfaces[0].owner = rds_instance
#         rds_instance.network_resource.network_interfaces[0].subnet = subnet
#         rds_instance.port = 3306
#         rds_cluster.cluster_instances = [rds_instance]
#         rds_cluster.cluster_id = 'rds_cluster_id'
#         context = EnvironmentContext(rds_clusters=[rds_cluster])
#         # Act
#         result = self.rule.run(context, {})
#         # Assert
#         self.assertEqual(RuleResultType.FAILED, result.status)
#         self.assertEqual(1, len(result.issues))
#
#     def test_indirect_public_access_db_rds__rds_instance__fail(self):
#         # Arrange
#         network_resource: NetworkResource = create_empty_entity(NetworkResource)
#         network_interface = create_empty_entity(NetworkInterface)
#         security_group: SecurityGroup = create_empty_entity(SecurityGroup)
#         rds_instance: RdsInstance = create_empty_entity(RdsInstance)
#         subnet: Subnet = create_empty_entity(Subnet)
#         network_acl: NetworkAcl = create_empty_entity(NetworkAcl)
#         network_acl.name = 'subnet_network_acl_name'
#         subnet.name = 'subnet_testing_name'
#         subnet.subnet_id = 'subnet_testing_id'
#         subnet.network_acl = network_acl
#         inbound_permissions = [SecurityGroupRule(0, 65535, '-1', SecurityGroupRulePropertyType.IP_RANGES,
#                                                  '0.0.0.0/0', False, ConnectionType.Inbound,
#                                                  'AllInclusiveSecurityGroup', 'us-east-1', '1111111')]
#         outbound_permissions = [SecurityGroupRule(0, 65535, '-1',
#                                                   SecurityGroupRulePropertyType.IP_RANGES, '10.10.10.0/24', False,
#                                                   ConnectionType.Outbound, 'AllInclusiveSecurityGroup', 'us-east-1', '1111111')]
#         security_group.security_group_id = 'sg-pseudo-some-id'
#         security_group.inbound_permissions = inbound_permissions
#         security_group.outbound_permissions = outbound_permissions
#         network_interface.security_groups.append(security_group)
#         connection_detail = PublicConnectionDetail(PolicyConnectionProperty([]), ConnectionDirectionType.INBOUND)
#         network_interface.inbound_connections.add(connection_detail)
#         network_resource.network_interfaces.append(network_interface)
#         rds_instance.publicly_accessible = True
#         rds_instance.security_group_ids = [security_group]
#         rds_instance.name = 'rds_instance_name'
#         rds_instance.network_resource = network_resource
#         rds_instance.network_resource.network_interfaces[0].add_private_inbound_conn(PortConnectionProperty(ports=[(443, 443)],
#                                                                                                             cidr_block='0.0.0.0/0',
#                                                                                                             ip_protocol_type='tcp'),
#                                                                                      rds_instance.network_resource.network_interfaces[0])
#         rds_instance.network_resource.network_interfaces[0].secondary_ip_addresses = ['10.10.10.16/24']
#         rds_instance.network_resource.network_interfaces[0].primary_ip_address = '10.10.10.10/24'
#         rds_instance.network_resource.network_interfaces[0].owner = rds_instance
#         rds_instance.network_resource.network_interfaces[0].subnet = subnet
#         rds_instance.port = 3306
#         context = EnvironmentContext(rds_instances=[rds_instance])
#         # Act
#         result = self.rule.run(context, {})
#         # Assert
#         self.assertEqual(RuleResultType.FAILED, result.status)
#         self.assertEqual(1, len(result.issues))
#
#     def test_indirect_public_access_db_rds__rds_cluster__pass(self):
#         # Arrange
#         rds_cluster: RdsCluster = create_empty_entity(RdsCluster)
#         network_resource: NetworkResource = create_empty_entity(NetworkResource)
#         network_interface = create_empty_entity(NetworkInterface)
#         security_group: SecurityGroup = create_empty_entity(SecurityGroup)
#         rds_instance: RdsInstance = create_empty_entity(RdsInstance)
#         subnet: Subnet = create_empty_entity(Subnet)
#         network_acl: NetworkAcl = create_empty_entity(NetworkAcl)
#         network_acl.name = 'subnet_network_acl_name'
#         subnet.name = 'subnet_testing_name'
#         subnet.subnet_id = 'subnet_testing_id'
#         subnet.network_acl = network_acl
#         inbound_permissions = [SecurityGroupRule(0, 65535, '-1', SecurityGroupRulePropertyType.IP_RANGES,
#                                                  '0.0.0.0/0', False, ConnectionType.Inbound,
#                                                  'AllInclusiveSecurityGroup', 'us-east-1', '1111111')]
#         outbound_permissions = [SecurityGroupRule(0, 65535, '-1',
#                                                   SecurityGroupRulePropertyType.IP_RANGES, '10.10.10.0/24', False,
#                                                   ConnectionType.Outbound, 'AllInclusiveSecurityGroup', 'us-east-1', '1111111')]
#         security_group.security_group_id = 'sg-pseudo-some-id'
#         security_group.inbound_permissions = inbound_permissions
#         security_group.outbound_permissions = outbound_permissions
#         network_interface.security_groups.append(security_group)
#         connection_detail = PrivateConnectionDetail(PolicyConnectionProperty([]), ConnectionDirectionType.INBOUND, ConnectionInstance())
#         network_interface.inbound_connections.add(connection_detail)
#         network_resource.network_interfaces.append(network_interface)
#         rds_instance.publicly_accessible = True
#         rds_instance.security_group_ids = [security_group]
#         rds_instance.name = 'rds_instance_name'
#         rds_instance.network_resource = network_resource
#         rds_instance.network_resource.network_interfaces[0].add_private_inbound_conn(PortConnectionProperty(ports=[(443, 443)],
#                                                                                                             cidr_block='0.0.0.0/0',
#                                                                                                             ip_protocol_type='tcp'),
#                                                                                      rds_instance.network_resource.network_interfaces[0])
#         rds_instance.network_resource.network_interfaces[0].secondary_ip_addresses = ['10.10.10.16/24']
#         rds_instance.network_resource.network_interfaces[0].primary_ip_address = '10.10.10.10/24'
#         rds_instance.network_resource.network_interfaces[0].owner = rds_instance
#         rds_instance.network_resource.network_interfaces[0].subnet = subnet
#         rds_instance.port = 3306
#         rds_cluster.cluster_instances = [rds_instance]
#         rds_cluster.cluster_id = 'rds_cluster_id'
#         context = EnvironmentContext(rds_clusters=[rds_cluster])
#         # Act
#         result = self.rule.run(context, {})
#         # Assert
#         self.assertEqual(RuleResultType.SUCCESS, result.status)
#         self.assertEqual(0, len(result.issues))
#
#     def test_indirect_public_access_db_rds__rds_instance__pass(self):
#         # Arrange
#         network_resource: NetworkResource = create_empty_entity(NetworkResource)
#         network_interface = create_empty_entity(NetworkInterface)
#         security_group: SecurityGroup = create_empty_entity(SecurityGroup)
#         rds_instance: RdsInstance = create_empty_entity(RdsInstance)
#         subnet: Subnet = create_empty_entity(Subnet)
#         network_acl: NetworkAcl = create_empty_entity(NetworkAcl)
#         network_acl.name = 'subnet_network_acl_name'
#         subnet.name = 'subnet_testing_name'
#         subnet.subnet_id = 'subnet_testing_id'
#         subnet.network_acl = network_acl
#         inbound_permissions = [SecurityGroupRule(0, 65535, '-1', SecurityGroupRulePropertyType.IP_RANGES,
#                                                  '0.0.0.0/0', False, ConnectionType.Inbound,
#                                                  'AllInclusiveSecurityGroup', 'us-east-1', '1111111')]
#         outbound_permissions = [SecurityGroupRule(0, 65535, '-1',
#                                                   SecurityGroupRulePropertyType.IP_RANGES, '10.10.10.0/24', False,
#                                                   ConnectionType.Outbound, 'AllInclusiveSecurityGroup', 'us-east-1', '1111111')]
#         security_group.security_group_id = 'sg-pseudo-some-id'
#         security_group.inbound_permissions = inbound_permissions
#         security_group.outbound_permissions = outbound_permissions
#         network_interface.security_groups.append(security_group)
#         connection_detail = PrivateConnectionDetail(PolicyConnectionProperty([]), ConnectionDirectionType.INBOUND, ConnectionInstance())
#         network_interface.inbound_connections.add(connection_detail)
#         network_resource.network_interfaces.append(network_interface)
#         rds_instance.publicly_accessible = True
#         rds_instance.security_group_ids = [security_group]
#         rds_instance.name = 'rds_instance_name'
#         rds_instance.network_resource = network_resource
#         rds_instance.network_resource.network_interfaces[0].add_private_inbound_conn(PortConnectionProperty(ports=[(443, 443)],
#                                                                                                             cidr_block='0.0.0.0/0',
#                                                                                                             ip_protocol_type='tcp'),
#                                                                                      rds_instance.network_resource.network_interfaces[0])
#         rds_instance.network_resource.network_interfaces[0].secondary_ip_addresses = ['10.10.10.16/24']
#         rds_instance.network_resource.network_interfaces[0].primary_ip_address = '10.10.10.10/24'
#         rds_instance.network_resource.network_interfaces[0].owner = rds_instance
#         rds_instance.network_resource.network_interfaces[0].subnet = subnet
#         rds_instance.port = 3306
#         context = EnvironmentContext(rds_instances=[rds_instance])
#         # Act
#         result = self.rule.run(context, {})
#         # Assert
#         self.assertEqual(RuleResultType.SUCCESS, result.status)
#         self.assertEqual(0, len(result.issues))
