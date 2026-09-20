"""Industry Templates Interface."""

from __future__ import annotations

from app.platform.templates.template_engine import (
    OrganizationTemplate,
    TemplateEngine,
    global_template_engine,
)

__all__ = ["OrganizationTemplate", "TemplateEngine", "global_template_engine"]
