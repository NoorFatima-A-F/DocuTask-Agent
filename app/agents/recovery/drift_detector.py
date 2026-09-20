"""
Drift Detector.
Detects drift between expected checkpointed state and live runtime execution graph state.
"""

from typing import Any, Dict


class DriftDetector:
    """Detects divergence between checkpoint payloads and live outputs."""

    def has_drifted(self, checkpoint_outputs: Dict[str, Any], live_outputs: Dict[str, Any]) -> bool:
        for k, v in checkpoint_outputs.items():
            if k in live_outputs and live_outputs[k] != v:
                return True
        return False
