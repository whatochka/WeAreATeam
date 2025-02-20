from aiogram import Router
from aiogram_dialog import DialogManager, ShowMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from dishka import FromDishka

from database.repos.users import UsersRepo
from .states import StartStates
from ..menu.states import MenuStates

router = Router(name="auth_router")


@router.message(CommandStart())
async def start_handler(message: Message, dialog_manager: DialogManager, users_repo: FromDishka[UsersRepo]) -> None:
    user = await users_repo.get_user_by_tg_id(message.from_user.id)

    if user and user.is_active:
        await dialog_manager.start(state=MenuStates.menu, show_mode=ShowMode.DELETE_AND_SEND)
    else:
        await dialog_manager.start(state=StartStates.number_password, show_mode=ShowMode.DELETE_AND_SEND)
