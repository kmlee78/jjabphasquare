from django.shortcuts import render
from .forms import FilterForm
from .jjabphamining import backtest


def filters(request):
    context = {}
    context["form"] = FilterForm()
    filter_form = FilterForm(request.GET)
    if filter_form.is_valid():
        filters = filter_form.cleaned_data.get("filters")
        data_to_use = filter_form.cleaned_data.get("data_to_use")
        context["filters"] = filters
        if request.method == "POST":
            parameters = request.POST
            history = backtest(data_to_use, parameters)
            context["history"] = history
    return render(request, "strategy/index.html", context)
