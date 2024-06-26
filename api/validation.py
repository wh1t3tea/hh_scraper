from dataclasses import field, dataclass
from typing import Optional


@dataclass
class Vacancy:
    hh_id: Optional[int] = field(default=None)
    name: Optional[str] = field(default=None)
    area_id: Optional[int] = field(default=None)
    vacancy_id: Optional[int] = field(default=None)
    area: Optional[str] = field(default=None)
    salary_from: Optional[int] = field(default=None)
    salary_to: Optional[int] = field(default=None)
    url: Optional[str] = field(default=None)
    requirement: Optional[str] = field(default=None)
    responsibility: Optional[str] = field(default=None)
    employment: Optional[str] = field(default=None)
