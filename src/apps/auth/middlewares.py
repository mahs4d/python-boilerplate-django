from apps.core.decorators import middleware_error_handler
from apps.core.error_helpers import CustomApiError
from . import error_descriptors
from .services import role as role_services
from .services import token as token_services


def fill_user_info(get_response):
    @middleware_error_handler
    def middleware(request):
        if 'Authorization' in request.headers:
            authorization_header = request.headers.get('Authorization')

            if not authorization_header.startswith('bearer ') and not authorization_header.startswith('Bearer '):
                raise CustomApiError(**error_descriptors.INVALID_ACCESS_TOKEN)

            token = authorization_header[7:]
            user_id, role_slugs = token_services.verify_access_token(token)

            request.is_authenticated = True
            request.user_id = user_id
            request.user_role_slugs = role_slugs
            request.user_is_admin = 'admin' in role_slugs
        else:
            request.is_authenticated = False

        return get_response(request)

    return middleware


def fill_permission_info(get_response):
    @middleware_error_handler
    def middleware(request):
        if request.is_authenticated:
            roles = role_services.get_roles_by_slug_list(request.user_role_slugs)
            permissions = []
            for role in roles:
                permissions.extend(role.permissions)

            request.user_permissions = set(permissions)
        else:
            request.user_permissions = []

        return get_response(request)

    return middleware
