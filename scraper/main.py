from typing import Optional

from fastapi import FastAPI, Query

from hh_parser import parse_vacancies

app = FastAPI()


@app.get("/parse/")
async def parse(name: Optional[str] = Query(None),
                salary: Optional[int] = Query(None),
                employment: Optional[str] = Query(None),
                experience: Optional[str] = Query(None),
                only_with_salary: Optional[str] = Query(None),
                page: Optional[int] = Query(None),
                area: Optional[int] = Query(None)):
    vac_dict = {
        "text": name,
        "salary": salary,
        "employment": employment,
        "experience": experience,
        "only_with_salary": only_with_salary,
        "page": page,
        "area": area
    }

    data = await parse_vacancies(vac_dict)

    return data
