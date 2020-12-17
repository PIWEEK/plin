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
    PlanSerializer,
    TripSerializer
)
from trips.models import Trip, Plan, Day
from users.models import User


class TripViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):
        if self.action == 'list':
            return LightTripSerializer

        return TripSerializer

    def get_queryset(self):
        return self.request.user.trips.all()

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.members.add(self.request.user)

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

    @action(detail=False, methods=['get'])
    def photo(self, request):
        photoreference = request.query_params['photoreference']
        maxwidth = request.query_params['maxwidth']
        url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth={maxwidth}&photoreference={photoreference}&key={settings.GOOGLE_API_KEY}"
        res = requests.get(url)
        return Response({
          "url": res.url
        })

    @action(detail=True, methods=['post'])
    def invite(self, request, pk=None):
        trip = Trip.objects.get(pk=pk)
        email = request.data['email']
        user = User.objects.filter(email=email).first()
        if user:
            trip.members.add(user)
            serializer = TripSerializer(trip)
            return Response(serializer.data)
        else:
            return Response('user not found')


    @action(detail=True, methods=['post'])
    def reset(self, request, pk=None):
        trip = Trip.objects.get(pk=pk)
        plans = trip.plans.all().update(day=None)
        return Response('all plans reset')



class PlanViewSet(viewsets.ModelViewSet):
    serializer_class = PlanSerializer
    queryset = Plan.objects.all()

    def perform_update(self, serializer):
        day = None
        if 'day_to' in self.request.data:
            day = Day.objects.get(id=self.request.data['day_to'])

        if 'before_plan' in self.request.data:
            before_plan_id = self.request.data['before_plan']

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
            order = -1
            if after_plan != None:
                order = after_plan.order + 1
            instance = serializer.save(day=day, order=order)
            instance.save()


class DayViewSet(viewsets.ModelViewSet):
    serializer_class = DaySerializer
    queryset = Day.objects.all()
