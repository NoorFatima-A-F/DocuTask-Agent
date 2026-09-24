"""
Generic Search and Filter Criteria.
"""
from enum import Enum
from typing import Any, List, Optional
from pydantic import BaseModel, Field

class SortOrder(str, Enum):
    ASC = "ASC"
    DESC = "DESC"


class FilterCriteria(BaseModel):
    field: str
    operator: str = "eq"  # eq, neq, gt, gte, lt, lte, in, contains
    value: Any


class SearchQuery(BaseModel):
    query_text: Optional[str] = None
    filters: List[FilterCriteria] = Field(default_factory=list)
    sort_by: str = "created_at"
    sort_order: SortOrder = SortOrder.DESC
    tags: List[str] = Field(default_factory=list)
