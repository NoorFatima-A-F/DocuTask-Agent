"""
API Pagination Standard Models.
"""

from dataclasses import dataclass, field
from typing import Any, Generic, List, Optional, TypeVar

T = TypeVar("T")


@dataclass
class PageRequest:
    """Standard pagination request parameters."""
    page: int = 1
    page_size: int = 20
    sort_by: Optional[str] = None
    sort_desc: bool = False

    @property
    def offset(self) -> int:
        return max(0, (self.page - 1) * self.page_size)


@dataclass
class PageResult(Generic[T]):
    """Standard paginated response envelope."""
    items: List[T] = field(default_factory=list)
    total_count: int = 0
    page: int = 1
    page_size: int = 20
    total_pages: int = 1
    has_next: bool = False
    has_prev: bool = False

    @classmethod
    def create(cls, items: List[T], total_count: int, page_request: PageRequest) -> "PageResult[T]":
        total_pages = max(1, (total_count + page_request.page_size - 1) // page_request.page_size)
        return cls(
            items=items,
            total_count=total_count,
            page=page_request.page,
            page_size=page_request.page_size,
            total_pages=total_pages,
            has_next=page_request.page < total_pages,
            has_prev=page_request.page > 1,
        )
