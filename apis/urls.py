from django.urls import path
from . import views

urlpatterns = [
    path("appointments/management", views.AppointmentManagement.as_view()),
    path("appointments/view", views.AppointmentView.as_view()),
    path(
        "appointments/<int:appointment_id>/book/",
        views.AppointmentBookingView.as_view(),
        name="appointment-booking",
    ),
    path(
        "appointments/<int:appointment_id>/cancel",
        views.AppointmentCancellationView.as_view(),
        name="appointment-cancel",
    ),
    path(
        "my_appointments/<int:customer_id>",
        views.MyAppointments.as_view(),
        name="my_appointments",
    ),
    path("create_record/<int:id>", views.create_record, name="create_record"),
]
