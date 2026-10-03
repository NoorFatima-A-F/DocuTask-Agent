"""
Unit and Integration Tests for Enterprise Verification Repository Architecture & Shared Kernel.
"""
from app.platform_verification.shared_kernel.result import Success, Failure, Some, Empty
from app.platform_verification.shared_kernel.identifiers import (
    CorrelationId, ExecutionId, TenantId, RunId
)
from app.platform_verification.shared_kernel.clock import VirtualClock
from app.platform_verification.shared_kernel.pagination import PaginationQuery
from app.platform_verification.shared_kernel.filtering import FilterCriteria, SearchQuery, SortOrder
from app.platform_verification.shared_kernel.security import CanonicalHasher
from app.platform_verification.configuration.scopes import ConfigScope
from app.platform_verification.configuration.manager import verification_config_manager
from app.platform_verification.events.bus import EnterpriseEventBus
from app.platform_verification.events.domain_events import VerificationStartedDomainEvent
from app.platform_verification.modules.core.interfaces.facade import core_facade
from app.platform_verification.modules.ocr.interfaces.facade import ocr_facade
from app.platform_verification.modules.datasets.interfaces.facade import datasets_facade


def test_shared_kernel_result_and_option_patterns():
    success = Success(42)
    assert success.is_success is True
    assert success.is_failure is False
    assert success.unwrap() == 42
    assert success.map(lambda x: x * 2).unwrap() == 84

    failure = Failure("Critical invariant violation")
    assert failure.is_success is False
    assert failure.is_failure is True
    assert failure.error == "Critical invariant violation"
    assert failure.unwrap_or(100) == 100

    some_opt = Some("active_sandbox")
    assert some_opt.is_some is True
    assert some_opt.unwrap() == "active_sandbox"

    empty_opt = Empty()
    assert empty_opt.is_empty is True
    assert empty_opt.unwrap_or("fallback") == "fallback"


def test_shared_kernel_strongly_typed_identifiers():
    corr = CorrelationId.generate()
    assert corr.value.startswith("corr_")
    
    exec_id = ExecutionId.generate()
    assert exec_id.value.startswith("exec_")
    
    run_id = RunId.generate()
    assert run_id.value.startswith("vrun_")
    
    tenant = TenantId.default()
    assert tenant.value == "default-tenant"


def test_shared_kernel_virtual_clock():
    clock = VirtualClock()
    clock.now()
    t1_iso = clock.now_iso()
    assert "2026-01-01" in t1_iso


def test_shared_kernel_pagination_and_filtering():
    pq = PaginationQuery(page=2, page_size=20)
    assert pq.offset == 20
    assert pq.limit == 20

    sq = SearchQuery(
        query_text="invoice_ocr",
        filters=[FilterCriteria(field="status", operator="eq", value="PASSED")],
        sort_by="created_at",
        sort_order=SortOrder.DESC
    )
    assert len(sq.filters) == 1
    assert sq.filters[0].field == "status"


def test_shared_kernel_security_and_merkle_tree():
    leaves = [
        CanonicalHasher.hash_payload({"batch": 1}),
        CanonicalHasher.hash_payload({"batch": 2}),
        CanonicalHasher.hash_payload({"batch": 3})
    ]
    merkle_root = CanonicalHasher.calculate_merkle_root(leaves)
    assert len(merkle_root) == 64
    
    # Tamper check
    tampered_leaves = list(leaves)
    tampered_leaves[0] = CanonicalHasher.hash_payload({"batch": 999})
    tampered_root = CanonicalHasher.calculate_merkle_root(tampered_leaves)
    assert merkle_root != tampered_root


def test_scoped_configuration_resolution_and_freeze():
    verification_config_manager.set_scoped_config(ConfigScope.ENVIRONMENT, "max_workers", 16)
    
    resolved = verification_config_manager.resolve_effective_config(
        module_name="ocr_verification",
        overrides={"custom_timeout": 600}
    )
    assert resolved["max_workers"] == 16
    assert resolved["custom_timeout"] == 600

    config_hash = verification_config_manager.freeze_execution_config("exec_001", resolved)
    assert len(config_hash) == 64
    frozen = verification_config_manager.get_frozen_config("exec_001")
    assert frozen is not None
    assert frozen["max_workers"] == 16


def test_enterprise_event_bus_and_dlq():
    bus = EnterpriseEventBus()
    received = []

    def handler(evt):
        received.append(evt)

    def failing_handler(evt):
        raise ValueError("Simulated handler crash")

    bus.subscribe(VerificationStartedDomainEvent, handler)
    bus.subscribe(VerificationStartedDomainEvent, failing_handler)

    evt = VerificationStartedDomainEvent(aggregate_id="vrun_123", aggregate_type="VerificationRun")
    bus.publish(evt)

    assert len(received) == 1
    assert len(bus.get_history()) == 1
    assert len(bus.get_dead_letters()) == 1
    assert "Simulated handler crash" in bus.get_dead_letters()[0]["error"]


def test_modular_bounded_context_facades():
    # Core Facade
    core_res = core_facade.service.create("Core Verification Pipeline", tenant_id="tenant-alpha")
    assert core_res.is_success is True
    assert core_res.unwrap().name == "Core Verification Pipeline"

    # OCR Facade
    ocr_res = ocr_facade.service.create("OCR Precision Suite", accuracy_target=0.99)
    assert ocr_res.is_success is True
    assert ocr_res.unwrap().name == "OCR Precision Suite"

    # Datasets Facade
    ds_res = datasets_facade.service.create("Golden Invoices v2", sample_count=500)
    assert ds_res.is_success is True
    assert ds_res.unwrap().tenant_id == "default-tenant"
