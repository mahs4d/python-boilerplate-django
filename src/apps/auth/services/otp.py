import random
from datetime import datetime, timedelta
from typing import Optional

from django.conf import settings

from apps.core.decorators import optional_raise
from apps.user import services as user_services
from utils.errors import CustomApiError
from .. import error_descriptors
from ..models import OtpCode


@optional_raise
def get_otp_code_for_user(user_id: int) -> Optional[OtpCode]:
    """
    returns the last valid otp code for use saved in the database
    """

    try:
        unexpired_creation_time = datetime.now() - timedelta(**settings.OTP_CODE_DURATION)
        otp_code = OtpCode.objects.get(user_id=user_id, creation_time__gte=unexpired_creation_time, is_used=False)
        return otp_code
    except OtpCode.DoesNotExist:
        raise CustomApiError(**error_descriptors.OTP_CODE_NOT_FOUND)


@optional_raise
def create_otp_code(phone: str) -> None:
    """
    creates and sends the otp code for the user with specified phone number
    """

    user = user_services.get_user_by_phone(phone=phone)

    old_otp_code = get_otp_code_for_user(user_id=user.id, raise_exception=False)
    if old_otp_code:
        raise CustomApiError(**error_descriptors.OTP_CODE_ALREADY_SENT)

    otp_code = OtpCode(user_id=user.id, code=_generate_random_code())
    otp_code.save()

    _send_otp_code(phone=phone, code=otp_code.code)


def use_otp_code(otp_code: OtpCode) -> None:
    """
    marks otp code as used
    """
    
    otp_code.is_used = True
    otp_code.save()


def _generate_random_code() -> str:
    """
    generates a random number as otp code (not saved to database)
    """

    code = random.randrange(10 ** (settings.OTP_CODE_LENGTH - 1), 10 ** settings.OTP_CODE_LENGTH)
    return str(code)


def _send_otp_code(phone: str, code: str) -> None:
    """
    sends the sms message (not implemented)
    """

    raise NotImplementedError('otp is not supported yet :)')
