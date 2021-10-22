from django.urls import path
from . import views

urlpatterns = [
    path("", views.chart_detail, name="chart-page"),
    path("<int: corp_code>/", views.chart_detail, name="chart-detail"),
]
