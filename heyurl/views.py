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


# @json_view
def store(request):
    # FIXME: Insert a new URL object into storage
    original_url = request.POST.get('original_url')
    validator = URLValidator()
    try:
        validator(original_url)
    except ValidationError:
        return HttpResponse(f'Invalid Url:<br>{original_url}')

    if existing_url := db_services.get_url_by_original(original_url):
        url_serialized = serializers.serialize('json', [existing_url,])
        return HttpResponse(f'Original url already exists:<br>{url_serialized}')

    url = db_services.create_short_url(original_url)
    url_serialized = serializers.serialize('json', [url])
    return HttpResponse(f"Storing a new URL object into storage<br>{url_serialized}")


def short_url(request, short_url):
    # FIXME: Do the logging to the db of the click with the user agent and browser
    return HttpResponse("You're looking at url %s" % short_url)


def _update_clicks(request, _short_url):
    target_url = None
    if url := db_services.get_url_by_short(_short_url):
        click = models.Click()
        browser, platform = helper.get_data_clicks(get_user_agent(request))
        click = db_services.save_click(_short_url, browser, platform)
        target_url = url.original_url
    return target_url

@json_view
def handler404(request, exception):
    url_fragments = [fragment for fragment in request.path.split('/') if fragment]
    if len(url_fragments) == 1:
        if target_url := _update_clicks(request, url_fragments[0]):
            return redirect(target_url)
    return render(request, 'heyurl/404.html')
