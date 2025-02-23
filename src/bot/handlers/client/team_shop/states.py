from aiogram.fsm.state import State, StatesGroup


class TeamShopStates(StatesGroup):
    list = State()
    one = State()
    final = State()
