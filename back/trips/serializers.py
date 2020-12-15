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
    plans = PlanSerializer(required=False, many=True)

    class Meta:
        model = Trip
        fields = ("duration", "title", "url_picture", "members", "days", "plans")

    def get_plans(self, obj):
        return Plan.objects.filter(trip=obj, day__isnull=True).all()
