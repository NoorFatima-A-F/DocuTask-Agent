"""
Pagination & Filtering Primitives.
"""
from typing import Generic, List, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")

class PaginationQuery(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=50, ge=1, le=500)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size

    @property
    def limit(self) -> int:
        return self.page_size


class PageMetadata(BaseModel):
    page: int
    page_size: int
    total_items: int
    total_pages: int
    has_next: bool
    has_previous: bool


class PaginatedResult(BaseModel, Generic[T]):
    items: List[T]
    metadata: PageMetadata
