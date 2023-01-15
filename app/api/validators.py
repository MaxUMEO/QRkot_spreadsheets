from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import charity_project_crud
from app.models.charity_project import CharityProject


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    """Проверка на существование такого имени в БД"""
    project_id = await charity_project_crud.get_project_id_by_name(project_name, session)
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_charity_project_exists(
    charity_project_id: int,
    session: AsyncSession,
) -> CharityProject:
    """Проверка существования проекта в БД"""
    charity_project = await charity_project_crud.get(charity_project_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!'
        )
    return charity_project


async def check_deleting_charity_project_already_closed_or_invested(
    charity_project_id: int,
    session: AsyncSession,
) -> None:
    """Проверка при удалении:проект не закрыт, в нем нет средств"""
    prj_obj = await charity_project_crud.get(charity_project_id, session)

    if prj_obj.fully_invested == 1:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!',
        )

    if prj_obj.invested_amount != 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!',
        )


async def check_patch_charity_project_fully_invested(
    charity_project_id: int,
    session: AsyncSession,
) -> None:
    """Проверка при обновлении: проект не закрыт"""
    prj_obj = await charity_project_crud.get(charity_project_id, session)

    if prj_obj.fully_invested == 1:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!',
        )