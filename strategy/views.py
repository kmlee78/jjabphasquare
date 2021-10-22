from django.shortcuts import render

# Create your views here.
def filters(request):
    return render(request, "strategy/index.html")
