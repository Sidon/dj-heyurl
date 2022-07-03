from datetime import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django_user_agents.utils import get_user_agent
from django.core.validators import URLValidator, ValidationError
from jsonview.decorators import json_view

from .models import Url
from heyurl.utils import db_services, helper


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
    except URLValidator:
        return HttpResponse("invalid URL")

    if existing_url := db_services.get_by_original(original_url):
        return HttpResponse("URL Exists")

    db_services.create_short_url(original_url)
    return HttpResponse("Storing a new URL object into storage")


def _update_clicks(request, short_url):
    if url := db_services.get_by_short(short_url):
        browser, platform = helper.get_data_clicks(get_user_agent(request))
        db_services.save_click(short_url, browser, platform)
    return url


def redirect_short_url(request, short_url):
    # FIXME: Do the logging to the db of the click with the user agent and browser
    if not (target_url := _update_clicks(request, short_url)):
        return HttpResponse('Invalid Url')
    return redirect(target_url.original_url)


# Placeholders #
################################

def handler404(request, exception):
    fragments = [f for f in request.path.split('/') if f]
    if len(fragments) == 1:
        if url := _update_clicks(request, fragments[0]):
            try:
                return redirect(url.original_url)
            except exception:
                print(exception)
    return render(request, 'heyurl/404.html')


@json_view
def month_metrics(request):
    if short_url := request.GET.get('short_url', None):
        if db_services.get_by_short(short_url):
            today = datetime.today()
            month = request.GET.get('month', today.month)
            year = request.GET.get('year', today.year)
            return [db_services.get_metrics(short_url, year, month)]
    return render(request, 'heyurl/404.html')


@json_view
def top_ten(request):
    return db_services.get_top_metrics()
