from django.contrib.sites.shortcuts import get_current_site
from dataclasses import dataclass, field
from collections import namedtuple
import string
import secrets


@dataclass
class DataHelper:
    chars: str = f'{string.ascii_uppercase}{string.ascii_lowercase}{string.digits}'
    max_length: int = 5
    original_url: str = 'http://fullstacklabs.com'
    short_url: str = 'a'
    invalid_url: str = 'invalid#url'
    new_urls: list = field(default_factory=lambda: ['http://t.me', 'http://z.com'])
    host: str = '127.0.0.1:8000'


def key_gen():
    key_len = secrets.choice(range(1,  DataHelper().max_length+1))
    key = "".join(secrets.choice(DataHelper().chars) for n_times in range(key_len))
    return key


def get_data_clicks(user_agent):
    browser = user_agent.browser.family
    if user_agent.is_mobile:
        platform='Mobile'
    elif user_agent.is_tablet:
        platform='Tablet'
    else:
        platform='PC'
    return browser, platform



