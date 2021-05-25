from typing import List, Dict

from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.azure_resources.azure_resource_group import AzureResourceGroup
from cloudrail.knowledge.context.azure.azure_resources.databases.azure_app_service import AzureAppService
from cloudrail.knowledge.context.azure.azure_resources.databases.azure_sql_server import AzureSqlServer
from cloudrail.knowledge.context.azure.azure_resources.nsg.azure_nsg import AzureNetworkSecurityGroup
from cloudrail.knowledge.context.azure.azure_resources.security_group_to_subnet_association.azure_security_group_to_subnet_association import \
    AzureSecurityGroupToSubnetAssociation
from cloudrail.knowledge.context.azure.azure_resources.subnet.azure_subnet import AzureSubnet
from cloudrail.knowledge.context.base_environment_context import BaseEnvironmentContext
from cloudrail.knowledge.context.environment_context import CheckovResult


class AzureEnvironmentContext(BaseEnvironmentContext):

    def __init__(self,
                 checkov_results: Dict[str, List[CheckovResult]] = None,
                 resource_groups: AliasesDict[AzureResourceGroup] = None,
                 sql_servers: AliasesDict[AzureSqlServer] = None,
                 #net_security_groups: AliasesDict[AzureNetworkSecurityGroup] = None,
                 net_security_groups: List[AzureNetworkSecurityGroup] = None,
                 app_services: AliasesDict[AzureAppService] = None,
                 subnet_network_security_group_association: List[AzureSecurityGroupToSubnetAssociation] = None,
                 subnets: AliasesDict[AzureSubnet] = None):
        BaseEnvironmentContext.__init__(self)
        self.checkov_results: Dict[str, List[CheckovResult]] = checkov_results or {}
        self.resource_groups: AliasesDict[AzureResourceGroup] = resource_groups or AliasesDict()
        self.sql_servers: AliasesDict[AzureSqlServer] = sql_servers or AliasesDict()
        #self.net_security_groups = AliasesDict[AzureNetworkSecurityGroup] = net_security_groups or AliasesDict()
        self.net_security_groups = net_security_groups or []
        self.app_services: AliasesDict[AzureAppService] = app_services or AliasesDict()
        self.subnet_network_security_group_association: List[AzureSecurityGroupToSubnetAssociation] = subnet_network_security_group_association or []
        self.subnets: AliasesDict[AzureSubnet] = subnets or AliasesDict()
