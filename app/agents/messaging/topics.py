"""
Message Topics Domain Model.
"""

from pydantic import BaseModel, Field


class MessageTopic(BaseModel):
    topic_name: str
    description: str = Field(default="")
    model_config = {"frozen": True}
