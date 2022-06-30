from django.db import models


class Url(models.Model):
    short_url = models.CharField(max_length=255)
    original_url = models.CharField(max_length=255)
    clicks = models.IntegerField(default=0)
    created_at = models.DateTimeField('date created', auto_now_add=True)
    updated_at = models.DateTimeField('date updated', auto_now=True)


class Click(models.Model):
    url = models.ForeignKey(Url, on_delete=models.CASCADE, related_name='related_clicks')
    browser = models.CharField(max_length=255)
    platform = models.CharField(max_length=255)
    created_at = models.DateTimeField('date created', auto_now_add=True)
    updated_at = models.DateTimeField('date updated', auto_now=True)
