import pytest

from django.core.management import call_command
from requests import Session

@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'sdn_fixture.json')
        
        
    
            