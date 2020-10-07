import logging

from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.views import Response

from .exceptions import CustomApiError

logger = logging.getLogger(__name__)


def exception_handler(exc: Exception, context):
    if isinstance(exc, APIException):
        custom_api_error = CustomApiError(status_code=exc.status_code, message=exc.detail, code=exc.detail.code)
        return custom_api_error.get_response()

    if isinstance(exc, CustomApiError):
        return exc.get_response()

    logger.error(exc, exc_info=True)
    return Response(data={
        'code': 'internal-server-error',
        'message': 'internal server error',
        'details': str(exc) if settings.DEBUG else None,
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
