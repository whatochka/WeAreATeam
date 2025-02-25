from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandObject, Command
from core.services.users import UsersService

router = Router(name=__file__)


@router.message(Command("medal"))
async def set_medal(message: Message, command: CommandObject, users_service: UsersService):
    if not command.args:
        await message.answer(
            "⚠️ Введите индивидуальный номер и название медали (bronze, silver, gold).\nПример: /medal 101 bronze")
        return

    try:
        number, medal = command.args.split()
        await users_service.assign_medal(number, medal)
        await message.answer(f"✅ Медаль '{medal}' успешно выдана участнику с номером {number}.")
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")
