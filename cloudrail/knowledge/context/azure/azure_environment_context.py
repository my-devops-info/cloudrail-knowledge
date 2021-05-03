from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.azure_resources.azure_resource_group import AzureResourceGroup
from cloudrail.knowledge.context.azure.azure_resources.databases.azure_sql_server import AzureSqlServer
from cloudrail.knowledge.context.base_environment_context import BaseEnvironmentContext


class AzureEnvironmentContext(BaseEnvironmentContext):

    def __init__(self) -> None:
        BaseEnvironmentContext.__init__(self)
        self.resource_groups: AliasesDict[AzureResourceGroup] = AliasesDict()
        self.sql_servers: AliasesDict[AzureSqlServer] = AliasesDict()
