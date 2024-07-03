import os

import gspread
from oauth2client.service_account import ServiceAccountCredentials


def authorize():
    json_token = os.environ["GOOGLE_TOKEN"]
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_token, scope)
    client = gspread.authorize(credentials)
    return client
