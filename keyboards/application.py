from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


SERVICE_OPTIONS = (
    "Генеральная уборка",
    "Поддерживающая уборка",
    "Уборка после ремонта",
    "Другое",
)


def start_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Оставить заявку")]],
        resize_keyboard=True,
    )


def services_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Генеральная уборка")],
            [KeyboardButton(text="Поддерживающая уборка")],
            [KeyboardButton(text="Уборка после ремонта")],
            [KeyboardButton(text="Другое")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def phone_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📱 Отправить номер", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def confirmation_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅ Отправить")],
            [KeyboardButton(text="🔄 Заполнить заново")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
