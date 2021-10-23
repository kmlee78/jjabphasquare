from django.urls import path
from . import views

urlpatterns = [
    path("", views.chart_page, name="chart-page"),
    path("detail/load/", views.chart_load, name="chart-load"),
    path("detail/<str:stock_code>/", views.chart_detail, name="chart-detail"),
]
