from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from bot.handlers.admin.team_shop.view.states import ViewTeamProductsStates
from core.ids import ProductId
from database.repos.team_products import TeamProductsRepo


@inject
async def on_edit_price_input(
    message: Message,
    _: MessageInput,
    dialog_manager: DialogManager,
    products_repo: FromDishka[TeamProductsRepo],
) -> None:
    product_id: ProductId = dialog_manager.dialog_data["product_id"]
    price = int(message.text)
    await products_repo.update(product_id, price=price)
    await dialog_manager.start(ViewTeamProductsStates.one, data={"product_id": product_id})


@inject
async def on_edit_stock_input(
    message: Message,
    _: MessageInput,
    dialog_manager: DialogManager,
    products_repo: FromDishka[TeamProductsRepo],
) -> None:
    product_id: ProductId = dialog_manager.dialog_data["product_id"]
    stock = int(message.text)
    await products_repo.update(product_id, stock=stock)
    await dialog_manager.start(ViewTeamProductsStates.one, data={"product_id": product_id})
