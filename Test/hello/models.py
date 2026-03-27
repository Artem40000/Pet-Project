from django.db import models


class Person(models.Model):
    Name = models.CharField()
    Password = models.CharField()


class Tasks(models.Model):
    PersonName = models.CharField()
    TaskName = models.CharField()
    Title = models.CharField()
    Time = models.TimeField()