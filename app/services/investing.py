from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.models.donation import Donation


async def get_investment_objects(session: AsyncSession):
    """Извлекает из БД объекты доступные к расходу/внесению средств"""
    donationt_obj = await session.execute(
        select(Donation).where(
            Donation.fully_invested == 0).order_by('create_date'))

    project_obj = await session.execute(
        select(CharityProject).where(
            CharityProject.fully_invested == 0).order_by('create_date'))

    return donationt_obj.scalars().first(), project_obj.scalars().first()


async def chng_dnt_obj_values(
    obj,
    add_funds=None,
    fully_invested=False,
    current_time=None
) -> None:
    """Устанавливает значения для объектов пожертвований и проектов"""
    obj.invested_amount += add_funds
    obj.fully_invested = fully_invested
    obj.close_date = current_time


async def investment_process(
    obj,
    session: AsyncSession,
):
    """Инвестирует пожертвования в проекты"""
    donationt_obj, project_obj = await get_investment_objects(session)

    if (donationt_obj is None) or (project_obj is None):
        return obj

    need_invest = project_obj.full_amount - project_obj.invested_amount
    available_funds = donationt_obj.full_amount - donationt_obj.invested_amount
    current_time = datetime.now()

    if available_funds > need_invest:
        await chng_dnt_obj_values(
            obj=project_obj,
            add_funds=need_invest,
            fully_invested=True,
            current_time=current_time
        )
        await chng_dnt_obj_values(
            obj=donationt_obj,
            add_funds=need_invest
        )

    elif available_funds == need_invest:
        await chng_dnt_obj_values(
            obj=project_obj,
            add_funds=available_funds,
            fully_invested=True,
            current_time=current_time
        )
        await chng_dnt_obj_values(
            obj=donationt_obj,
            add_funds=available_funds,
            fully_invested=True,
            current_time=current_time
        )

    elif available_funds < need_invest:
        await chng_dnt_obj_values(
            obj=project_obj, add_funds=available_funds
        )
        await chng_dnt_obj_values(
            obj=donationt_obj,
            add_funds=available_funds,
            fully_invested=True,
            current_time=current_time
        )

    session.add(project_obj)
    session.add(donationt_obj)
    await session.commit()
    await session.refresh(project_obj)
    await session.refresh(donationt_obj)
    return await investment_process(obj, session)
