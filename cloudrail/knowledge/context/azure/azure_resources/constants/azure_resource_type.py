from enum import Enum


class AzureResourceType(Enum):

    AZURERM_RESOURCE_GROUP = 'azurerm_resource_group'
    AZURERM_SQL_SERVER = 'azurerm_sql_server'
    AZURERM_MSSQL_SERVER = 'azurerm_mssql_server'
    AZURERM_SQL_FIREWALL_RULE = 'azurerm_sql_firewall_rule'
    AZURERM_APP_SERVICE = 'azurerm_app_service'
