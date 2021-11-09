from django.shortcuts import render
from .forms import FilterForm
from .jjabphamining import get_history
from .backtest import rebalanced_inputs, get_backtest_page
from .diagnosis import summary


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
            history = get_history(data_to_use, parameters)
            context["history"] = history
            portfolio_rtn, benchmark_rtn = rebalanced_inputs(history)
            get_backtest_page(portfolio_rtn, benchmark_rtn)
            diagnosis_summary = summary(portfolio_rtn, benchmark_rtn)
            context["summary"] = diagnosis_summary
    return render(request, "strategy/index.html", context)


def result(request):
    return render(request, "strategy/detail.html")
