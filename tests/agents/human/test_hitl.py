"""
Production Tests for Human-In-The-Loop (HITL) Collaboration System.
Covers ApprovalQueue, FeedbackProcessor, HumanFeedbackMemory, and HumanTaskManager.
"""

import time
import pytest
from uuid import uuid4

from app.agents.human.approval_queue import (
    ApprovalQueue,
    HumanTaskTicket,
    TicketPriority,
    TicketStatus,
)
from app.agents.human.feedback_processor import (
    FeedbackProcessor,
    HumanActionType,
    HumanFeedbackDirective,
)
from app.agents.human.human_feedback_memory import HumanFeedbackMemory
from app.agents.human.human_task_manager import HumanTaskManager
from app.agents.memory.intelligence.episodic_memory import EpisodicMemory
from app.agents.memory.intelligence.semantic_memory import SemanticFact, SemanticMemory


class TestApprovalQueue:
    def test_submit_ticket_priority_ordering(self):
        queue = ApprovalQueue()
        t_low = queue.submit_ticket(
            execution_id="e1",
            task_id="t_low",
            reason="Low priority review",
            extracted_data={},
            priority=TicketPriority.LOW,
        )
        t_crit = queue.submit_ticket(
            execution_id="e1",
            task_id="t_crit",
            reason="Critical financial discrepancy",
            extracted_data={},
            priority=TicketPriority.CRITICAL,
        )
        t_med = queue.submit_ticket(
            execution_id="e1",
            task_id="t_med",
            reason="Medium review",
            extracted_data={},
            priority=TicketPriority.MEDIUM,
        )

        assert len(queue) == 3

        # Highest priority (CRITICAL = 1) should be popped first
        first = queue.get_next_pending_ticket()
        assert first.ticket_id == t_crit.ticket_id

        # Next: MEDIUM = 3
        second = queue.get_next_pending_ticket()
        assert second.ticket_id == t_med.ticket_id

        # Next: LOW = 4
        third = queue.get_next_pending_ticket()
        assert third.ticket_id == t_low.ticket_id

    def test_sla_timeout_expiration(self):
        queue = ApprovalQueue()
        # Submit ticket with 0.01 second SLA
        ticket = queue.submit_ticket(
            execution_id="e_sla",
            task_id="t_sla",
            reason="Fast timeout",
            extracted_data={},
            priority=TicketPriority.HIGH,
            sla_timeout_seconds=0.01,
        )
        time.sleep(0.02)
        assert ticket.is_expired() is True

        # Popping should discard expired ticket and return None
        popped = queue.get_next_pending_ticket()
        assert popped is None
        assert ticket.status == TicketStatus.TIMED_OUT

    def test_ticket_to_dict(self):
        ticket = HumanTaskTicket(
            priority=TicketPriority.HIGH,
            created_at_timestamp=time.time(),
            execution_id="e1",
            task_id="t1",
            reason="Test",
        )
        d = ticket.to_dict()
        assert d["priority"] == "HIGH"
        assert d["execution_id"] == "e1"
        assert d["status"] == "PENDING"


class TestFeedbackProcessor:
    def test_process_approve_decision(self):
        processor = FeedbackProcessor()
        ticket = HumanTaskTicket(
            priority=TicketPriority.HIGH,
            created_at_timestamp=time.time(),
            execution_id="e1",
            task_id="t1",
            extracted_data={"total_amount": 1000.0},
        )
        directive = processor.process_decision(
            ticket=ticket,
            action=HumanActionType.APPROVE,
            operator_id="operator_alice",
            notes="Looks good",
        )
        assert ticket.status == TicketStatus.APPROVED
        assert directive.should_resume_graph is True
        assert directive.should_abort is False
        assert directive.effective_data["total_amount"] == 1000.0

    def test_process_modify_decision(self):
        processor = FeedbackProcessor()
        ticket = HumanTaskTicket(
            priority=TicketPriority.HIGH,
            created_at_timestamp=time.time(),
            execution_id="e2",
            task_id="t2",
            extracted_data={"total_amount": 900.0},
        )
        directive = processor.process_decision(
            ticket=ticket,
            action=HumanActionType.MODIFY,
            operator_id="operator_bob",
            corrected_data={"total_amount": 1100.0, "vendor_name": "ACME"},
            notes="Corrected total and vendor",
        )
        assert ticket.status == TicketStatus.MODIFIED
        assert directive.should_resume_graph is True
        assert directive.effective_data["total_amount"] == 1100.0
        assert directive.effective_data["vendor_name"] == "ACME"

    def test_process_reject_decision(self):
        processor = FeedbackProcessor()
        ticket = HumanTaskTicket(
            priority=TicketPriority.CRITICAL,
            created_at_timestamp=time.time(),
            execution_id="e3",
            task_id="t3",
        )
        directive = processor.process_decision(
            ticket=ticket,
            action=HumanActionType.REJECT,
            operator_id="operator_carol",
            notes="Fraudulent document",
        )
        assert ticket.status == TicketStatus.REJECTED
        assert directive.should_resume_graph is False
        assert directive.should_abort is True


