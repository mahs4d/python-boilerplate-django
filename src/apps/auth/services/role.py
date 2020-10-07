from typing import List, Optional

from apps.core.decorators import optional_raise
from utils import pagination
from utils.errors import CustomApiError
from .. import error_descriptors
from ..models import Role


def get_user_roles(user_id: int) -> List[Role]:
    """
    returns user roles
    """

    return Role.objects.filter(users__id=user_id)


@optional_raise
def get_role_by_slug(slug: str) -> Optional[Role]:
    """
    returns a role by it's slug
    """

    try:
        return Role.objects.get(slug=slug)
    except Role.DoesNotExist:
        raise CustomApiError(**error_descriptors.ROLE_NOT_FOUND)


def get_roles_by_slug_list(slugs: List[str]) -> List[Role]:
    """
    return list of roles based on input slugs (if role with specified slug does not exist, it is ignored)
    """

    return Role.objects.filter(slug__in=slugs)


def get_roles_list(page: int = 1) -> List[Role]:
    """
    returns list of available roles
    """

    start, end = pagination.get_start_and_end(page)
    return Role.objects.all()[start: end]


@optional_raise
def create_role(slug: str, name: str, permissions: List[str]) -> Role:
    """
    creates a role
    """

    if slug == 'admin':
        raise CustomApiError(**error_descriptors.ROLE_RESERVED_SLUG)

    role_with_same_slug = get_role_by_slug(slug=slug, raise_exception=False)
    if role_with_same_slug:
        raise CustomApiError(**error_descriptors.ROLE_DUPLICATE_SLUG)

    role = Role(slug=slug, name=name, permissions=permissions)
    role.save()

    return role


@optional_raise
def update_role(slug: str, name: Optional[str], permissions: Optional[List[str]]) -> Role:
    """
    updates a role by slug
    """

    role = get_role_by_slug(slug=slug)

    if name is not None:
        role.name = name

    if permissions is not None:
        role.permissions = permissions

    role.save()

    return role


@optional_raise
def remove_role(slug: str) -> None:
    """
    removes role by slug
    """

    role = get_role_by_slug(slug=slug)
    role.delete()
