from aiogram import F
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import (
    Back,
    Button,
    Multiselect,
    Next,
    Row,
    ScrollingGroup,
)
from aiogram_dialog.widgets.text import Const, Format, Multi

from bot.dialogs.buttons import GoToMenuButton

from .getters import get_purchases
from .on_actions import on_cart_item_selected, on_refund_cart_confirm
from .states import CartStates

cart_window = Window(
    Multi(
        Format("🧺 <b>Корзина</b>"),
        Format("📦 <b>Количество товаров:</b> {total_products} шт."),
        Format("🛒 <b>Cписок покупок:</b>\n{formated_info}"),
        sep="\n\n",
        when=F["total_purchases"],
    ),
    Const(
        "🧺 Корзина пустая",
        when=~F["total_purchases"],
    ),
    ScrollingGroup(
        Multiselect(
            checked_text=Format("🔘 {item[0][1]}: {item[1]}"),
            unchecked_text=Format("{item[0][1]}: {item[1]}"),
            id="select",
            item_id_getter=lambda p: p[0][0],
            items="products_to_quantity",
            type_factory=int,
            on_state_changed=on_cart_item_selected,
        ),
        height=10,
        width=1,
        hide_on_single_page=True,
        id="pager",
    ),
    Button(
        Const("♻️ Вернуть товары"),
        id="refund",
        on_click=Next(),
        when=F["dialog_data"]["selected"],
    ),
    GoToMenuButton(),
    getter=get_purchases,
    state=CartStates.view,
)

refund_cart_window = Window(
    Format("❓ Уверен, что хочешь вернуть выделенные позиции обратно в магазин?"),
    Row(
        Back(Const("⏪ Корзина")),
        Button(Const("✅ Подтвердить"), id="confirm", on_click=on_refund_cart_confirm),
    ),
    GoToMenuButton(),
    state=CartStates.refund,
)

cart_dialog = Dialog(
    cart_window,
    refund_cart_window,
)
