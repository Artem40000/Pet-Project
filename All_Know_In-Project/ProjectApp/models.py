from django.db import models


class Person(models.Model):
    Name = models.CharField()
    Password = models.CharField()
    ConfirmPassword = models.CharField()


class Tasks(models.Model):
    Task_Name = models.CharField()
    Task_Descriptions = models.CharField()
    Task_Time = models.CharField()
    Person = models.CharField()