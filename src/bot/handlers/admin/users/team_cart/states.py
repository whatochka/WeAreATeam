from aiogram.fsm.state import State, StatesGroup


class TeamCartUserStates(StatesGroup):
    cart = State()
    clear = State()
    confirm = State()
