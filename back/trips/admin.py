from django.contrib import admin

from trips.models import Trip, Day, Plan


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    ...


@admin.register(Day)
class DayAdmin(admin.ModelAdmin):
    ...


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    ...
