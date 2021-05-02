from dataclasses import dataclass
from enum import Enum


class BlockType(str, Enum):
    DATASOURCE = 'datasource'


@dataclass
class UnknownBlock:
    block_type: BlockType
    block_address: str
