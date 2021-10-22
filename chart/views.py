from django.shortcuts import render


def chart_detail(request):
    return render(request, "chart/index.html")
