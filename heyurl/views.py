from datetime import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django_user_agents.utils import get_user_agent
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.core import serializers
from jsonview.decorators import json_view

from . import models
from .models import Url
from heyurl.utils import db_services, helper

dh = helper.DataHelper()


def index(request):
    urls = Url.objects.order_by('-created_at')
    context = {'urls': urls}
    return render(request, 'heyurl/index.html', context)


def store(request):
    # FIXME: Insert a new URL object into storage
    original_url = request.POST.get('original_url')
    validator = URLValidator()
    try:
        validator(original_url)
    except ValidationError:
        return HttpResponse(f'Invalid Url:<br>{original_url}')

    if existing_url := db_services.get_url_by_original(original_url):
        url_serialized = serializers.serialize('json', [existing_url, ])
        return HttpResponse(f'Original url already exists:<br>{url_serialized}')

    url = db_services.create_short_url(original_url)
    url_serialized = serializers.serialize('json', [url])
    return HttpResponse(f"Storing a new URL object into storage<br>{url_serialized}")


def _update_clicks(request, _short_url):
    if url := db_services.get_url_by_short(_short_url):
        click = models.Click()
        browser, platform = helper.get_data_clicks(get_user_agent(request))
        click = db_services.save_click(_short_url, browser, platform)
    return url


def short_url(request, _short_url):
    # FIXME: Do the logging to the db of the click with the user agent and browser
    if not (target_url := _update_clicks(request, _short_url)):
        return HttpResponse(f'Invalid Url:<br>{_short_url}')

    return redirect(target_url.original_url)
    # return HttpResponse("You're looking at url %s" % short_url)


@json_view
def handler404(request, exception):
    url_fragments = [fragment for fragment in request.path.split('/') if fragment]
    if len(url_fragments) == 1:
        if url := _update_clicks(request, url_fragments[0]):
            return redirect(url.original_url)
    return render(request, 'heyurl/404.html')

@json_view
def month_metrics(request):
    valid_query = False
    if _short_url := request.GET.get('short_url', None):
        if db_services.get_url_by_short(_short_url):
            today = datetime.today()
            month = request.GET.get('month', today.month)
            year = request.GET.get('year', today.year)
            valid_query = True

    if not valid_query:
        return render(request, 'heyurl/404.html')

    metrics = [db_services.get_metrics(_short_url, year, month)]
    return metrics

@json_view
def top_ten(request):
    return db_services.get_top_metrics()

