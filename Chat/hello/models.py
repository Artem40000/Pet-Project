from django.db import models


class Searchs(models.Model):
    Search = models.CharField()
    Url = models.CharField()