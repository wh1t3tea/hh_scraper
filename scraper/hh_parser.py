import os

import aiohttp


async def parse_vacancies(data):
    params = {key: value for key, value in data.items()}
    params["per_page"] = 100

    if params["page"] is None:
        params["page"] = 0

    params = {k: v for k, v in params.items() if v is not None}
    url = os.environ["HH_ROUTE"]

    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                return None
