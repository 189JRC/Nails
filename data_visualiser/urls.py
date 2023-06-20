from django.urls import path
from . import views

urlpatterns = [
    path("", views.export_apt_data, name="export_users_csv"),
    path("chart/", views.chart_view, name="chart"),
    #path("get_weeks", views.get_weeks, name="get_weeks"),
    path("records/1", views.record_info, name="record_info"),
    path("records/2", views.record_info_2, name="record_info_2"),
    path("records/3", views.record_info_3, name="record_info_3"),
    path("records/4", views.record_info_4, name="record_info_4"),
    # path('full_appointment_data', views.generate_pdf, name='generate_pdf'),
    path("records/5", views.render_df, name="render_df"),
    path("csv_appointment_data", views.export_apt_data, name="csv_appointment_data"),
]
