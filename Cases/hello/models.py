from django.db import models


class Person(models.Model):
    Name = models.CharField()
    Email = models.EmailField()
    Password = models.CharField()


class Items(models.Model):
    pOne = models.CharField()
    pTwo = models.CharField()
    Url = models.CharField()

    def __str__(self):
        return f'{self.pOne} {self.pTwo} {self.Url}'

class ItemsTwo(models.Model):
    pOne = models.CharField()
    pTwo = models.CharField()
    Url = models.CharField()

    def __str__(self):
        return f'{self.pOne} {self.pTwo} {self.Url}'

class ItemsThree(models.Model):
    pOne = models.CharField()
    pTwo = models.CharField()
    Url = models.CharField()

    def __str__(self):
        return f'{self.pOne} {self.pTwo} {self.Url}'


class InvItem(models.Model):
    pOne = models.CharField()
    pTwo = models.CharField()
    Url = models.CharField()
    Name = models.CharField()