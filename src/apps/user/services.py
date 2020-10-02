from typing import List, Optional

from rest_framework import status

from utils import pagination
from utils.errors import CustomApiError
from .models import User
from . import error_descriptors


def create_user(phone: str, is_admin: bool):
    user = User(phone=phone, is_admin=is_admin)
    user.save()


def get_users(page: int = 1) -> List[User]:
    start, end = pagination.get_start_and_end(page)
    return User.objects.all()[start:end]


def get_user_by_id(user_id: int, *, raise_exception=True) -> Optional[User]:
    try:
        return User.objects.get(pk=user_id)
    except User.DoesNotExist:
        if raise_exception:
            raise CustomApiError(**error_descriptors.USER_NOT_FOUND)
        else:
            return None


def get_user_by_phone(phone: str, *, raise_exception=True) -> Optional[User]:
    try:
        return User.objects.get(phone=phone)
    except User.DoesNotExist:
        if raise_exception:
            raise CustomApiError(**error_descriptors.USER_NOT_FOUND)
        else:
            return None
