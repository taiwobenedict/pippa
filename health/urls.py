from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name ="home" ),
    path("auth/<str:page>/", views.auth, name = "auth"),
    path('stress-report', views.stress_report, name="stress-report"),
    path('programs/', views.programs, name="programs")
]
