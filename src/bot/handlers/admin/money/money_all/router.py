from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from dishka import FromDishka

from core.ids import UserId
from core.services.users import UsersService

router = Router(name=__file__)


@router.message(Command("money_all"))
async def admin_update_money(
    message: Message,
    command: CommandObject,
    users_service: FromDishka[UsersService],
) -> None:
    if command.args and len(command.args.split()) == 1:
        args = command.args.split()
        amount = int(args[0])
        user = await users_service.users_repo.get_user_by_tg_id(message.from_user.id)
        await users_service.update_balance_all(user.id, amount)
        await message.answer(f"Добавлено {amount} всем пользователям")
    else:
        await message.answer("Формат: /money_all <amount>", parse_mode=None)
