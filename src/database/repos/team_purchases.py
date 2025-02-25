from dataclasses import dataclass

from sqlalchemy import delete, select

from core.ids import ProductId, UserId
from database.models import TeamProductModel, TeamPurchasesModel
from database.repos.base import BaseAlchemyRepo


@dataclass
class TeamPurchasesInfo:
    total_products: int
    total_purchases: int
    product_to_quantity: list[tuple[tuple[ProductId, str], int]]
    formated_info: str


class TeamPurchasesRepo(BaseAlchemyRepo):
    async def create(
            self,
            user_id: UserId,
            product_id: ProductId,
            quantity: int,
    ) -> TeamPurchasesModel:
        purchase = TeamPurchasesModel(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity,
        )
        self.session.add(purchase)
        await self.session.flush()
        return purchase

    async def get_all_user_purchases(
            self,
            user_id: UserId,
    ) -> list[tuple[TeamProductModel, TeamPurchasesModel]]:
        query = (
            select(TeamProductModel, TeamPurchasesModel)
            .join(TeamPurchasesModel, TeamPurchasesModel.product_id == TeamProductModel.id)
            .where(TeamPurchasesModel.user_id == user_id)
            .order_by(TeamProductModel.price.asc(), TeamProductModel.name.asc())
        )
        return list(await self.session.execute(query))

    async def get_user_purchases_by_product_id(
            self,
            user_id: UserId,
            product_id: ProductId,
    ) -> list[tuple[TeamProductModel, TeamPurchasesModel]]:
        query = (
            select(TeamProductModel, TeamPurchasesModel)
            .join(TeamPurchasesModel, TeamPurchasesModel.product_id == TeamProductModel.id)
            .where(TeamPurchasesModel.user_id == user_id, TeamProductModel.id == product_id)
            .order_by(TeamProductModel.price.asc(), TeamProductModel.name.asc())
        )
        return list(await self.session.execute(query))

    async def clear_purchases(
            self,
            user_id: UserId,
            product_ids: list[ProductId],
    ) -> None:
        query = delete(TeamPurchasesModel).where(
            TeamPurchasesModel.user_id == user_id,
            TeamPurchasesModel.product_id.in_(product_ids),
        )
        await self.session.execute(query)
        await self.session.flush()

    @staticmethod
    def format_purchases(
            purchases: list[tuple[TeamProductModel, TeamPurchasesModel]],
    ) -> TeamPurchasesInfo:
        total_products = len({i[0].id for i in purchases})
        total_purchases = sum(i[1].quantity for i in purchases)

        product_to_quantity: dict[tuple[ProductId, str], int] = {}
        for product, purchase in purchases:
            if (product.id, product.name) not in product_to_quantity:
                product_to_quantity[(product.id, product.name)] = 0
            product_to_quantity[(product.id, product.name)] += purchase.quantity

        sorted_product_to_quntity = sorted(
            product_to_quantity.items(),
            key=lambda x: x[0][0],
        )
        formated_purchases = "\n".join(
            f"<b>{product_name}</b>: {quantity}"
            for (product_id, product_name), quantity in sorted_product_to_quntity
        )

        return TeamPurchasesInfo(
            total_products,
            total_purchases,
            sorted_product_to_quntity,
            formated_purchases,
        )
