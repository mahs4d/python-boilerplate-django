from functools import wraps

from rest_framework.renderers import JSONRenderer

from .error_helpers import exception_handler


def optional_raise(fn):
    @wraps(fn)
    def wrapper(*args, raise_exception: bool = True, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as ex:
            if raise_exception:
                raise ex
            else:
                return None

    return wrapper


def middleware_error_handler(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as ex:
            response = exception_handler(ex, None)
            response.accepted_renderer = JSONRenderer()
            response.accepted_media_type = "application/json"
            response.renderer_context = {}
            return response.render()

    return wrapper
