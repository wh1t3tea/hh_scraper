from typing import List
from typing import Optional

from fastapi import FastAPI, Depends, HTTPException, status, Query
from sqlalchemy import select, and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from base import Base
from models import VacancyORM
from session import engine
from session import get_db
from val_models import Vacancy

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.post("/vacancies/")
async def create_vacancy(data: Vacancy,
                         db: AsyncSession = Depends(get_db)):
    vacancy_model = VacancyORM(**data.model_dump(exclude_none=True))

    try:
        db.add(vacancy_model)
        await db.flush()
        await db.commit()
        return {"message": "Vacancy created successfully"}

    except IntegrityError as e:
        if "vacancies_hh_id_key" in str(e):
            await db.rollback()
            existing_vacancy = await db.scalar(
                select(VacancyORM).where(VacancyORM.hh_id == data.hh_id)
            )

            if existing_vacancy:
                for key, value in data.model_dump().items():
                    if key != "vacancy_id":
                        setattr(existing_vacancy, key, value)

                await db.commit()
                return {"message": "Vacancy updated successfully"}
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.get("/vacancies/", response_model=List[Vacancy])
async def read_vacancies(vacancy_id: Optional[int] = Query(None),
                         hh_id: Optional[int] = Query(None),
                         name: Optional[str] = Query(None),
                         area: Optional[str] = Query(None),
                         url: Optional[str] = Query(None),
                         requirement: Optional[str] = Query(None),
                         responsibility: Optional[str] = Query(None),
                         employment: Optional[str] = Query(None),
                         salary_from: Optional[int] = Query(None),
                         salary_to: Optional[int] = Query(None),
                         text: Optional[str] = Query(None),
                         db: AsyncSession = Depends(get_db)):
    query = select(VacancyORM)

    conditions = []
    if vacancy_id is not None:
        conditions.append(VacancyORM.vacancy_id == vacancy_id)
    if hh_id is not None:
        conditions.append(VacancyORM.hh_id == hh_id)
    if name is not None:
        conditions.append(VacancyORM.name.ilike(f"%{name}%"))
    if area is not None:
        conditions.append(VacancyORM.area.ilike(f"%{area}%"))
    if url is not None:
        conditions.append(VacancyORM.url.ilike(f"%{url}%"))
    if requirement is not None:
        conditions.append(VacancyORM.requirement.ilike(f"%{requirement}%"))
    if responsibility is not None:
        conditions.append(VacancyORM.responsibility.ilike(f"%{responsibility}%"))
    if employment is not None:
        conditions.append(VacancyORM.employment.ilike(f"%{employment}%"))
    if salary_from is not None:
        conditions.append(VacancyORM.salary_from >= salary_from)
    if salary_to is not None:
        conditions.append(VacancyORM.salary_to <= salary_to)
    if text is not None:
        conditions.append(VacancyORM.text.ilike(f"%{text}%"))

    if conditions:
        query = query.where(and_(*conditions))

    results = await db.execute(query)
    vacancies = results.scalars().all()

    return vacancies
