from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Person, Tasks
from django.db import connection


def register(request):
    if request.method == "POST":
        person = Person()
        person.Name = request.POST.get("Name")
        person.Password = request.POST.get("Password")
        ValidName = Person.objects.filter(Name=person.Name)
        if ' ' in person.Name or ' ' in person.Password: return HttpResponse("<h2>Пробел в поле(ях)</h2>")
        if not str(person.Name).isalpha(): return HttpResponse("<h2>Неккоректное имя</h2>")
        if ValidName: return HttpResponse("<h2>Такой пользователь существует</h2>")
        else: person.save()
        return HttpResponseRedirect(f"http://localhost:8000/prime/{person.Name}")
    return render(request, "register.html")


def login(request):
    if request.method == "POST":
        person = Person()
        person.Name = request.POST.get("Name")
        person.Password = request.POST.get("Password")
        with connection.cursor() as cursor:
            cursor.execute(f'SELECT "Name" FROM hello_Person WHERE "Name" = \'{person.Name}\'')
            OneString = cursor.fetchone()
            if OneString: PersonName = OneString[0]
            else: return HttpResponse("<h2>Пользователя не существует</h2>")

            cursor.execute(f'SELECT "Password" FROM hello_Person WHERE "Password" = \'{person.Password}\'')
            TwoString = cursor.fetchone()
            if TwoString: PersonPassword = TwoString[0]
            else: return HttpResponse("<h2>Неверный пароль</h2>")
        if person.Name == PersonName and person.Password == PersonPassword: return HttpResponseRedirect(f"http://localhost:8000/prime/{person.Name}")
    return render(request, "login.html")


def createTask(request):
    if request.method == "POST":
        name = request.POST.get("Name")
        tasks = Tasks()
        tasks.PersonName = name
        tasks.TaskName = request.POST.get("TaskName")
        tasks.Title = request.POST.get("Title")
        tasks.Time = request.POST.get("Time")
        tasks.save()
        return redirect('Prime', Name=name)


def deleteTask(request, Id, Name):
    person = Person.objects.filter(Name=Name).first()
    tasks = Tasks.objects.get(id=Id)
    tasks.delete()
    return HttpResponseRedirect(f"http://localhost:8000/prime/{person.Name}")


def edit(request, Name):
    person = Person.objects.get(Name=Name)
    tasks = Tasks.objects.filter(PersonName=Name)
    if request.method == "POST":
        person.Name = request.POST.get("Name")
        person.Password = request.POST.get("Password")
        ValidName = Person.objects.filter(Name=person.Name)
        if ' ' in person.Name or ' ' in person.Password: return HttpResponse("<h2>Пробел в поле(ях)</h2>")
        if not str(person.Name).isalpha(): return HttpResponse("<h2>Неккоректное имя</h2>")
        if ValidName: return HttpResponse("<h2>Такой пользователь существует</h2>")
        else:
            person.save()
            if tasks is None: tasks = []
            else:
                for task in tasks:
                    task.PersonName = person.Name
                    task.save()
        return redirect('Prime', Name=person.Name)


def prime(request, Name):
    person = Person.objects.filter(Name=Name).first()
    tasks = Tasks.objects.all().filter(PersonName=Name)
    content = {}
    content.update({"person": person})
    if tasks is not None:
        content.update({"tasks": tasks})
    return render(request, "prime.html", content)


def delete(request, Name):
    person = Person.objects.filter(Name=Name)
    person.delete()
    return HttpResponseRedirect("http://localhost:8000/register/")