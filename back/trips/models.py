from django.contrib.gis.db import models as gis_models
from django.db import models
from django.dispatch import receiver

from users.models import User



class Trip(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    duration = models.IntegerField(blank=False, null=False)
    from_date = models.DateField(blank=True, null=True)
    members = models.ManyToManyField(User, related_name="trips", blank=True, null=True)
    title = models.CharField(max_length=100, blank=False, null=False)
    to_date = models.DateField(blank=True, null=True)
    url_picture = models.URLField(blank=True, null=True)
    finished = models.BooleanField(blank=False, null=False, default=False)

    class Meta:
        ordering = ['from_date',]

    def __str__(self):
        return self.title


class Day(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    date = models.DateField(blank=True, null=True)
    order = models.IntegerField()
    trip = models.ForeignKey(Trip, related_name="days", on_delete=models.CASCADE)

    class Meta:
        ordering = ['order',]

    def __str__(self):
        return f"{self.trip}: {self.order}"


class Plan(models.Model):
    address = models.CharField(max_length=100, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    day = models.ForeignKey(Day, related_name="plans", blank=True, null=True, on_delete=models.SET_NULL)
    duration = models.FloatField()
    google_id = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=False, null=False)
    price_min = models.CharField(max_length=100, blank=True, null=True)
    price_max = models.CharField(max_length=100, blank=True, null=True)
    opening_hours = models.CharField(max_length=500, blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)
    latlon = gis_models.PointField(blank=True, null=True)
    popular_times = models.URLField(blank=True, null=True)
    telephone = models.CharField(max_length=100, blank=True, null=True)
    trip = models.ForeignKey(Trip, related_name="plans", on_delete=models.CASCADE)
    url_picture = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ['order', 'created_at', ]

    def __str__(self):
        return self.name


@receiver(models.signals.post_save, sender=Trip)
def add_days_on_trip_creation(sender, instance, created, **kwargs):
    if created:
        for i in range(instance.duration):
            Day.objects.create(
                order=i+1,
                trip=instance
            )


@receiver(models.signals.post_delete, sender=Day)
def move_plans_on_day_deletion(sender, instance, **kwargs):
    for plan in instance.plans.all():
        plan.day = None
        plan.save()
