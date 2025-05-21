from pydantic import BaseModel
from enum import Enum
from typing import Optional

class TeamCreate(BaseModel):
    name: str
    password: str
    email: Optional[str] = None

class SolutionCreate(BaseModel):
    team_id: str
    task_id: str
    solution: dict

class SolutionStatus(str, Enum):
    ACCEPTED = "зачтено"
    SUBMITTED = "отправлено"
    REJECTED = "отклонено"