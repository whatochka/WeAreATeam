from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from dishka import FromDishka

from core.ids import UserId
from core.services.users import UsersService
from core.enums import Medal

router = Router(name=__file__)


@router.message(Command("medal"))
async def admin_update_medal(
    message: Message,
    command: CommandObject,
    user_id: UserId,
    users_service: FromDishka[UsersService],
) -> None:
    if command.args and len(command.args.split()) == 2:
        args = command.args.split()
        slave_id, medal_name = UserId(int(args[0])), str(args[1].upper())

        await users_service.update_medal(slave_id, user_id, Medal[medal_name])
        await message.answer(f"{medal_name} медаль получил пользователь {slave_id}")
    else:
        await message.answer("Формат: /medal <user_id> <medal>", parse_mode=None)
