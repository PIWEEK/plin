from django.contrib.auth.models import User
from django.db import models


class Trip(models.Model):
    duration = models.IntegerField(blank=True, null=False)
    members = models.ManyToManyField(User, related_name="trips")
    title = models.CharField(max_length=100, blank=False, null=False)
    url_picture = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title


class Day(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    order = models.IntegerField()
    trip = models.ForeignKey(Trip, related_name="days", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Plan(models.Model):
    address = models.CharField(max_length=100, blank=True, null=True)
    day = models.ForeignKey(Day, related_name="plans", blank=True, null=True, on_delete=models.SET_NULL)
    duration = models.IntegerField()
    google_id = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=False, null=False)
    opening_hours = models.CharField(max_length=100, blank=True, null=True)
    popular_times = models.URLField(blank=True, null=True)
    trip = models.ForeignKey(Trip, related_name="plans", on_delete=models.CASCADE)
    url_picture = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name
