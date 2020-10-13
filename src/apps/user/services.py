from typing import List
from typing import Optional

from django.db import transaction

from apps.auth.services import role as role_services
from apps.core.decorators import optional_raise
from apps.core.error_helpers import CustomApiError
from utils import pagination
from . import error_descriptors
from .models import User


@optional_raise
def create_user(phone: str, password: str, is_admin: bool, is_active: bool, first_name: str, last_name: str,
                roles: List[str]):
    """
    creates a new user
    """

    same_phone_user = get_user_by_phone(phone=phone, raise_exception=False)
    if same_phone_user is not None:
        raise CustomApiError(**error_descriptors.USER_DUPLICATE_PHONE)

    with transaction.atomic():
        user = User(phone=phone, is_admin=is_admin, is_active=is_active)
        user.save()

        user.set_password(raw_password=password)

        user.profile.first_name = first_name
        user.profile.last_name = last_name
        user.profile.save()

        for role in roles:
            role_services.add_role_to_user(role_slug=role, user_id=user.id)


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

    user = User.objects.filter(pk=user_id).first()
    if user is None:
        raise CustomApiError(**error_descriptors.USER_NOT_FOUND)

    return user


@optional_raise
def get_user_by_phone(phone: str) -> Optional[User]:
    """
    returns user with specified phone
    """

    user = User.objects.filter(phone=phone).first()
    if user is None:
        raise CustomApiError(**error_descriptors.USER_NOT_FOUND)

    return user


@optional_raise
def update_user(user_id: int, password: Optional[str], is_admin: Optional[bool] = None,
                is_active: Optional[bool] = None, first_name: Optional[str] = None, last_name: Optional[str] = None,
                roles: Optional[List[str]] = None):
    """
    updates the user with specified id
    """

    user = get_user_by_id(user_id=user_id)

    if password is not None:
        user.set_password(raw_password=password)

    if is_admin is not None:
        user.is_admin = is_admin

    if is_active is not None:
        user.is_active = is_active

    is_profile_updated = False
    if first_name is not None:
        user.profile.first_name = first_name
        is_profile_updated = True

    if last_name is not None:
        user.profile.last_name = last_name
        is_profile_updated = True

    if roles is not None:
        role_services.clear_user_roles(user=user)
        for role in roles:
            role_services.add_role_to_user(role_slug=role, user_id=user.id)

    if is_profile_updated:
        user.profile.save()
    user.save()

    return user


@optional_raise
def remove_user(user_id: int) -> None:
    """
    removes the user
    """

    user = get_user_by_id(user_id=user_id)
    user.delete()
