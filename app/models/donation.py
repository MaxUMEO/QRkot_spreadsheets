from sqlalchemy import Column, Text, Integer, ForeignKey

from app.models.abstract_models import AbstractCharityProjectAndDonationModel


class Donation(AbstractCharityProjectAndDonationModel):
    """Модель пожертвований."""
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text, nullable=True)

    def __repr__(self) -> str:
        return (
            f'user_id: {self.user_id}, '
            f'comment: {self.comment[:15]}, '
            f'{super().__repr__()}'
        )