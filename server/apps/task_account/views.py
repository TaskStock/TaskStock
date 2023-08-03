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
            
            if request.user.email == '':
                return redirect('/signup/step2/')
            else:
                return redirect('/main/')
        else:
            context = {
                'form': form,
            }
            return render(request, 'account/login.html', context=context)
    else:
        auth.logout(request)

        form = AuthenticationForm()
        context = {
            'form': form,
        }
        return render(request, 'account/login.html', context=context)

def logout(request):
    auth.logout(request)

    return redirect("/login/")


def signup1(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()

            user.backend = 'django.contrib.auth.backends.ModelBackend'
            auth.login(request, user)

            return redirect('/signup/step2/')
        else:
            
            ctx={
                'form':form,
            }
            return render(request, 'account/signup1.html',context=ctx)
    else:
        form = SignupForm()
        ctx = {
            'form': form,
        }
        return render(request, template_name='account/signup1.html', context=ctx)

def signup2(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        request.user.email = email
        request.user.save()

        return redirect('/main/')


    return render(request, 'account/signup2.html')