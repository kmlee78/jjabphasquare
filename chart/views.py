from django.shortcuts import render
from main.models import CorpModel
from .forms import ChartForm
from .jjabphachart import get_chart


def chart_page(request):
    context = {}
    context["form"] = ChartForm()
    context["corp"] = None
    context["post_received"] = False
    if request.method == "POST":
        context["post_received"] = True
        form = ChartForm(request.POST)
        if form.is_valid():
            corp_name = request.POST["corp_name"]
            period = request.POST["period"]
            moving_average = form.cleaned_data.get("moving_average")
            try:
                corp = CorpModel.objects.get(corp_name=corp_name)
                stock_code = corp.stock_code
                get_chart(stock_code, period, moving_average)
                context["corp"] = corp
            except Exception:
                pass

    return render(request, "chart/index.html", context=context)
