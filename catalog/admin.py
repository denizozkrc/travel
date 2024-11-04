from django.contrib import admin

# Register your models here.

from .models import Trip, Stop, Lodging, Transport, Invite


class StopsInLine(admin.TabularInline):
    model = Stop
    extra = 1


class TripsAdmin(admin.ModelAdmin):
    # fields =["title", "start_date", "end_date"]
    inlines = [
        StopsInLine,
    ]


admin.site.register(Trip, TripsAdmin)
admin.site.register(Stop)
admin.site.register(Lodging)
admin.site.register(Transport)
admin.site.register(Invite)





