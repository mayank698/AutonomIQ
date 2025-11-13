from django.urls import path
from . import views

urlpatterns = [
    path("send_emails/", views.send_emails, name="send_emails"),  # type: ignore
    path("track/click/<unique_id>/", views.track_click, name="track_click"),  # type: ignore
    path("track/open/<unique_id>/", views.track_open, name="track_open"),  # type: ignore
    path("track/dashboard/", views.track_dashboard, name="track_dashboard"),  # type: ignore
    path("track/stats/<int:pk>/", views.track_stats, name="track_stats"),  # type: ignore
]
