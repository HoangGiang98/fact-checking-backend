from django.urls import path, include
from . import views

urlpatterns = [
    path("health/", views.health),
    path("verify/", views.verify),
    path("history/", views.history),
]
