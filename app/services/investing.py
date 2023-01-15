from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.models.donation import Donation


async def get_available_donation(session: AsyncSession):
    """Извлекает из БД доступное к расходу пожертвование"""
    dnt_obj = await session.execute(
        select(Donation).where(
            Donation.fully_invested == 0).order_by('create_date'))
    return dnt_obj.scalars().first()


async def get_investment_project(session: AsyncSession):
    """Извлекает из БД доступный для инвестиций проект"""
    prj_obj = await session.execute(
        select(CharityProject).where(
            CharityProject.fully_invested == 0).order_by('create_date'))
    return prj_obj.scalars().first()


async def chng_dnt_obj_values(
    obj,
    add_fnds=None,
    fully_invested=False,
    current_time=None
) -> None:
    """Устанавливает значения для объектов пожертвований и проектов"""
    obj.invested_amount += add_fnds
    obj.fully_invested = fully_invested
    obj.close_date = current_time


async def investment_process(
    obj,
    session: AsyncSession,
):
    """Инвестирует пожертвования в проекты"""

    dnt_obj = await get_available_donation(session)
    prj_obj = await get_investment_project(session)

    if (dnt_obj is None) or (prj_obj is None):
        return obj

    need_invest = prj_obj.full_amount - prj_obj.invested_amount
    avlbl_fnds = dnt_obj.full_amount - dnt_obj.invested_amount
    current_time = datetime.now()

    if avlbl_fnds > need_invest:
        await chng_dnt_obj_values(
            obj=prj_obj,
            add_fnds=need_invest,
            fully_invested=True,
            current_time=current_time
        )
        await chng_dnt_obj_values(
            obj=dnt_obj,
            add_fnds=need_invest
        )

    elif avlbl_fnds == need_invest:
        await chng_dnt_obj_values(
            obj=prj_obj,
            add_fnds=avlbl_fnds,
            fully_invested=True,
            current_time=current_time
        )
        await chng_dnt_obj_values(
            obj=dnt_obj,
            add_fnds=avlbl_fnds,
            fully_invested=True,
            current_time=current_time
        )

    elif avlbl_fnds < need_invest:
        await chng_dnt_obj_values(
            obj=prj_obj, add_fnds=avlbl_fnds
        )
        await chng_dnt_obj_values(
            obj=dnt_obj,
            add_fnds=avlbl_fnds,
            fully_invested=True,
            current_time=current_time
        )

    session.add(prj_obj)
    session.add(dnt_obj)
    await session.commit()
    await session.refresh(prj_obj)
    await session.refresh(dnt_obj)
    return await investment_process(obj, session)
