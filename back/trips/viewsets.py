from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from trips.serializers import TripSerializer, LightTripSerializer
from trips.models import Trip


class TripViewSet(viewsets.ModelViewSet):
    serializer_class = TripSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return LightTripSerializer

        return TripSerializer

    def get_queryset(self):
        return self.request.user.trips.all()
