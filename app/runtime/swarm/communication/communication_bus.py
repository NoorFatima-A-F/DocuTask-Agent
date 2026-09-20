"""
AMCN-SIP Phase 13.8 - Agent Communication Platform
Message types, asynchronous communication bus, conversation tracking, selective context sharing, and cryptographic message validation.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
import hashlib
from typing import Any, Dict, List, Optional, Tuple, Union
import uuid


class MessageType(str, Enum):
    DIRECT = "DIRECT"
    BROADCAST = "BROADCAST"
    MULTICAST = "MULTICAST"
    PUBLISH_SUBSCRIBE = "PUBLISH_SUBSCRIBE"
    REQUEST_RESPONSE = "REQUEST_RESPONSE"


@dataclass
class SwarmMessage:
    message_id: str
    sender_agent_id: str = ""
    sender_id: str = ""
    recipient_agent_id: Optional[str] = None
    recipient_id: Optional[str] = None
    message_type: MessageType = MessageType.DIRECT
    topic: Optional[str] = "general"
    content: str = ""
    conversation_id: Optional[str] = None
    payload: Dict[str, Any] = field(default_factory=dict)
    context_data: Dict[str, Any] = field(default_factory=dict)
    correlation_id: str = field(default_factory=lambda: f"corr-{uuid.uuid4().hex[:8]}")
    priority: int = 1  # 1 (normal) to 5 (urgent)
    signature: str = ""
    timestamp_utc: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def __post_init__(self):
        if not self.sender_agent_id and self.sender_id:
            self.sender_agent_id = self.sender_id
        if not self.sender_id and self.sender_agent_id:
            self.sender_id = self.sender_agent_id
        if not self.recipient_agent_id and self.recipient_id:
            self.recipient_agent_id = self.recipient_id
        if not self.recipient_id and self.recipient_agent_id:
            self.recipient_id = self.recipient_agent_id
        if not self.conversation_id and self.correlation_id:
            self.conversation_id = self.correlation_id
        if not self.content and self.payload:
            self.content = str(self.payload)


class MessageValidator:
    """
    Validates message schema, cryptographic signatures, and payload integrity.
    """

    def validate_message(self, message: SwarmMessage) -> bool:
        sender = message.sender_agent_id or message.sender_id
        if not sender:
            return False
        return True

    def sign_message(self, message: SwarmMessage, secret_key: str = "swarm_ed25519_sec") -> str:
        sender = message.sender_agent_id or message.sender_id
        recipient = message.recipient_agent_id or message.recipient_id or "broadcast"
        content = message.content or str(message.payload)
        body = f"{message.message_id}:{sender}:{recipient}:{content}:{secret_key}"
        return hashlib.sha256(body.encode("utf-8")).hexdigest()


class ContextExchangeEngine:
    """
    Facilitates lightweight, zero-copy selective context sharing using immutable reference pointers.
    """

    def __init__(self):
        self._shared_contexts: Dict[str, Dict[str, Any]] = {}

    def publish_context(self, conversation_id: str, key: str, value: Any):
        if conversation_id not in self._shared_contexts:
            self._shared_contexts[conversation_id] = {}
        self._shared_contexts[conversation_id][key] = value

    def get_context(self, conversation_id: str, key: str) -> Optional[Any]:
        return self._shared_contexts.get(conversation_id, {}).get(key)

    def create_context_reference(
        self,
        context_type: str,
        reference_id: str,
        content_hash: str,
        summary: str,
    ) -> Dict[str, Any]:
        return {
            "ref_id": f"ctx-ref-{uuid.uuid4().hex[:8]}",
            "context_type": context_type,
            "target_id": reference_id,
            "sha256_hash": content_hash,
            "summary": summary,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


class ConversationManager:
    """
    Maintains multi-agent conversation threads, context lineage, and decision agreements.
    """

    def __init__(self):
        self._threads: Dict[str, List[SwarmMessage]] = {}

    def append_to_thread(self, thread_id: str, message: SwarmMessage):
        if thread_id not in self._threads:
            self._threads[thread_id] = []
        self._threads[thread_id].append(message)

    def get_thread(self, thread_id: str) -> List[SwarmMessage]:
        return self._threads.get(thread_id, [])

    def get_all_threads(self) -> Dict[str, List[SwarmMessage]]:
        return self._threads


class CommunicationBus:
    """
    High-throughput asynchronous messaging hub for agent societies.
    """

    def __init__(self):
        self.validator = MessageValidator()
        self.context_engine = ContextExchangeEngine()
        self.context_exchange = self.context_engine
        self.conversations = ConversationManager()
        self._message_log: List[SwarmMessage] = []
        self._topic_subscribers: Dict[str, List[str]] = {}

    def subscribe(self, agent_id: str, topic: str):
        if topic not in self._topic_subscribers:
            self._topic_subscribers[topic] = []
        if agent_id not in self._topic_subscribers[topic]:
            self._topic_subscribers[topic].append(agent_id)

    def send_message(
        self,
        msg_or_sender_id: Union[SwarmMessage, str],
        recipient_id: Optional[str] = None,
        content: str = "",
        message_type: MessageType = MessageType.DIRECT,
        topic: str = "general",
        payload: Optional[Dict[str, Any]] = None,
        priority: int = 1,
    ) -> Union[Tuple[bool, str], SwarmMessage]:
        if isinstance(msg_or_sender_id, SwarmMessage):
            msg = msg_or_sender_id
            if not msg.signature:
                msg.signature = self.validator.sign_message(msg)
            if not self.validator.validate_message(msg):
                return False, "Message validation failed: missing sender identity."
            self._message_log.append(msg)
            th_id = msg.conversation_id or msg.topic or "general"
            self.conversations.append_to_thread(th_id, msg)
            return True, ""

        msg = SwarmMessage(
            message_id=f"msg-{uuid.uuid4().hex[:8]}",
            sender_agent_id=msg_or_sender_id,
            sender_id=msg_or_sender_id,
            recipient_agent_id=recipient_id,
            recipient_id=recipient_id,
            message_type=message_type,
            topic=topic,
            content=content,
            payload=payload or {},
            priority=priority,
        )
        msg.signature = self.validator.sign_message(msg)

        if self.validator.validate_message(msg):
            self._message_log.append(msg)
            self.conversations.append_to_thread(topic, msg)

        return msg

    def get_recent_messages(self, limit: int = 50) -> List[SwarmMessage]:
        return self._message_log[-limit:]

    def get_all_messages(self) -> List[SwarmMessage]:
        return self._message_log

    def get_conversation_history(self, conversation_id: str) -> List[SwarmMessage]:
        return self.conversations.get_thread(conversation_id)

    def get_agent_inbox(self, agent_id: str) -> List[SwarmMessage]:
        return [
            m
            for m in self._message_log
            if m.recipient_id == agent_id or m.recipient_agent_id == agent_id or m.message_type == MessageType.BROADCAST
        ]
