from rest_framework import serializers

from trips.models import Trip, Day, Plan
from users.serializers import UserSerializer


class PlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Plan
        fields = '__all__'


class DaySerializer(serializers.ModelSerializer):
    plans = PlanSerializer(required=False, many=True)

    class Meta:
        model = Day
        fields = '__all__'


class LightTripSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trip
        fields = ("id", "duration", "title", "url_picture", "members")


class TripSerializer(serializers.ModelSerializer):
    days = DaySerializer(required=False, many=True)
    wishlist = serializers.SerializerMethodField()
    members = UserSerializer(required=False, many=True)

    class Meta:
        model = Trip
        fields = '__all__'

    def get_wishlist(self, obj):
        wishlist = Plan.objects.filter(trip=obj, day__isnull=True)
        serializer = PlanSerializer(instance=wishlist, many=True)
        return serializer.data
