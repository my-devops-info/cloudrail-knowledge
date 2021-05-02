from enum import Enum


class TerraformActionType(str, Enum):
    NO_OP = 'no-op'
    CREATE = 'create'
    DELETE = 'delete'
    UPDATE = 'update'
    READ = 'read'
