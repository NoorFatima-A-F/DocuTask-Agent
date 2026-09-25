"""
Strongly Typed Domain Identifiers.
Prevents primitive obsession across all 12 platform domains.
"""
from dataclasses import dataclass
from typing import Generic, TypeVar
import uuid
import hashlib

T = TypeVar("T")

@dataclass(frozen=True)
class TypedId(Generic[T]):
    """Generic strongly-typed ID base class."""
    value: str

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.value!r})"

    @classmethod
    def generate(cls, prefix: str = "id") -> "TypedId[T]":
        return cls(f"{prefix}_{uuid.uuid4().hex[:16]}")

    @classmethod
    def from_str(cls, raw: str) -> "TypedId[T]":
        return cls(raw.strip())

    @classmethod
    def deterministic(cls, seed: str, prefix: str = "id") -> "TypedId[T]":
        h = hashlib.sha256(seed.encode("utf-8")).hexdigest()[:16]
        return cls(f"{prefix}_{h}")

@dataclass(frozen=True)
class EntityId(TypedId[str]):
    pass

@dataclass(frozen=True)
class ExecutionId(TypedId[str]):
    @classmethod
    def generate(cls, prefix: str = "exec") -> "ExecutionId":
        return cls(f"{prefix}_{uuid.uuid4().hex[:16]}")

@dataclass(frozen=True)
class VerificationRunId(TypedId[str]):
    @classmethod
    def generate(cls, prefix: str = "vrun") -> "VerificationRunId":
        return cls(f"{prefix}_{uuid.uuid4().hex[:16]}")

@dataclass(frozen=True)
class DatasetId(TypedId[str]):
    @classmethod
    def generate(cls, prefix: str = "ds") -> "DatasetId":
        return cls(f"{prefix}_{uuid.uuid4().hex[:16]}")

@dataclass(frozen=True)
class VerificationId(TypedId[str]):
    @classmethod
    def generate(cls, prefix: str = "ver") -> "VerificationId":
        return cls(f"{prefix}_{uuid.uuid4().hex[:16]}")

@dataclass(frozen=True)
class EvidenceId(TypedId[str]):
    @classmethod
    def generate(cls, prefix: str = "ev") -> "EvidenceId":
        return cls(f"{prefix}_{uuid.uuid4().hex[:16]}")

@dataclass(frozen=True)
class MetricId(TypedId[str]):
    @classmethod
    def generate(cls, prefix: str = "met") -> "MetricId":
        return cls(f"{prefix}_{uuid.uuid4().hex[:16]}")

@dataclass(frozen=True)
class PluginId(TypedId[str]):
    @classmethod
    def generate(cls, prefix: str = "plg") -> "PluginId":
        return cls(f"{prefix}_{uuid.uuid4().hex[:16]}")

@dataclass(frozen=True)
class ConfigurationId(TypedId[str]):
    @classmethod
    def generate(cls, prefix: str = "cfg") -> "ConfigurationId":
        return cls(f"{prefix}_{uuid.uuid4().hex[:16]}")

@dataclass(frozen=True)
class EnvironmentId(TypedId[str]):
    @classmethod
    def generate(cls, prefix: str = "env") -> "EnvironmentId":
        return cls(f"{prefix}_{uuid.uuid4().hex[:16]}")

@dataclass(frozen=True)
class AuditId(TypedId[str]):
    @classmethod
    def generate(cls, prefix: str = "aud") -> "AuditId":
        return cls(f"{prefix}_{uuid.uuid4().hex[:16]}")

@dataclass(frozen=True)
class CertificationId(TypedId[str]):
    @classmethod
    def generate(cls, prefix: str = "cert") -> "CertificationId":
        return cls(f"{prefix}_{uuid.uuid4().hex[:16]}")

@dataclass(frozen=True)
class CertificateId(CertificationId):
    pass

@dataclass(frozen=True)
class TenantId(TypedId[str]):
    @classmethod
    def generate(cls, prefix: str = "ten") -> "TenantId":
        return cls(f"{prefix}_{uuid.uuid4().hex[:16]}")

@dataclass(frozen=True)
class CorrelationId(TypedId[str]):
    @classmethod
    def generate(cls, prefix: str = "corr") -> "CorrelationId":
        return cls(f"{prefix}_{uuid.uuid4().hex[:16]}")

@dataclass(frozen=True)
class TraceId(TypedId[str]):
    @classmethod
    def generate(cls, prefix: str = "trc") -> "TraceId":
        return cls(f"{prefix}_{uuid.uuid4().hex[:16]}")

@dataclass(frozen=True)
class RequestId(TypedId[str]):
    @classmethod
    def generate(cls, prefix: str = "req") -> "RequestId":
        return cls(f"{prefix}_{uuid.uuid4().hex[:16]}")

@dataclass(frozen=True)
class SessionId(TypedId[str]):
    @classmethod
    def generate(cls, prefix: str = "ses") -> "SessionId":
        return cls(f"{prefix}_{uuid.uuid4().hex[:16]}")

@dataclass(frozen=True)
class CausationId(TypedId[str]):
    @classmethod
    def generate(cls, prefix: str = "cau") -> "CausationId":
        return cls(f"{prefix}_{uuid.uuid4().hex[:16]}")
