from typing import Optional

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import select, func, and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from session import get_db

from session import engine
from models import VacancyORM
from validation import Vacancy
from base import Base

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.post("/vacancies/")
async def create_vacancy(data: dict, db: AsyncSession = Depends(get_db)):
    data_class = Vacancy(**data)

    vacancy_model = VacancyORM(
        hh_id=data_class.hh_id,
        name=data_class.name,
        area=data_class.area,
        area_id=data_class.area_id,
        salary_from=data_class.salary_from,
        salary_to=data_class.salary_to,
        url=data_class.url,
        requirement=data_class.requirement,
        responsibility=data_class.responsibility,
        employment=data_class.employment
    )

    try:
        db.add(vacancy_model)
        await db.flush()
        await db.commit()
        return {"message": "Vacancy created successfully"}

    except IntegrityError as e:
        if "vacancies_hh_id_key" in str(e):
            await db.rollback()
            existing_vacancy = await db.scalar(
                select(VacancyORM).where(VacancyORM.hh_id == data_class.hh_id)
            )

            if existing_vacancy:
                for key, value in data.items():
                    setattr(existing_vacancy, key, value)

                await db.commit()
                return {"message": "Vacancy updated successfully"}
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.get("/vacancies/")
async def read_vacancies(data: dict, db: AsyncSession = Depends(get_db)):
    data = Vacancy(**data)

    query = select(VacancyORM)

    conditions = []
    if data.vacancy_id is not None:
        conditions.append(VacancyORM.vacancy_id == data.vacancy_id)

    if data.hh_id is not None:
        conditions.append(VacancyORM.hh_id == data.hh_id)

    if data.name is not None:
        conditions.append(VacancyORM.name.ilike(f"%{data.name}%"))

    if data.area is not None:
        conditions.append(VacancyORM.area.ilike(f"%{data.area}%"))

    if data.area_id is not None:
        conditions.append(VacancyORM.area_id == data.area_id)

    if data.salary_from is not None:
        conditions.append(VacancyORM.salary_from >= data.salary_from)

    if data.salary_to is not None:
        conditions.append(VacancyORM.salary_to <= data.salary_to)

    if data.url is not None:
        conditions.append(VacancyORM.url.ilike(f"%{data.url}%"))

    if data.requirement is not None:
        conditions.append(VacancyORM.requirement.ilike(f"%{data.requirement}%"))

    if data.responsibility is not None:
        conditions.append(VacancyORM.responsibility.ilike(f"%{data.responsibility}%"))

    if data.employment is not None:
        conditions.append(VacancyORM.employment.ilike(f"%{data.employment}%"))

    if conditions:
        query = query.where(and_(*conditions))

    results = await db.execute(query)
    vacancies = results.scalars().all()

    if vacancies:
        return vacancies
