from enum import Enum


class KeyManager(Enum):
    """
        Enum

        AWS - key is managed by AWS

        CUSTOMER - key is managed by the Customer

        NONE - key is unmanaged
    """
    AWS = 'AWS'
    CUSTOMER = 'CUSTOMER'
    NONE = 'NONE'
