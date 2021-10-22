from django.urls import path
from . import views

urlpatterns = [
    path("", views.start_page, name="start-page"),
    path("main/", views.main_page, name="main-page"),
]
