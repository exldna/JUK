from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, SignUpForm
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .forms import FeedbackForm

from tenant.models import Tenant, Company, House
from manager.models import Manager


def _get_base_context(title, sign_in_button=True):
    context = {
        'title': title,
        'if_sign_but': sign_in_button,

    }
    return context


def index_view(request):
    context = _get_base_context('JUK')
    return render(request, 'pages/index.html', context)


def login_view(request):
    context = _get_base_context('login', False)
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['login'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/')
                else:
                    context.update({
                        'error': 'Аккаунт отключён',
                    })
            else:
                context.update({
                    'error': 'Неправильный логин или пароль',
                })
    else:
        form = LoginForm()
    context.update({'form': form})
    return render(request, 'accounts/login/login_page.html', context)


def signup_view(request):
    context = _get_base_context('sign up', False)
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            print('save form')
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            role = request.POST.get('role')
            if role == "tenant":
                tenant = Tenant.objects.create(user=user)
                tenant.save()

            elif role == "manager":
                manager = Manager.objects.create(user=user)
                manager.save()

            return redirect('/')
        else:
            context.update({
                'form': SignUpForm(request),
                'error': 'Форма не валидна',
            })
    else:
        context.update({
            'form': SignUpForm(),
        })
    return render(request, 'accounts/signup/signup_page.html', context)


def logout_view(request):
    logout(request)
    return redirect('/')


def feedback(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)

        if form.is_valid():
            subject = str(form.data['subject'])
            message = str(form.data['message'])
            user_mail = str(form.data['user_mail'])
            mail = 'juk_feedback_mail@mail.ru'
            subject_back = 'Отзывы о JUK'
            message_back = 'Ваш отзыв успешно отправлен'

            context = {
                'subject': subject,
                'message': message,
                'user_mail': user_mail,

            }

            message = 'Отправитель: ' + user_mail + '\n'\
                      + '\n' + message

            # TODO: оформление при помощи django forms
            # TODO: валидация входных параметров

            message = 'Отправитель: ' + user_mail + '\n' + '\n' + message

            # TODO: вынести отправку письма в отдельный субпроцесс (при помощи celery)
            send_mail(subject, message, mail,
                      [mail], fail_silently=False)

            send_mail(subject_back, message_back, mail,
                      [user_mail], fail_silently=False)

        else:
            pass

    return render(request, 'pages/feedback.html')
