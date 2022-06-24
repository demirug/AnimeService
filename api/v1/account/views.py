from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.account.serializers import UserSerializer


class CurrentUserView(APIView):
    """Return current user params"""
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
