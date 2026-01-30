from django.db import models

class Tasks(models.Model):
    Name = models.CharField(max_length=50)
    Task = models.CharField(max_length=150)
    Time = models.TimeField()