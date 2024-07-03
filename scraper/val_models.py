from pydantic import BaseModel
from typing import Optional


class Vacancy(BaseModel):
    name: Optional[str] = None
    experience: Optional[str] = None
    salary: Optional[int] = None
    employment: Optional[str] = None
    page: Optional[int] = None
    only_with_salary: Optional[bool] = None
