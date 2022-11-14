from django.urls import path
from applications.factchecker import views

urlpatterns = [
    path("health/", views.health),
]