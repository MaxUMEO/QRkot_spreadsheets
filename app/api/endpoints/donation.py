from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models.user import User
from app.schemas.donation import DonationCreate, CutDonationsDB, ExtDonationsDB
from app.services.investing import investment_process


router = APIRouter()


@router.post(
    '/',
    response_model=CutDonationsDB,
    response_model_exclude_none=True,
)
async def create_donation(
    new_donation: DonationCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Внесение пожертвования"""
    new_donation = await donation_crud.create(new_donation, session, user)
    new_donation = await investment_process(new_donation, session)
    return new_donation


@router.get(
    '/',
    response_model=list[ExtDonationsDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """Возвращает список всех пожертвований. Только для суперюзеров."""
    all_donations = await donation_crud.get_multi(session)
    return all_donations


@router.get(
    '/my',
    response_model=list[CutDonationsDB],
    response_model_exclude_none=True,
)
async def get_user_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Возвращает список всех пожертвований пользователя."""
    all_donations = await donation_crud.get_user_donations(user, session)
    return all_donations