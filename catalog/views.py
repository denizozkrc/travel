from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Trip, Stop, Lodging, Transport, Invite
from .forms import (
    TripForm,
    StopForm,
    LodgingForm,
    TransportForm,
    LoginForm,
    SignupForm,
    InviteForm
)
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from guardian.shortcuts import assign_perm
from guardian.shortcuts import remove_perm


# Details (Stops, transports and lodgings of the trip)
class DetailView(LoginRequiredMixin, View):

    login_url = "catalog:ulogin"

    def get(self, request, **kwargs):
        trip_id = self.kwargs['trip_id']
        trip = get_object_or_404(Trip, pk=trip_id)
        stop_objects = trip.stop_set.all().order_by('date').order_by('time')
        lodging_objects = trip.lodging_set.all().order_by('start_date').order_by('start_time')
        transport_objects = trip.transport_set.all().order_by('date').order_by('time')
        
        stop_paginator = Paginator(stop_objects, 4)
        lodging_paginator = Paginator(lodging_objects, 4)
        transport_paginator = Paginator(transport_objects, 4)
        stop_page_number = request.GET.get('stop_page')
        lodging_page_number = request.GET.get('lodging_page')
        transport_page_number = request.GET.get('transport_page')
        stop_page_obj = stop_paginator.get_page(stop_page_number)
        lodging_page_obj = lodging_paginator.get_page(lodging_page_number)
        transport_page_obj = transport_paginator.get_page(transport_page_number)

        if not request.user == trip.user and not request.user.has_perm('catalog.view_trip', trip):
            logout(request)
            return redirect("catalog:ulogin")
        else:
            context = {"trip": trip, "stop_page_obj": stop_page_obj, "lodging_page_obj": lodging_page_obj, 
                       "transport_page_obj": transport_page_obj}
            return render(request, "catalog/detail.html", context)


class StopDetailView(LoginRequiredMixin, View):  # details of a stop

    login_url = "catalog:ulogin"

    def get(self, request, **kwargs):
        stop_id = self.kwargs['stop_id']
        trip_id = self.kwargs['trip_id']
        stop = get_object_or_404(Stop, pk=stop_id)
        trip = get_object_or_404(Trip, pk=trip_id)
        if not request.user == stop.trip.user and not request.user.has_perm('catalog.view_trip', trip):
            logout(request)
            return redirect("catalog:ulogin")
        else:
            context = {"stop": stop, "trip": trip}
            return render(request, "catalog/stop_detail.html", context)


class LodgingDetailView(LoginRequiredMixin, View):  # details of a lodging

    login_url = "catalog:ulogin"

    def get(self, request, **kwargs):
        lodging_id = self.kwargs['lodging_id']
        trip_id = self.kwargs['trip_id']
        lodging = get_object_or_404(Lodging, pk=lodging_id)
        trip = get_object_or_404(Trip, pk=trip_id)
        if not request.user == lodging.trip.user and not request.user.has_perm('catalog.view_trip', trip):
            logout(request)
            return redirect("catalog:ulogin")
        context = {"lodging": lodging, "trip": trip}
        return render(request, "catalog/lodging_detail.html", context)


class TransportDetailView(LoginRequiredMixin, View):  # details of stop
    login_url = "catalog:ulogin"

    def get(self, request, **kwargs):
        transport_id = self.kwargs['transport_id']
        trip_id = self.kwargs['trip_id']
        transport = get_object_or_404(Transport, pk=transport_id)
        trip = get_object_or_404(Trip, pk=trip_id)
        if not request.user == transport.trip.user and not request.user.has_perm('catalog.view_trip', trip):
            logout(request)
            return redirect("catalog:ulogin")
        context = {"transport": transport, "trip": trip}
        return render(request, "catalog/transport_detail.html", context)


class HomeView(LoginRequiredMixin, View):

    login_url = "catalog:ulogin"

    def get(self, request, **kwargs):
        # this is not loggedin user's homepage, it is the homepage
        username = self.kwargs['username']
        # of the user at the url. If not the same, we redirect to login
        user = User.objects.get(username=username)
        if not request.user == user:
            logout(request)
            return redirect("catalog:ulogin")
        all_trips = (
            user.trip_set.all().order_by('start_date')
        )
        paginator = Paginator(all_trips, 6)
        page_number = request.GET.get('page')  # from url
        page_obj = paginator.get_page(page_number)
        context = {"page_obj": page_obj, "username": username}
        return render(request, "catalog/home.html", context)


