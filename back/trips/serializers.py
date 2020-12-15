from rest_framework import serializers

from trips.models import Trip, Day, Plan


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ("name", "day")


class DaySerializer(serializers.ModelSerializer):
    plans = PlanSerializer(required=False, many=True)
    class Meta:
        model = Day
        fields = ("name", "order", "plans")


class TripSerializer(serializers.ModelSerializer):
    days = DaySerializer(required=False, many=True)
    wishlist = serializers.SerializerMethodField()

    class Meta:
        model = Trip
        fields = ("duration", "title", "url_picture", "members", "days", "wishlist")

    def get_wishlist(self, obj):
        wishlist = Plan.objects.filter(trip=obj, day__isnull=True).all()
        serializer = PlanSerializer(instance=wishlist, many=True)
        return serializer.data
