from django.shortcuts import render
from .forms import FilterForm


def filters(request):
    context = {}
    context["form"] = FilterForm()
    filter_form = FilterForm(request.GET)
    if filter_form.is_valid():
        filters = filter_form.cleaned_data.get("filters")
        context["filters"] = filters
    return render(request, "strategy/index.html", context)
