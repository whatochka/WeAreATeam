from aiogram.fsm.state import State, StatesGroup


class ViewTeamProductsStates(StatesGroup):
    list = State()
    one = State()
    confirm = State()
