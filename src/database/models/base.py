import datetime
from typing import Any

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm.exc import DetachedInstanceError


def utc_now() -> datetime.datetime:
    return datetime.datetime.now(tz=datetime.UTC)


class BaseAlchemyModel(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        },
    )

    def __repr__(self) -> str:
        """Вывод информации о моделе в человекочитаемом виде."""
        return self._repr(
            **{
                c.name: getattr(self, c.name)
                for c in self.__table__.columns  # type: ignore
            },
        )

    def _repr(self, **fields: Any) -> str:
        """
        Помощник __repr__.

        Взят с https://stackoverflow.com/a/55749579
        """
        field_strings = []
        at_least_one_attached_attribute = False

        for key, field in fields.items():
            try:
                field_strings.append(f"{key}={field!r}")
            except DetachedInstanceError:
                field_strings.append(f"{key}=DetachedInstanceError")
            else:
                at_least_one_attached_attribute = True

        if at_least_one_attached_attribute:
            return f"<{self.__class__.__name__}({', '.join(field_strings)})>"
        return f"<{self.__class__.__name__} {id(self)}>"
