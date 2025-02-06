import asyncio
import contextlib
import logging
import sys

from dishka.integrations.aiogram import setup_dishka
from bot.config import get_bot_config
from bot.factories import create_bot, create_dispatcher
from bot.handlers import include_routers
from bot.middlewares import setup_middlewares
from di.container import make_container


async def main() -> None:
    bot_config = get_bot_config()

    bot = create_bot(bot_config)
    dp = create_dispatcher()

    container = make_container()
    setup_dishka(container=container, router=dp, auto_inject=True)
    dp.shutdown.register(container.close)

    setup_middlewares(bot, dp)
    include_routers(dp)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(
        bot,
        allowed_updates=dp.resolve_used_update_types(),
        bot_config=bot_config,
        owner_id=bot_config.owner_id,
    )


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
        format="%(asctime)s %(levelname)-8s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    if sys.platform == "win32":
        from asyncio import WindowsSelectorEventLoopPolicy

        asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())
    with contextlib.suppress(KeyboardInterrupt, SystemExit):
        asyncio.run(main())
