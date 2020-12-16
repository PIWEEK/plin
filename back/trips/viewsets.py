from django.conf import settings
from django.db.models import Q
import requests
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

    @action(detail=False, methods=['get'])
    def search(self, request):
        search_term = request.query_params['place']
        url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={search_term}&key={settings.GOOGLE_API_KEY}"
        res = requests.get(url)
        return Response(res.json())

    @action(detail=False, methods=['get'])
    def locate(self, request):
        place_id = request.query_params['place_id']
        url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={settings.GOOGLE_API_KEY}"
        res = requests.get(url)
        return Response(res.json())


class PlanViewSet(viewsets.ModelViewSet):
    serializer_class = PlanSerializer
    queryset = Plan.objects.all()

    def perform_update(self, serializer):
        day = Day.objects.get(id=self.request.query_params['day_to'])

        if 'before_plan' in self.request.query_params:
            before_plan_id = self.request.query_params['before_plan']

            before_plan = Plan.objects.get(id=before_plan_id)
            before_plan_order = before_plan.order
            plans_to_reorder = Plan.objects.filter(day=day, order__gte=before_plan_order).order_by('order')

            for i, plan in enumerate(plans_to_reorder):
                plan.order = before_plan_order + i + 1
                plan.save()

            instance = serializer.save(day=day)
            instance.order = before_plan_order
            instance.save()
        else:
            after_plan = Plan.objects.filter(day=day).order_by('-order').first()
            instance = serializer.save(day=day, order=after_plan.order + 1)
            instance.save()


class DayViewSet(viewsets.ModelViewSet):
    serializer_class = DaySerializer
    queryset = Day.objects.all()
