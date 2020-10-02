from logging import getLogger

from rest_framework import status
from rest_framework.views import APIView, Response

from . import services as core_services

logger = getLogger(__name__)


class ServerInfoView(APIView):
    def get(self, request):
        info = core_services.get_server_info()
        logger.debug('info')
        return Response(data=info, status=status.HTTP_200_OK)
