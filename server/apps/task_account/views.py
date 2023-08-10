from django.shortcuts import render, redirect
from .models import *

from django.contrib.auth import authenticate, login, logout
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignupForm

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Value, Category

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
            error_message = "로그인에 실패했습니다. 아이디와 비밀번호를 확인해주세요."
            context = {
                'form': form,
                'error_message': error_message,
            }
            return render(request, 'account/login.html', context=context)
    else:
        auth.logout(request)

        form = AuthenticationForm()
        context = {
            'form': form,
        }
        return render(request, 'account/login.html', context=context)
    
@csrf_exempt
def find_password(request):
    if request.method == 'POST':
        password=request.POST.get('password')
        password_check=request.POST.get('password-check')
        username=request.POST.get('username')

        if password==password_check:
            user=User.objects.get(username=username)
            user.set_password(password)
            return JsonResponse({"success": True, "redirect": '/login/'})
        else:
            return JsonResponse({"success": False, "redirect": ''})


    context = {
    }
    return render(request, 'account/find_password.html', context=context)

@csrf_exempt
def check_id(request):
    username = request.POST.get("id")

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({"result": False, "email": "", "username": ""})
    
    if user.is_superuser:
        return JsonResponse({"result": False, "email": "", "username": ""})
    
    return JsonResponse({"result": True, "email": user.email, "username": username})

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


@csrf_exempt
def signup2(request):

    if request.method == 'POST':
        check_code = request.POST.get('check_code')
        check_email = request.POST.get('check_email')
        input_code = request.POST.get('signup-code')

        if check_code != '' and check_email != '' and check_code == input_code:
            request.user.email = check_email
            request.user.save()
            response_data = {'redirect': '/main/'}
            return JsonResponse(response_data)

        if check_code == '':
            error_message = "먼저 인증코드 메일을 받으세요."
        elif check_email == '':
            error_message = "이메일이 올바른지 확인하세요."
        else:
            error_message = "코드가 올바르지 않습니다."

        response_data = {'error_message': error_message, 'redirect': ''}
        return JsonResponse(response_data)

    return render(request, 'account/signup2.html')

from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError

import random
import string

from django.core.mail import EmailMessage

@csrf_exempt
def email_validation(request):
    email = request.POST.get("email")
    type = request.POST.get("type")

    if type=="email_validation":
        # 이메일 형식 검증
        email_validator = EmailValidator()
        try:
            email_validator(email)  # 이메일 형식이 올바르지 않으면 ValidationError 발생
        except ValidationError:
            response_data = {'error': True}
            return JsonResponse(response_data, status=400)

    # 이메일 중복 검사 필요
    # 이메일 중복 허용할 것인지?

    code = ''.join(random.choices(string.digits, k=6))

    # 이메일 보내기
    if type=="email_validation":
        email_send = EmailMessage(
            'TaskStock 이메일 인증 코드',
            '안녕하세요! TaskStock에 오신 것을 환영합니다! 다음 인증 코드를 입력해주세요.\n'+code,
            to=[email],
        )
    elif type=="find_password":
        email_send = EmailMessage(
            'TaskStock 비밀번호 변경 인증 코드',
            '안녕하세요! 비밀번호 변경을 위해 다음 인증 코드를 입력해주세요.\n'+code,
            to=[email],
        )
    email_send.send()

    response_data = {'error': False, 'code': code, 'email': email,}

    return JsonResponse(response_data)