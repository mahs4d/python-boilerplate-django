from rest_framework import status
from rest_framework.request import Request
from rest_framework.views import APIView, Response

from apps.core import serializers as core_serializers
from . import serializers as auth_serializers
from .decorators import require_permission
from .services import otp as otp_services, role as role_services, token as token_services


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

        output = core_serializers.MessageOutputSerializer({})
        return Response(data=output.data, status=status.HTTP_201_CREATED)


class RolesView(APIView):
    @require_permission('role')
    def get(self, request: Request) -> Response:
        input_serializer = core_serializers.PaginationInputSerializer(data=request.query_params)
        input_serializer.is_valid(raise_exception=True)

        page = input_serializer.validated_data.get('page')

        roles = role_services.get_roles_list(page=page)

        output = auth_serializers.RoleSerializer(instance=roles, many=True)
        return Response(data={'roles': output.data}, status=status.HTTP_200_OK)

    @require_permission('role')
    def post(self, request: Request) -> Response:
        input_serializer = auth_serializers.CreateRoleSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        slug = input_serializer.validated_data.get('slug')
        name = input_serializer.validated_data.get('name')
        permissions = input_serializer.validated_data.get('permissions')

        role = role_services.create_role(slug=slug, name=name, permissions=permissions)

        output = auth_serializers.RoleSerializer(instance=role)
        return Response(data={'role': output.data}, status=status.HTTP_201_CREATED)


class RoleDetailsView(APIView):
    @require_permission('role')
    def get(self, request: Request, slug: str) -> Response:
        role = role_services.get_role_by_slug(slug=slug)

        output = auth_serializers.RoleSerializer(instance=role)
        return Response(data={'role': output.data}, status=status.HTTP_200_OK)

    @require_permission('role')
    def put(self, request: Request, slug: str) -> Response:
        input_serializer = auth_serializers.UpdateRoleSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        name = input_serializer.validated_data.get('name')
        permissions = input_serializer.validated_data.get('permissions')

        role = role_services.update_role(slug=slug, name=name, permissions=permissions)

        output = auth_serializers.RoleSerializer(instance=role)
        return Response(data={'role': output.data}, status=status.HTTP_200_OK)

    @require_permission('role')
    def delete(self, request: Request, slug: str) -> Response:
        role_services.remove_role(slug=slug)

        output = core_serializers.MessageOutputSerializer({})
        return Response(data=output.data, status=status.HTTP_204_NO_CONTENT)
