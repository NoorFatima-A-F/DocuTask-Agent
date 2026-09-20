from typing import Dict, List, Any
from ..domain.quality_domain import QualityGateAggregate, QualityGateEvaluated
from app.shared_kernel import Result, Ok, get_event_bus

class QualityGateService:
    def __init__(self, repo):
        self.repo = repo

    async def evaluate_metrics(self, gate_id: str, run_id: str, metrics: Dict[str, float], rules: List[Dict[str, Any]]) -> Result[QualityGateAggregate, str]:
        passed = True
        blockers = []
        for r in rules:
            m_name = r["metric"]
            val = metrics.get(m_name)
            if val is None or val < r["threshold"]:
                passed = False
                blockers.append(f"Rule failed for {m_name}")
        agg = QualityGateAggregate(id=gate_id, run_id=run_id, is_passed=passed, blockers=blockers)
        self.repo.save(agg)
        await get_event_bus().publish(QualityGateEvaluated(gate_id=gate_id, passed=passed))
        return Ok(agg)
