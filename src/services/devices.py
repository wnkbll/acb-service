from fastapi import HTTPException, status
from sqlalchemy import delete, insert, select, update

from src.db.tables import BatteryTable, DeviceTable
from src.models import SuccessMessage
from src.models.batteries import BatteryResponseModel
from src.models.devices import DeviceCreateModel, DeviceResponseModel, DeviceUpdateModel
from src.services import Service


class DevicesService(Service):
    async def is_name_available(self, name: str) -> bool:
        query = select(DeviceTable).where(DeviceTable.name == name)

        async with self.session_factory() as session:
            response = await session.execute(query)
            row = response.scalar_one_or_none()

            return row is None

    async def set_batteries_to_device(self, device_id: int, batteries_id: list[int]):
        query = (
            update(BatteryTable)
            .where(BatteryTable.id.in_(batteries_id))
            .values(device_id=device_id)
        )

        async with self.session_factory() as session:
            await session.execute(query)
            await session.commit()

    async def get(self, id_: int) -> DeviceResponseModel:
        query = select(DeviceTable).where(DeviceTable.id == id_)

        async with self.session_factory() as session:
            response = await session.execute(query)
            row = response.scalar_one_or_none()

            if row is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Запись с таким id не найдена",
                )

            device = DeviceResponseModel.model_validate(row, from_attributes=True)
            device.batteries = [
                BatteryResponseModel.model_validate(battery, from_attributes=True)
                for battery in row.batteries
            ]

            return device

    async def get_all(self) -> list[DeviceResponseModel]:
        query = select(DeviceTable)

        async with self.session_factory() as session:
            response = await session.execute(query)
            rows = response.scalars().all()

            result = []
            for device_row in rows:
                device = DeviceResponseModel.model_validate(
                    device_row, from_attributes=True
                )
                device.batteries = [
                    BatteryResponseModel.model_validate(battery, from_attributes=True)
                    for battery in device_row.batteries
                ]
                result.append(device)
            return result

    async def create(self, device_to_create: DeviceCreateModel) -> SuccessMessage:
        if not await self.is_name_available(device_to_create.name):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Запись с таким name уже существует",
            )

        query = (
            insert(DeviceTable)
            .values(**device_to_create.model_dump(exclude={"batteries"}))
            .returning(DeviceTable)
        )

        async with self.session_factory() as session:
            response = await session.execute(query)
            await session.commit()
            row = response.scalar_one_or_none()

            if row is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Произошла непредвиденная ошибка",
                )

        return SuccessMessage(message="Запись успешно создана")

    async def update(
        self, id_: int, device_to_update: DeviceUpdateModel
    ) -> SuccessMessage:
        if device_to_update.name is not None:
            if not await self.is_name_available(device_to_update.name):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Запись с таким name уже существует",
                )

        query = (
            update(DeviceTable)
            .where(DeviceTable.id == id_)
            .values(
                **device_to_update.model_dump(exclude={"batteries"}, exclude_none=True)
            )
        )

        async with self.session_factory() as session:
            response = await session.execute(query)
            await session.commit()
            row = response.scalar_one_or_none()

            if row is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Произошла непредвиденная ошибка",
                )

        return SuccessMessage(message="Запись успешно обновлена")

    async def delete(self, id_: int) -> SuccessMessage:
        query = delete(DeviceTable).where(DeviceTable.id == id_)

        async with self.session_factory() as session:
            await session.execute(query)
            await session.commit()

        return SuccessMessage(message="Запись успешно удалена")
