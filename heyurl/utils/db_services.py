from collections import Counter
from jsonview.decorators import json_view
from heyurl import models
from heyurl.utils import helper

dh = helper.DataHelper()


def get_url_by_original(original_url):
    return models.Url.objects.filter(original_url=original_url).first()


def get_url_by_short(short_url):
    # breakpoint()
    return models.Url.objects.filter(short_url=short_url).first()


def create_short_url(original_url):
    key = 'a'
    while models.Url.objects.filter(short_url=key).exists():
        key = helper.key_gen()

    url = models.Url()
    url.original_url = original_url
    url.short_url = key
    url.save()
    return url


def save_click(short_url, browser, platform):
    if url := get_url_by_short(short_url):
        click = models.Click()
        click.url = url
        click.browser = browser
        click.platform = platform
        click.save()
        url.clicks += 1
        url.save()
    return url


def _get_top_n_metrics(clicks):

    cnt_browser = Counter()
    cnt_platform = Counter()

    for click in clicks:
        cnt_browser[click.browser] += 1
        cnt_platform[click.platform] += 1

    metrics = dict(browsers=dict(cnt_browser), platforms=dict(cnt_platform))
    return metrics


def get_top_metrics(n=10, host=dh.host):
    top_urls = models.Url.objects.all().order_by('-clicks')[:n]
    data = []
    for url in top_urls:
        metrics = _get_top_n_metrics(url.related_clicks.all())
        data.append(
            dict(
                type='urls',
                id=url.id,
                atributes=dict(
                    created_at=url.created_at,
                    original_url=url.original_url,
                    url=f'{host}/{url.short_url}',
                    clicks=url.clicks
                ),
                relationships=dict(
                    metrics=metrics
                )
            )
        )

    return data







