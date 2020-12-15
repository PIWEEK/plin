from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import generics

from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# class MeView(mixins.RetrieveModelMixin,
#              # mixins.UpdateModelMixin,
#              # mixins.DestroyModelMixin,
#              generics.GenericAPIView):
#
#     serializer_class = UserSerializer
#     # queryset = User.objects.all()
#
#     def get_queryset(self):
#         return User.objects.get(pk=self.request.user.id)
