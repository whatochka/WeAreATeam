from aiogram.types import Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from database.models import UserModel
from database.repos.users import UsersRepo
from ..menu.states import MenuStates


@inject
async def auth_number_password_handler(
    message: Message,
    _: MessageInput,
    dialog_manager: DialogManager,
    users_repo: FromDishka[UsersRepo],
) -> None:
    text = message.text.strip()
    if " " not in text:
        await message.delete()
        await message.answer("❌ Ошибка: номер или пароль указаны неверно.")
        return

    number, password = text.split(" ", 1)
    registered_user = await users_repo.get_pre_registered_user(number)

    if not registered_user or not UserModel.verify_password(password, registered_user.password_hash):
        await message.delete()
        await message.answer("❌ Ошибка: номер или пароль указаны неверно.")
        return

    existing_user = await users_repo.get_by_number(number)
    if existing_user:
        if existing_user.tg_id != message.from_user.id:
            await message.delete()
            await message.answer("❗ Этот пользователь уже авторизован с другого аккаунта.")
            return
        else:
            await users_repo.update_user_from_pre_registered(existing_user, registered_user, message.from_user.username)
            user = existing_user
    else:
        user = await users_repo.create_user_from_pre_registered(
            registered_user,
            message.from_user.id,
            message.from_user.username
        )

    dialog_manager.middleware_data["user"] = user

    await message.delete()
    await dialog_manager.start(state=MenuStates.menu, data={}, show_mode=ShowMode.DELETE_AND_SEND)
