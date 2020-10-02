from functools import wraps
from . import error_descriptors
from utils.errors import CustomApiError


def require_authentication():
    """
    requires the request user to be authenticated
    """

    def decorator(fn):
        @wraps(fn)
        def wrapper(request, *args, **kwargs):
            if not request.is_authenticated:
                raise CustomApiError(**error_descriptors.AUTHENTICATION_REQUIRED)

            fn(request, *args, **kwargs)

        return wrapper

    return decorator


def require_permission(permission: str):
    """
    requires the request user to be: 1. authenticated 2. has specified permission
    """

    def decorator(fn):
        @require_authentication()
        @wraps(fn)
        def wrapper(request, *args, **kwargs):
            if not request.user_permissions or permission not in request.user_permissions:
                raise CustomApiError(**error_descriptors.PERMISSION_DENIED)

            fn(request, *args, **kwargs)

        return wrapper

    return decorator
