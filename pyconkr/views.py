# -*- coding: utf-8 -*-
import datetime

from mail_templated import send_mail
from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from allauth.socialaccount.signals import social_account_added
from django.contrib.auth import login as user_login, logout as user_logout
from django.contrib.auth import get_user_model
from django import template
from django.urls import reverse
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from django.utils.translation import get_language, activate
from django.views.generic import ListView, DetailView
from announcement.models import Announcement

User = get_user_model()


def index(request):
    KST, now = get_KST_now()
    sat_start = datetime.datetime(2020, 9, 26, 10, 0, tzinfo=KST)
    sat_end = datetime.datetime(2020, 9, 26, 17, 30, tzinfo=KST)
    sun_start = datetime.datetime(2020, 9, 27, 10, 0, tzinfo=KST)
    sun_end = datetime.datetime(2020, 9, 27, 17, 30, tzinfo=KST)
    live = False
    if sat_start < now < sat_end or sun_start < now < sun_end:
        live = True
    return render(request, 'index.html', {
        'index': True,
        'recent_announcements': Announcement.objects.filter(active=True),
        'live': live,
    })


def robots(request):
    http_host = request.get_host()
    if http_host is not None and http_host.startswith("dev.pycon.kr"):
        return render(request, 'dev-robots.txt', content_type='text/plain')
    return render(request, 'robots.txt', content_type='text/plain')


def login(request):
    if request.user.is_authenticated:
        return redirect('profile')

    return render(request, 'login.html', {
        'title': _('Login'),
    })


def logout(request):
    user_logout(request)
    return redirect(reverse('index'))


@receiver(user_signed_up)
def user_signed_up_custom(request, user, **kwargs):
    from_email = 'PyCon Korea <pyconkr@pycon.kr>'
    email = user.email
    if not email:
        return
    send_mail('mail/welcome.html', {'user': user},
              from_email, [email], fail_silently=True)


def error_page_404(request, exception):
    path = request.get_full_path()
    if path[:5] != "/2020":
        return redirect("/2020" + path)

    return render(request, 'base.html', {'title': '???????????? ???????????? ?????? ??? ????????????.',
                                         'base_content': '????????? ??????????????????. ?????? ?????? ???????????? ?????? ?????? ??? ????????????.'})


def error_page_500(request):
    return render(request, 'base.html', {'title': '?????? ?????? ????????????.', 'base_content': '?????? ??? ?????? ??????????????????.'})


def get_KST_now():
    KST = datetime.timezone(datetime.timedelta(hours=9))
    now = datetime.datetime.now(tz=KST)
    return KST, now
