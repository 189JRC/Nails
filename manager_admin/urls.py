from django.urls import path
from . import views

app_name = "manager_admin"

urlpatterns = [
    path("planner", views.planner, name="planner"),
    path("home/", views.home, name="home"),
    path("generate", views.generate, name="generate"),
    path("delete_apt/<int:id>", views.delete_apt, name="delete_apt"),
    path("delete_apt/<int:id>", views.delete_apt, name="delete_apt"),
]
