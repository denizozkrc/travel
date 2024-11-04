from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Trip, Stop, Lodging, Transport
from django import forms
from django.forms import ValidationError


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ["username", "password"]


class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ["title", "start_date", "end_date", "ltd", "lng", 
                  "location_name", "location_id", "formattedAddress"]  # Update user yourself
        labels = {
            "title": "Title",
            "start_date": ("Start Date"),
            "end_date": ("End Date"),
        }
        widgets = {"start_date": forms.SelectDateWidget(),
                   "end_date": forms.SelectDateWidget()}

    def clean(self):  # is_valid calls this
        if self.cleaned_data.get("start_date") > self.cleaned_data.get("end_date"):
            raise ValidationError("Start date cannot be after end date")
        return self.cleaned_data


class StopForm(forms.ModelForm):
    class Meta:
        model = Stop
        fields = ["title", "date", "time", "type_of_stop", "ltd", "lng", "note"]  # Update trip yourself
        labels = {
            "title": ("Title"),
            "date": ("Date"),
            "time": ("Time"),
            "type_of_stop": ("Type of Stop"),
            "note": ("Note")
        }
        widgets = {"date": forms.SelectDateWidget(),
                   "time": forms.TimeInput(attrs={'type': 'time'})}


class LodgingForm(forms.ModelForm):
    class Meta:
        model = Lodging
        fields = ["title", "start_date", "start_time", "end_date", "end_time", "ltd", "lng", "note"]
        labels = {
            "title": ("Title"),
            "start_date": ("Check-In Date"),
            "end_date": ("Check-Out Date"),
            "start_time": ("Check-In Time"),
            "end_time": ("Check-Out Time"),
            "note": ("Note")
        }
        widgets = {"start_date": forms.SelectDateWidget(),
                   "end_date": forms.SelectDateWidget(),
                   "start_time": forms.TimeInput(attrs={'type': 'time'}),
                   "end_time": forms.TimeInput(attrs={'type': 'time'})}

    def clean(self):
        cd = self.cleaned_data
        start_date = cd.get("start_date")
        end_date = cd.get("end_date")
        start_time = cd.get("start_time")
        end_time = cd.get("end_time")

        if start_date > end_date:
            raise ValidationError("Check-In date cannot be after Check-Out date")
        elif start_date == end_date and start_time > end_time:
            raise ValidationError("Check-In time cannot be after Check-Out time")
        return cd


class TransportForm(forms.ModelForm):
    class Meta:
        model = Transport
        fields = ["title", "date", "time", "ltd", "lng", "type_of_transport", "note"]  # Update trip yourself
        labels = {
            "title": ("Title"),
            "date": ("Date"),
            "time": ("Time"),
            "type_of_transport": ("Type of Transport"),
            "note": ("Note")
        }
        widgets = {"date": forms.SelectDateWidget(),
                   "time": forms.TimeInput(attrs={'type': 'time'})}


class InviteForm(forms.Form):
    username = forms.CharField(label="User's username", max_length=200)
