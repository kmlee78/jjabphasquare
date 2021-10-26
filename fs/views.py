from django.shortcuts import render
from main.models import CorpModel
from .forms import FSForm
from .jjabphacrawler import get_rcept_no, get_url


def fs_page(request):
    context = {}
    context["form"] = FSForm()
    context["url"] = None
    if request.method == "POST":
        form = FSForm(request.POST)
        if form.is_valid():
            corp_name = form.cleaned_data.get("corp_name")
            bsns_year = int(form.cleaned_data.get("bsns_year"))
            quarter = int(form.cleaned_data.get("quarter"))
            connected = form.cleaned_data.get("connected")
            print(corp_name, bsns_year, quarter, connected)

            try:
                corp = CorpModel.objects.get(corp_name=corp_name)
                corp_code = corp.corp_code
                rcept_no = get_rcept_no(corp_code, bsns_year, quarter)
                url = get_url(rcept_no, connected)
                context["corp"] = corp
                context["url"] = url
            except Exception:
                pass

    return render(request, "fs/index.html", context=context)
