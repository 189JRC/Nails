from django.urls import path
from . import views

urlpatterns = [
    path("appointments", views.user_home, name="appointments"),
]
