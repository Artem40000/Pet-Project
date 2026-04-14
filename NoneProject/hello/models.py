from django.db import models

class Person(models.Model):
    Name = models.CharField()
    Password = models.CharField()


class Tasks(models.Model):
    Name = models.CharField()
    Description = models.CharField()
    Time = models.CharField()
    PersonName = models.CharField()