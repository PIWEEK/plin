from rest_framework import generics
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.response import Response

from users.models import User
from users.serializers import UserSerializer



class CreateUserViewSet(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):

    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class MeView(generics.GenericAPIView):

    def get(self, request):
        serializer = UserSerializer(self.request.user)
        return Response(serializer.data)

    def patch(self, request):
        user = self.request.user
        if 'first_name' in request.data:
            user.first_name = request.data['first_name']
        if 'email' in request.data:
            user.email = request.data['email']
        if 'password' in request.data:
            user.set_password(request.data['password'])

        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data)
