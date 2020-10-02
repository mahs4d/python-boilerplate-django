from typing import List

from ..models import Role


def get_user_roles(user_id: int) -> List[Role]:
    """
    returns user roles
    """

    return Role.objects.filter(users__id=user_id)


def get_roles_by_slug_list(slugs: List[str]) -> List[Role]:
    """
    return list of roles based on input slugs (if role with specified slug does not exist, it is ignored)
    """

    return Role.objects.filter(slug__in=slugs)
