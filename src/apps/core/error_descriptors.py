from rest_framework import status

SERVER_METHOD_NOT_ALLOWED = {
    'status_code': status.HTTP_405_METHOD_NOT_ALLOWED,
    'message': 'method not allowed',
    'code': 'core:method-not-allowed',
}

SERVER_ENDPOINT_NOT_FOUND = {
    'status_code': status.HTTP_400_BAD_REQUEST,
    'message': 'endpoint not found',
    'code': 'core:endpoint-not-found',
}

SERVER_VALIDATION_ERROR = {
    'status_code': status.HTTP_400_BAD_REQUEST,
    'message': 'validation error',
    'code': 'core:validation-error',
}

SERVER_UNSUPPORTED_MEDIA = {
    'status_code': status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
    'message': 'unsupported media',
    'code': 'core:unsupported-media',
}

SERVER_NOT_ACCEPTABLE = {
    'status_code': status.HTTP_406_NOT_ACCEPTABLE,
    'message': 'not acceptable',
    'code': 'core:not-acceptable',
}

SERVER_INTERNAL_ERROR = {
    'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
    'message': 'internal error',
    'code': 'core:internal-error',
}
