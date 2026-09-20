# Event Taxonomy
from dataclasses import dataclass
from app.runtime.events.base import RuntimeEvent
@dataclass(frozen=True)
class MissionCreated(RuntimeEvent):
    event_type: str = 'MissionCreated'
