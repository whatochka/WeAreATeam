from core.exceptions import (
    InvalidValue,
    NotEnoughMoney,
    NotEnoughStock,
    ProductNotFound,
    UserNotFound,
)
from core.ids import ProductId, UserId
from core.services.roles import RolesService
from core.services.users import UsersService
from database.repos.logs import LogsRepo
from database.repos.products import ProductsRepo
from database.repos.purchases import PurchasesRepo
from database.repos.users import UsersRepo
from database.models.products import ProductModel
from database.models.users import UserModel
from dishka import FromDishka
from ..exceptions import NotEnoughMoney


class ProductsService:
    def __init__(
        self,
        products_repo: ProductsRepo,
        users_repo: UsersRepo,
        purchases_repo: PurchasesRepo,
        logs_repo: LogsRepo,
        roles_service: RolesService,
        users_service: FromDishka[UsersService]
    ) -> None:
        self.products_repo = products_repo
        self.users_repo = users_repo
        self.purchases_repo = purchases_repo
        self.logs_repo = logs_repo
        self.roles_service = roles_service
        self.users_service = users_service

    async def buy_product(
        self,
        user_id: UserId,
        product_id: ProductId,
        quantity: int,
    ) -> int:
        product = await self.products_repo.get_by_id(product_id)
        if product is None:
            raise ProductNotFound(product_id)

        if product.stock < quantity:
            raise NotEnoughStock(product.stock, quantity)

        user = await self.users_repo.get_by_id(user_id)
        if user is None:
            raise UserNotFound(user_id)

        total_price = product.price * quantity
        if user.balance < total_price:
            raise NotEnoughMoney(user.balance, total_price)

        await self.purchases_repo.create(user.id, product_id, quantity)

        new_balance = user.balance - total_price
        await self.users_repo.set_balance(user.id, new_balance)

        new_stock = product.stock - quantity
        await self.set_stock(product_id, new_stock)

        await self.logs_repo.log_action(
            user.id,
            f"Bought {product_id=} for {quantity=} units. {new_balance=} {new_stock=}",
        )

        return new_balance

    async def set_stock(self, product_id: ProductId, new_stock: int) -> int:
        if new_stock < 0:
            raise InvalidValue("Кол-во товара не может быть отрицательным")

        product = await self.products_repo.get_by_id(product_id)
        if product is None:
            raise ProductNotFound(product_id)

        return await self.products_repo.set_stock(product_id, new_stock)

    async def set_price(self, product_id: ProductId, new_price: int) -> int:
        if new_price <= 0:
            raise InvalidValue("Цена не может быть 0 или отрицательной")

        product = await self.products_repo.get_by_id(product_id)
        if product is None:
            raise ProductNotFound(product_id)

        return await self.products_repo.set_price(product_id, new_price)

    async def create(
        self,
        name: str,
        description: str,
        price: int,
        stock: int,
        master_id: UserId,
    ) -> ProductId:
        await self.roles_service.is_admin(master_id)

        product_id = await self.products_repo.create_product(
            name,
            description,
            price,
            stock,
        )

        await self.logs_repo.log_action(master_id, f"Create {product_id=}")

        return product_id

    async def delete(self, product_id: ProductId, master_id: UserId) -> None:
        await self.roles_service.is_admin(master_id)

        product = await self.products_repo.get_by_id(product_id)
        if product is None:
            raise ProductNotFound(product_id)

        await self.products_repo.delete(product_id)

        await self.logs_repo.log_action(master_id, f"Delete {product_id=}")

    async def refund(self, product_id: ProductId, quantity: int) -> int:
        if quantity <= 0:
            raise InvalidValue("Нельзя вернуть 0 или отрицательное число товаров")

        product = await self.products_repo.get_by_id(product_id)
        if product is None:
            raise ProductNotFound(product_id)

        new_stock = product.stock + quantity
        await self.set_stock(product_id, new_stock)

        refund_money = product.price * quantity
        return refund_money  # noqa: RET504

    async def purchase(self, user: UserModel, product: ProductModel, quantity: int) -> None:
        """Покупка товара с учетом скидки за медаль."""
        discount_percentage = self.users_service.get_discount(user)
        price_with_discount = product.price * (1 - discount_percentage / 100)  # 💰 Скидка на товар

        total_price = int(price_with_discount * quantity)

        if user.balance < total_price:
            raise NotEnoughMoney

        user.balance -= total_price
        await self.users_repo.update(user.id, user.name, user.role)
