from functools import wraps


def optional_raise(fn):
    @wraps(fn)
    def wrapper(*args, raise_exception: bool = True, **kwargs):
        try:
            return fn(*args, **kwargs)
        except BaseException as ex:
            if raise_exception:
                raise ex
            else:
                return None

    return wrapper
