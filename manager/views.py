from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import datetime
from .forms import CreateNewsForm
from .models import News


def get_base_context(title, sign_in_button=True):
    context = {

        'background_color': '#F4FFE6',
        'header_color': '#8CFF00',
        'header_text_color1': '#F4FFE6',
        'header_text_color2': '#85D523',
        'footer_color': '#85D523',
        'footer_text_color1': '#F4FFE6',
        'footer_text_color2': '#6CC400',

        'title': title,
        'if_sign_but': sign_in_button,

    }
    return context


def news_page(request):
    context = get_base_context('News')
    record = News.objects.all()
    context.update({
        'user': request.user,
        'record': record,
    })
    return render(request, 'pages/manager/news/news.html', context)


@login_required
def create_news_page(request):
    context = get_base_context('Create news')
    context.update({
        'user': request.user,
    })
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
