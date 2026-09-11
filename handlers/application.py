from html import escape
import asyncio
import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from google_sheets import add_application

from keyboards.application import (
    SERVICE_OPTIONS,
    confirmation_keyboard,
    phone_keyboard,
    services_keyboard,
)
from states.application import ApplicationForm

logger = logging.getLogger(__name__)
router = Router()


async def ask_for_service(message: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(ApplicationForm.choosing_service)
    await message.answer(
        "Выберите услугу:",
        reply_markup=services_keyboard(),
    )


@router.message(F.text == "Оставить заявку")
async def start_application(message: Message, state: FSMContext) -> None:
    await ask_for_service(message, state)


@router.message(ApplicationForm.choosing_service, F.text.in_(SERVICE_OPTIONS))
async def choose_service(message: Message, state: FSMContext) -> None:
    if message.text == "Другое":
        await state.set_state(ApplicationForm.entering_custom_service)
        await message.answer(
            "Напишите, какая услуга вам нужна:",
            reply_markup=ReplyKeyboardRemove(),
        )
        return

    await state.update_data(service=message.text)
    await state.set_state(ApplicationForm.entering_name)
    await message.answer(
        "Как вас зовут?",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(ApplicationForm.choosing_service)
async def invalid_service(message: Message) -> None:
    await message.answer(
        "Пожалуйста, выберите услугу с помощью кнопок ниже.",
        reply_markup=services_keyboard(),
    )


@router.message(ApplicationForm.entering_custom_service, F.text)
async def custom_service(message: Message, state: FSMContext) -> None:
    service = message.text.strip()
    if not service:
        await message.answer("Напишите, какая услуга вам нужна:")
        return

    await state.update_data(service=service)
    await state.set_state(ApplicationForm.entering_name)
    await message.answer("Как вас зовут?")


@router.message(ApplicationForm.entering_custom_service)
async def invalid_custom_service(message: Message) -> None:
    await message.answer("Пожалуйста, отправьте название услуги текстом.")


@router.message(ApplicationForm.entering_name, F.text)
async def save_name(message: Message, state: FSMContext) -> None:
    name = message.text.strip()
    if not name:
        await message.answer("Как вас зовут?")
        return

    await state.update_data(name=name)
    await state.set_state(ApplicationForm.entering_phone)
    await message.answer(
        "Оставьте номер телефона для связи.\n\n"
        "Можно нажать кнопку ниже или написать номер текстом.",
        reply_markup=phone_keyboard(),
    )


@router.message(ApplicationForm.entering_name)
async def invalid_name(message: Message) -> None:
    await message.answer("Пожалуйста, отправьте имя текстом.")


@router.message(ApplicationForm.entering_phone, F.contact)
async def save_phone_from_contact(message: Message, state: FSMContext) -> None:
    phone = message.contact.phone_number
    await state.update_data(phone=phone)
    await state.set_state(ApplicationForm.entering_comment)
    await message.answer(
        "Коротко расскажите о задаче.\n\n"
        "Например: квартира 70 м², нужна генеральная уборка в субботу.",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(ApplicationForm.entering_phone, F.text)
async def save_phone_from_text(message: Message, state: FSMContext) -> None:
    phone = message.text.strip()
    if not phone:
        await message.answer("Напишите номер телефона или отправьте его кнопкой ниже.")
        return

    await state.update_data(phone=phone)
    await state.set_state(ApplicationForm.entering_comment)
    await message.answer(
        "Коротко расскажите о задаче.\n\n"
        "Например: квартира 70 м², нужна генеральная уборка в субботу.",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(ApplicationForm.entering_phone)
async def invalid_phone(message: Message) -> None:
    await message.answer("Напишите номер телефона текстом или отправьте контакт кнопкой ниже.")


@router.message(ApplicationForm.entering_comment, F.text)
async def save_comment(message: Message, state: FSMContext) -> None:
    comment = message.text.strip()
    if not comment:
        await message.answer("Коротко расскажите о задаче.")
        return

    await state.update_data(comment=comment)
    data = await state.get_data()
    await state.set_state(ApplicationForm.confirming)

    await message.answer(
        "Проверьте заявку:\n\n"
        f"Услуга: {data['service']}\n"
        f"Имя: {data['name']}\n"
        f"Телефон: {data['phone']}\n"
        f"Комментарий: {data['comment']}",
        reply_markup=confirmation_keyboard(),
    )


@router.message(ApplicationForm.entering_comment)
async def invalid_comment(message: Message) -> None:
    await message.answer("Пожалуйста, отправьте комментарий текстом.")


@router.message(ApplicationForm.confirming, F.text == "🔄 Заполнить заново")
async def restart_application(message: Message, state: FSMContext) -> None:
    await ask_for_service(message, state)


@router.message(ApplicationForm.confirming, F.text == "✅ Отправить")
async def submit_application(message: Message, state: FSMContext, bot, config) -> None:
    data = await state.get_data()

    username = message.from_user.username if message.from_user else None
    telegram_label = f"@{username}" if username else "username не указан"
    telegram_id = message.from_user.id if message.from_user else "неизвестен"

    admin_text = (
        "<b>🆕 Новая заявка</b>\n\n"
        f"<b>Услуга:</b> {escape(str(data.get('service', '')))}\n"
        f"<b>Имя:</b> {escape(str(data.get('name', '')))}\n"
        f"<b>Телефон:</b> {escape(str(data.get('phone', '')))}\n"
        f"<b>Комментарий:</b> {escape(str(data.get('comment', '')))}\n\n"
        f"<b>Telegram:</b> {escape(telegram_label)}\n"
        f"<b>Telegram ID:</b> {telegram_id}"
    )

    try:
        await bot.send_message(
            config.admin_id,
            admin_text,
            parse_mode="HTML",
        )
    except Exception:
        await message.answer(
            "Не удалось отправить заявку администратору. Попробуйте ещё раз чуть позже.",
            reply_markup=confirmation_keyboard(),
        )
        return

    try:
        await asyncio.to_thread(
            add_application,
            data.get("service", ""),
            data.get("name", ""),
            data.get("phone", ""),
            data.get("comment", ""),
            username,
            telegram_id,
        )
    except Exception:
        logger.exception("Не удалось сохранить заявку в Google Sheets")

    await state.clear()

    await message.answer(
        "Спасибо! Заявка отправлена. Менеджер свяжется с вами.",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(ApplicationForm.confirming)
async def invalid_confirmation(message: Message) -> None:
    await message.answer(
        "Выберите действие с помощью кнопок ниже.",
        reply_markup=confirmation_keyboard(),
    )
