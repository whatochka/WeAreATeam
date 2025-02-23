from aiogram import F
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Back, Button, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Const, Format

from bot.dialogs.buttons import EmptyButton, GoToMenuButton
from bot.dialogs.on_actions import on_go_to_products, on_start_update_dialog_data

from .getters import get_available_products, get_can_buy, get_one_product
from .on_actions import on_buy_product, on_product_selected
from .states import TeamShopStates


view_available_products_window = Window(
    Const("🙌 Список командных товаров\n"),
    Format(
        "В наличии <b>{products_len}</b> наименований "
        "в количестве <b>{total_stock}</b> штук",
        when=F["total_stock"],
    ),
    Const("Товаров в наличии нет", when=~F["total_stock"]),
    Format("Баланс: {middleware_data[user].balance} червонцев\n", when=F["total_stock"]),
    ScrollingGroup(
        Select(
            Format("{item.name} — {item.price} червонцев"),
            id="products_select",
            item_id_getter=lambda item: item.id,
            items="products",
            type_factory=int,
            on_click=on_product_selected,
        ),
        width=1,
        height=10,
        hide_on_single_page=True,
        id="products_group",
    ),
    EmptyButton(when=F["products"]),
    GoToMenuButton(),
    state=TeamShopStates.list,
    getter=get_available_products,
)

view_one_product_window = Window(
    Format("<b>{product.name}</b>\n"),
    Format("Цена: {product.price} червонцев"),
    Format("В наличии {product.stock} шт.\n"),
    Format("{product.description}"),
    Button(Const("💵 Купить"), id="buy", on_click=on_buy_product, when=F["can_buy"]),
    Back(Const("⏪ Все товары")),
    getter=[get_one_product, get_can_buy],
    state=TeamShopStates.one,
)

final_window = Window(
    Format("{dialog_data[final_message]}"),
    Button(Const("🛍️ Все товары"), id="to_products", on_click=on_go_to_products),
    GoToMenuButton(),
    state=TeamShopStates.final,
)

team_shop_dialog = Dialog(
    view_available_products_window,
    view_one_product_window,
    final_window,
    on_start=on_start_update_dialog_data,
)
