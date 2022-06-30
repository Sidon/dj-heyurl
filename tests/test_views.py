import pytest
from heyurl import views
from .mocks import Mocks, dh


mocks = Mocks()


@pytest.mark.django_db
def test_store():
    response = views.store(mocks.http_request_new)
    assert response.status_code == 200

@pytest.mark.django_db
def test_short_url():   # Redirect
    response = views.short_url(mocks.http_request, dh.short_url)
    breakpoint()
    assert True