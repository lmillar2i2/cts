from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("verify/<str:token>/", views.VerifyView.as_view(), name="verify"),
    path("set-password/", views.SetPasswordView.as_view(), name="set-password"),
]
