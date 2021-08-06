from django.db import models


class UserDataModel(models.Model):
    userid = models.CharField(max_length=50)
    uid = models.CharField(max_length=50)
    title = models.CharField(max_length=500)
    body = models.TextField(max_length=4000, blank=False)
