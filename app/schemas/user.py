from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """Получить пользователя"""
    pass


class UserCreate(schemas.BaseUserCreate):
    """Создать пользователя"""
    pass


class UserUpdate(schemas.BaseUserUpdate):
    """Обновить пользователя"""
    pass