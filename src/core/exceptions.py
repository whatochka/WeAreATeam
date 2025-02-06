from core.enums import RightsRole
from core.ids import ProductId, SecretId, TaskId, UserId


class ServiceException(Exception):
    def __init__(self, message: str = "-") -> None:
        self.message = message

    def __str__(self) -> str:
        return self.message

    def __repr__(self) -> str:
        return f"{type(self).__name__}('{self}')"


class EntityAlreadyExists(ServiceException):
    pass


class SecretAlreadyExists(EntityAlreadyExists):
    def __init__(self, phrase: str) -> None:
        super().__init__(f'Секрет с фразой "{phrase}" уже существует')


class EntityNotFound(ServiceException):
    pass


class UserNotFound(EntityNotFound):
    def __init__(self, user_id: UserId) -> None:
        super().__init__(f"Пользователь с айди {user_id} не найден")


class SecretNotFound(EntityNotFound):
    def __init__(self, pharse: str) -> None:
        super().__init__(f'Секрет по фразе "{pharse}" не найден')


class ProductNotFound(EntityNotFound):
    def __init__(self, product_id: ProductId) -> None:
        super().__init__(f"Товар с айди {product_id} не найден")


class RoleNotFound(EntityNotFound):
    def __init__(self, role: str) -> None:
        super().__init__(f'Роль "{role}" не найдена')


class TaskNotFound(EntityNotFound):
    def __init__(self, task_id: TaskId) -> None:
        super().__init__(f'Задание с айди "{task_id}" не найдено')


class ActiveTaskNotFound(EntityNotFound):
    def __init__(self, user_id: UserId) -> None:
        super().__init__(f'Активное задание у юзера {user_id}" не найдено')


class NotEnoughStock(ServiceException):
    def __init__(self, current_stock: int, excepted_stock: int) -> None:
        super().__init__(
            "Недостаточное кол-во товара.\n"
            f"Текущее: {current_stock}, ожидаемое: {excepted_stock}",
        )


class NotEnoughMoney(ServiceException):
    def __init__(self, current_balance: int, excepted_balance: int) -> None:
        super().__init__(
            "Недостаточно Пятаков на балансе.\n"
            f"Текущее: {current_balance}, ожидаемое: {excepted_balance}",
        )


class InvalidValue(ServiceException):
    pass


class WrongTaskAnswer(InvalidValue):
    pass


class WrongQuestAnswer(InvalidValue):
    pass


class WrongCouponAnswer(InvalidValue):
    pass


class InvalidValueAfterUpdate(InvalidValue):
    pass


class NotEnoughRights(ServiceException):
    pass


class NotRightRole(NotEnoughRights):
    def __init__(self, user_id: UserId, role: RightsRole | None) -> None:
        super().__init__(f"Пользователь с айди {user_id} не является {role}")


class RewardAlreadyClaimed(ServiceException):
    pass


class SecretRewardAlreadyClaimed(RewardAlreadyClaimed):
    def __init__(self, user_id: UserId, secret_id: SecretId) -> None:
        super().__init__(
            f"Пользователь {user_id} уже забрал награду за секрет {secret_id}",
        )


class TaskRewardAlreadyClaimed(RewardAlreadyClaimed):
    def __init__(self, user_id: UserId, task_id: TaskId) -> None:
        super().__init__(
            f"Пользователь {user_id} уже забрал награду за квест {task_id}",
        )


class CouponAlreadyClaimed(RewardAlreadyClaimed):
    def __init__(self, user_id: UserId) -> None:
        super().__init__(f"Пользователь {user_id} уже активировал купон")


class NoFreeCoupons(ServiceException):
    def __init__(self) -> None:
        super().__init__("Купоны закончились.")


class ActivationLimitReached(ServiceException):
    pass
