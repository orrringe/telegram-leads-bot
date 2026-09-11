from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.application import start_keyboard


router = Router()


@router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        "Привет! 👋\n"
        "Здесь можно оставить заявку на наши услуги.",
        reply_markup=start_keyboard(),
    )


@router.message(Command("cancel"))
async def command_cancel(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        "Заполнение заявки отменено.",
        reply_markup=ReplyKeyboardRemove(),
    )
