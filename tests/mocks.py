from collections import namedtuple
from heyurl.utils import helper

browser = namedtuple(
    'Browser',
    ['family'],
    defaults=['Chrome']
)

user_agent = namedtuple(
    'UserAgent',
    ['browser', 'is_pc', 'is_mobile', 'is_tablet'],
    defaults=[browser(), None, None, None]
)

post = namedtuple(
    'Post',
    ['get'],
    defaults=
    [lambda original_url=helper.original_url: None]
)

new_post = post(lambda original_url: helper.new_url)

get = namedtuple(
    'Get',
    ['get'],
    defaults=[lambda *args: helper.short_url if args[0] == 'short_url' else None])

request = namedtuple(
    'RequestMock',
    ['POST', 'GET', 'user_agent', 'path', 'method'],
    defaults=[
        post(),
        dict(short_url=helper.short_url),
        user_agent(),
        helper.short_url,
        'POST'
    ]
)

request_new = request(
    new_post,
    dict(short_url=helper.short_url), user_agent(), None, 'POST'
)

Mocks = namedtuple(
    'HelpTest',
    ['browser', 'user_agent', 'post', 'get', 'request', 'request_new'],
    defaults=[browser, user_agent, post, get, request, request_new]
)
