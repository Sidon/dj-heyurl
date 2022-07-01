import heyurl.views
import pytest
from heyurl import views
from .mocks import Mocks, dh


mocks = Mocks()


@pytest.mark.django_db
def test_store(django_db_setup):
    response = views.store(mocks.http_request_new)
    assert response.status_code == 200

@pytest.mark.django_db
def test_short_url(monkeypatch, django_db_setup):
    monkeypatch.setattr('heyurl.views.get_user_agent', lambda request: mocks.user_agent())# Redirect
    response = views.short_url(mocks.http_request, dh.short_url)
    breakpoint()
    assert True