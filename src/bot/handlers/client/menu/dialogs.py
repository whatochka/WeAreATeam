from aiogram import F
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Group
from aiogram_dialog.widgets.text import Const, Format

from bot.dialogs.buttons import GoToAdminPanelButton, GoToTaskButton
from bot.dialogs.filters.roles import IsWithRole, IsOrganizer

from .getters import get_user_info
from .on_actions import (
    on_cart,
    on_help,
    on_shop,
    on_transfer_funds,
)
from .states import MenuStates

menu_dialog = Dialog(
    Window(
        Const("<b>Главное меню</b>\n"),
        Format("Твой номер: <code>{number}</code>"),
        Format("Команда: <b>{team_name}</b>"),
        Format("Баланс: {balance} <b>червонцев</b>\n"),
        Format("Ты - <u>{role}</u>", when=IsWithRole()),
        Group(
            Button(Const("🛍️ Магазин"), id="shop", on_click=on_shop),
            Button(Const("🧺 Корзина"), id="cart", on_click=on_cart),
            Button(
                Const("💸 Перевод"),
                id="transfer",
                on_click=on_transfer_funds,
                when=F["balance"] > 0,
            ),
            Button(Const("🆘 Помощь"), id="help", on_click=on_help),
            width=2,
        ),
        GoToAdminPanelButton(when=IsOrganizer()),
        getter=get_user_info,
        state=MenuStates.menu,
    ),
)
