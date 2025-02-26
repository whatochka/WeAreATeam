from aiogram import F
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Group
from aiogram_dialog.widgets.text import Const, Format

from bot.dialogs.buttons import GoToAdminPanelButton, GoToTaskButton
from bot.dialogs.filters.roles import IsWithRole, IsOrganizer, IsCaptain
from database.models.users import Medal

from .getters import get_user_info
from .on_actions import (
    on_cart,
    on_help,
    on_shop,
    on_transfer_funds,
    on_team_shop,
    on_team_cart,
)
from .states import MenuStates

menu_dialog = Dialog(
    Window(
        Const("🏠 <b>Главное меню</b>\n"),
        Format("🔢 <b>Твой номер:</b> <code>{number}</code>"),
        Format("👥 <b>Команда:</b> <b>{team_name}</b>"),
        Format("💰 <b>Баланс:</b> {balance} <b>червонцев</b>\n"),
        Format("🏅 <b>Медаль:</b> {medal}\n", when=F["medal"] != Medal.NONE),
        Format("💸 <b>Отрядный баланс:</b> {team_balance} <b>червонцев</b>\n", when=IsWithRole()),
        Format("🧩 <b>Твой статус:</b> <u>{role}</u>", when=IsWithRole()),

        Group(
            Button(Const("🛍️ Магазин"), id="shop", on_click=on_shop),
            Button(Const("🙌 Отрядный магазин"), id="team_shop", on_click=on_team_shop, when=IsWithRole()),
            Button(Const("🧺 Корзина"), id="cart", on_click=on_cart),
            Button(Const("📦 Отрядная корзина"), id="team_cart", on_click=on_team_cart, when=IsWithRole()),
            # Button(
            #     Const("💸 Перевод"),
            #     id="transfer",
            #     on_click=on_transfer_funds,
            #     when=F["balance"] > 0,
            # ),
            # Button(Const("🆘 Помощь"), id="help", on_click=on_help),
            width=2,
        ),
        GoToAdminPanelButton(when=IsOrganizer()),
        getter=get_user_info,
        state=MenuStates.menu,
    ),
)
