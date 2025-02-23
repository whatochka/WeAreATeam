from aiogram.fsm.state import State, StatesGroup


class EditTeamProductStates(StatesGroup):
    price = State()
    stock = State()
