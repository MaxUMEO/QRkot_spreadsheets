from typing import Dict, List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.crud.base import CRUDBase


class CRUDCharityProject(CRUDBase):
    async def get_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        db_room_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        db_room_id = db_room_id.scalars().first()
        return db_room_id

    async def get_projects_by_completion_rate(
        self,
        session: AsyncSession
    ) -> List[Dict[str, str]]:
        """Получить данные о закрытых проектах и отсортировать по скорости закрытия"""
        projects = await session.execute(
            select([CharityProject]).where(CharityProject.fully_invested == 1)
        )
        projects = projects.scalars().all()
        project_list = []
        for project in projects:
            project_list.append({
                'name': project.name,
                'closing_time': project.close_date - project.create_date,
                'description': project.description
            })
        project_list = sorted(project_list, key=lambda x: x['closing_time'])
        return project_list


charity_project_crud = CRUDCharityProject(CharityProject)
