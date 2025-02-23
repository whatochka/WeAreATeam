from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager

from bot.enums import SlashCommand
from bot.handlers.client.team_cart.states import TeamCartStates

router = Router(name=__file__)


@router.message(Command(SlashCommand.CART))
async def cart_handler(message: Message, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(state=TeamCartStates.view)
