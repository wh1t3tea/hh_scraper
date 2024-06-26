from sqlalchemy import Column, Integer, BigInteger, Text
from base import Base


class VacancyORM(Base):
    __tablename__ = "vacancies"

    vacancy_id = Column(BigInteger, primary_key=True)
    hh_id = Column(Integer, unique=True, nullable=False)
    name = Column(Text, default=None, nullable=False)
    area = Column(Text, default=None)
    area_id = Column(Integer, nullable=False)
    salary_from = Column(BigInteger, default=None)
    salary_to = Column(BigInteger, default=None)
    url = Column(Text, default=None, unique=True)
    requirement = Column(Text, default=None)
    responsibility = Column(Text, default=None)
    employment = Column(Text, default=None)
