"""
API Version 1 Router Aggregator.
Combines sub-routers into single v1 API router.
"""

from fastapi import APIRouter
from app.api.v1.endpoints import (
    ai,
    auth,
    documents,
    health,
    jobs,
    ocr,
    runtime,
    planning,
    probabilistic,
    evolution,
    planner,
    replay,
    optimization,
    validation,
    transparency,
    organization,
    evidence,
    platform,
    intelligence,
    trust,
    resilience,
    events,
    confidence,
    learning,
    operations,
    swarm,
    meta,
    world,
    strategy,
    science,
    execution,
    world_model,
    ai_operations,
    distributed_runtime,
    business_process,
    saas_platform,
    ai_lifecycle,
    knowledge,
    cognitive,
    workforce,
    verification,
    config_versioning,
    plugins,
    domain_verification,
)

api_v1_router = APIRouter()

api_v1_router.include_router(health.router)
api_v1_router.include_router(auth.router)
api_v1_router.include_router(documents.router)
api_v1_router.include_router(ocr.router)
api_v1_router.include_router(ai.router)
api_v1_router.include_router(jobs.router)
api_v1_router.include_router(runtime.router, prefix="/runtime", tags=["Runtime Observability"])
api_v1_router.include_router(planning.router, prefix="/planning", tags=["Autonomous Planning"])
api_v1_router.include_router(planner.router, prefix="/planner", tags=["Dynamic DAG & Replanning (APDLE)"])
api_v1_router.include_router(probabilistic.router, prefix="/intelligence", tags=["Probabilistic Intelligence"])
api_v1_router.include_router(evolution.router, prefix="/evolution", tags=["Cognitive Evolution"])
api_v1_router.include_router(replay.router, prefix="/replay", tags=["Mission Replay & Decision Provenance (ESMR)"])
api_v1_router.include_router(optimization.router, prefix="/optimization", tags=["Quantitative Decision Intelligence (QDIOP)"])
api_v1_router.include_router(validation.router, prefix="/validation", tags=["Autonomous Scientific Validation (ASVSP)"])
api_v1_router.include_router(transparency.router, prefix="/transparency", tags=["Runtime Transparency & Credibility (ARTEICP)"])
api_v1_router.include_router(organization.router, prefix="/organization", tags=["Autonomous Enterprise Organization (AMAEOP)"])
api_v1_router.include_router(evidence.router, prefix="/evidence", tags=["Autonomous Execution Evidence (AEEERP)"])
api_v1_router.include_router(platform.router, prefix="/platform", tags=["Autonomous Agent Platform & OS (AAPEROS)"])
api_v1_router.include_router(intelligence.router, prefix="/intelligence", tags=["Adaptive Intelligence & Continuous Optimization (AISLCOP)"])
api_v1_router.include_router(trust.router, prefix="/trust", tags=["Verifiable Autonomous Intelligence & Runtime Truth (VAIRTSEP)"])
api_v1_router.include_router(resilience.router, prefix="/resilience", tags=["Production Reliability & Chaos (APRCORP+)"])
api_v1_router.include_router(events.router, prefix="/events", tags=["Domain Events & Runtime Observability (ARODP)"])
api_v1_router.include_router(confidence.router, prefix="/confidence", tags=["Scientific Confidence Engine & Governance (ASCE-CGP)"])
api_v1_router.include_router(learning.router, prefix="/learning", tags=["Reflection, Learning & Policy Evolution (ARLP-KIP)"])
api_v1_router.include_router(operations.router, prefix="/operations", tags=["Autonomous Operations & Resilience (AOIS-HROP)"])
api_v1_router.include_router(swarm.router, prefix="/swarm", tags=["Autonomous Swarm Intelligence & Coordination (AMCN-SIP)"])
api_v1_router.include_router(meta.router, prefix="/meta", tags=["Autonomous Meta-Reasoning & Self-Improvement (AMRS-RSIP)"])
api_v1_router.include_router(world.router, prefix="/world", tags=["Autonomous World Modeling & Digital Twin Intelligence (AWM-PSDTIP)"])
api_v1_router.include_router(strategy.router, prefix="/strategy", tags=["Autonomous Strategic Cognition & Executive Intelligence (ASC-GEEIP)"])
api_v1_router.include_router(science.router, prefix="/science", tags=["Autonomous Scientific Discovery & Knowledge Evolution (ASD-HGCKEP)"])
api_v1_router.include_router(execution.router, prefix="/execution", tags=["Autonomous Real-World Execution & Operations (ARWE-UTOCOP)"])
api_v1_router.include_router(world_model.router, prefix="/world_model", tags=["Autonomous World Modeling, Predictive Intelligence & Causal Reasoning (AWMPICRP)"])
api_v1_router.include_router(ai_operations.router, prefix="/ai_operations", tags=["Autonomous AI Operations Center (AAIOC)"])
api_v1_router.include_router(distributed_runtime.router, prefix="/distributed", tags=["Autonomous Cloud Runtime & Distributed Agent Fabric (ACR-DAF)"])
api_v1_router.include_router(business_process.router, prefix="/business", tags=["Enterprise Process Intelligence & Autonomous Business Orchestration (EPI-ABOP)"])
api_v1_router.include_router(saas_platform.router, prefix="/saas", tags=["Enterprise AI Platform & Multi-Tenant SaaS Operating System (EAP-MTSOS)"])
api_v1_router.include_router(ai_lifecycle.router, prefix="/ai-lifecycle", tags=["Autonomous AI Application Lifecycle Platform (AAILP)"])
api_v1_router.include_router(knowledge.router, prefix="/knowledge", tags=["Enterprise AI Knowledge & Context Intelligence Platform (EAKCIP)"])
api_v1_router.include_router(cognitive.router, prefix="/cognitive", tags=["Enterprise Cognitive Intelligence & Autonomous Organizational Learning (ECIAOLP)"])
api_v1_router.include_router(workforce.router, prefix="/workforce", tags=["Enterprise Autonomous Agent Workforce & Digital Organization (EAAWDOP)"])
api_v1_router.include_router(verification.router, prefix="/verification", tags=["Foundational Verification Platform Architecture (FVPA)"])
api_v1_router.include_router(config_versioning.router, prefix="/verification/config-versioning", tags=["Enterprise Verification Configuration & Versioning (EV-CVDM)"])
api_v1_router.include_router(plugins.router, prefix="/verification/plugins", tags=["Enterprise Verification Extension Framework & Plugins (EV-EFIPA)"])
api_v1_router.include_router(domain_verification.router, prefix="/verification/domain", tags=["Enterprise Verification Domain Model & Data Architecture (EV-DMDA)"])







