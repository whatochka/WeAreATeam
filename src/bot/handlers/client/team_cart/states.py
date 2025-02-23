from aiogram.fsm.state import State, StatesGroup


class TeamCartStates(StatesGroup):
    view = State()
    refund = State()
