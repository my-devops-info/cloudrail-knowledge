import uuid
from dataclasses import dataclass
from typing import Optional


@dataclass
class IacResourceMetadata:
    cloud_res_locator: str
    file_name: str
    start_line: int
    end_line: int
    module_metadata: Optional['IacResourceMetadata'] = None
    id: Optional[str] = None
    resource_type: Optional[str] = None
    run_execution_id: str = None

    def __post_init__(self):
        self.id = self.id or str(uuid.uuid4())
