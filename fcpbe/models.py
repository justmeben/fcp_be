from django.db import models


class Vote(models.Model):
    voter = models.CharField(max_length=128, blank=False, null=False)
    date = models.CharField(blank=False, null=False, max_length=64)
    fb_id = models.CharField(blank=True, null=True, max_length=64)
