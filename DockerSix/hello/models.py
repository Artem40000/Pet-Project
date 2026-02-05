from django.db import models

class Person(models.Model):
    Name = models.CharField(max_length=16)
    Age = models.IntegerField()
    Password = models.CharField(max_length=24)