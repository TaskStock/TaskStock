from django.shortcuts import render, redirect
from .models import *

from django.contrib.auth import authenticate, login, logout
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignupForm

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from .models import Value, Category

from django.utils import timezone
from datetime import timedelta

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()

            today = timezone.now().date()
            ten_days_ago = today - timedelta(days=10)

            if user.last_login.date()<ten_days_ago:
                Alarm.objects.create(
                    user=user,
                    content="오랜만에 돌아오신 것을 환영합니다!",
                    alarm_type="account",
                )

            auth.login(request, user)
            
            if not request.user.custom_active:
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

        if password=="":
            return JsonResponse({"error_text": "변경할 비밀번호를 입력해주세요.", "redirect": ''})
        elif password==password_check:
            user=User.objects.get(username=username)
            user.set_password(password)
            return JsonResponse({"error_text": "", "redirect": '/login/'})
        else:
            return JsonResponse({"error_text": "비밀번호가 일치하지 않습니다. 다시 입력해 주세요.", "redirect": ''})


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
            user.custom_active=True
            user.save()

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
@login_required
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

import smtplib
from django.http import Http404

from decouple import config

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
    try:
        smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_server.starttls()

        EMAIL_HOST_USER = config('EMAIL_HOST_USER')
        EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
        smtp_server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)

        EMAIL_LINK = config('EMAIL_LINK')

        if type=="email_validation":
            user=request.user
            user.email=email
            user.save()

            subject = 'Activate Your Account'
            message = f'Click the link to activate your account: {EMAIL_LINK}/activate/{user.username}/'
        elif type=="find_password":
            username = request.POST.get("username")
            user=User.objects.get(username=username)

            subject = 'Change Your Password'
            message = f'Please enter the following authentication code to change the password.\n {code}'

        sender_email = EMAIL_HOST_USER
        recipient_email = email
            
        msg = f'Subject: {subject}\n\n{message}'
        smtp_server.sendmail(sender_email, recipient_email, msg.encode('utf-8'))

    except smtplib.SMTPException as e:
        print("An error occurred:", str(e))
    finally:
        smtp_server.quit()

    response_data = {'error': False, 'code': code, 'email': email,}

    return JsonResponse(response_data)

def activate_account(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404("User does not exist")
    
    user.custom_active=True
    user.save()

    return redirect('/login/')
