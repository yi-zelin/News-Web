from django.db import models


# Create your models here.
class UserInfo(models.Model):
    name = models.CharField(max_length=16)
    password = models.CharField(max_length=16)


class NewsList(models.Model):
    title = models.CharField(max_length=100)
    source = models.CharField(max_length=20)
    link = models.CharField(max_length=100)
    detail = models.CharField(max_length=250)
