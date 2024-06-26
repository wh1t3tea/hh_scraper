from fastapi import FastAPI
from hh_parser import parse_vacancies

app = FastAPI()


@app.get("/parse/")
async def parse(args: dict):
    data = await parse_vacancies(**args)
    return data