class userLoginView(View):  # form made here

    def post(self, request):
        if request.user.is_authenticated:
            # if already logged in, do nothing, back to homepage
            username = request.POST.get("username")
            return redirect("catalog:home", username=username)
        else:
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("catalog:home", username=username)
            else:
                # not shown yet, should deal in templates
                messages.info(request, "Incorrect password or username")
                form = LoginForm()
                context = {"form": form}
                return render(request, "catalog/login.html", context)

    def get(self, request):

        if request.user.is_authenticated:  # if already logged in, do nothing,
            # back to homepage
            username = request.POST.get("username")
            return redirect("catalog:home", username=username)
        else:
            form = (
                LoginForm()
            )  
            context = {"form": form}
            return render(request, "catalog/login.html", context)


class userLogoutView (LoginRequiredMixin, View):

    login_url = "catalog:ulogin"

    def get(self, request):
        logout(request)
        return redirect("catalog:ulogin")


class userSignupView(View):

    def post(self, request):
        if request.user.is_authenticated:
            # if already logged in, do nothing, back to homepage
            username = request.POST.get("username")
            return redirect("catalog:home", username=username)
        else:
            # form = UserCreationForm(request.POST)  #default form
            # custom form that inherits from UserCreationForm
            form = SignupForm(request.POST)
            if (
                form.is_valid()
            ):
                form.save()
                # user = User.objects.get(username = username)
                # UserData.objects.create(user=user, username=username)
                messages.success(
                    request, "Account was created for " + username)
                return redirect("catalog:ulogin")
            else:
                context = {"form": form}
                return render(request, "catalog/signup.html", context)

    def get(self, request):

        if request.user.is_authenticated:
            # if already logged in, do nothing, back to homepage
            username = request.POST.get("username")
            return redirect("catalog:home", username=username)
        else:
            # form = UserCreationForm() #default form
            form = (
                SignupForm()
            )  # custom form that inherits from UserCreationForm
            context = {"form": form}
            return render(request, "catalog/signup.html", context)


class AddTripView(LoginRequiredMixin, View):

    login_url = "catalog:ulogin"

    def post(self, request, **kwargs):
        username = self.kwargs['username']
        user = User.objects.get(username=username)
        if not request.user == user:
            logout(request)
            return redirect("catalog:ulogin")
        form = TripForm(request.POST)
        if form.is_valid():
            trip = form.save(commit=False) 
            trip.user = User.objects.get(username=username)
            trip.save()
            return redirect("catalog:detail", trip.id)
        else:
            messages.info(request, "Incorrect form entry")
            context = {"form": form, "username": username}
            return render(request, "catalog/addTrip.html", context)

    def get(self, request, **kwargs):
        username = self.kwargs['username']
        form = TripForm()
        context = {"form": form, "username": username}
        return render(request, "catalog/addTrip.html", context)


class RemoveTripView(LoginRequiredMixin, View):

    login_url = "catalog:ulogin"

    def get(self, request, **kwargs):
        trip_id = self.kwargs['trip_id']
        trip = Trip.objects.get(id=trip_id)
        if not request.user == trip.user:
            logout(request)
            return redirect("catalog:ulogin")
        trip.delete()
        return redirect("catalog:home", request.user.username)


class UpdateTripView(LoginRequiredMixin, View):

    login_url = "catalog:ulogin"

    def get(self, request, **kwargs):
        trip_id = self.kwargs['trip_id']
        trip = Trip.objects.get(id=trip_id)
        if not request.user == trip.user and not request.user.has_perm('catalog.view_trip', trip):
            logout(request)
            return redirect("catalog:ulogin")
        form = TripForm(instance=trip)
        return render(
            request,
            "catalog/updateTrip.html",
            {"form": form, "trip": trip}
        )

    def post(self, request, **kwargs):
        trip_id = self.kwargs['trip_id']
        trip = Trip.objects.get(id=trip_id)
        form = TripForm(request.POST, instance=trip)
        if form.is_valid():
            form.save()
            return redirect("catalog:home", request.user.username)
        else:
            return render(
                request, "catalog/updateTrip.html",
                {"form": form, "trip": trip}
            )


