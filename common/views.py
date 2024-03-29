"""
Используемые модули
"""
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from .forms import FeedbackForm
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from tenant.models import Tenant, Company, Forum, House
from tenant.models import Manager, ManagerRequest
from .models import Admin
from tenant.forms import AppendCompany, ManagerRequestForm

from .forms import LoginForm, SignUpForm, FeedbackForm
from .models import Feedback
from .tasks import send_email


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
            "all_houses": House.objects.all(),
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
            cleaned_data = form.cleaned_data
            user = authenticate(username=cleaned_data['login'],
                                password=cleaned_data['password'])
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
                    elif hasattr(user, 'admin'):
                        if user.admin.is_admin:
                            return redirect('/admin')
                        else:
                            messages.info(request, "Подождите подтверждения вашей регистрации")
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
    context.update({
        "is_tenant": hasattr(request.user, 'tenant'),
        "is_manager": hasattr(request.user, 'manager'),
    })
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
    context.update({
        "is_tenant": hasattr(request.user, 'tenant'),
        "is_manager": hasattr(request.user, 'manager'),
    })
    return render(request, 'accounts/signup/signup_page.html', context)


def admin_signup(request):
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
            first_name = form.cleaned_data.get("first_name")
            second_name = form.cleaned_data.get("last_name")
            admin = Admin.objects.create(user=user, name=first_name, surname=second_name)
            admin.save()
            messages.success(request, "Ваша заявка отправлена")
            return redirect(login_view)
        else:
            context.update({
                'form': SignUpForm(request),
                'error': 'Форма не валидна',
            })
    else:
        context.update({
            'form': SignUpForm(),
        })
    context.update({
        "is_tenant": hasattr(request.user, 'tenant'),
        "is_manager": hasattr(request.user, 'manager'),
    })
    return render(request, 'admin/admin_signup.html', context)


@login_required
def logout_view(request):
    """
    Функция выхода из аккаунта

    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :return: Переход на главную страницу
    """
    logout(request)
    context = {}
    context.update({
        "is_tenant": hasattr(request.user, 'tenant'),
        "is_manager": hasattr(request.user, 'manager'),
    })
    return redirect('/')


def feedback(request):
    """
    Функция отображения страницы для обратной связи

    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :return: Отображене страницы
    """
    feedbacks = Feedback.objects.all()[::-1]

    context = {
        'feedbacks': feedbacks,
    }

    if request.method == "POST":
        form = FeedbackForm(request.POST)
        context.update({
            'form': form,
        })
        if form.is_valid():
            post = form.save(commit=False)
            post.mail = 'juk_feedback_mail@mail.ru'
            post.title_back = 'Отзывы о JUK'
            post.text_back = 'Ваш отзыв успешно отправлен'
            post.finished = 0
            post.text = post.text

            post.save()
            send_email(Feedback.objects.last())

            post.finished = 1
            post.save()

            return redirect('/common/feedback', context)
    else:
        form = FeedbackForm()
        context.update({
            'form': form,
        })
    context.update({
        "is_tenant": hasattr(request.user, 'tenant'),
        "is_manager": hasattr(request.user, 'manager'),
    })
    return render(request, 'pages/feedback.html', context)


@login_required(login_url="/login")
def admin(request):
    """
    Функция отображения страницы админа

    :param request: объект с деталями запроса.
    :return: объект ответа сервера с HTML-кодом внутри
    """
    user = request.user
    if hasattr(request.user, 'tenant'):
        if not user.tenant.is_admin:
            return redirect('/')
    elif hasattr(request.user, 'manager'):
        if not user.manager.is_admin:
            return redirect('/')
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
    context.update({
        "is_tenant": hasattr(request.user, 'tenant'),
        "is_manager": hasattr(request.user, 'manager'),
    })
    return render(request, 'admin/manager_requests.html', context)


def admin_create(request):
    """
    Функция создания админа

    :param request: объект с деталями запроса.
    :return: объект ответа сервера с HTML-кодом внутри
    """
    user = request.user
    if hasattr(request.user, 'tenant'):
        if not user.tenant.is_admin:
            return redirect('/')
    elif hasattr(request.user, 'manager'):
        if not user.manager.is_admin:
            return redirect('/')
    company = Company.objects.filter()
    context = {
        'company': company
    }
    if request.method == 'POST':
        form = AppendCompany(request.POST)
        if form.is_valid():
            inn = form.cleaned_data.get('inn_company')
            name = form.cleaned_data.get('company_name')
            ya_num = form.cleaned_data.get('company_ya_num')
            try:
                check_company = Company.objects.get(inn=inn)
                flag = 0
            except BaseException:
                flag = 1
            if flag:
                if ya_num is None:
                    new_company = Company(inn=inn, name=name, ya_num=-1)
                else:
                    new_company = Company(inn=inn, name=name, ya_num=ya_num)
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
    context.update({
        "is_tenant": hasattr(request.user, 'tenant'),
        "is_manager": hasattr(request.user, 'manager'),
    })
    return render(request, 'admin/create_company.html', context)


def admin_verification(request):
    user = request.user
    if not user.is_superuser:
        return redirect('/')
    admins = Admin.objects.filter(is_admin=0)
    context = {
        'admins': admins,
    }
    if request.method == "POST":
        for request_admin in admins:
            if request.POST.get("agree" + str(request_admin.id)):
                request_admin.is_admin = 1
                request_admin.save()
                messages.success(request, "Новый администратор одобрен")
            elif request.POST.get("refused"+ str(request_admin.id)):
                request_admin.is_admin = 0
                request_admin.save()
                messages.info(request, "Запрос на подключение нового администратора отклонен")
        return redirect(admin_verification)
    context.update({
        "is_tenant": hasattr(request.user, 'tenant'),
        "is_manager": hasattr(request.user, 'manager'),
    })
    return render(request, 'admin/admin_verification.html', context)
