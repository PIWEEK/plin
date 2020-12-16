from rest_framework import generics
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import viewsets

from users.models import User
from users.serializers import UserSerializer



class CreateUserViewSet(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):

    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


# class MeViewSet(viewsets.ViewSet):
#
#     def list(self, request):
#         serializer = UserSerializer(self.request.user)
#         return Response(serializer.data)

class MeViewSet(mixins.RetrieveModelMixin,
             # mixins.UpdateModelMixin,
             # mixins.DestroyModelMixin,
                viewsets.GenericViewSet):

    serializer_class = UserSerializer
    queryset = User.objects.all()
