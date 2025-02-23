from typing import Any

from aiogram.filters import Filter

from core.enums import RightsRole
from database.models import UserModel


class AiogramRoleAccess(Filter):
    def __init__(self, roles: list[RightsRole]) -> None:
        self.roles = roles

    async def __call__(
        self,
        _: Any,
        user: UserModel | None,
    ) -> bool:
        if user is None:
            return False
        return user.role in self.roles


class IsAdmin(AiogramRoleAccess):
    def __init__(self) -> None:
        super().__init__([RightsRole.ADMIN])


class IsOrganizer(AiogramRoleAccess):
    def __init__(self) -> None:
        super().__init__([RightsRole.ORGANIZER, RightsRole.ADMIN])


class IsCaptain(AiogramRoleAccess):
    def __init__(self) -> None:
        super().__init__([RightsRole.CAPTAIN])


class IsWithRole(AiogramRoleAccess):
    def __init__(self) -> None:
        super().__init__(RightsRole.values())