class TestHumanTaskManager:
    def test_escalate_and_resolve_lifecycle(self):
        sem_mem = SemanticMemory()
        ep_mem = EpisodicMemory()
        mgr = HumanTaskManager(semantic_memory=sem_mem, episodic_memory=ep_mem)

        # 1. Escalate
        ticket = mgr.escalate(
            execution_id="exec_hitl_1",
            task_id="validate_invoice",
            reason="Unrecognized tax format",
            extracted_data={"vendor_name": "NewVendor", "tax_id": "UNKNOWN"},
            priority=TicketPriority.HIGH,
        )
        assert ticket.status == TicketStatus.PENDING
        assert len(mgr.get_pending_tickets()) == 1

        # 2. Operator submits correction
        directive = mgr.submit_operator_decision(
            ticket_id=ticket.ticket_id,
            action=HumanActionType.MODIFY,
            operator_id="supervisor_dan",
            corrected_data={"vendor_name": "NewVendor", "tax_id": "TAX-9988"},
            notes="Vendor uses custom German VAT header",
            document_id="doc_hitl_1",
        )

        assert directive.action_type == HumanActionType.MODIFY
        assert ticket.status == TicketStatus.MODIFIED
        assert len(mgr.get_pending_tickets()) == 0

        # 3. Verify permanent learning in Semantic Memory
        facts_with_scores = sem_mem.retrieve_relevant_facts(query="NewVendor")
        assert len(facts_with_scores) > 0
        tax_fact = next(f for f, _ in facts_with_scores if "tax_id" in f.predicate)
        assert tax_fact.fact_value == "TAX-9988"
        assert tax_fact.confidence == 1.0

        # 4. Verify Episodic Memory record
        episodes = ep_mem.retrieve_relevant_episodes(query="NewVendor")
        assert len(episodes) > 0
        assert "hitl" in episodes[0][0].tags

    @pytest.mark.parametrize(
        "priority,sla_sec,should_expire",
        [
            (TicketPriority.CRITICAL, 0.01, True),
            (TicketPriority.HIGH, 0.01, True),
            (TicketPriority.MEDIUM, 10.0, False),
            (TicketPriority.LOW, 10.0, False),
            (TicketPriority.CRITICAL, 0.0, False),
        ],
    )
    def test_sla_timeout_parameterized(self, priority, sla_sec, should_expire):
        queue = ApprovalQueue()
        ticket = queue.submit_ticket(
            execution_id="e_sla_param",
            task_id="t_sla_param",
            reason="Timeout test",
            extracted_data={},
            priority=priority,
            sla_timeout_seconds=sla_sec,
        )
        if should_expire:
            time.sleep(0.02)
            assert ticket.is_expired() is True
            popped = queue.get_next_pending_ticket()
            assert popped is None
        else:
            assert ticket.is_expired() is False
            popped = queue.get_next_pending_ticket()
            assert popped is not None
            assert popped.ticket_id == ticket.ticket_id

    def test_retry_with_hint_action(self):
        processor = FeedbackProcessor()
        ticket = HumanTaskTicket(
            priority=TicketPriority.HIGH,
            created_at_timestamp=time.time(),
            execution_id="e_retry",
            task_id="t_retry",
            extracted_data={"raw_text": "Sample text"},
        )
        directive = processor.process_decision(
            ticket=ticket,
            action=HumanActionType.RETRY_WITH_HINT,
            operator_id="operator_dave",
            notes="Look at bottom table instead of top",
        )
        assert ticket.status == TicketStatus.MODIFIED
        assert directive.should_resume_graph is True
        assert directive.action_type == HumanActionType.RETRY_WITH_HINT
        assert "bottom table" in directive.guidance_notes

    def test_manager_get_tickets_by_execution(self):
        mgr = HumanTaskManager()
        mgr.escalate(execution_id="exec_A", task_id="t1", reason="R1", extracted_data={})
        mgr.escalate(execution_id="exec_A", task_id="t2", reason="R2", extracted_data={})
        mgr.escalate(execution_id="exec_B", task_id="t3", reason="R3", extracted_data={})

        assert len(mgr.get_tickets_for_execution("exec_A")) == 2
        assert len(mgr.get_tickets_for_execution("exec_B")) == 1
        assert len(mgr.get_tickets_for_execution("exec_C")) == 0

    def test_feedback_memory_overwrites_low_confidence_fact(self):
        sem_mem = SemanticMemory()
        # Seed memory with low confidence guess
        sem_mem.store_fact(
            SemanticFact(
                subject="VendorXYZ",
                predicate="iban",
                fact_value="DE0000000000",
                confidence=0.45,
                metadata={"source": "heuristic_guess"},
            )
        )

        fb_mem = HumanFeedbackMemory(semantic_memory=sem_mem)
        directive = HumanFeedbackDirective(
            execution_id="exec_xyz",
            task_id="extract_iban",
            action_type=HumanActionType.MODIFY,
            operator_id="supervisor_eve",
            effective_data={"vendor_name": "VendorXYZ", "iban": "DE998877665544"},
        )
        fb_mem.learn_from_feedback(directive=directive, document_id="doc_xyz")

        facts = sem_mem.retrieve_relevant_facts("VendorXYZ")
        high_conf_fact = next(f for f, _ in facts if "iban" in f.predicate and f.confidence == 1.0)
        assert high_conf_fact.fact_value == "DE998877665544"

    def test_invalid_ticket_decision_raises_error(self):
        mgr = HumanTaskManager()
        with pytest.raises(ValueError):
            mgr.submit_operator_decision(ticket_id=uuid4(), action=HumanActionType.APPROVE)