class AddStopView(LoginRequiredMixin, View):  # form made here

    login_url = "catalog:ulogin"

    def post(self, request, **kwargs):
        trip_id = self.kwargs['trip_id']
        form = StopForm(request.POST)
        if form.is_valid():
            stop = form.save(commit=False)  
            stop.trip = Trip.objects.get(id=trip_id)
            stop.save()
            return redirect("catalog:detail", trip_id)
        else:
            messages.info(request, "Incorrect form entry")
            context = {"form": form, "trip_id": trip_id, "trip": Trip.objects.get(id=trip_id)}
            return render(request, "catalog/addStop.html", context)

    def get(self, request, **kwargs):
        trip_id = self.kwargs['trip_id']
        trip = Trip.objects.get(id=trip_id)
        if not request.user == trip.user and not request.user.has_perm('catalog.view_trip', trip):
            logout(request)
            return redirect("catalog:ulogin")
        form = StopForm()
        context = {"form": form, "trip_id": trip_id, "trip": Trip.objects.get(id=trip_id)}
        return render(request, "catalog/addStop.html", context)


class RemoveStopView(LoginRequiredMixin, View):

    login_url = "catalog:ulogin"

    def get(self, request, **kwargs):
        stop_id = self.kwargs['stop_id']
        trip_id = Stop.objects.get(id=stop_id).trip.id
        trip = Trip.objects.get(id=trip_id)
        if not request.user == trip.user and not request.user.has_perm('catalog.view_trip', trip):
            logout(request)
            return redirect("catalog:ulogin")
        Stop.objects.get(id=stop_id).delete()
        return redirect("catalog:detail", trip_id)


class UpdateStopView(LoginRequiredMixin, View):

    login_url = "catalog:ulogin"

    def get(self, request, **kwargs):
        stop_id = self.kwargs['stop_id']
        trip_id = self.kwargs['trip_id']
        trip = Trip.objects.get(id=trip_id)
        stop = Stop.objects.get(id=stop_id)
        if not request.user == trip.user and not request.user.has_perm('catalog.view_trip', trip):
            logout(request)
            return redirect("catalog:ulogin")
        form = StopForm(instance=stop)
        return render(
            request,
            "catalog/updateStop.html",
            {"form": form, "stop": stop, "trip": trip}
        )

    def post(self, request, **kwargs):
        stop_id = self.kwargs['stop_id']
        trip_id = self.kwargs['trip_id']
        stop = Stop.objects.get(id=stop_id)
        trip = Trip.objects.get(id=trip_id)
        form = StopForm(request.POST, instance=stop)
        if form.is_valid():
            form.save()
            return redirect("catalog:stopDetail", trip_id, stop_id)
        else:                                           
            return render(
                request,
                "catalog/updateStop.html",
                {"form": form, "stop": stop, "trip": trip}
            )


class AddLodgingView(LoginRequiredMixin, View):  # form made here

    login_url = "catalog:ulogin"

    def post(self, request, **kwargs):
        trip_id = self.kwargs['trip_id']
        form = LodgingForm(request.POST)
        if form.is_valid():
            lodging = form.save(commit=False)  # does not save, NICEE
            lodging.trip = Trip.objects.get(id=trip_id)
            lodging.save()
            return redirect("catalog:detail", trip_id)
        else:
            messages.info(request, "Incorrect form entry")
            context = {"form": form, "trip_id": trip_id, "trip": Trip.objects.get(id=trip_id)}
            return render(request, "catalog/addLodging.html", context)

    def get(self, request, **kwargs):
        trip_id = self.kwargs['trip_id']
        trip = Trip.objects.get(id=trip_id)
        if not request.user == trip.user and not request.user.has_perm('catalog.view_trip', trip):
            logout(request)
            return redirect("catalog:ulogin")
        form = LodgingForm()
        context = {"form": form, "trip_id": trip_id, "trip": Trip.objects.get(id=trip_id)}
        return render(request, "catalog/addLodging.html", context)


class RemoveLodgingView(LoginRequiredMixin, View):

    login_url = "catalog:ulogin"

    def get(self, request, **kwargs):
        lodging_id = self.kwargs['lodging_id']
        trip_id = Lodging.objects.get(id=lodging_id).trip.id
        trip = Trip.objects.get(id=trip_id)
        if not request.user == trip.user and not request.user.has_perm('catalog.view_trip', trip):
            logout(request)
            return redirect("catalog:ulogin")
        Lodging.objects.get(id=lodging_id).delete()
        return redirect("catalog:detail", trip_id)


