from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm

import os

def login(request):
    
    return render(request, 'account/login.html')

def logout(request):
    auth.logout(request)

    return redirect("/login")
