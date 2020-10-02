import re

_COMPILED_PHONE_REGEX = re.compile(r'^09\d{9}$')


def validate_phone(phone):
    return _COMPILED_PHONE_REGEX.match(phone)
