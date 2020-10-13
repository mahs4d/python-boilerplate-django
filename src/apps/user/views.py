from typing import Union

from rest_framework import status
from rest_framework.request import Request
from rest_framework.views import APIView, Response

from apps.auth.decorators import require_permission
from apps.core import serializers as core_serializers
from . import serializers as user_serializers
from . import services as user_services


class UsersView(APIView):
    @require_permission('user')
    def get(self, request: Request) -> Response:
        input_serializer = core_serializers.PaginationInputSerializer(data=request.query_params)
        input_serializer.is_valid(raise_exception=True)

        page = input_serializer.validated_data.get('page')

        users = user_services.get_users_list(page=page)

        output = user_serializers.UserSerializer(instance=users, many=True)
        return Response(data={'users': output.data}, status=status.HTTP_200_OK)

    @require_permission('user')
    def post(self, request: Request) -> Response:
        input_serializer = user_serializers.CreateUserInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        phone = input_serializer.validated_data.get('phone')
        password = input_serializer.validated_data.get('password')

        if request.user_is_admin:
            is_admin = input_serializer.validated_data.get('is_admin', False)
        else:
            is_admin = False

        is_active = input_serializer.validated_data.get('is_active', True)
        first_name = input_serializer.validated_data.get('first_name')
        last_name = input_serializer.validated_data.get('last_name')

        if request.user_is_admin:
            roles = input_serializer.validated_data.get('roles', [])
        else:
            roles = []

        user = user_services.create_user(phone=phone, password=password, is_admin=is_admin, is_active=is_active,
                                         first_name=first_name, last_name=last_name, roles=roles)

        output = user_serializers.UserSerializer(instance=user)
        return Response(data={'user': output.data}, status=status.HTTP_201_CREATED)


class UserDetailsView(APIView):
    @require_permission(lambda request, user_id: None if user_id == 'me' else 'user')
    def get(self, request: Request, user_id: Union[str, int]) -> Response:
        if user_id == 'me':
            user_id = request.user_id

        user = user_services.get_user_by_id(user_id=user_id)

        output = user_serializers.UserSerializer(instance=user)
        return Response(data={'user': output.data}, status=status.HTTP_200_OK)

    @require_permission(lambda request, user_id: None if user_id == 'me' else 'user')
    def put(self, request: Request, user_id: Union[str, int]) -> Response:
        if user_id == 'me':
            user_id = request.user_id

        input_serializer = user_serializers.UpdateUserInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        password = input_serializer.validated_data.get('password', None)

        if request.user_is_admin:
            is_admin = input_serializer.validated_data.get('is_admin', None)
        else:
            is_admin = None

        is_active = input_serializer.validated_data.get('is_active', None)
        first_name = input_serializer.validated_data.get('first_name', None)
        last_name = input_serializer.validated_data.get('last_name', None)

        if request.user_is_admin:
            roles = input_serializer.validated_data.get('roles', None)
        else:
            roles = None

        user = user_services.update_user(user_id=user_id, password=password, is_admin=is_admin, is_active=is_active,
                                         first_name=first_name, last_name=last_name, roles=roles)

        output = user_serializers.UserSerializer(instance=user)
        return Response(data={'user': output.data}, status=status.HTTP_200_OK)

    @require_permission('user')
    def delete(self, request: Request, user_id: int):
        user_services.remove_user(user_id=user_id)

        output = core_serializers.MessageOutputSerializer(instance={})
        return Response(data=output.data, status=status.HTTP_204_NO_CONTENT)
