"""
Learning Engine for Phase 13.5 (ARLP-KIP).
Coordinates pattern mining, institutional rule extraction, and strategy synthesis from reflections.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import uuid
from pydantic import BaseModel, Field

from app.runtime.learning.reflection.reflection_engine import MissionReflectionReport
from app.runtime.learning.learning.pattern_miner import PatternMiner, ExecutionPattern
from app.runtime.learning.learning.lesson_extractor import LessonExtractor, ExtractedRule
from app.runtime.learning.learning.strategy_builder import StrategyBuilder, ExecutionStrategy
from app.runtime.learning.learning.knowledge_compiler import KnowledgeCompiler, CompiledKnowledgeBundle


class MinedLesson(BaseModel):
    lesson_id: str = Field(default_factory=lambda: f"lsn_{uuid.uuid4().hex[:10]}")
    mission_id: str
    summary: str = "Institutional learning cycle results"
    mined_patterns: List[ExecutionPattern] = Field(default_factory=list)
    extracted_rules: List[ExtractedRule] = Field(default_factory=list)
    compiled_strategy: Optional[ExecutionStrategy] = None
    knowledge_bundle: Optional[CompiledKnowledgeBundle] = None
    confidence_score: float = 0.945
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class LearningEngine:
    """
    Coordinates pattern mining, institutional rule extraction, and strategy synthesis.
    """

    def __init__(self):
        self._lessons: Dict[str, MinedLesson] = {}
        # Pre-seed a default lesson
        self._seed_default_lesson()

    def _seed_default_lesson(self):
        patterns = PatternMiner.mine_patterns("mission-001")
        rules = LessonExtractor.extract_rules(patterns)
        strategy = StrategyBuilder.build_strategy(rules, goal_type="DYNAMIC_EXTRACTION")
        bundle = KnowledgeCompiler.compile_bundle("lsn_default", rules, strategy)
        lesson = MinedLesson(
            lesson_id="lsn_default_001",
            mission_id="mission-001",
            summary="Parallel Wavefront and Resilient Throttle Mitigation Rules",
            mined_patterns=patterns,
            extracted_rules=rules,
            compiled_strategy=strategy,
            knowledge_bundle=bundle,
            confidence_score=0.962,
        )
        self._lessons[lesson.lesson_id] = lesson

    def mine_lessons(self, reflection: MissionReflectionReport) -> MinedLesson:
        patterns = PatternMiner.mine_patterns(reflection.mission_id)
        rules = LessonExtractor.extract_rules(patterns)
        strategy = StrategyBuilder.build_strategy(rules, goal_type="DYNAMIC_EXTRACTION")
        lesson_id = f"lsn_{uuid.uuid4().hex[:10]}"
        bundle = KnowledgeCompiler.compile_bundle(lesson_id, rules, strategy)

        lesson = MinedLesson(
            lesson_id=lesson_id,
            mission_id=reflection.mission_id,
            summary=f"Mined lessons for mission {reflection.mission_id}",
            mined_patterns=patterns,
            extracted_rules=rules,
            compiled_strategy=strategy,
            knowledge_bundle=bundle,
            confidence_score=round(reflection.confidence_metrics.avg_confidence, 3),
        )

        self._lessons[lesson.lesson_id] = lesson
        return lesson

    def list_lessons(self) -> List[MinedLesson]:
        return list(self._lessons.values())

    def get_lesson(self, lesson_id: str) -> Optional[MinedLesson]:
        return self._lessons.get(lesson_id)


learning_engine = LearningEngine()
