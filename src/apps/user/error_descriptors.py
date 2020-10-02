from rest_framework import status

USER_NOT_FOUND = {
    'status_code': status.HTTP_404_NOT_FOUND,
    'message': 'user not found',
    'code': 'user:user-not-found',
}
