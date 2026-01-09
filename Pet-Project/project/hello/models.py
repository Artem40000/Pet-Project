from django.db import models

class Person(models.Model):
    name = models.CharField()
    age = models.IntegerField()
    email = models.EmailField(max_length=25)
    password = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.name} {self.password}'