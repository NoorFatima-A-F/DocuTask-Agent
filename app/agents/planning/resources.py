"""
Resource Requirements and Allocation Models.
"""

from pydantic import BaseModel, Field


class ResourceRequirement(BaseModel):
    """Resource requirement for node execution."""
    resource_type: str = Field(default="MEMORY")  # CPU, GPU, MEMORY, TOKEN, NETWORK
    amount: float = Field(default=1.0, ge=0.0)
    unit: str = Field(default="UNITS")
    model_config = {"frozen": True}


class ResourceAllocation(BaseModel):
    """Allocated resources for plan execution."""
    allocated_tokens: int = Field(default=0, ge=0)
    max_parallel_workers: int = Field(default=4, ge=1)
    model_config = {"frozen": True}
