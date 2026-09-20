"""
Tests for Platform Event Bus, DLQ, Idempotency, and Replay.
"""

import pytest
import asyncio
from app.events.bus import EventBus
from app.events.models import CloudEventEnvelope
from app.events.subscribers import IdempotentConsumer
from app.events.replay import EventReplayEngine


def test_event_bus_publish_and_pattern_subscribe():
    bus = EventBus()
    received = []

    bus.subscribe("document.*", lambda evt: received.append(evt.data.get("filename")))

    evt = CloudEventEnvelope(
        type="document.uploaded",
        data={"filename": "invoice_123.pdf"},
    )

    asyncio.run(bus.publish(evt))

    assert len(received) == 1
    assert received[0] == "invoice_123.pdf"


def test_event_bus_dlq_on_failure():
    bus = EventBus()

    def failing_handler(evt):
        raise RuntimeError("Database connection timed out")

    bus.subscribe("payment.*", failing_handler, subscriber_name="payment_listener")

    evt = CloudEventEnvelope(type="payment.initiated", data={"amount": 500})
    asyncio.run(bus.publish(evt, max_retries=2, retry_delay_seconds=0.01))

    assert bus.dlq.count() == 1
    dead_letter = bus.dlq.list_dead_letters()[0]
    assert dead_letter["subscriber"] == "payment_listener"
    assert "Database connection timed out" in dead_letter["error"]


def test_idempotent_consumer():
    consumer = IdempotentConsumer()
    counter = {"count": 0}

    def handler(evt):
        counter["count"] += 1

    wrapped = consumer.wrap(handler)

    evt = CloudEventEnvelope(type="test.event", data={})
    wrapped(evt)
    wrapped(evt)  # duplicate

    assert counter["count"] == 1


def test_event_replay():
    bus = EventBus()
    received = []
    bus.subscribe("order.*", lambda evt: received.append(evt.id))

    evt1 = CloudEventEnvelope(type="order.created", data={})
    evt2 = CloudEventEnvelope(type="order.fulfilled", data={})

    asyncio.run(bus.publish(evt1))
    asyncio.run(bus.publish(evt2))
    assert len(received) == 2

    # Clear received and replay
    received.clear()
    replay_engine = EventReplayEngine(bus)
    replayed_count = asyncio.run(replay_engine.replay(event_type_filter="order.created"))

    assert replayed_count == 1
    assert len(received) == 1
    assert received[0] == evt1.id
