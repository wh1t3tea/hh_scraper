import asyncio
import aiohttp


async def parse_vacancies(name,
                          area=1,
                          page=0,
                          salary=100000,
                          employment="full",
                          experience="noExperience",
                          vacancy_search_order="publication_time"):

    params = {
        'text': f'NAME:{name}',
        'area': area,
        'page': page,
        'per_page': 100,
        'salary': salary,
        'employment': employment,
        'experience': experience,
        'vacancy_search_order': vacancy_search_order
    }

    params = {k: v for k, v in params.items() if v is not None}
    url = 'https://api.hh.ru/vacancies'

    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                return None

