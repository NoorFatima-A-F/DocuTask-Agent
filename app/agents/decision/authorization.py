"""
Authorization Policy Models.
"""

from pydantic import BaseModel, Field


class AuthorizationPolicy(BaseModel):
    required_role: str = Field(default="USER")
    model_config = {"frozen": True}
