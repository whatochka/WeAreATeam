from typing import Any

from sqlalchemy import delete, select, update

from core.ids import ProductId
from database.models.team_products import TeamProductModel
from database.repos.base import BaseAlchemyRepo


class TeamProductsRepo(BaseAlchemyRepo):
    async def create_product(
        self,
        name: str,
        description: str,
        price: int,
        stock: int,
    ) -> ProductId:
        product = TeamProductModel(
            name=name,
            description=description,
            price=price,
            stock=stock,
        )
        self.session.add(product)
        await self.session.flush()
        return product.id

    async def get_by_id(self, product_id: ProductId) -> TeamProductModel | None:
        query = select(TeamProductModel).where(TeamProductModel.id == product_id)
        return await self.session.scalar(query)

    async def get_available(self) -> list[TeamProductModel]:
        query = (
            select(TeamProductModel)
            .where(TeamProductModel.stock > 0)
            .order_by(TeamProductModel.price.asc(), TeamProductModel.name.asc())
        )
        return list(await self.session.scalars(query))

    async def get_all(self) -> list[TeamProductModel]:
        query = select(TeamProductModel).order_by(
            TeamProductModel.price.asc(),
            TeamProductModel.name.asc(),
        )
        return list(await self.session.scalars(query))

    async def set_stock(self, product_id: ProductId, new_stock: int) -> int:
        query = (
            update(TeamProductModel)
            .where(TeamProductModel.id == product_id)
            .values(stock=new_stock)
        )
        await self.session.execute(query)
        await self.session.flush()
        return new_stock

    async def set_price(self, product_id: ProductId, new_price: int) -> int:
        query = (
            update(TeamProductModel)
            .where(TeamProductModel.id == product_id)
            .values(price=new_price)
        )
        await self.session.execute(query)
        await self.session.flush()
        return new_price

    async def delete(self, product_id: ProductId) -> None:
        query = delete(TeamProductModel).where(TeamProductModel.id == product_id)
        await self.session.execute(query)
        await self.session.flush()

    async def set_qrcode_image_id(self, product_id: ProductId, image_id: str) -> None:
        query = (
            update(TeamProductModel)
            .where(TeamProductModel.id == product_id)
            .values(qrcode_image_id=image_id)
        )
        await self.session.execute(query)
        await self.session.flush()

    async def update(self, product_id: ProductId, **kwargs: Any) -> None:
        query = (
            update(TeamProductModel).where(TeamProductModel.id == product_id).values(**kwargs)
        )
        await self.session.execute(query)
        await self.session.flush()
