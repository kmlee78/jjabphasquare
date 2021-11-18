from django.shortcuts import render


def start_page(request):
    return render(request, "main/title.html")
