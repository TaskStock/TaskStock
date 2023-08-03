from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignupForm

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            print('form is valid')
            return redirect('/')
        else:
            print('form isnt valid')
            context = {
                'form': form,
            }
            return render(request, 'account/login.html', context=context)
    else:
        print("form print")
        form = AuthenticationForm()
        context = {
            'form': form,
        }
        return render(request, 'account/login.html', context=context)

def logout(request):
    auth.logout(request)

    return redirect("/login/")
  
def signup1(request):
    return render(request, 'account/signup1.html')


def signup2(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()

            user.backend = 'django.contrib.auth.backends.ModelBackend'
            auth.login(request, user)

            print('signup is valid')

            return redirect('/login/')
        else:
            print('signup is invalid')
            
            ctx={
                'form':form,
            }
            return render(request, 'account/signup2.html',context=ctx)
    else:
        form = SignupForm()
        print('signup page')
        ctx = {
            'form': form,
        }
        return render(request, template_name='account/signup2.html', context=ctx)