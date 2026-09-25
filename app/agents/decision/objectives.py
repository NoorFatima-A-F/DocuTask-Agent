"""
Strategic Objective Models.
"""

from pydantic import BaseModel


class StrategicObjective(BaseModel):
    objective_name: str
    target_metric: str
    model_config = {"frozen": True}
