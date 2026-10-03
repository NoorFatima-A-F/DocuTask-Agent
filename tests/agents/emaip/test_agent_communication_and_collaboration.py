"""
Tests for Agent Message Bus, Skills Registry, Supervisor Agent, and Worker Collaboration.
"""

from app.agents.collaboration.supervisor import SupervisorAgent
from app.agents.collaboration.worker import WorkerAgent
from app.agents.communication.message_bus import (
    AgentMessage,
    AgentMessageBus,
    AgentMessageType,
)
from app.agents.decomposition.task_decomposer import TaskDecomposer
from app.agents.domain.agent_entity import AgentType, GoalModel
from app.agents.skills.skill_registry import AgentSkill, SkillRegistry


def test_agent_message_bus_routing_and_broadcast():
    bus = AgentMessageBus()
    received_msgs = []

    bus.subscribe("Supervisor", lambda msg: received_msgs.append(msg))

    msg1 = AgentMessage(
        sender="Worker1",
        receiver="Supervisor",
        type=AgentMessageType.RESPONSE,
        payload={"result": "extraction_done"},
    )
    bus.send(msg1)

    assert len(received_msgs) == 1
    assert received_msgs[0].payload["result"] == "extraction_done"

    # Direct pop from receiver mailbox
    popped = bus.receive("Supervisor")
    assert popped is not None
    assert popped.id == msg1.id


import asyncio

def test_supervisor_worker_plan_execution():
    async def _run():
        bus = AgentMessageBus()
        skills = SkillRegistry()
        skills.register(AgentSkill(
            name="custom_extraction",
            capability="extraction",
            handler=lambda data: {"extracted": True, "data": data},
        ))

        worker1 = WorkerAgent(
            agent_id="worker-exec-1",
            name="ExecutionAgent",
            agent_type=AgentType.EXECUTION,
            skill_registry=skills,
        )
        worker2 = WorkerAgent(
            agent_id="worker-valid-1",
            name="ValidationAgent",
            agent_type=AgentType.VALIDATION,
            skill_registry=skills,
        )

        supervisor = SupervisorAgent(message_bus=bus)

        decomposer = TaskDecomposer()
        goal = GoalModel(description="Process vendor invoice for Acme Corp")
        plan = decomposer.decompose(goal=goal)

        workers = {
            "ExecutionAgent": worker1,
            "ValidationAgent": worker2,
            "ComplianceAgent": worker1,
            "HumanLiaisonAgent": worker2,
        }

        report = await supervisor.execute_plan(plan=plan, worker_registry=workers, budget_limit_usd=5.0)

        assert report.status == "COMPLETED"
        assert report.completed_steps == len(plan.steps)
        assert report.total_cost_usd > 0
        assert len(report.step_results) == len(plan.steps)

    asyncio.run(_run())

