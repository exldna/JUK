"""
Используемые модули
"""
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, SignUpForm
from django.core.mail import send_mail
from .forms import FeedbackForm
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from tenant.models import Tenant, Company, Forum, House
from tenant.models import Manager, ManagerRequest
from tenant.forms import ManagerRequestForm, AppendCompany


def _get_base_context(title, sign_in_button=True):
    """
    Функция создания базового словаря

    :param title: Название страницы
    :param sign_in_button: Наличие кнопки авторизации
    :return: Базовый словарь
    """
    context = {
        'title': title,
        'if_sign_but': sign_in_button,

    }
    return context


def index_view(request):
    """
    Функция для отображения основной страницы

    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :return: Отображение страницы
    """
    context = _get_base_context('JUK')
    if request.user is not AnonymousUser:
        context.update({
            "is_tenant": hasattr(request.user, 'tenant'),
            "is_manager": hasattr(request.user, 'manager'),
        })
    return render(request, 'pages/index.html', context)


def login_view(request):
    """
    Функция отображения авторизации

    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :return: Возврат на основную страницу при успешной авторизации
    :return: Отображение страницы
    """
    context = _get_base_context('login', False)
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['login'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if hasattr(user, 'tenant'):
                        if user.tenant.is_admin:
                            return redirect('/admin')
                        return redirect('/tenant')
                    if hasattr(user, 'manager'):
                        if user.manager.is_admin:
                            return redirect('/admin')
                        return redirect('/manager')
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
    """
    Функция отображения страницы регистрации

    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :return: Возвращение на главную страницу при успешной авториации
    :return: Отображение страницы
    """
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
                return redirect('/tenant')
            elif role == "manager":
                manager = Manager.objects.create(user=user)
                manager.save()
                return redirect('/manager')
            
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


@login_required
def logout_view(request):
    """
    Функция выхода из аккаунта

    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :return: Переход на главную страницу
    """
    logout(request)
    return redirect('/')


def feedback(request):
    """
    Функция отображения страницы для обратной связи

    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :return: Отображене страницы
    """
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


@login_required(login_url="/login")
def admin(request):
    user = request.user
    if hasattr(request.user, 'tenant'):
        if not user.tenant.is_admin:
            return HttpResponse("Nice try, bro", status=401)
    elif hasattr(request.user, 'manager'):
        if not user.manager.is_admin:
            return HttpResponse("Nice try, bro", status=401)
    manager_requests = ManagerRequest.objects.filter(status=3)
    context = {
        'requests': manager_requests,
    }
    if request.method == "POST":
        for request_man in manager_requests:
            if request.POST.get("agree"+str(request_man.id)):
                manager_id = request_man.author_id
                managers = Manager.objects.filter(user_id=manager_id)
                for manager in managers:
                    if manager.user_id == manager_id:
                        company = Company.objects.filter(inn=request_man.inn_company)
                        for comp in company:
                            if comp.inn == request_man.inn_company:
                                manager.company_id = comp.id
                                manager.save(update_fields=['company_id'])
                request_man.status = 1
                request_man.save()
            elif request.POST.get("refused" + str(request_man.id)):
                request_man.status = 2
                request_man.save()
        return redirect(admin)
    return render(request, 'admin/manager_requests.html', context)


def admin_create(request):
    user = request.user
    if hasattr(request.user, 'tenant'):
        if not user.tenant.is_admin:
            return HttpResponse("Nice try, bro", status=401)
    elif hasattr(request.user, 'manager'):
        if not user.manager.is_admin:
            return HttpResponse("Nice try, bro", status=401)
    company = Company.objects.filter()
    context = {
        'company': company
    }
    if request.method == 'POST':
        form = AppendCompany(request.POST)
        if form.is_valid():
            inn = form.cleaned_data.get('inn_company')
            name = form.cleaned_data.get('company_name')
            try:
                check_company = Company.objects.get(inn=inn)
                flag = 0
            except BaseException:
                flag = 1
            if flag:
                new_company = Company(inn=inn, name=name)
                new_company.save()
                new_company_forum = Forum.objects.create(company=new_company, categories="Объявления|Другое")
                new_company_forum.save()
                messages.success(request, "УК добавлена")
            else:
                messages.info(request, 'УК с указанным ИНН уже существует')
            return redirect(admin_create)
    else:
        form = AppendCompany()
    context.update({
        'form': form
    })
    return render(request, 'admin/create_company.html', context)


class HouseContext:
    def __init__(self, address, company_name):
        self.address = address
        self.company_name = company_name


import random


def config_view(request):
    IN = open('common/static/houses-companies.txt', 'r')

    all = IN.readlines()
    # ДОБАВЛЕНИЕ ДОМОВ
    out_hous = {}
    out_hous1 = []


    for i in range(len(all)):
        line = all[i]
        skip = False
        for j in range(len(line) - 1):
            if 'А' <= line[j] <= 'Я' and 'А' <= line[j + 1] <= 'Я' and not skip:
                if line[len(line) - 1] == '\n':
                    com = line[j:-1]
                else:
                    com = line[j:]

                hou = line[:j]
                while hou[len(hou) - 1] == ' ':
                    hou = hou[:-1]

                out_hous1.append((hou, com))

                out_hous.update({
                    hou: com
                })
                skip = True

    print(len(out_hous.keys()))

    if request.method == 'POST':
        for k in out_hous.keys():
            if len(House.objects.filter(address=k)) == 0:
                print(k, out_hous.get(k))
                if len(Company.objects.filter(name=out_hous.get(k))) == 0:
                    new_company = Company(inn=random.randint(770000000000, 779999999999), name=out_hous.get(k))
                    new_company.save()
                house = House.objects.create(
                    address=k,
                    company=Company.objects.filter(name=out_hous.get(k))[0],
                )
                house.save()
                forum = Forum.objects.create(
                    house=house,
                    categories="Вода|Электричество|Петиции|Объявления|Пропажи|Другое",
                )
                forum.save()
        for c in Company.objects.all():
            forum = Forum.objects.create(
                company=c,
                categories="Новости|Петиции|Отчёты компании|Другое",
            )
            forum.save()

    return render(request, 'pages/config.html', {})
