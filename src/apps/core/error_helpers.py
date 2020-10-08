import logging

from django.conf import settings
from rest_framework.exceptions import APIException, ValidationError, MethodNotAllowed, NotFound, NotAcceptable, \
    UnsupportedMediaType
from rest_framework.response import Response

from . import error_descriptors

logger = logging.getLogger(__name__)


class CustomApiError(Exception):
    """
    a general easily customizable exception for apis
    """

    def __init__(self, status_code: int, message: str, code: str, details: any = None):
        super().__init__(message)

        self.status_code = status_code
        self.message = message
        self.code = code
        self.details = details

    def get_response(self):
        if self.details is None:
            return Response(data={
                'message': self.message,
                'code': self.code,
            }, status=self.status_code)
        else:
            return Response(data={
                'message': self.message,
                'code': self.code,
                'details': self.details,
            }, status=self.status_code)


def exception_handler(exc: Exception, context):
    if isinstance(exc, APIException):
        if isinstance(exc, ValidationError):
            error_desc = dict(error_descriptors.SERVER_VALIDATION_ERROR)
            error_desc['details'] = exc.detail
            custom_api_error = CustomApiError(**error_desc)
        elif isinstance(exc, MethodNotAllowed):
            custom_api_error = CustomApiError(**error_descriptors.SERVER_METHOD_NOT_ALLOWED)
        elif isinstance(exc, NotFound):
            custom_api_error = CustomApiError(**error_descriptors.SERVER_ENDPOINT_NOT_FOUND)
        elif isinstance(exc, NotAcceptable):
            custom_api_error = CustomApiError(**error_descriptors.SERVER_NOT_ACCEPTABLE)
        elif isinstance(exc, UnsupportedMediaType):
            custom_api_error = CustomApiError(**error_descriptors.SERVER_UNSUPPORTED_MEDIA)
        else:
            logger.error(exc, exc_info=True)
            custom_api_error = CustomApiError(status_code=exc.status_code, message=str(exc.detail), code='core:unknown')

        return custom_api_error.get_response()

    if isinstance(exc, CustomApiError):
        return exc.get_response()

    logger.error(exc, exc_info=True)
    error_desc = dict(error_descriptors.SERVER_INTERNAL_ERROR)
    if settings.DEBUG:
        error_desc['details'] = str(exc) if settings.DEBUG else None

    return CustomApiError(**error_desc).get_response()
