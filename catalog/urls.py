from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views


app_name = "catalog"
urlpatterns = [
    path("home/<str:username>/", views.HomeView.as_view(), name="home"), #as_view is a function of View base class
    path("home/<str:username>/add_trip", views.AddTripView.as_view(), name="addTrip"),
    path("home/remove_trip/<int:trip_id>/", views.RemoveTripView.as_view(), name="removeTrip"),
    path("home/update_trip/<int:trip_id>/", views.UpdateTripView.as_view(), name="updateTrip"),

    path("home/<int:trip_id>/add_lodging", views.AddLodgingView.as_view(), name="addLodging"),
    path("home/remove_lodging/<int:lodging_id>/", views.RemoveLodgingView.as_view(), name="removeLodging"),
    path("home/update_lodging/<int:trip_id>/<int:lodging_id>/", views.UpdateLodgingView.as_view(), name="updateLodging"),

    path("home/<int:trip_id>/add_transport", views.AddTransportView.as_view(), name="addTransport"),
    path("home/remove_transport/<int:transport_id>/", views.RemoveTransportView.as_view(), name="removeTransport"),
    path("home/update_transport/<int:trip_id>/<int:transport_id>/", views.UpdateTransportView.as_view(), name="updateTransport"),

    path("home/<int:trip_id>/add_stop", views.AddStopView.as_view(), name="addStop"),
    path("home/remove_stop/<int:stop_id>/", views.RemoveStopView.as_view(), name="removeStop"),
    path("home/update_stop/<int:trip_id>/<int:stop_id>/", views.UpdateStopView.as_view(), name="updateStop"),
    path("trips/<int:trip_id>/", views.DetailView.as_view(), name="detail"), #class based view kullanınca as_view dedik
    path("stops/<int:trip_id>/<int:stop_id>/", views.StopDetailView.as_view(), name="stopDetail"),
    path("lodgings/<int:trip_id>/<int:lodging_id>/", views.LodgingDetailView.as_view(), name="lodgingDetail"), 
    path("transports/<int:trip_id>/<int:transport_id>/", views.TransportDetailView.as_view(), name="transportDetail"),
    path('login/', views.userLoginView.as_view(), name='ulogin'),
    path('signup/', views.userSignupView.as_view(), name='usignup'),
    path('logout/', views.userLogoutView.as_view(), name='ulogout'),
    path("send_invite/<str:username>/<int:trip_id>/", views.SendInviteView.as_view(), name="sendInvite"),
    path("remove_invite/<int:invite_id>/", views.RemoveInviteView.as_view(), name="removeInvite"),
    path("pending_invites/<str:username>/", views.PendingInvitesView.as_view(), name="pendingInvites"),
    path("accept_invite/<int:invite_id>/", views.AcceptInviteView.as_view(), name="acceptInvite"),
    path("reject_invite/<int:invite_id>/", views.RejectInviteView.as_view(), name="rejectInvite"),
    path("invited_trips/<str:username>/", views.InvitedTripsView.as_view(), name="invitedTrips"),
    #path("add_file/<str:username>/<str:category>/<int:id>", views.AddFile.as_view(), name="addFile"),

] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# path "detail" was "<int:pk>" before, than it became "trips/<int:pk>/". Since I named it as "detail", I don't 
# need to update it anywhere. (Now it no longer needs to be pk bc I stopped using genericView)