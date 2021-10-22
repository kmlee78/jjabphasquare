from django.shortcuts import render


def fs_detail(request):
    return render(request, "fs/index.html")
