from typing import List, Optional
from pydantic import BaseModel


class ProjectionConfig(BaseModel):
    include_fields: Optional[List[str]] = None
    exclude_fields: Optional[List[str]] = None