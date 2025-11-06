from fastapi import HTTPException, status
from sqlalchemy import select, update

from src.db.tables import BatteryTable, DeviceTable
from src.models import SuccessMessage
from src.models.bind import BindManyCreateModel, BindOneCreateModel
from src.services import Service


class BindService(Service):
    async def is_device_exists(self, device_id: int) -> bool:
        query = select(DeviceTable).where(DeviceTable.id == device_id)

        async with self.session_factory() as session:
            response = await session.execute(query)
            row = response.scalar_one_or_none()

            return row is not None

    async def is_battery_exists(self, battery_id: int) -> bool:
        query = select(BatteryTable).where(BatteryTable.id == battery_id)

        async with self.session_factory() as session:
            response = await session.execute(query)
            row = response.scalar_one_or_none()

            return row is not None

    async def bind_many(self, bind_to_create: BindManyCreateModel) -> SuccessMessage:
        if len(bind_to_create.batteries) > 5:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Максимальное число связей: 5",
            )

        if not await self.is_device_exists(bind_to_create.device_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Устройство с id={bind_to_create.device_id} не существует",
            )

        query = select(BatteryTable.id).where(
            BatteryTable.id.in_(bind_to_create.batteries)
        )
        async with self.session_factory() as session:
            response = await session.execute(query)
            rows = response.scalars().all()

        for battery in bind_to_create.batteries:
            if battery not in rows:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Аккумулятор с id={battery} не существует",
                )

        query = (
            update(BatteryTable)
            .where(BatteryTable.device_id == bind_to_create.device_id)
            .values(device_id=None)
        )

        async with self.session_factory() as session:
            await session.execute(query)
            query = (
                update(BatteryTable)
                .where(BatteryTable.id.in_(bind_to_create.batteries))
                .values(device_id=bind_to_create.device_id)
            )
            await session.execute(query)
            await session.commit()

        return SuccessMessage(message="Запись успешно создана")

    async def bind_one(self, bind_to_create: BindOneCreateModel) -> SuccessMessage:
        if not await self.is_device_exists(bind_to_create.device_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Устройство с id={bind_to_create.device_id} не существует",
            )

        if not await self.is_battery_exists(bind_to_create.battery_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Аккумулятор с id={bind_to_create.battery_id} не существует",
            )

        query = select(BatteryTable).where(
            BatteryTable.device_id == bind_to_create.device_id
        )

        async with self.session_factory() as session:
            response = await session.execute(query)
            rows = response.scalars().all()
            if len(rows) >= 5:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Количество связей равно или превышает максимальное значение",
                )

        query = (
            update(BatteryTable)
            .where(BatteryTable.id == bind_to_create.battery_id)
            .values(device_id=bind_to_create.device_id)
        )

        async with self.session_factory() as session:
            await session.execute(query)
            await session.commit()

        return SuccessMessage(message="Запись успешно создана")

    async def delete_bind(self, battery_id: int) -> SuccessMessage:
        if not await self.is_battery_exists(battery_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Аккумулятор с id={battery_id} не существует",
            )

        query = (
            update(BatteryTable)
            .where(BatteryTable.id == battery_id)
            .values(device_id=None)
        )

        async with self.session_factory() as session:
            await session.execute(query)
            await session.commit()

        return SuccessMessage(message="Запись успешно удалена")
