"""Tests for Event Processor, Deduplication, and Event Analyzer."""

from app.observability.core.events import EventCategory, EventStream, PlatformEvent
from app.observability.events.analyzer import EventAnalyzer
from app.observability.events.processor import EventProcessor


def test_event_processor_deduplication():
    stream = EventStream()
    processor = EventProcessor(event_stream=stream, dedup_window_seconds=1.0)

    event = PlatformEvent(
        name="worker.heartbeat_timeout",
        category=EventCategory.RUNTIME,
        severity="WARNING",
    )

    # First event passes through
    res1 = processor.process(event)
    assert res1 is not None

    # Duplicate within window is deduplicated
    res2 = processor.process(event)
    assert res2 is None

    stats = processor.get_dedup_stats()
    assert list(stats.values())[0] == 2


def test_event_analyzer_pattern_correlation():
    stream = EventStream()
    analyzer = EventAnalyzer(event_stream=stream)

    # Publish correlated events: worker failure + queue spike
    stream.publish(PlatformEvent(name="worker.crash", category=EventCategory.RUNTIME, severity="CRITICAL"))
    stream.publish(PlatformEvent(name="queue.backlog_spike", category=EventCategory.RUNTIME, severity="WARNING"))
    stream.publish(PlatformEvent(name="cpu.high_usage", category=EventCategory.INFRASTRUCTURE, severity="WARNING"))

    insights = analyzer.analyze_recent_events(window_seconds=60.0)
    assert len(insights) >= 1
    assert "Worker Node Saturation" in insights[0].title
    assert insights[0].confidence >= 0.90
