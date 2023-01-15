from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.donation import Donation
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.donation import CutDonationsDB


class CRUDDonation(CRUDBase):
    async def get_user_donations(
        self,
        user: User,
        session: AsyncSession,
    ) -> list[CutDonationsDB]:
        """Получить объекты пожертвований пользователя из БД"""
        user_donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        donations_objs = user_donations.scalars().all()
        return donations_objs


donation_crud = CRUDDonation(Donation)