from enum import Enum


class CloudProvider(str, Enum):
    AMAZON_WEB_SERVICES = 'amazon_web_services'
    AZURE = 'azure'
