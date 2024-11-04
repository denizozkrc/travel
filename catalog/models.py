from django.db import models
from django.contrib.auth.models import User


# Create your models here.

# I MIGHT WANT TO make CustomUser a subclass of User instead of foreign key thing.
# But that would mean flushing the whole db, so if I have time...

"""class UserData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    username = models.CharField(max_length=200)


    def __str__(self):
        return self.user.username"""


class Trip(models.Model):  # created by user
    title = models.CharField(max_length=200)
    start_date = models.DateField("start_date")
    end_date = models.DateField("end_date")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ltd = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)
    location_name = models.CharField(max_length=200, null=True, blank=True)
    location_id = models.CharField(max_length=200, null=True, blank=True)
    formattedAddress = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.title


class Stop(models.Model):  # created by us, custom ones can be added by user
    title = models.CharField(max_length=200)
    date = models.DateField(null=True)  # because I try to add fields that
    # are not allowed to be null, to a table
    # that already contains records, I allow
    # NULL values for the new field.
    time = models.TimeField(null=True)

    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    ltd = models.FloatField()
    lng = models.FloatField()
    TYPE_OF_STOP_CHOICES = {
        "sea": "Sea",
        "cafe": "Cafe",
        "city": "City",
        "restaurant": "Restaurant",
        "nature": "Nature",
        "sightSeeing": "Sight Seeing",
        "travel": "Travel",
        "freeTime": "Free Time",
        "historical_museum": "Historical/Museum",
        "shopping": "Shopping",
        "event": "Event",
    }
    type_of_stop = models.CharField(
        max_length=30,
        choices=TYPE_OF_STOP_CHOICES,
        default="other",
    )
    note = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.title


class Lodging(models.Model):
    title = models.CharField(max_length=200)
    start_date = models.DateField("start_date")
    start_time = models.TimeField(null=True)

    end_date = models.DateField("end_date")
    end_time = models.TimeField(null=True)

    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    ltd = models.FloatField()
    lng = models.FloatField()
    note = models.CharField(max_length=200, null=True, blank=True)


class Transport(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField(null=True)
    time = models.TimeField(null=True)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    ltd = models.FloatField()
    lng = models.FloatField()
    TYPE_OF_TRANSPORT_CHOICES = {
        "plane": "Plane",
        "train": "Train",
        "bus": "Bus",
        "ferry": "Ferry",
    }
    type_of_transport = models.CharField(
        max_length=30,
        choices=TYPE_OF_TRANSPORT_CHOICES,
        default="freeTime",
    )
    note = models.CharField(max_length=200, null=True, blank=True)
    note2 = models.CharField(max_length=200, null=True, blank=True)


class Invite(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_invites")
    invited_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pending_invites")
    approved = models.BooleanField(default=False)
    denied = models.BooleanField(default=False)

    class Meta:
        unique_together = ['trip', 'invited_user']
