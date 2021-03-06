from functools import wraps
from typing import Union, Callable

from apps.core.error_helpers import CustomApiError
from . import error_descriptors


def require_authentication():
    """
    requires the request user to be authenticated
    """

    def decorator(fn):
        @wraps(fn)
        def wrapper(view, request, *args, **kwargs):
            if not request.is_authenticated:
                raise CustomApiError(**error_descriptors.AUTHENTICATION_REQUIRED)

            return fn(view, request, *args, **kwargs)

        return wrapper

    return decorator


def require_permission(permission: Union[str, Callable]):
    """
    requires the request user to be: 1. authenticated 2. has the specified permission
    """

    def decorator(fn):
        @require_authentication()
        @wraps(fn)
        def wrapper(view, request, *args, **kwargs):
            prms = permission
            if callable(permission):
                prms = permission(request, *args, **kwargs)

            if prms is not None:
                if prms not in request.user_permissions and not request.user_is_admin:
                    raise CustomApiError(**error_descriptors.PERMISSION_DENIED)

            return fn(view, request, *args, **kwargs)

        return wrapper

    return decorator
