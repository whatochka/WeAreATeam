from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from database.models.base import BaseAlchemyModel
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PreRegisteredUserModel(BaseAlchemyModel):
    __tablename__ = "pre_registered_users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    number: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    tg_username: Mapped[str | None] = mapped_column(String(64), unique=True, nullable=True)
    phone: Mapped[str | None] = mapped_column(String(64), nullable=True)
    team_name: Mapped[str | None] = mapped_column(String(64), nullable=True)
    is_captain: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    role: Mapped[str] = mapped_column(String(64), nullable=False)

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        return pwd_context.verify(password, password_hash)
