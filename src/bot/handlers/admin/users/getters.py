from typing import Any

from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from bot.translate import translate_role
from core.ids import UserId, Number
from database.repos.users import UsersRepo


@inject
async def get_view_user_info(
    dialog_manager: DialogManager,
    users_repo: FromDishka[UsersRepo],
    **__: Any,
) -> dict[str, Any]:
    view_user_id: UserId = dialog_manager.dialog_data["view_user_id"]
    user = await users_repo.get_by_id(view_user_id)
    role = translate_role(user.role, "Пользователь")
    return {
        "view_user": user,
        "role": role,
    }
