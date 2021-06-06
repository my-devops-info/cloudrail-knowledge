from enum import Enum


class FtpState(Enum):
    ALL_ALLOWED = 'AllAllowed'
    FTPS_ONLY = 'FtpsOnly'
    DISABLED = 'Disabled'
