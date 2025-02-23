from aiogram.fsm.state import State, StatesGroup


class CreateTeamProductStates(StatesGroup):
    name = State()
    description = State()
    price = State()
    stock = State()
    confirm = State()
