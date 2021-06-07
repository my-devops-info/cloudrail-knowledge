from enum import Enum


class FtpState(Enum):
    ALL_ALLOWED = 'AllAllowed'
    FTPS_ONLY = 'FtpsOnly'
    DISABLED = 'Disabled'


class FieldMode(Enum):
    REQUIRED = 'Required'
    OPTIONAL = 'Optional'
