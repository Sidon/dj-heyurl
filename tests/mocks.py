from collections import namedtuple
from dataclasses import dataclass, field
from requests import request
from heyurl.utils.helper import DataHelper

dh = DataHelper()


mock_browser = namedtuple('Browser', ['family'], defaults=['Chrome'])
mock_user_agent = namedtuple(
    'UserAgent',
    ['browser', 'is_pc', 'is_mobile', 'is_tablet'],
    defaults=[mock_browser(), None, None, None]
)

mock_http_post = namedtuple('Post', ['get'], defaults=[lambda original_url=dh.original_url: None])
mock_post_new = mock_http_post(lambda original_url: dh.new_urls[0])
mock_http_get = namedtuple('Get', ['get'], defaults=[lambda *args: dh.short_url if args[0] == 'short_url' else None])

mock_request = namedtuple(
    'RequestMock',
    ['POST', 'GET', 'user_agent', 'path', 'method'],
    defaults=[
        mock_http_post(), 
        dict(short_url=dh.short_url),
        mock_user_agent(),
        dh.short_url,
        'POST'
    ]
)

mock_request_new = mock_request(mock_post_new, dict(short_url=dh.short_url), mock_user_agent(), None, 'POST')

Mocks = namedtuple(
    'HelpTest',
    ['browser', 'user_agent', 'http_post', 'http_get', 'http_request', 'http_request_new'],
    defaults=[mock_browser, mock_user_agent, mock_http_post, mock_http_get, mock_request, mock_request_new]
)

