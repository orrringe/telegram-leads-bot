from aiogram.fsm.state import State, StatesGroup


class ApplicationForm(StatesGroup):
    choosing_service = State()
    entering_custom_service = State()
    entering_name = State()
    entering_phone = State()
    entering_comment = State()
    confirming = State()
