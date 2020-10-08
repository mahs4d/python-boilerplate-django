from typing import List, Optional

from apps.core.decorators import optional_raise
from utils import pagination
from apps.core.error_helpers import CustomApiError
from . import error_descriptors
from .models import User


def create_user(phone: str, is_admin: bool):
    user = User(phone=phone, is_admin=is_admin)
    user.save()


def get_users_list(page: int = 1) -> List[User]:
    """
    returns paginated users list
    """

    start, end = pagination.get_start_and_end(page)
    return User.objects.all().prefetch_related(['profile'])[start:end]


@optional_raise
def get_user_by_id(user_id: int) -> Optional[User]:
    """
    returns user with specified id
    """
    
    try:
        return User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise CustomApiError(**error_descriptors.USER_NOT_FOUND)


@optional_raise
def get_user_by_phone(phone: str) -> Optional[User]:
    """
    returns user with specified phone
    """

    try:
        return User.objects.get(phone=phone)
    except User.DoesNotExist:
        raise CustomApiError(**error_descriptors.USER_NOT_FOUND)
