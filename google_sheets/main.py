from fastapi import FastAPI

from authorization import authorize
from models import DataModel

app = FastAPI()


@app.post("/create")
async def create_sheet(sheet_data: dict):
    data = DataModel(data=sheet_data["data"])
    sheet_name = sheet_data["sheet_name"]
    client = authorize()
    sheet = client.create(sheet_name)
    worksheet = sheet.get_worksheet(0)
    headers = data.data[0].keys()
    worksheet.append_row(list(headers))
    for item in data.data:
        row = [item[key] for key in headers]
        worksheet.append_row(row)
    sheet.share(None, perm_type='anyone', role='reader')
    url = sheet.url
    return {"url": url}
