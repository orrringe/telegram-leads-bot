import os
from datetime import datetime
from pathlib import Path

import gspread
from dotenv import load_dotenv


load_dotenv()

SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
CREDENTIALS_FILE = Path(__file__).with_name("credentials.json")


def add_application(service, name, phone, comment, username, telegram_id):
    gc = gspread.service_account(filename=str(CREDENTIALS_FILE))
    worksheet = gc.open_by_key(SHEET_ID).sheet1

    telegram = f"@{username}" if username else "username не указан"

    worksheet.append_row(
        [
            datetime.now().strftime("%d.%m.%Y %H:%M"),
            service,
            name,
            phone,
            comment,
            telegram,
            telegram_id,
        ],
        value_input_option="USER_ENTERED",
    )
