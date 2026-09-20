"""Tool Trace Collector and Execution Ledger.

Records granular traces of every tool invocation, input parameters, execution logs,
token cost, energy consumption (Joules), and output digests in an immutable ledger.
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ToolTrace:
    trace_id: str
    tool_name: str
    input_digest: str
    output_digest: str
    latency_ms: float
    token_cost_usd: float
    energy_joules: float
    exit_code: int
    stdout_snippet: str
    stderr_snippet: str
    side_effects: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "trace_id": self.trace_id,
            "tool_name": self.tool_name,
            "input_digest": self.input_digest,
            "output_digest": self.output_digest,
            "latency_ms": self.latency_ms,
            "token_cost_usd": self.token_cost_usd,
            "energy_joules": self.energy_joules,
            "exit_code": self.exit_code,
            "stdout_snippet": self.stdout_snippet,
            "stderr_snippet": self.stderr_snippet,
            "side_effects": self.side_effects,
        }


@dataclass
class ToolExecutionEntry:
    entry_id: str
    call_id: str
    tool_name: str
    timestamp: float
    input_parameters: Dict[str, Any]
    output_result: Dict[str, Any]
    trace: ToolTrace
    previous_hash: str
    entry_hash: str = ""

    def compute_hash(self) -> str:
        payload = {
            "entry_id": self.entry_id,
            "call_id": self.call_id,
            "tool_name": self.tool_name,
            "timestamp": round(self.timestamp, 4),
            "input_parameters": self.input_parameters,
            "output_result": self.output_result,
            "trace": self.trace.to_dict(),
            "previous_hash": self.previous_hash,
        }
        serialized = json.dumps(payload, sort_keys=True, default=str)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entry_id": self.entry_id,
            "call_id": self.call_id,
            "tool_name": self.tool_name,
            "timestamp_iso": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(self.timestamp)),
            "input_parameters": self.input_parameters,
            "output_result": self.output_result,
            "trace": self.trace.to_dict(),
            "previous_hash": self.previous_hash,
            "entry_hash": self.entry_hash,
        }


class ToolTraceCollector:
    @staticmethod
    def capture_trace(
        tool_name: str,
        inputs: Dict[str, Any],
        outputs: Dict[str, Any],
        latency_ms: float,
        cost_usd: float = 0.0008,
        energy_joules: float = 0.35,
        exit_code: int = 0,
        stdout: str = "",
        stderr: str = "",
        side_effects: Optional[List[str]] = None,
    ) -> ToolTrace:
        in_digest = hashlib.sha256(json.dumps(inputs, sort_keys=True, default=str).encode("utf-8")).hexdigest()
        out_digest = hashlib.sha256(json.dumps(outputs, sort_keys=True, default=str).encode("utf-8")).hexdigest()

        return ToolTrace(
            trace_id=f"tr-{int(time.time()*1000)}",
            tool_name=tool_name,
            input_digest=in_digest,
            output_digest=out_digest,
            latency_ms=round(latency_ms, 2),
            token_cost_usd=round(cost_usd, 6),
            energy_joules=round(energy_joules, 4),
            exit_code=exit_code,
            stdout_snippet=stdout[:200] if stdout else "OK",
            stderr_snippet=stderr[:200] if stderr else "",
            side_effects=side_effects or ["memory_buffer_updated"],
        )


class ToolExecutionLedger:
    def __init__(self):
        self._entries: List[ToolExecutionEntry] = []
        self._last_hash = "genesis_tool_block_0000"

    def record_execution(
        self,
        call_id: str,
        tool_name: str,
        inputs: Dict[str, Any],
        outputs: Dict[str, Any],
        latency_ms: float,
        cost_usd: float = 0.0008,
        energy_joules: float = 0.35,
        exit_code: int = 0,
        stdout: str = "",
        stderr: str = "",
        side_effects: Optional[List[str]] = None,
    ) -> ToolExecutionEntry:
        trace = ToolTraceCollector.capture_trace(
            tool_name=tool_name,
            inputs=inputs,
            outputs=outputs,
            latency_ms=latency_ms,
            cost_usd=cost_usd,
            energy_joules=energy_joules,
            exit_code=exit_code,
            stdout=stdout,
            stderr=stderr,
            side_effects=side_effects,
        )

        entry = ToolExecutionEntry(
            entry_id=f"tee-{len(self._entries) + 1:04d}",
            call_id=call_id,
            tool_name=tool_name,
            timestamp=time.time(),
            input_parameters=inputs,
            output_result=outputs,
            trace=trace,
            previous_hash=self._last_hash,
        )
        entry.entry_hash = entry.compute_hash()
        self._last_hash = entry.entry_hash
        self._entries.append(entry)
        return entry

    def list_entries(self) -> List[ToolExecutionEntry]:
        return list(self._entries)

    def get_entry(self, entry_id: str) -> Optional[ToolExecutionEntry]:
        for e in self._entries:
            if e.entry_id == entry_id or e.call_id == entry_id:
                return e
        return None

    def verify_chain(self) -> bool:
        prev = "genesis_tool_block_0000"
        for e in self._entries:
            if e.previous_hash != prev:
                return False
            if e.compute_hash() != e.entry_hash:
                return False
            prev = e.entry_hash
        return True

    def count(self) -> int:
        return len(self._entries)

    def clear(self) -> None:
        self._entries.clear()
        self._last_hash = "genesis_tool_block_0000"


global_tool_ledger = ToolExecutionLedger()
