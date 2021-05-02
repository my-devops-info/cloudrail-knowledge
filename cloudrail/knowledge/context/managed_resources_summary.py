from dataclasses import dataclass


@dataclass
class ManagedResourcesSummary:
    created: int
    updated: int
    deleted: int
    total: int
