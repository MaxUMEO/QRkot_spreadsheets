from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectUpdate, CharityProjectDB)
from app.api.validators import (
    check_name_duplicate, check_charity_project_exists,
    check_deleting_charity_project_already_closed_or_invested,
    check_patch_charity_project_fully_invested)
from app.services.investing import investment_process

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
    new_charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Содание благотворительного проекта. Только для суперюзеров."""
    await check_name_duplicate(new_charity_project.name, session)
    new_charity_project = await charity_project_crud.create(new_charity_project, session)
    new_charity_project = await investment_process(new_charity_project, session)
    return new_charity_project


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    """Возвращает список всех проектов."""
    return await charity_project_crud.get_multi(session)


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Обновление проекта. Только для суперюзеров."""
    charity_project = await check_charity_project_exists(
        project_id, session
    )

    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    await check_patch_charity_project_fully_invested(charity_project.id, session)
    return await charity_project_crud.update(
        charity_project,
        obj_in,
        session
    )


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Удаление проекта. Только для суперюзеров."""
    charity_project = await check_charity_project_exists(
        project_id, session
    )
    await check_deleting_charity_project_already_closed_or_invested(project_id, session)
    return await charity_project_crud.remove(charity_project, session)