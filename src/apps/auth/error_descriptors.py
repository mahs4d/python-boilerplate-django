from rest_framework import status

INVALID_CREDENTIALS = {
    'status_code': status.HTTP_422_UNPROCESSABLE_ENTITY,
    'message': 'invalid credentials were provided',
    'code': 'auth:invalid-credentials',
}

INACTIVE_USER = {
    'status_code': status.HTTP_401_UNAUTHORIZED,
    'message': 'user is not active',
    'code': 'auth:inactive-user',
}

INVALID_ROLE = {
    'status_code': status.HTTP_403_FORBIDDEN,
    'message': 'user does not have the specified role',
    'code': 'auth:invalid-role',
}

INVALID_REFRESH_TOKEN = {
    'status_code': status.HTTP_401_UNAUTHORIZED,
    'message': 'invalid refresh token',
    'code': 'auth:invalid-refresh-token',
}

INVALID_ACCESS_TOKEN = {
    'status_code': status.HTTP_401_UNAUTHORIZED,
    'message': 'invalid access token',
    'code': 'auth:invalid-access-token',
}

EXPIRED_REFRESH_TOKEN = {
    'status_code': status.HTTP_401_UNAUTHORIZED,
    'message': 'expired refresh token',
    'code': 'auth:expired-refresh-token',
}

EXPIRED_ACCESS_TOKEN = {
    'status_code': status.HTTP_401_UNAUTHORIZED,
    'message': 'expired access token',
    'code': 'auth:expired-access-token',
}

INVALID_GRANT_TYPE = {
    'status_code': status.HTTP_400_BAD_REQUEST,
    'message': 'invalid grant type',
    'code': 'auth:invalid-grant-type',
}

AUTHENTICATION_REQUIRED = {
    'status_code': status.HTTP_401_UNAUTHORIZED,
    'message': 'authentication required',
    'code': 'auth:authentication-required',
}

PERMISSION_DENIED = {
    'status_code': status.HTTP_403_FORBIDDEN,
    'message': 'permission denied',
    'code': 'auth:permission-denied',
}

OTP_CODE_ALREADY_SENT = {
    'status_code': status.HTTP_422_UNPROCESSABLE_ENTITY,
    'message': 'otp code already sent',
    'code': 'auth:otp-already-sent',
}

OTP_CODE_NOT_FOUND = {
    'status_code': status.HTTP_404_NOT_FOUND,
    'message': 'otp code not found',
    'code': 'auth:otp-not-found',
}

ROLE_NOT_FOUND = {
    'status_code': status.HTTP_404_NOT_FOUND,
    'message': 'role not found',
    'code': 'auth:role-not-found',
}

ROLE_RESERVED_SLUG = {
    'status_code': status.HTTP_422_UNPROCESSABLE_ENTITY,
    'message': 'this role slug is reserved',
    'code': 'auth:role-reserved-slug',
}

ROLE_DUPLICATE_SLUG = {
    'status_code': status.HTTP_422_UNPROCESSABLE_ENTITY,
    'message': 'role with same slug exists',
    'code': 'auth:role-duplicate-slug',
}
