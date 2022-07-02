import string
import secrets

chars = f'{string.ascii_uppercase}{string.ascii_lowercase}{string.digits}'
max_len = 5
original_url = 'http://fullstacklabs.co'
short_url = 'a'
new_urls = ['http://t.me', 'http://z.com']
host = '127.0.0.1:8000'


def key_gen():
    key_len = secrets.choice(range(1, max_len))
    key = "".join(secrets.choice(chars) for n_times in range(key_len))
    return key


def get_data_clicks(user_agent):
    browser = user_agent.browser.family
    if user_agent.is_mobile:
        platform = 'Mobile'
    elif user_agent.is_tablet:
        platform = 'Tablet'
    else:
        platform = 'PC'
    return browser, platform
