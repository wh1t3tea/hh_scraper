from pydantic import BaseModel
from typing import Optional


class Vacancy(BaseModel):
    vacancy_id: Optional[int] = None
    hh_id: Optional[int] = None
    name: Optional[str] = None
    text: Optional[str] = None
    area: Optional[str] = None
    url: Optional[str] = None
    requirement: Optional[str] = None
    responsibility: Optional[str] = None
    employment: Optional[str] = None
    salary_from: Optional[int] = None
    salary_to: Optional[int] = None
    area_id: Optional[int] = None