class UpdateLodgingView(LoginRequiredMixin, View):

    login_url = "catalog:ulogin"

    def get(self, request, **kwargs):
        lodging_id = self.kwargs['lodging_id']
        trip_id = self.kwargs['trip_id']
        trip = Trip.objects.get(id=trip_id)
        trip = Trip.objects.get(id=trip_id)
        if not request.user == trip.user and not request.user.has_perm('catalog.view_trip', trip):
            logout(request)
            return redirect("catalog:ulogin")
        lodging = Lodging.objects.get(id=lodging_id)
        form = LodgingForm(instance=lodging)
        return render(
            request,
            "catalog/updateLodging.html",
            {"form": form, "lodging": lodging, "trip": trip}
        )

    def post(self, request, **kwargs):
        lodging_id = self.kwargs['lodging_id']
        trip_id = self.kwargs['trip_id']
        lodging = Lodging.objects.get(id=lodging_id)
        trip = Trip.objects.get(id=trip_id)
        form = LodgingForm(request.POST, instance=lodging)
        if form.is_valid():
            form.save()
            return redirect("catalog:lodgingDetail", trip_id, lodging_id)
        else:
            return render(
                request,
                "catalog/updateLodging.html",
                {"form": form, "lodging": lodging, "trip": trip}
            )


class AddTransportView(LoginRequiredMixin, View):  # form made here

    login_url = "catalog:ulogin"

    def post(self, request, **kwargs):
        trip_id = self.kwargs['trip_id']
        form = TransportForm(request.POST)
        if form.is_valid():
            transport = form.save(commit=False)
            transport.trip = Trip.objects.get(id=trip_id)
            transport.save()
            return redirect("catalog:detail", trip_id)
        elif not form.cleaned_data.get("location"):
            messages.info(request, "You need to choose a location")
            context = {"form": form, "trip_id": trip_id, "trip": Trip.objects.get(id=trip_id)}
            return render(request, "catalog/addTransport.html", context)

    def get(self, request, **kwargs):
        trip_id = self.kwargs['trip_id']
        trip = Trip.objects.get(id=trip_id)
        if not request.user == trip.user and not request.user.has_perm('catalog.view_trip', trip):
            logout(request)
            return redirect("catalog:ulogin")
        form = TransportForm()
        context = {"form": form, "trip_id": trip_id, "trip": Trip.objects.get(id=trip_id)}
        return render(request, "catalog/addTransport.html", context)


class RemoveTransportView(LoginRequiredMixin, View):

    login_url = "catalog:ulogin"

    def get(self, request, **kwargs):
        transport_id = self.kwargs['transport_id']
        trip_id = Transport.objects.get(id=transport_id).trip.id
        trip = Trip.objects.get(id=trip_id)
        if not request.user == trip.user and not request.user.has_perm('catalog.view_trip', trip):
            logout(request)
            return redirect("catalog:ulogin")
        Transport.objects.get(id=transport_id).delete()
        return redirect("catalog:detail", trip_id)


class UpdateTransportView(LoginRequiredMixin, View):

    login_url = "catalog:ulogin"

    def get(self, request, **kwargs):
        transport_id = self.kwargs['transport_id']
        trip_id = self.kwargs['trip_id']
        trip = Trip.objects.get(id=trip_id)
        if not request.user == trip.user and not request.user.has_perm('catalog.view_trip', trip):
            logout(request)
            return redirect("catalog:ulogin")
        transport = Transport.objects.get(id=transport_id)
        form = TransportForm(instance=transport)
        return render(
            request,
            "catalog/updateTransport.html",
            {"form": form, "transport": transport, "trip": trip}
        )

    def post(self, request, **kwargs):
        transport_id = self.kwargs['transport_id']
        trip_id = self.kwargs['trip_id']
        transport = Transport.objects.get(id=transport_id)
        trip = Trip.objects.get(id=trip_id)
        form = TransportForm(request.POST, instance=transport)
        if form.is_valid():
            form.save()
            return redirect("catalog:transportDetail", trip_id, transport_id)
        else:
            return render(
                request,
                "catalog/updateTransport.html",
                {"form": form, "transport": transport, "trip": trip}
            )


