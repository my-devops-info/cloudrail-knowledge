from typing import Set, List
from cloudrail.knowledge.context.mergeable import Mergeable
from cloudrail.knowledge.context.unknown_block import UnknownBlock


class BaseEnvironmentContext:

    def __init__(self, invalidated_resources: Set[Mergeable] = None, unknown_blocks: List[UnknownBlock] = None) -> None:
        super().__init__()
        self.invalidated_resources: Set[Mergeable] = invalidated_resources or set()
        self.unknown_blocks: List[UnknownBlock] = unknown_blocks or list()

    def clear_cache(self):
        for attr in dir(self):
            func = getattr(self, attr)
            if callable(func):
                try:
                    func.cache_clear()  # clearing lru_cache
                except Exception:
                    pass
