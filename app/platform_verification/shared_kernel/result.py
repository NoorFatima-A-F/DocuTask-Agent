"""
Result and Option Patterns (Railway Oriented Programming).
"""
from typing import TypeVar, Generic, Union, Callable, Any, Optional

T = TypeVar("T")
E = TypeVar("E")
U = TypeVar("U")

class Success(Generic[T]):
    __slots__ = ("_value",)

    def __init__(self, value: T):
        self._value = value

    @property
    def value(self) -> T:
        return self._value

    @property
    def is_success(self) -> bool:
        return True

    @property
    def is_failure(self) -> bool:
        return False

    def unwrap(self) -> T:
        return self._value

    def unwrap_or(self, default: T) -> T:
        return self._value

    def map(self, fn: Callable[[T], U]) -> "Success[U]":
        return Success(fn(self._value))

    def bind(self, fn: Callable[[T], "Result[U, E]"]) -> "Result[U, E]":
        return fn(self._value)

    def __repr__(self) -> str:
        return f"Success({self._value!r})"


class Failure(Generic[E]):
    __slots__ = ("_error",)

    def __init__(self, error: E):
        self._error = error

    @property
    def error(self) -> E:
        return self._error

    @property
    def is_success(self) -> bool:
        return False

    @property
    def is_failure(self) -> bool:
        return True

    def unwrap(self) -> Any:
        if isinstance(self._error, Exception):
            raise self._error
        raise ValueError(f"Called unwrap on Failure: {self._error}")

    def unwrap_or(self, default: T) -> T:
        return default

    def map(self, fn: Callable[[Any], Any]) -> "Failure[E]":
        return self

    def bind(self, fn: Callable[[Any], Any]) -> "Failure[E]":
        return self

    def __repr__(self) -> str:
        return f"Failure({self._error!r})"


Result = Union[Success[T], Failure[E]]


class Option(Generic[T]):
    __slots__ = ("_value", "_is_some")

    def __init__(self, value: Optional[T], is_some: bool):
        self._value = value
        self._is_some = is_some

    @classmethod
    def some(cls, value: T) -> "Option[T]":
        return cls(value, True)

    @classmethod
    def empty(cls) -> "Option[T]":
        return cls(None, False)

    @property
    def is_some(self) -> bool:
        return self._is_some

    @property
    def is_empty(self) -> bool:
        return not self._is_some

    def unwrap(self) -> T:
        if not self._is_some:
            raise ValueError("Called unwrap on Empty Option")
        return self._value  # type: ignore

    def unwrap_or(self, default: T) -> T:
        return self._value if self._is_some else default

    def map(self, fn: Callable[[T], U]) -> "Option[U]":
        if self._is_some:
            return Option.some(fn(self._value))  # type: ignore
        return Option.empty()

    def __repr__(self) -> str:
        return f"Some({self._value!r})" if self._is_some else "Empty()"


Some = Option.some
Empty = Option.empty
