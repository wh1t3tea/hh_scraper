import os

import aiohttp
from aiogram.types import Message


def get_area_id(message: Message, areas_info: dict):
    target_city = message.text.lower().strip()
    areas_info = areas_info["areas"]

    for region in areas_info:
        if region["name"].lower() == target_city:
            return region["id"]

        elif len(region["areas"]) > 0:
            for city in region["areas"]:
                if city["name"].lower() == target_city:
                    return region["id"]
    return None


def form_answer(vacancies: list[dict]):
    message_parts = []

    for vac in vacancies:
        if vac["salary_from"] is None and vac["salary_to"] is None:
            salary_string = "Salary not specified"
        else:
            if vac["salary_from"] is None:
                vac["salary_from"] = 0
            salary_string = f'Salary: {vac["salary_from"]}'
            if vac["salary_to"]:
                salary_string += F' - {vac["salary_to"]}'
            salary_string += '₽\n'
        part = (
                f'<a href="{vac["url"]}">{vac["name"]}</a>\n'
                + salary_string +
                f'Area: {vac["area"]}'
        )

        message_parts.append(part)

    return message_parts


async def create_sheet(data: list[dict], table_name: str):
    connector = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        url = os.environ["SHEETS_ROUTE"]
        async with session.post(url, json={"data": data, "sheet_name": table_name}) as response:
            url = await response.json()
    return url["url"]
