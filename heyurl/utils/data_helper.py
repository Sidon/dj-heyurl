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
    new_urls: list = field(default_factory=lambda: ['t.me', 'z.com'])
    host: str = '127.0.0.1:8000'


_dh = DataHelper()

mock_http_post = namedtuple("Post", ['get'], defaults=[lambda original_url: None])
mock_http_get = namedtuple("Get", ['get'], defaults=[lambda *args: 'a' if args[0]=='short_url' else None])
mock_browser = namedtuple("Browser", ['family'], defaults=['chrome'])
mock_user_agent = namedtuple('UserAgent', ['browser', 'is_pc', 'is_tablet', 'is_mobile'], defaults=[mock_browser])

mock_request = namedtuple('Request', ['POST', 'GET', 'method', 'path', 'user_agent'],
                          defaults=[mock_http_post, dict(original_url=_dh.original_url), 'POST', '/a', mock_user_agent]
                          )

hey_helper = namedtuple(
    "HeyHelper",
    ['http_POST', 'http_GET', 'browser', 'user_agent', 'request'],
    defaults=[mock_http_post(), mock_http_get, mock_browser, mock_user_agent, mock_request]
)


def key_gen():
    key_len = secrets.choice(range(1, _dh.max_length+1))
    key = "".join(secrets.choice(_dh.chars) for n_times in range(key_len))
    return key







