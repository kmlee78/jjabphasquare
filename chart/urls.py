from django.urls import path
from . import views

urlpatterns = [
    path("", views.chart_page, name="chart-page"),
    path("detail/", views.chart_detail, name="chart-detail"),
    path("detail/<int:corp_code>", views.chart_load, name="chart-load"),
]
