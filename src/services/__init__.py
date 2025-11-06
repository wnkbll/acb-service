from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class Service:
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self.session_factory: async_sessionmaker[AsyncSession] = session_factory
