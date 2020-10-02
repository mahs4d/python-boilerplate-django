import logging

from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.views import Response

from .exceptions import CustomApiError

logger = logging.getLogger(__name__)


def exception_handler(exc: Exception, context):
    if isinstance(exc, APIException):
        return Response(data={
            'code': exc.detail.code,
            'message': exc.detail,
        }, status=exc.status_code)

    if isinstance(exc, CustomApiError):
        return Response(data={
            'code': exc.code,
            'message': exc.message,
        }, status=exc.status_code)

    logger.error(exc, exc_info=True)
    return Response(data={
        'code': 'internal_server_error',
        'message': 'internal server error',
        'details': str(exc) if settings.DEBUG else None,
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
