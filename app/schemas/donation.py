from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field


class DonationCreate(BaseModel):
    """Схема создания пожертвования"""
    full_amount: int = Field(..., gt=0)
    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class CutDonationsDB(DonationCreate):
    """Краткое отображение пожертвований"""
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class ExtDonationsDB(CutDonationsDB):
    """Полное отображения пожертвований"""
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime] = Field(None)