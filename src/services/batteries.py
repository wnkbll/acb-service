from fastapi import HTTPException, status
from sqlalchemy import delete, insert, select, update

from src.db.tables import BatteryTable
from src.models import SuccessMessage
from src.models.batteries import (
    BatteryCreateModel,
    BatteryResponseModel,
    BatteryUpdateModel,
)
from src.services import Service


class BatteriesService(Service):
    async def get_battery(self, battery_id: int) -> BatteryResponseModel:
        query = select(BatteryTable).where(BatteryTable.id == battery_id)

        async with self.session_factory() as session:
            response = await session.execute(query)
            row = response.scalar_one_or_none()

            if row is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Запись с таким id не найдена",
                )

            battery = BatteryResponseModel.model_validate(row, from_attributes=True)
            return battery

    async def get_batteries(self) -> list[BatteryResponseModel]:
        query = select(BatteryTable)

        async with self.session_factory() as session:
            response = await session.execute(query)
            rows = response.scalars().all()

            return [
                BatteryResponseModel.model_validate(row, from_attributes=True)
                for row in rows
            ]

    async def create_battery(
        self, battery_to_create: BatteryCreateModel
    ) -> SuccessMessage:
        query = insert(BatteryTable).values(**battery_to_create.model_dump())

        async with self.session_factory() as session:
            await session.execute(query)
            await session.commit()

        return SuccessMessage(message="Запись успешно создана")

    async def update_battery(
        self, battery_id: int, battery_to_update: BatteryUpdateModel
    ) -> SuccessMessage:
        query = select(BatteryTable).where(BatteryTable.id == battery_id)

        async with self.session_factory() as session:
            response = await session.execute(query)
            row = response.scalar_one_or_none()
            if row is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Запись с таким id не найдена",
                )

        query = (
            update(BatteryTable)
            .where(BatteryTable.id == battery_id)
            .values(**battery_to_update.model_dump(exclude_none=True))
        )

        async with self.session_factory() as session:
            await session.execute(query)
            await session.commit()

        return SuccessMessage(message="Запись успешно обновлена")

    async def delete_battery(self, battery_id: int) -> SuccessMessage:
        query = select(BatteryTable).where(BatteryTable.id == battery_id)

        async with self.session_factory() as session:
            response = await session.execute(query)
            row = response.scalar_one_or_none()
            if row is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Запись с таким id не найдена",
                )

        query = delete(BatteryTable).where(BatteryTable.id == battery_id)

        async with self.session_factory() as session:
            await session.execute(query)
            await session.commit()

        return SuccessMessage(message="Запись успешно удалена")
