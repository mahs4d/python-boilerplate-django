from typing import Tuple

from django.conf import settings
from rest_framework import status

from apps.core.error_helpers import CustomApiError


def get_offset_and_limit(page: int) -> Tuple[int, int]:
    """
    converts page number to offset and limit
    """
    if page <= 0:
        raise CustomApiError(status_code=status.HTTP_400_BAD_REQUEST, message='invalid page number',
                             code='invalid-page')

    limit = settings.PAGE_SIZE
    offset = (page - 1) * limit

    return offset, limit


def get_start_and_end(page: int) -> Tuple[int, int]:
    offset, limit = get_offset_and_limit(page)
    return offset, offset + limit
