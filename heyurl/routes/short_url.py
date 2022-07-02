from django.urls import path

from heyurl import views

urlpatterns = [
    path('', views.redirect_short_url, name='redirect_short_url'),
]
