from sqlalchemy import BigInteger, Boolean, Identity, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from core.ids import TgId, UserId
from database.models._mixins import CreatedAtMixin, UpdatedAtMixin
from database.models.base import BaseAlchemyModel
from passlib.context import CryptContext
from database.models.pre_registred_users import PreRegisteredUserModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserModel(CreatedAtMixin, UpdatedAtMixin, BaseAlchemyModel):
    __tablename__ = "users"

    id: Mapped[UserId] = mapped_column(
        Integer,
        Identity(start=1000),
        primary_key=True,
        autoincrement=True,
        index=True,
    )
    number: Mapped[str] = mapped_column(String(3), unique=True, nullable=True)
    tg_id: Mapped[TgId] = mapped_column(BigInteger, nullable=False, unique=True, index=True)
    tg_username: Mapped[str | None] = mapped_column(String(32), unique=True, nullable=True)
    name: Mapped[str] = mapped_column(String(64), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(16), nullable=True)
    team_number: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_captain: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    role: Mapped[str] = mapped_column(String(16), nullable=False, default="user")
    balance: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    qrcode_image_id: Mapped[str | None] = mapped_column(String(128), nullable=True, unique=True)

    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        return pwd_context.verify(password, password_hash)

    @classmethod
    def from_pre_registered_user(cls, registered_user: PreRegisteredUserModel, tg_id: int, tg_username: str | None) -> "UserModel":
        return cls(
            number=registered_user.number,
            tg_id=tg_id,
            tg_username=tg_username,
            name=registered_user.name,
            phone=registered_user.phone,
            team_number=registered_user.team_number,
            is_captain=registered_user.is_captain,
            role=registered_user.role if registered_user.role else "user",
            balance=0,
            is_active=True,
        )
