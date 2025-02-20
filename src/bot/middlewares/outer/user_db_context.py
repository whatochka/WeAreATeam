from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.dispatcher.middlewares.user_context import EVENT_FROM_USER_KEY
from aiogram.types import TelegramObject, User
from dishka import AsyncContainer

from database.repos.users import UsersRepo


class UserDbContextMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: dict[str, Any],
    ) -> Any:
        from_user: User | None = data.get(EVENT_FROM_USER_KEY)
        if from_user is not None:
            container: AsyncContainer = data["dishka_container"]
            users_repo = await container.get(UsersRepo)

            db_user = await users_repo.get_user_by_tg_id(from_user.id)
            if db_user and db_user.is_active:
                data.update({"user": db_user, "user_id": db_user.id})
            else:
                data.update({"user": None, "user_id": None})

        return await handler(event, data)
