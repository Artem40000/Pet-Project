from django.db import models


class Person(models.Model):
    Name = models.CharField()
    Password = models.CharField()


class Tasks(models.Model):
    TaskName = models.CharField()
    TaskDoing = models.CharField()
    TaskTime = models.TimeField()
    Name = models.CharField()