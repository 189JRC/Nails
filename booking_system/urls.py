from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("appointments.urls")),
    path("api/", include("apis.urls")),
    path("data/", include("data_visualiser.urls")),
    path("user/", include("user_admin.urls")),
    path("manager_admin/", include("manager_admin.urls")),
]
