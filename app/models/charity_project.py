from sqlalchemy import Column, String, Text

from app.models.abstract_models import AbstractCharityProjectAndDonationModel


class CharityProject(AbstractCharityProjectAndDonationModel):
    """Модель проектов пожертвований."""
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=False)

    def __repr__(self) -> str:
        return (
            f'name: {self.name[:15]}, '
            f'description: {self.description[:15]}, '
            f'{super().__repr__()}'
        )