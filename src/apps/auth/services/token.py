from datetime import datetime, timedelta
from typing import List, Tuple

import jwt
from django.conf import settings

from apps.user import services as user_services
from apps.user.models import User
from utils.errors import CustomApiError
from . import otp as otp_services
from . import role as roles_services
from .. import error_descriptors


def _generate_token(user: User, requested_role_slugs: List[str] = None) -> dict:
    """
    generates a pair of access/refresh tokens for user
    """

    if not user.is_active:
        raise CustomApiError(**error_descriptors.INACTIVE_USER)

    roles = roles_services.get_user_roles(user_id=user.id)
    user_role_slugs = [role.slug for role in roles]

    if user.is_admin:
        user_role_slugs.append('admin')
    else:
        user_role_slugs.remove('admin')

    if not requested_role_slugs:
        requested_role_slugs = user_role_slugs

    for role_slug in requested_role_slugs:
        if role_slug not in user_role_slugs:
            raise CustomApiError(**error_descriptors.INVALID_ROLE)

    expires_at = datetime.now() + timedelta(**settings.AUTH_ACCESS_TOKEN_DURATION)
    access_token = jwt.encode(payload={
        'exp': expires_at,
        'sub': user.id,
        'roles': requested_role_slugs,
    }, key=settings.AUTH_ACCESS_TOKEN_KEY, algorithm='HS256').decode('UTF-8')

    refresh_token = jwt.encode(payload={
        'exp': datetime.now() + timedelta(**settings.AUTH_ACCESS_TOKEN_DURATION),
        'sub': user.id,
        'roles': requested_role_slugs,
    }, key=settings.AUTH_ACCESS_TOKEN_KEY, algorithm='HS256').decode('UTF-8')

    return {
        'user': user,
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'Bearer',
        'expires_at': expires_at.timestamp(),
    }


def generate_tokens_with_password(phone: str, password: str, requested_role_slugs: List[str]) -> dict:
    """
    generates access token for the user with specified phone using provided password
    """

    user = user_services.get_user_by_phone(phone=phone, raise_exception=False)
    if not user:
        raise CustomApiError(**error_descriptors.INVALID_CREDENTIALS)

    if not user.check_password(password):
        raise CustomApiError(**error_descriptors.INVALID_CREDENTIALS)

    return _generate_token(user=user, requested_role_slugs=requested_role_slugs)


def generate_tokens_with_otp(phone: str, code: str, requested_role_slugs: List[str]) -> dict:
    """
    generates access token for the user with specified phone using provided otp_code
    """

    user = user_services.get_user_by_phone(phone=phone, raise_exception=False)
    if not user:
        raise CustomApiError(**error_descriptors.INVALID_CREDENTIALS)

    otp_code = otp_services.get_otp_code_for_user(user_id=user.id, raise_exception=False)
    if not otp_code or otp_code.code != code:
        raise CustomApiError(**error_descriptors.INVALID_CREDENTIALS)
    otp_services.use_otp_code(otp_code=otp_code)
    
    return _generate_token(user=user, requested_role_slugs=requested_role_slugs)


def generate_tokens_with_refresh_token(refresh_token: str) -> dict:
    """
    generate a pair of access/refresh tokens from refresh token
    """

    try:
        payload = jwt.decode(jwt=refresh_token, key=settings.AUTH_REFRESH_TOKEN_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise CustomApiError(**error_descriptors.EXPIRED_REFRESH_TOKEN)
    except jwt.InvalidTokenError:
        raise CustomApiError(**error_descriptors.INVALID_REFRESH_TOKEN)

    user_id = payload['sub']
    requested_role_slugs = payload['roles']

    user = user_services.get_user_by_id(user_id=user_id, raise_exception=False)
    if not user:
        raise CustomApiError(**error_descriptors.INVALID_CREDENTIALS)

    return _generate_token(user=user, requested_role_slugs=requested_role_slugs)


def generate_tokens_with_grant_type(grant_type: str, phone: str, requested_role_slugs: List[str] = None,
                                    password: str = None, otp_code: str = None, refresh_token: str = None) -> dict:
    """
    calls appropriate token generator based on grant type
    """

    if grant_type == 'password':
        return generate_tokens_with_password(phone=phone, password=password, requested_role_slugs=requested_role_slugs)
    elif grant_type == 'otp':
        return generate_tokens_with_otp(phone=phone, code=otp_code, requested_role_slugs=requested_role_slugs)
    elif grant_type == 'refresh_token':
        return generate_tokens_with_refresh_token(refresh_token=refresh_token)

    raise CustomApiError(**error_descriptors.INVALID_GRANT_TYPE)


def verify_access_token(access_token: str) -> Tuple[int, List[str]]:
    """
    verifies access token and returns user id and list of role slugs associated to the token
    """

    try:
        payload = jwt.decode(jwt=access_token, key=settings.AUTH_ACCESS_TOKEN_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise CustomApiError(**error_descriptors.EXPIRED_ACCESS_TOKEN)
    except jwt.InvalidTokenError:
        raise CustomApiError(**error_descriptors.INVALID_ACCESS_TOKEN)

    user_id = payload['sub']
    role_slugs = payload['roles']

    return user_id, role_slugs
