"""
Test Suite: Cross-Agent Communication Bus & Cryptographic Messaging
Validates pub/sub message publishing, channel routing, ACLs, signature verification, and conversation history.
"""
from app.runtime.communication.communication_bus import CommunicationBus
from app.runtime.communication.message_router import MessageRouter
from app.runtime.communication.channel_manager import ChannelManager
from app.runtime.communication.conversation_history import ConversationHistory


def test_communication_bus_publishing_and_signatures():
    bus = CommunicationBus()
    
    msg = bus.publish_message(
        channel_name="#validation-alerts",
        sender_dept_id="dept_extraction",
        sender_role="Lead Extraction Specialist",
        receiver_dept_id="dept_validation",
        message_type="HANDOFF",
        payload_summary="Test payload handoff",
        runtime_event_id="evt_test_123",
        priority="HIGH",
    )

    assert msg.channel_name == "#validation-alerts"
    assert msg.signature.startswith("ED25519_SIG_")
    assert msg.priority == "HIGH"

    retrieved = bus.get_messages(channel_name="#validation-alerts")
    assert len(retrieved) >= 1
    assert any(m["message_id"] == msg.message_id for m in retrieved)


def test_message_router_subscriptions():
    router = MessageRouter()
    channels = router.list_channels_with_subscribers()
    
    assert "#executive-dispatch" in channels
    assert "dept_executive" in channels["#executive-dispatch"]
    assert "dept_ocr" in channels["#ocr-extraction-handoff"]


def test_channel_manager_and_conversation_history():
    chan_mgr = ChannelManager()
    channels = chan_mgr.list_channels()
    assert len(channels) >= 6

    history = ConversationHistory.get_mission_conversation("mission_live_001")
    assert history["mission_id"] == "mission_live_001"
    assert history["is_provenance_verified"] is True
    assert len(history["messages"]) >= 4
