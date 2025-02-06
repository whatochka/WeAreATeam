from sqlalchemy.ext.asyncio import AsyncSession


class BaseAlchemyRepo:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
