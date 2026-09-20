"""Tests for Agent Marketplace and Organization Templates."""

import pytest
from app.platform.marketplace.marketplace_service import (
    MarketplaceService,
)
from app.platform.templates.template_engine import TemplateEngine


def test_marketplace_and_template_deployment():
    m_svc = MarketplaceService()
    pkgs = m_svc.list_packages()
    assert len(pkgs) >= 4

    # 1-Click Install
    install_res = m_svc.install_package("pkg.fintech.invoice_pro")
    assert install_res["status"] == "INSTALLED"

    t_engine = TemplateEngine()
    tpls = t_engine.list_templates()
    assert len(tpls) >= 4

    deploy_res = t_engine.deploy_template("tpl-healthcare-hospital")
    assert deploy_res["status"] == "DEPLOYED"
    assert deploy_res["organization_name"] == "Regional Hospital Health System"
