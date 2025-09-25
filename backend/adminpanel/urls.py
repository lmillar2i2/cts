from django.urls import path
from .views import AdminLoginView, ParticipantsAdminListView, DrawWinnerView

urlpatterns = [
    path("login/", AdminLoginView.as_view(), name="admin-login"),
    path("participants/", ParticipantsAdminListView.as_view(), name="admin-participants"),
    path("draw/", DrawWinnerView.as_view(), name="admin-draw"),
]
