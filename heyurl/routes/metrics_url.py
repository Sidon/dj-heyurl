from django.urls import path

from heyurl import views

urlpatterns = [
    path('month/', views.month_metrics, name='api-month'),
    path('top-ten/', views.top_ten, name='api-top')
]
