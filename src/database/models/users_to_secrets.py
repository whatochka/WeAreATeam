from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.core.ids import SecretId, UserId
from src.database.models._mixins import CreatedAtMixin
from src.database.models.base import BaseAlchemyModel


class UsersToSecretsModel(CreatedAtMixin, BaseAlchemyModel):
    __tablename__ = "users_to_secrets"

    user_id: Mapped[UserId] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
        index=True,
    )
    secret_id: Mapped[SecretId] = mapped_column(
        ForeignKey("secrets.id", ondelete="CASCADE"),
        primary_key=True,
        index=True,
    )
