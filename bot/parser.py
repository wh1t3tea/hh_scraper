import os

import aiohttp


class ParserOutHandler:
    def __init__(self,
                 data,
                 n_vacancies=20):
        self.data = data["items"] if data.get("items") else data
        self.n_vacancies = n_vacancies
        self.outp_values = [
            "name",
            "salary_from",
            "salary_to",
            "alternate_url"
        ]

    async def save_to_db(self):
        for vac in self.data:
            vac_dict = {}

            vac_dict["hh_id"] = vac["id"]
            vac_dict["name"] = vac["name"]
            vac_dict["area"] = vac["area"]["name"]
            vac_dict["url"] = vac["alternate_url"]
            vac_dict["requirement"] = vac["snippet"]["requirement"]
            vac_dict["responsibility"] = vac["snippet"]["responsibility"]
            vac_dict["employment"] = vac["employment"]["id"]
            vac_dict["area_id"] = vac["area"]["id"]
            vac_dict["salary_from"] = vac["salary"]["from"]
            vac_dict["salary_to"] = vac["salary"]["to"]
            vac_dict["text"] = vac["text"]

            async with aiohttp.ClientSession() as session:
                async with session.post(url=os.environ["API_ROUTE"], json=vac_dict) as response:
                    pass

    async def get_vacancies_to_show(self):
        vacancies = self.data[:min(self.n_vacancies, len(self.data))]

        vac_to_show = []

        for vac in vacancies:
            vac_dict = {}

            vac_dict["name"] = vac["name"]
            vac_dict["url"] = vac["alternate_url"]
            vac_dict["area"] = vac["area"]["name"]
            vac_dict["salary_from"] = vac["salary"]["from"]
            vac_dict["salary_to"] = vac["salary"]["to"]

            vac_to_show.append(vac_dict)

        return vac_to_show
