from django.contrib import admin

from trips.models import Trip, Day, Plan


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Main', {'fields': ('title', 'url_picture',)}),
        ('Dates', {'fields': ('from_date', 'to_date', 'duration', 'finished')}),
        ('Other', {'fields': ('members',)}),
    )
    list_display = ['title',]
    save_on_top = True


@admin.register(Day)
class DayAdmin(admin.ModelAdmin):
    list_display = ['__str__',]
    save_on_top = True


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Main', {'fields': ('name', 'url_picture', 'address')}),
        ('Dates', {'fields': ('day', 'duration', 'opening_hours', 'popular_times')}),
        ('Other', {'fields': ('trip',)}),
    )
    list_display = ['name',]
    save_on_top = True
