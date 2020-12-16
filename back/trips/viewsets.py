from django.db.models import Q
from rest_framework import views
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from trips.serializers import (
    DaySerializer,
    LightTripSerializer,
    PlaceSerializer,
    PlanSerializer,
    SearchSerializer,
    TripSerializer
)
from trips.models import Trip, Plan, Day


class TripViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):
        if self.action == 'list':
            return LightTripSerializer

        return TripSerializer

    def get_queryset(self):
        return self.request.user.trips.all()


class PlanViewSet(viewsets.ModelViewSet):
    serializer_class = PlanSerializer
    queryset = Plan.objects.all()

    @action(detail=False, methods=['get'])
    def search(self, request, trip_pk):
        # do the search
        results = [
            {'gid': '1', 'name': 'Museo del Prado'},
            {'gid': '2', 'name': 'Museo Thyssen'},
            {'gid': '3', 'name': 'Museo Lázaro Galdiano'}
        ]
        serializer = SearchSerializer(results, many=True, context={'request': request})
        return Response(serializer.data)


    @action(detail=False, methods=['get'])
    def locate(self, request, trip_pk):
        # locate the details of the place
        place = {'gid': '1', 'name': 'Museo del Prado'}
        serializer = PlaceSerializer(place, context={'request': request})
        return Response(serializer.data)


class DayViewSet(viewsets.ModelViewSet):
    serializer_class = DaySerializer
    queryset = Day.objects.all()
