from rest_framework import status
from rest_framework.request import Request
from rest_framework.views import APIView, Response

from apps.core import serializers as core_serializers
from . import serializers as auth_serializers
from .services import otp as otp_services, token as token_services


class TokensView(APIView):
    def post(self, request: Request) -> Response:
        input_serializer = auth_serializers.GenerateTokensInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        grant_type = input_serializer.validated_data.get('grant_type')
        phone = input_serializer.validated_data.get('phone')
        password = input_serializer.validated_data.get('password', None)
        otp_code = input_serializer.validated_data.get('otp_code', None)
        refresh_token = input_serializer.validated_data.get('refresh_token', None)
        role_slugs = input_serializer.validated_data.get('roles', [])

        tokens = token_services.generate_tokens_with_grant_type(grant_type=grant_type, phone=phone,
                                                                requested_role_slugs=role_slugs, password=password,
                                                                otp_code=otp_code, refresh_token=refresh_token)

        output = auth_serializers.TokensSerializer(instance=tokens)
        return Response(data=output.data, status=status.HTTP_201_CREATED)


class OtpCodeView(APIView):
    def post(self, request: Request) -> Response:
        input_serializer = auth_serializers.CreateOtpCodeInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        phone = input_serializer.validated_data.get('phone')

        otp_services.create_otp_code(phone=phone)

        output = core_serializers.MessageOutputSerializer(instance={'message': 'otp sent'})
        return Response(data=output.data, status=status.HTTP_201_CREATED)
