from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import datetime
from .forms import CreateNewsForm
from .models import News

from tenant.models import Tenants


def news_page(request):
    record = News.objects.all()
    context = {
        'user': request.user,
        'record': record,
    }
    return render(request, 'pages/manager/news/news.html', context)


def list_of_tenants(request):
    context = {}

    context.update({
        # 'data': Tenants.objects.all(),
        'data': [1, 2, 3, 4, 5],
    })

    return render(request, 'pages/manager/list_of_tenants.html', context)


@login_required
def create_news_page(request):
    context = {
        'user': request.user,
    }
    if request.method == 'POST':
        createnews = CreateNewsForm(request.POST)
        if createnews.is_valid():
            record = News(
                companyName=request.user,
                publicationTitle=createnews.data['publicationTitle'],
                publicationText=createnews.data['publicationText'],
                publicationDate=datetime.datetime.now(),
            )
            record.save()
            return redirect('news')
    else:
        context['createnews'] = CreateNewsForm(
            initial={
                'companyName': request.user,
            }
        )

    return render(request, 'pages/manager/news/create_news.html', context)
