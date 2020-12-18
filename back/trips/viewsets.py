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
        plans = trip.plans.all().update(day=None, order=None)
        return Response('all plans reset')

    @action(detail=True, methods=['post'])
    def plinit(self, request, pk=None):
        trip = Trip.objects.get(pk=pk)
        plans = trip.plans.order_by('?').all()
        duration = trip.duration
        plans_per_day = int(len(plans) / duration)
        for i, day in enumerate(trip.days.all()):
            start = i * plans_per_day
            end = i * plans_per_day + plans_per_day
            for j, plan in enumerate(plans[start:end]):
                plan.day = day
                plan.order = j + 1
                plan.save()

        first_day = trip.days.first()
        max_order = first_day.plans.order_by('order').first().order
        for i, plan in enumerate(trip.plans.filter(day__isnull=True)):
            plan.day = first_day
            plan.order = max_order + i + 1
            plan.save()

        serializer = TripSerializer(trip)
        return Response(serializer.data)


class PlanViewSet(viewsets.ModelViewSet):
    serializer_class = PlanSerializer
    queryset = Plan.objects.all()

    def perform_create(self, serializer):
        if Plan.objects.count() == 0:
            order = 1
        else:
            order = Plan.objects.all().order_by('-order').first().order + 1
        instance = serializer.save(created_by=self.request.user, order=order, day=None)

    @action(detail=True, methods=['post'])
    def move(self, request, trip_pk, pk=None):
        # Get the orig and dest data
        moving_plan = Plan.objects.get(pk=pk)
        orig_order = moving_plan.order
        orig_day = moving_plan.day # None|Wishlist or day
        dest_day = None # None|Wishlisht
        if 'day_to' in request.data: # or day
            dest_day = Day.objects.get(id=request.data['day_to'])

        # conseguir el orden destino en un día con planes
        if 'before_plan' in request.data:
            before_plan_id = request.data['before_plan']

            # reordenar día destino posterior a la card que vamos a colocar
            before_plan = Plan.objects.get(id=before_plan_id)
            if before_plan.order:
                order = before_plan.order
            else:
                order = 1

            if dest_day:
                plans_to_reorder = Plan.objects.filter(day=dest_day, order__gte=order).order_by('order')
            else:
                plans_to_reorder = Plan.objects.filter(day__isnull=True, order__gte=order).order_by('order')
            for i, plan in enumerate(plans_to_reorder):
                plan.order = order + i + 1
                plan.save()

        # conseguir el orden destino en un día sin planes o al final
        else:
            after_plan = Plan.objects.filter(day=dest_day).order_by('-order').first()
            if after_plan and after_plan.order:
                order = after_plan.order + 1
            else:
                order = 1

        # guardamos el plan nuevo
        moving_plan.day = dest_day
        moving_plan.order = order
        moving_plan.save()

        # reordenamos días en la columna origen
        if orig_day:
            plans_to_reorder = Plan.objects.filter(day=orig_day, order__gt=orig_order,).order_by('order')
        else:
            plans_to_reorder = Plan.objects.filter(day__isnull=True, order__gt=orig_order,).order_by('order')
        for i, plan in enumerate(plans_to_reorder):
            plan.order = plan.order - 1
            plan.save()

        serializer = PlanSerializer(moving_plan)
        return Response(serializer.data)


class DayViewSet(viewsets.ModelViewSet):
    serializer_class = DaySerializer
    queryset = Day.objects.all()
