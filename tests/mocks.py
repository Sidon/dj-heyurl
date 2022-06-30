from collections import namedtuple
from dataclasses import dataclass, field

from requests import request
from heyurl.utils.data_helper import DataHelper

dh = DataHelper()


mock_http_post = namedtuple('Post', ['get'], defaults=[lambda orginal_url=dh.original_url: None])
# mock_http_get = namedtuple('Get', ['get'], defaults=[lambda *args: dh.original_url if args[0] else None])
mock_browser = namedtuple('Browser', ['Family'], defaults=['chrome'])

mock_user_agent = namedtuple(
    'UserAgent',
    ['browser', 'is_pc', 'is_mobile', 'is_tablet'],
    defaults=[mock_browser, None, None, None]
)

mock_request = namedtuple(
    'Request', 
    ['POST', 'GET', 'user_agent', 'path', 'method'],
    defaults=[
        mock_http_post(), 
        dict(original_url=dh.original_url),
        mock_user_agent(),
        dh.short_url,
        'POST'
    ]
)

Mocks = namedtuple(
    'HelpTest',
    ['request'], defaults=[mock_request()], 
)

mocks = Mocks()
request = mocks.request