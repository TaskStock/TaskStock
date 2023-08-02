from django.shortcuts import render

def login(request):
    
    return render(request, 'account/login.html')

def signup1(request):
    return render(request, 'account/signup1.html')


def signup2(request):
    return render(request, 'account/signup2.html')

    
