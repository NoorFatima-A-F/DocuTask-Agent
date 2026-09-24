"""
Fluent Builders Suite for Enterprise Planning Contracts.
Provides PlanBuilder, GraphBuilder, WorkflowBuilder, TaskBuilder, GoalBuilder, DependencyBuilder, and ConstraintBuilder.
Enforces structural integrity during graph and plan creation.
"""

from typing import Dict, List, Optional
from uuid import uuid4
from app.agents.planning.constraints import ConstraintType, PlanConstraint
from app.agents.planning.contracts import Plan
from app.agents.planning.dependencies import Dependency, DependencyType
from app.agents.planning.edges import EdgeType, PlanEdge
from app.agents.planning.goals import PlanGoal
from app.agents.planning.graph import PlanGraph
from app.agents.planning.metadata import PlanIdentity, PlanStatistics
from app.agents.planning.nodes import NodeType, PlanNode
from app.agents.planning.tasks import PlanningTask
from app.agents.planning.validators import PlanStructuralValidator
from app.agents.planning.workflow import WorkflowDefinition


class GraphBuilder:
    """Fluent builder for PlanGraph DAG instances."""

    def __init__(self, graph_id: Optional[str] = None):
        self._graph_id = graph_id or str(uuid4())
        self._nodes: Dict[str, PlanNode] = {}
        self._edges: List[PlanEdge] = []
        self._entry_node_ids: List[str] = []
        self._exit_node_ids: List[str] = []

    def add_node(self, node_id: str, name: str, node_type: NodeType = NodeType.TASK, timeout_seconds: float = 300.0) -> "GraphBuilder":
        node = PlanNode(node_id=node_id, name=name, node_type=node_type, timeout_seconds=timeout_seconds)
        self._nodes[node_id] = node
        return self

    def add_edge(self, source_id: str, target_id: str, edge_type: EdgeType = EdgeType.SEQUENTIAL) -> "GraphBuilder":
        edge = PlanEdge(
            edge_id=f"{source_id}->{target_id}",
            source_node_id=source_id,
            target_node_id=target_id,
            edge_type=edge_type
        )
        self._edges.append(edge)
        return self

    def with_entry_nodes(self, entry_ids: List[str]) -> "GraphBuilder":
        self._entry_node_ids = list(entry_ids)
        return self

    def with_exit_nodes(self, exit_ids: List[str]) -> "GraphBuilder":
        self._exit_node_ids = list(exit_ids)
        return self

    def build(self) -> PlanGraph:
        return PlanGraph(
            graph_id=self._graph_id,
            nodes=self._nodes,
            edges=self._edges,
            entry_node_ids=self._entry_node_ids,
            exit_node_ids=self._exit_node_ids
        )


class PlanBuilder:
    """Fluent builder for Plan aggregates."""

    def __init__(self, name: str = "ExecutionPlan"):
        self._name = name
        self._goal_id: Optional[str] = None
        self._graph: Optional[PlanGraph] = None
        self._cost_usd = 0.0
        self._duration_seconds = 0.0
        self._constraints: List[PlanConstraint] = []
        self._dependencies: List[Dependency] = []

    def for_goal(self, goal_id: str) -> "PlanBuilder":
        self._goal_id = goal_id
        return self

    def with_graph(self, graph: PlanGraph) -> "PlanBuilder":
        self._graph = graph
        return self

    def with_cost(self, cost_usd: float) -> "PlanBuilder":
        self._cost_usd = cost_usd
        return self

    def with_duration(self, duration_seconds: float) -> "PlanBuilder":
        self._duration_seconds = duration_seconds
        return self

    def add_constraint(self, constraint: PlanConstraint) -> "PlanBuilder":
        self._constraints.append(constraint)
        return self

    def build(self) -> Plan:
        graph = self._graph or PlanGraph(graph_id=str(uuid4()))
        stats = PlanStatistics(
            total_nodes_count=len(graph.nodes),
            total_edges_count=len(graph.edges),
            estimated_cost_usd=self._cost_usd,
            estimated_duration_seconds=self._duration_seconds
        )
        identity = PlanIdentity(goal_id=self._goal_id)
        plan = Plan(
            name=self._name,
            identity=identity,
            graph=graph,
            statistics=stats,
            constraints=self._constraints,
            dependencies=self._dependencies
        )
        PlanStructuralValidator.validate_plan_structure(plan)
        return plan


class WorkflowBuilder:
    """Fluent builder for WorkflowDefinition."""

    def __init__(self, name: str, graph: PlanGraph):
        self._workflow_id = str(uuid4())
        self._name = name
        self._graph = graph
        self._timeout_seconds = 3600.0

    def with_timeout(self, timeout_seconds: float) -> "WorkflowBuilder":
        self._timeout_seconds = timeout_seconds
        return self

    def build(self) -> WorkflowDefinition:
        return WorkflowDefinition(
            workflow_id=self._workflow_id,
            name=self._name,
            graph=self._graph,
            timeout_seconds=self._timeout_seconds
        )


class TaskBuilder:
    """Fluent builder for PlanningTask."""

    def __init__(self, task_id: str, name: str):
        self._task_id = task_id
        self._name = name
        self._capability: Optional[str] = None
        self._duration = 1.0

    def requiring_capability(self, capability: str) -> "TaskBuilder":
        self._capability = capability
        return self

    def with_duration(self, duration_seconds: float) -> "TaskBuilder":
        self._duration = duration_seconds
        return self

    def build(self) -> PlanningTask:
        return PlanningTask(
            task_id=self._task_id,
            name=self._name,
            capability_requirement=self._capability,
            estimated_duration_seconds=self._duration
        )


class GoalBuilder:
    """Fluent builder for PlanGoal."""

    def __init__(self, goal_id: str, name: str):
        self._goal_id = goal_id
        self._name = name
        self._criteria: List[str] = []

    def with_criterion(self, criterion: str) -> "GoalBuilder":
        self._criteria.append(criterion)
        return self

    def build(self) -> PlanGoal:
        return PlanGoal(
            goal_id=self._goal_id,
            name=self._name,
            success_criteria=self._criteria
        )


class DependencyBuilder:
    """Fluent builder for Dependency."""

    def __init__(self, source_id: str, target_id: str):
        self._source_id = source_id
        self._target_id = target_id
        self._type = DependencyType.HARD

    def with_type(self, dep_type: DependencyType) -> "DependencyBuilder":
        self._type = dep_type
        return self

    def build(self) -> Dependency:
        return Dependency(
            source_id=self._source_id,
            target_id=self._target_id,
            dependency_type=self._type
        )


class ConstraintBuilder:
    """Fluent builder for PlanConstraint."""

    def __init__(self, constraint_id: str, constraint_type: ConstraintType):
        self._constraint_id = constraint_id
        self._type = constraint_type
        self._limit = 0.0

    def with_limit(self, limit_value: float) -> "ConstraintBuilder":
        self._limit = limit_value
        return self

    def build(self) -> PlanConstraint:
        return PlanConstraint(
            constraint_id=self._constraint_id,
            constraint_type=self._type,
            limit_value=self._limit
        )
