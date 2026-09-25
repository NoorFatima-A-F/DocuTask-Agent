"""
Message Channels Domain Model.
"""

from enum import Enum
from pydantic import BaseModel, Field


class ChannelType(str, Enum):
    POINT_TO_POINT = "POINT_TO_POINT"
    PUBLISH_SUBSCRIBE = "PUBLISH_SUBSCRIBE"
    DEAD_LETTER = "DEAD_LETTER"


class MessageChannel(BaseModel):
    channel_name: str
    channel_type: ChannelType = Field(default=ChannelType.PUBLISH_SUBSCRIBE)
    model_config = {"frozen": True}
