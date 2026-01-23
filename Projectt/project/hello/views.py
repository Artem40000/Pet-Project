from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Person
from django.db import connection
from django.urls import reverse

def create(request):
    if request.method == "POST":
        person = Person()
        person.name = request.POST.get("name")
        VName = Person.objects.filter(name=person.name)
        person.age = request.POST.get("age")
        person.email = request.POST.get("email")
        person.password = request.POST.get("password")
        if person.name == '':
            return HttpResponse("<h2>Заполните поле Имя</h2>")
        if len(person.name) < 3:
            return HttpResponse("<h2>Длина имени должна быть больше 2 символов</h2>")
        if len(person.name) > 12:
            return HttpResponse("<h2>Длина имени не должна быть больше 12 символов</h2>")

        for symbol in person.name:
            if symbol.isalpha() or symbol.isdigit():
                pass
            else:
                return HttpResponse("<h2>В имени должны быть только буквы или цифры</h2>")

        if person.age == '':
            return HttpResponse("<h2>Заполните поле Возраст</h2>")
        if int(person.age) < 1:
            return HttpResponse("<h2>Возраст не должен быть меньше 1</h2>")
        if int(person.age) > 110:
            return HttpResponse("<h2>Возраст не должен превышать 110</h2>")

        if person.email == '':
            return HttpResponse("<h2>Заполните поле Почта</h2>")
        if len(person.email) < 6:
            return HttpResponse("<h2>Длины почты не должна быть меньше 6 символов</h2>")

        if person.password == '':
            return HttpResponse("<h2>Заполните поле Пароль</h2>")
        if len(person.password) < 8:
            return HttpResponse("<h2>Длина пароль не должна быть меньше 8 символов</h2>")
        if ' ' in person.password:
            return HttpResponse("<h2>Пароль не должен содержать пробелы</h2>")
        if len(person.password) > 24:
            return HttpResponse("<h2>Длина пароля не должна превышать 24 символа</h2>")

        if VName:
            return HttpResponse("<h2>Такой пользователь уже есть</h2>")
        else:
            person.save()
        return HttpResponseRedirect(f'http://127.0.0.1:8000/Hello/{person.name}')


def delete(request, name):
    person = Person.objects.get(name=name)
    person.delete()
    return HttpResponseRedirect("http://127.0.0.1:8000/register/")


def edit(request, name):
    person = Person.objects.get(name=name)
    if request.method == "POST":
        person.name = request.POST.get("name")
        person.age = request.POST.get("age")
        person.password = request.POST.get("password")
        VName = Person.objects.filter(name=person.name)

        if person.name == '' or person.password == '' or person.age == '':
            return HttpResponse("<h2>Заполните все поля</h2>")
        if len(person.name) < 3:
            return HttpResponse("<h2>Длина имени должна быть больше 2 символов</h2>")

        for symbol in person.name:
            if symbol.isalpha() or symbol.isdigit():
                pass
            else:
                return HttpResponse("<h2>В имени должны быть только буквы или цифры</h2>")

        if int(person.age) < 1:
            return HttpResponse("<h2>Возраст не должен быть меньше 1</h2>")
        if int(person.age) > 110:
            return HttpResponse("<h2>Возраст не должен превышать 110</h2>")

        if len(person.password) < 6:
            return HttpResponse("<h2>Длина пароль не должна быть меньше 8 символов</h2>")
        if ' ' in person.password:
            return HttpResponse("<h2>Пароль не должен содержать пробелы</h2>")
        if len(person.password) > 24:
            return HttpResponse("<h2>Длина пароля не должна превышать 24 символа</h2>")

        if VName:
            return HttpResponse("<h2>Такой пользователь уже есть</h2>")
        person.save()
        return HttpResponseRedirect(f'http://127.0.0.1:8000/Hello/{person.name}')
    return render(request, "Edit.html", {"person": person})



def register(request):
    people = Person.objects.all()
    return render(request, "register.html", {"people": people})


def login(request):
    if request.method == "POST":
        person = Person()
        person = Person.objects.all()
        person.name = request.POST.get("name")
        person.password = request.POST.get("password")
        if person.name == '' or person.password == '':
            return HttpResponse("<h2>Заполните все поля</h2>")

        with connection.cursor() as cursor:
            cursor.execute(f"SELECT id FROM hello_person WHERE name = '{person.name}'")
            printId = cursor.fetchone()
            if printId:
                person.Id = printId[0]


            cursor.execute(f"SELECT name FROM hello_person WHERE name = '{person.name}'")
            printName = cursor.fetchone()

            if printName:
                Name = printName[0]
            else:
                return HttpResponse("<h2>Такого пользователя не существует</h2>")


            cursor.execute(f"SELECT password FROM hello_person WHERE password = '{person.password}'")
            printPassword = cursor.fetchone()

            if printPassword:
                Password = printPassword[0]
            else:
                return HttpResponse("<h2>Неверный пароль</h2>")

        return render(request, "Hello.html", {"person": person})
    return render(request, "login.html")


def Hello(request, name):
    person = Person.objects.get(name=name)
    return render(request, "Hello.html", {"person":person})


def Mymy(request, name):
    person = Person.objects.get(name=name)
    return render(request, "Mymy.html", {"person": person})



def Poselok1(request, name):
    person = Person.objects.get(name=name)
    return render(request, "Poselok1.html", {"person":person})

def Poselok2(request, name):
    person = Person.objects.get(name=name)
    return render(request, "Poselok2.html", {"person":person})

def Poselok3(request, name):
    person = Person.objects.get(name=name)
    return render(request, "Poselok3.html", {"person":person})

def Poselok4(request, name):
    person = Person.objects.get(name=name)
    return render(request, "Poselok4.html", {"person":person})



def Jatva1(request, name):
    person = Person.objects.get(name=name)
    return render(request, "Jatva1.html", {"person": person})

def Jatva2(request, name):
    person = Person.objects.get(name=name)
    return render(request, "Jatva2.html", {"person": person})

def Jatva3(request, name):
    person = Person.objects.get(name=name)
    return render(request, "Jatva3.html", {"person": person})



def LesGrimm1(request, name):
    person = Person.objects.get(name=name)
    return render(request, "LesGrimm1.html", {"person": person})

def LesGrimm2(request, name):
    person = Person.objects.get(name=name)
    return render(request, "LesGrimm2.html", {"person": person})

def LesGrimm3(request, name):
    person = Person.objects.get(name=name)
    return render(request, "LesGrimm3.html", {"person": person})

def LesGrimm4(request, name):
    person = Person.objects.get(name=name)
    return render(request, "LesGrimm4.html", {"person": person})