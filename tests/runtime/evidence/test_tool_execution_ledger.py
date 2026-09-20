"""Tests for Tool Execution Ledger and Trace Collector."""

import pytest
from app.runtime.tool_ledger.tool_execution_ledger import ToolExecutionLedger
from app.runtime.tool_ledger.tool_trace_collector import ToolTraceCollector


def test_tool_trace_collector():
    trace = ToolTraceCollector.capture_trace(
        tool_name="test_tool",
        inputs={"param": 1},
        outputs={"res": "ok"},
        latency_ms=85.0,
        cost_usd=0.0002,
        energy_joules=0.15,
        exit_code=0,
        stdout="Success",
    )
    assert trace.tool_name == "test_tool"
    assert len(trace.input_digest) == 64
    assert len(trace.output_digest) == 64
    assert trace.latency_ms == 85.0


def test_tool_execution_ledger_chain():
    ledger = ToolExecutionLedger()
    e1 = ledger.record_execution(
        call_id="call-1",
        tool_name="ocr_tool",
        inputs={"img": "data1"},
        outputs={"text": "hello"},
        latency_ms=110.0,
    )
    assert e1.previous_hash == "genesis_tool_block_0000"

    e2 = ledger.record_execution(
        call_id="call-2",
        tool_name="extract_tool",
        inputs={"text": "hello"},
        outputs={"name": "Alice"},
        latency_ms=90.0,
    )
    assert e2.previous_hash == e1.entry_hash
    assert ledger.count() == 2
    assert ledger.verify_chain() is True
    assert ledger.get_entry("call-1") is not None
