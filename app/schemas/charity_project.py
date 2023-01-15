from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, validator


class CharityProjectUpdate(BaseModel):
    """Схема обновления проекта"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[int] = Field(None, gt=0)

    class Config:
        extra = Extra.forbid
        min_anystr_length = 1


class CharityProjectCreate(CharityProjectUpdate):
    """Схема создания проекта"""
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: int = Field(..., gt=0)

    @validator('name', 'description')
    def none_and_empty_field_not_allowed(cls, value: str):
        if not value or value is None:
            raise ValueError('Все поля обязательны. "" или None не допускаются.')
        return value


class CharityProjectDB(CharityProjectCreate):
    """Схема проекта из БД"""
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime] = Field(None)

    class Config:
        orm_mode = True