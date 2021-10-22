from django.urls import path
from . import views

urlpatterns = [
    path("", views.filters, name="strategy-page"),
]
