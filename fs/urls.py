from django.urls import path
from . import views

urlpatterns = [
    path("", views.fs_detail, name="fs-page"),
    path("<int: corp_code>/", views.fs_detail, name="fs-detail"),
]
