from datetime import datetime, timedelta, UTC

from sqlalchemy import select, update, delete, Executable
from sqlalchemy.orm import selectinload

from src.db.errors import EntityDoesNotExistError
from src.models.devices import DeviceResponseModel
from src.db.repositories.repository import Repository
from src.db.tables import DeviceTable

class DevicesRepository(Repository):
    async def get(self, id_: int = 0) -> DeviceResponseModel: # type: ignore
        query = select(DeviceTable).where(DeviceTable.id == id)

        async with self.session_factory() as session:
            response = await session.execute(query)

            device_row = response.scalars().first()
            if device_row is None:
                raise EntityDoesNotExistError(f"Task with id:{id_} does not exist")

            return DeviceResponseModel.model_validate(device_row, from_attributes=True)
