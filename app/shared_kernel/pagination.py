"""
Reusable Pagination, Cursor, Filtering and Sorting Models.
Standardizes collection queries across all platform subsystems.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Generic, TypeVar, List, Optional, Any
import math

T = TypeVar("T")

class SortOrder(str, Enum):
    ASC = "ASC"
    DESC = "DESC"

class FilterOperator(str, Enum):
    EQ = "EQ"
    NEQ = "NEQ"
    GT = "GT"
    GTE = "GTE"
    LT = "LT"
    LTE = "LTE"
    IN = "IN"
    CONTAINS = "CONTAINS"
    LIKE = "LIKE"
    IS_NULL = "IS_NULL"
    NOT_NULL = "NOT_NULL"

@dataclass(frozen=True)
class SortCriteria:
    field: str
    order: SortOrder = SortOrder.ASC

@dataclass(frozen=True)
class FilterCriteria:
    field: str
    operator: FilterOperator
    value: Any = None

@dataclass(frozen=True)
class PaginationQuery:
    """Standard offset-based pagination query."""
    page: int = 1
    page_size: int = 20
    sorts: List[SortCriteria] = field(default_factory=list)
    filters: List[FilterCriteria] = field(default_factory=list)

    @property
    def offset(self) -> int:
        return max(0, (self.page - 1) * self.page_size)

    @property
    def limit(self) -> int:
        return self.page_size

@dataclass(frozen=True)
class PaginatedResult(Generic[T]):
    """Standard offset-based paginated response."""
    items: List[T]
    total_count: int
    page: int
    page_size: int

    @property
    def total_pages(self) -> int:
        if self.page_size <= 0:
            return 0
        return math.ceil(self.total_count / self.page_size)

    @property
    def has_next(self) -> bool:
        return self.page < self.total_pages

    @property
    def has_previous(self) -> bool:
        return self.page > 1

@dataclass(frozen=True)
class CursorPaginationQuery:
    """Standard cursor-based pagination query."""
    cursor: Optional[str] = None
    limit: int = 20
    sort_order: SortOrder = SortOrder.ASC

@dataclass(frozen=True)
class CursorPaginatedResult(Generic[T]):
    """Standard cursor-based paginated response."""
    items: List[T]
    next_cursor: Optional[str] = None
    prev_cursor: Optional[str] = None
    has_next: bool = False
