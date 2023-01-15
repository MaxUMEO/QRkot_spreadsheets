from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    # Переменные для работы приложения
    app_title: str = 'QRKot'
    description: str = 'Приложение для Благотворительного фонда поддержки котиков — QRKot'
    database_url: str = 'sqlite+aiosqlite:///./QRKot_app.db'
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    # Переменные для работы с Google API
    type: Optional[str] = None
    project_id: Optional[str] = None
    private_key_id: Optional[str] = None
    private_key: Optional[str] = None
    client_email: Optional[str] = None
    client_id: Optional[str] = None
    auth_uri: Optional[str] = None
    token_uri: Optional[str] = None
    auth_provider_x509_cert_url: Optional[str] = None
    client_x509_cert_url: Optional[str] = None
    email: Optional[str] = None

    class Config:
        env_file = '.env'


settings = Settings()