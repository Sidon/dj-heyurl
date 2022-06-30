from django.shortcuts import render, redirect
from django.http import HttpResponse
from django_user_agents.utils import get_user_agent

from . import models
from .models import Url
from heyurl.utils import db_services, data_helper


def index(request):
    urls = Url.objects.order_by('-created_at')
    context = {'urls': urls}
    return render(request, 'heyurl/index.html', context)


def store(request):
    # FIXME: Insert a new URL object into storage
    return HttpResponse("Storing a new URL object into storage")


def short_url(request, short_url):
    # FIXME: Do the logging to the db of the click with the user agent and browser
    return HttpResponse("You're looking at url %s" % short_url)


def _update_clicks(request, _short_url):
    target_url = None
    if url := db_services.get_url_by_short(_short_url):
        click = models.Click()
        browser, platform = data_helper.get_data_clicks(get_user_agent(request))
        click = db_services.save_click(_short_url, browser, platform)
        target_url = url.original_url
    return target_url


def handler404(request, exception):
    url_fragments = [fragment for fragment in request.path.split('/') if fragment]
    if len(url_fragments) == 1:
        if target_url := _update_clicks(request, url_fragments[0]):
            return redirect(target_url)
    return render(request, 'heyurl/404.html')
