from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.user_login, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
]
