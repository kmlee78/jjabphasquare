from re import template
from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path("", views.chart_page, name="chart-page"),
    path(
        "detail/",
        TemplateView.as_view(template_name="chart/detail.html"),
        name="chart-detail",
    ),
]
