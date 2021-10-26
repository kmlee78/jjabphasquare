from django.urls import path
from . import views

urlpatterns = [
    path("", views.fs_page, name="fs-page"),
]
