"""
Configurable Financial ROI calculation engine.
"""

from typing import Dict, Any
from app.business_value_verification.domain.models import ROIAnalysisResult


class ROIAnalyzer:
    """Calculates gross savings, net annual benefits, payback periods, and ROI multiples under configurable assumptions."""

    @staticmethod
    def calculate_roi(
        monthly_docs: int = 10000,
        employee_hourly_rate: float = 28.0,
        baseline_mins_per_doc: float = 16.0,
        ai_cost_per_doc: float = 0.0080,
        annual_platform_investment: float = 24000.0,
    ) -> ROIAnalysisResult:
        # Baseline labor cost per document = (mins / 60) * hourly rate
        baseline_cost_per_doc = (baseline_mins_per_doc / 60.0) * employee_hourly_rate
        baseline_monthly = monthly_docs * baseline_cost_per_doc

        # AI operating cost per month
        ai_monthly = (monthly_docs * ai_cost_per_doc) + (annual_platform_investment / 12.0)

        monthly_savings = max(0.0, baseline_monthly - ai_monthly)
        annual_savings = monthly_savings * 12.0

        # ROI % = (Net Annual Savings / Annual Investment) * 100
        roi_pct = (annual_savings / max(1.0, annual_platform_investment)) * 100.0
        roi_multiple = baseline_monthly / max(0.01, ai_monthly)

        # Payback period in months = Investment / Monthly Net Savings
        payback_months = (annual_platform_investment / monthly_savings) if monthly_savings > 0 else 999.0

        return ROIAnalysisResult(
            monthly_document_volume=monthly_docs,
            employee_hourly_rate=employee_hourly_rate,
            baseline_monthly_cost=baseline_monthly,
            ai_monthly_cost=ai_monthly,
            monthly_net_savings=monthly_savings,
            annual_net_savings=annual_savings,
            annual_platform_investment=annual_platform_investment,
            net_annual_roi_pct=roi_pct,
            roi_multiple=roi_multiple,
            payback_period_months=payback_months,
        )
