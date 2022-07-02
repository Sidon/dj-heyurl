import pytest
from heyurl import views
from heyurl.utils import helper
from .mocks import Mocks

mocks = Mocks()


@pytest.fixture
def patch_user_agent(monkeypatch):
    monkeypatch.setattr('heyurl.views.get_user_agent', lambda request: mocks.user_agent())


@pytest.mark.django_db
def test_store(django_db_setup):
    response = views.store(mocks.request_new)
    assert response.status_code == 200


@pytest.mark.django_db
def test_short_url(patch_user_agent, django_db_setup):
    # Redirect
    response = views.redirect_short_url(mocks.request, helper.short_url)
    assert response.status_code == 302 and response.url == helper.original_url


@pytest.mark.django_db
def test_handler404(django_db_setup, patch_user_agent, monkeypatch):
    monkeypatch.setattr('heyurl.views.render', lambda request, template: mocks.request())
    response = views.handler404(mocks.request(), None)
    assert response.url == helper.original_url


@pytest.mark.django_db
def test_month_metrics(django_db_setup):
    response = views.month_metrics(mocks.request())
    assert response.status_code == 200


@pytest.mark.django_db
def test_top_ten(django_db_setup):
    response = views.top_ten(mocks.request())
    assert response.status_code == 200
