from django.shortcuts import render

# Create your views here.
# ---정근 작업---#

# ---환희 작업---#


def home(request):
    return render(request, 'base.html')
# ---세원 작업---#

# ---지수 작업---#

# ---선우 작업---#


def search(request):
    return render(request, 'main/search.html')

def settings(request):
    return render(request, 'main/settings.html')
