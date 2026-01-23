from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=12)
    age = models.IntegerField()
    email = models.EmailField(max_length=35)
    password = models.CharField(max_length=128)