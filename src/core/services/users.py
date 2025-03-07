from core.enums import ALL_ROLES
from core.exceptions import (
    InvalidValue,
    InvalidValueAfterUpdate,
    NotEnoughMoney,
    RoleNotFound,
    UserNotFound,
)
from core.ids import UserId
from core.services.roles import RolesService
from database.repos.logs import LogsRepo
from database.repos.users import UsersRepo
from database.models.users import Medal


class UsersService:
    def __init__(
        self,
        users_repo: UsersRepo,
        logs_repo: LogsRepo,
        roles_service: RolesService,
    ) -> None:
        self.users_repo = users_repo
        self.logs_repo = logs_repo
        self.roles_service = roles_service

    async def update_balance(
        self,
        slave_id: UserId,
        master_id: UserId,
        amount: int,
    ) -> int:
        user = await self.users_repo.get_by_id(slave_id)
        if user is None:
            raise UserNotFound(slave_id)

        await self.roles_service.is_admin(master_id)

        if user.balance + amount < 0:
            raise InvalidValueAfterUpdate(
                f"Баланс станет отрицательным. Текущий: {user.balance}",
            )

        new_balance = user.balance + amount
        await self.users_repo.set_balance(slave_id, new_balance)

        await self.logs_repo.log_action(
            slave_id,
            f"Add money {amount=} by {master_id=}",
        )

        return new_balance

    async def update_balance_all_with_medal(
        self,
        master_id: UserId,
        base_amount: int,
    ) -> int:
        users = await self.users_repo.get_all()
        if not users:
            return 0

        await self.roles_service.is_admin(master_id)

        medal_multiplier = {
            Medal.NONE: 1.0,
            Medal.BRONZE: 1.5,
            Medal.SILVER: 1.7,
            Medal.GOLD: 2.0,
        }

        count = 0
        for user in users:
            amount = int(base_amount * medal_multiplier.get(user.medal, 1.0))
            if user.balance + amount >= 0:
                new_balance = user.balance + amount
                await self.users_repo.set_balance(user.id, new_balance)
                count += 1

                await self.logs_repo.log_action(
                    user.id,
                    f"Add money {amount=} considering medal {user.medal} by admin {master_id=}",
                )

        return count

    async def update_team_balance(
            self,
            slave_id: UserId,
            master_id: UserId,
            amount: int,
    ) -> int:
        user = await self.users_repo.get_by_id(slave_id)
        if user is None:
            raise UserNotFound(slave_id)

        await self.roles_service.is_admin(master_id)

        if user.team_balance + amount < 0:
            raise InvalidValueAfterUpdate(
                f"Баланс станет отрицательным. Текущий: {user.team_balance}",
            )

        new_balance = user.team_balance + amount
        await self.users_repo.set_team_balance(slave_id, new_balance)

        await self.logs_repo.log_action(
            slave_id,
            f"Add team money {amount=} by {master_id=}",
        )

        return new_balance

    async def update_team_balance_all(
            self,
            master_id: UserId,
            amount: int,
    ) -> int:
        await self.roles_service.is_admin(master_id)

        await self.users_repo.set_team_balance_all(amount)

        await self.logs_repo.log_action(
            master_id,
            f"Add team money all users {amount=} by {master_id=}",
        )

        return amount

    async def set_balance(
        self,
        slave_id: UserId,
        master_id: UserId,
        new_balance: int,
    ) -> int:
        if new_balance < 0:
            raise InvalidValue("Новый баланс не может быть отрицательным")

        user = await self.users_repo.get_by_id(slave_id)
        if user is None:
            raise UserNotFound(slave_id)

        await self.roles_service.is_admin(master_id)

        await self.users_repo.set_balance(slave_id, new_balance)

        await self.logs_repo.log_action(
            slave_id,
            f"Set money {new_balance=} by {master_id=}",
        )

        return new_balance

    async def transfer_funds(
        self,
        sender_id: UserId,
        receiver_id: UserId,
        amount: int,
    ) -> int:
        if amount <= 0:
            raise InvalidValue("Нельзя передать 0 или отрицательные Пятаки")

        sender = await self.users_repo.get_by_id(sender_id)
        if sender is None:
            raise UserNotFound(sender_id)

        if sender.balance < amount:
            raise NotEnoughMoney(sender.balance, amount)

        receiver = await self.users_repo.get_by_id(receiver_id)
        if receiver is None:
            raise UserNotFound(receiver_id)

        new_sender_balance = sender.balance - amount
        await self.users_repo.set_balance(sender_id, new_sender_balance)

        new_receiver_balance = receiver.balance + amount
        await self.users_repo.set_balance(receiver_id, new_receiver_balance)

        await self.logs_repo.log_action(
            sender_id,
            f"Transfer {amount=} to user {receiver_id=}",
        )
        await self.logs_repo.log_action(
            receiver_id,
            f"Receive {amount=} from user {sender_id=}",
        )

        return new_sender_balance

    async def change_role(
        self,
        slave_id: UserId,
        master_id: UserId,
        role: str | None,
    ) -> None:
        user = await self.users_repo.get_by_id(slave_id)
        if user is None:
            raise UserNotFound(slave_id)

        await self.roles_service.is_admin(master_id)

        if role not in ALL_ROLES:
            raise RoleNotFound(role)

        await self.users_repo.set_role(slave_id, role)

        await self.logs_repo.log_action(slave_id, f"New role {role=} by {master_id=}")

    async def update_medal(
            self,
            slave_id: UserId,
            master_id: UserId,
            medal: Medal) -> None:
        user = await self.users_repo.get_by_id(slave_id)

        if user is None:
            raise UserNotFound(slave_id)

        await self.roles_service.is_admin(master_id)

        await self.users_repo.set_medal(slave_id, medal)

        await self.logs_repo.log_action(
            slave_id,
            f"Update medal to {medal.name} by {master_id}"
        )
