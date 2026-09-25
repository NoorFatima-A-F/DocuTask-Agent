"""
Multi-Stage Planning Pipeline.
Executes Goal Analysis -> Decomposition -> Candidate Generation -> Optimization -> Reflection -> Repair.
"""

from app.agents.planner.candidate_generator import CandidatePlanGenerator
from app.agents.planner.context import PlannerRequest
from app.agents.planner.evaluation import CandidateEvaluator
from app.agents.planner.goal_analyzer import GoalAnalyzer
from app.agents.planner.interfaces import IPlanningPipeline
from app.agents.planner.plan_optimizer import PlanOptimizer
from app.agents.planner.plan_ranker import PlanRanker
from app.agents.planner.reflection import PlannerReflectionEngine
from app.agents.planner.repair import PlanRepairEngine
from app.agents.planning.contracts import Plan


class PlanningPipeline(IPlanningPipeline):
    """Orchestrates sequential cognitive stages of plan synthesis."""

    def __init__(self):
        self.goal_analyzer = GoalAnalyzer()
        self.candidate_generator = CandidatePlanGenerator()
        self.candidate_evaluator = CandidateEvaluator()
        self.plan_ranker = PlanRanker()
        self.plan_optimizer = PlanOptimizer()
        self.reflection_engine = PlannerReflectionEngine()
        self.repair_engine = PlanRepairEngine()

    async def execute_pipeline(self, request: PlannerRequest) -> Plan:
        # 1. Goal Analysis
        self.goal_analyzer.analyze_goal(request.goal, request.context)

        # 2. Candidate Generation
        raw_candidates = self.candidate_generator.generate_candidates(request)

        # 3. Candidate Evaluation & Ranking
        evaluated_candidates = self.candidate_evaluator.evaluate_candidates(raw_candidates, request.context)
        best_candidate = self.plan_ranker.rank_and_select_best(evaluated_candidates) or raw_candidates[0]

        # 4. Plan Optimization
        optimized_plan = self.plan_optimizer.optimize_plan(best_candidate.plan)

        # 5. Reflection & Self-Critique
        critique = self.reflection_engine.critique_plan(optimized_plan)

        # 6. Automatic Repair if needed
        final_plan = self.repair_engine.repair_plan(optimized_plan, critique)

        return final_plan
