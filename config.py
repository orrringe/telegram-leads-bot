import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Config:
    bot_token: str
    admin_id: int


def load_config() -> Config:
    bot_token = os.getenv("BOT_TOKEN")
    admin_id_raw = os.getenv("ADMIN_ID")

    if not bot_token:
        raise RuntimeError("BOT_TOKEN is not set in .env")

    if not admin_id_raw:
        raise RuntimeError("ADMIN_ID is not set in .env")

    try:
        admin_id = int(admin_id_raw)
    except ValueError as exc:
        raise RuntimeError("ADMIN_ID must be an integer") from exc

    return Config(bot_token=bot_token, admin_id=admin_id)
