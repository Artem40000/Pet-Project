from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from .models import Person
import string, secrets
from django.db import connection


def prime(request, name):
    person = Person.objects.get(Name=name)
    persons = Person.objects.all().last()

    Random = string.digits + string.ascii_letters
    Id = "".join(secrets.choice(Random) for _ in range(24))
    return render(request, "prime.html", {"person": persons, "Id": Id})


def create(request):
    if request.method == "POST":
        person = Person()
        person.Name = request.POST.get("Name")
        person.Age = request.POST.get("Age")
        person.Password = request.POST.get("Password")
        Vname = Person.objects.filter(Name=person.Name)

        if person.Name == '' or person.Age == '' or person.Password == '':
            return HttpResponse("<h2>Заполните все поля</h2>")

        for symbol in person.Name:
            if symbol.isalpha() or symbol.isdigit():
                pass
            else:
                return HttpResponse("<h2>В имени должны быть только буквы или цифры</h2>")

        if len(person.Name) > 16:
            return HttpResponse("<h2>Длина имени не должна быть больше 16</h2>")

        if len(person.Name) < 4:
            return HttpResponse("<h2>Длина имени не должна быть меньше 4</h2>")

        if len(person.Password) > 24:
            return HttpResponse("<h2>Длина пароля не должна быть больше 24</h2>")

        if ' ' in person.Password:
            return HttpResponse("<h2>Пароль не должен содержать пробелы</h2>")

        if len(person.Password) < 6:
            return HttpResponse("<h2>Длина пароля не должна быть меньше 6</h2>")

        if int(person.Age) < 0:
            return HttpResponse("<h2>Возраст меньше 0</h2>")

        if int(person.Age) > 101:
            return HttpResponse("<h2>Возраст не должен быть больше 101</h2>")

        if Vname == person.Name:
            return HttpResponse("<h2>Такой пользователь уже есть</h2>")
        else:
            person.save()
        return HttpResponseRedirect(f"http://localhost:8000/prime/{person.Name}")


def register(request):
    people = Person.objects.all()
    return render(request, "register.html", {"people": people})


def login(request):
    if request.method == "POST":
        person = Person()
        person = Person.objects.all()
        person.Name = request.POST.get("Name")
        person.Password = request.POST.get("Password")

        if person.Name == '' or person.Password == '':
            return HttpResponse("<h2>Заполните все поля</h2>")

        with connection.cursor() as cursor:
            cursor.execute(f'SELECT "id" FROM hello_person WHERE "Name" = \'{person.Name}\'')
            printId = cursor.fetchone()
            if printId:
                person.Id = printId[0]


            cursor.execute(f'SELECT "Name" FROM hello_person WHERE "Name" = \'{person.Name}\'')
            printName = cursor.fetchone()
            if printName:
                Name = printName[0]
            else:
                return HttpResponse("<h2>Пользователь не найден</h2>")


            cursor.execute(f'SELECT "Password" FROM hello_person WHERE "Password" = \'{person.Password}\'')
            printPasswords = cursor.fetchone()
            if printPasswords:
                Password = printPasswords[0]
            else:
                return HttpResponse("<h2>Неверный пароль</h2>")

            if person.Name == Name and person.Password == Password:
                with connection.cursor() as cursor:
                    cursor.execute(f'SELECT "Age" FROM hello_person WHERE "Name" = \'{person.Name}\'')
                    printAge = cursor.fetchone()
                    print(printAge)
                    person.Age = printAge[0]
        return render(request, "primeL.html", {"person": person})
    return render(request, "login.html")


def edit(request, name, Id):
    person = Person.objects.get(Name=name)
    Random = string.digits + string.ascii_letters
    Id = "".join(secrets.choice(Random) for _ in range(24))
    if request.method == "POST":
        person.Name = request.POST.get("Name")
        person.Age = request.POST.get("Age")
        person.Password = request.POST.get("Password")
        VName = Person.objects.filter(Name=person.Name)

        if person.Name == '' or person.Age == '' or person.Password == '':
            return HttpResponse("<h2>Заполните все поля</h2>")

        for symbol in person.Name:
            if symbol.isalpha() or symbol.isdigit():
                pass
            else:
                return HttpResponse("<h2>В имени должны быть только буквы или цифры</h2>")

        if len(person.Name) > 16:
            return HttpResponse("<h2>Длина имени не должна быть больше 16</h2>")

        if len(person.Name) < 4:
            return HttpResponse("<h2>Длина имени не должна быть меньше 4</h2>")

        if len(person.Password) > 24:
            return HttpResponse("<h2>Длина пароля не должна быть больше 24</h2>")

        if ' ' in person.Password:
            return HttpResponse("<h2>Пароль не должен содержать пробелы</h2>")

        if len(person.Password) < 6:
            return HttpResponse("<h2>Длина пароля не должна быть меньше 6</h2>")

        if int(person.Age) < 0:
            return HttpResponse("<h2>Возраст меньше 0</h2>")

        if int(person.Age) > 101:
            return HttpResponse("<h2>Возраст не должен быть больше 101</h2>")

        if VName:
            return HttpResponse("<h2>Такой пользователь уже есть</h2>")
        person.save()
        return HttpResponseRedirect('http://localhost:8000/register/')
    return render(request, "edit.html", {"person": person, "Id": Id})


def delete(request, name, Id):
    person = Person.objects.get(Name=name)
    Random = string.digits + string.ascii_letters
    Id = "".join(secrets.choice(Random) for _ in range(24))
    person.delete()
    return HttpResponseRedirect("http://localhost:8000/register/")