from pydantic import BaseModel
from typing import List


class MAP(BaseModel):
    task_id: str
    target_department: str
    action_required: str
    audit_metric: str
    required_threshold: str
    deadline: str


class PlannerOutput(BaseModel):
    document_id: str
    measurable_action_points: List[MAP]