class SendInviteView(LoginRequiredMixin, View):

    login_url = "catalog:ulogin"

    def get(self, request, **kwargs):
        username = self.kwargs['username']
        trip_id = self.kwargs['trip_id']
        trip = Trip.objects.get(id=trip_id)
        user = User.objects.get(username=username)
        if not request.user == trip.user:
            logout(request)
            return redirect("catalog:ulogin")
        form = InviteForm()
        context = {"user": user, "form": form, "trip": trip}
        return render(request, "catalog/sendInvite.html", context)
    
    def post(self, request, **kwargs):
        username = self.kwargs['username']
        trip_id = self.kwargs['trip_id']
        user = User.objects.get(username=username)
        trip = Trip.objects.get(id=trip_id)
        form = InviteForm(request.POST)
        if form.is_valid():
            if (username == form.cleaned_data.get("username")):
                messages.error(request, "You cannot invite yourself")
                context = {"user": user, "form": form, "trip": trip}
                return render(request, "catalog/sendInvite.html", context)
            elif (User.objects.filter(username=form.cleaned_data.get("username")).exists()):
                try:
                    invite = Invite()
                    invite.invited_user = User.objects.get(username=form.cleaned_data.get("username"))
                    invite.user = user
                    invite.trip = trip
                    invite.save()
                except IntegrityError:
                    messages.error(request, "An invite for this user already exists.") #unique together
                return redirect("catalog:detail", trip_id)
            else:
                messages.error(request, "No such user")
                context = {"user": user, "form": form, "trip": trip}
                return render(request, "catalog/sendInvite.html", context)
        else:
            messages.error(request, "Incorrect form entry")
            context = {"user": user, "form": form, "trip": trip}
            return render(request, "catalog/sendInvite.html", context)


class RemoveInviteView(LoginRequiredMixin, View):

    login_url = "catalog:ulogin"

    # only used by the sender of the invite
    def get(self, request, **kwargs):
        invite_id = self.kwargs['invite_id']
        invite = Invite.objects.get(id=invite_id)
        trip_id = invite.trip.id
        trip = Trip.objects.get(id=trip_id)
        if not request.user == trip.user:
            logout(request)
            return redirect("catalog:ulogin")
        if (invite.invited_user.has_perm('view_trip', invite.trip)):
            remove_perm('view_trip', invite.invited_user, invite.trip)
        invite.delete()
        return redirect("catalog:detail", trip_id)


class PendingInvitesView(LoginRequiredMixin, View):

    login_url = "catalog:ulogin"

    def get(self, request, **kwargs):
        username = self.kwargs['username']
        user = User.objects.get(username=username)
        if not request.user == user:
            logout(request)
            return redirect("catalog:ulogin")
        pending_invites = user.pending_invites.all() #not only pending but also approved ones
        context = {"pending_invites": pending_invites, "username": username}
        return render(request, "catalog/pendingInvites.html", context)


class AcceptInviteView(LoginRequiredMixin, View):

    login_url = "catalog:ulogin"

    def get(self, request, **kwargs):
        invite_id = self.kwargs['invite_id']
        invite = Invite.objects.get(id=invite_id)
        if not request.user == invite.invited_user:
            logout(request)
            return redirect("catalog:ulogin")
        invite.denied = False
        invite.approved = True
        invite.save()
        assign_perm('view_trip', invite.invited_user, invite.trip)
        return redirect("catalog:pendingInvites", request.user.username)


class RejectInviteView(LoginRequiredMixin, View):

    login_url = "catalog:ulogin"
    
    def get(self, request, **kwargs):
        invite_id = self.kwargs['invite_id']
        invite = Invite.objects.get(id=invite_id)
        if not request.user == invite.invited_user:
            logout(request)
            return redirect("catalog:ulogin")
        invite.approved = False
        invite.denied = True
        if (invite.invited_user.has_perm('view_trip', invite.trip)):
            remove_perm('view_trip', invite.invited_user, invite.trip)
        invite.save()
        return redirect("catalog:pendingInvites", request.user.username)


class InvitedTripsView(LoginRequiredMixin, View):

    login_url = "catalog:ulogin"

    def get(self, request, **kwargs):
        username = self.kwargs['username']
        user = User.objects.get(username=username)
        if not request.user == user:
            logout(request)
            return redirect("catalog:ulogin")
        invites = user.pending_invites.all().filter(approved=True, denied=False).order_by('trip__start_date')
        invited_trips = []
        for invite in invites:
            if user.has_perm('catalog.view_trip', invite.trip):
                invited_trips.append(invite.trip)
        paginator = Paginator(invited_trips, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {"page_obj": page_obj, "username": username}
        return render(request, "catalog/invitedTrips.html", context)
