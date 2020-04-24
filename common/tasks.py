# main/tasks.py

import logging

from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from juk.juk.celery import app
from .models import Feedback


@app.task
def send_email():
    all_feedback = Feedback.objects.all()

    for mail in all_feedback:

        if mail.finished == 1:
            continue

        send_mail(mail.title, mail.text, mail.host,
                  [mail.host], fail_silently=False)

        send_mail(mail.title, mail.text, mail.host,
                  [mail.author], fail_silently=False)

        mail.finished = 1
