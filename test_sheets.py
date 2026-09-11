import os

import gspread
from dotenv import load_dotenv


load_dotenv()

sheet_id = os.getenv("GOOGLE_SHEET_ID")

gc = gspread.service_account(filename="credentials.json")

spreadsheet = gc.open_by_key(sheet_id)
worksheet = spreadsheet.sheet1

worksheet.append_row(
    [
        "05.09.2026",
        "Тестовая услуга",
        "Арина",
        "+79999999999",
        "Тестовая заявка из Python",
        "@test",
        "123456789",
    ]
)

print("Строка успешно добавлена!")
