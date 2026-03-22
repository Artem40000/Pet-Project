from django.db import models


class Person(models.Model):
    Name = models.CharField()
    Password = models.CharField()
    ConfirmPassword = models.CharField()