"""Source: https://github.com/wakaree/simple_echo_bot."""

from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message
from cachetools import TTLCache


class ThrottlingMiddleware(BaseMiddleware):
    RATE_LIMIT = 0.5

    def __init__(self, rate_limit: float = RATE_LIMIT) -> None:
        self.cache = TTLCache(maxsize=10_000, ttl=rate_limit)

    async def __call__(
        self,
        handler: Callable[[Message | CallbackQuery, dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: dict[str, Any],
    ) -> Any:
        if (from_user := data.get("event_from_user")) is not None:
            if from_user.id in self.cache:
                return None

            self.cache[from_user.id] = None

        return await handler(event, data)
