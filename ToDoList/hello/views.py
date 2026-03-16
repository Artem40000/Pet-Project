from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.db import connection
from .models import Person, Tasks



def prime(request, Name):
    context = {}
    person = Person.objects.all().last()
    person = Person.objects.get(Name=Name)
    tasks = Tasks.objects.all().filter(Name=Name)
    context.update({'person': person, 'tasks': tasks})
    if tasks is not None:
        with connection.cursor() as cursor:
            cursor.execute(f'SELECT * FROM hello_Tasks WHERE "Name" = \'{Name}\'')
            AllTasks = cursor.fetchone()
            if AllTasks:
                TaskName = AllTasks[0]
                TaskDoing = AllTasks[1]
                TaskTime = AllTasks[2]
                context.update({"TaskName": TaskName, "TaskDoing": TaskDoing, "TaskTime": TaskTime})
    return render(request, "prime.html", context)


def register(request):
    return render(request, "register.html")


def create(request):
    person = Person.objects.all()
    if request.method == "POST":
        person = Person()
        person.Name = request.POST.get("Name")
        person.Password = request.POST.get("Password")
        if person.Name == '' or person.Password == '':
            return HttpResponse("<h2>Заполните все поля</h2>")
        if ' ' in person.Name or ' ' in person.Password:
            return HttpResponse("<h2>Пробел в имени или пароле</h2>")
        if len(person.Name) > 20:
            return HttpResponse("<h2>Слишком длинное имя</h2>")
        if len(person.Password) > 48:
            return HttpResponse("<h2>Слишком длинный пароль</h2>")
        if len(person.Name) < 3:
            return HttpResponse("<h2>Длина имени должна быть больше 3</h2>")
        if len(person.Password) < 6:
            return HttpResponse("<h2>Длина пароля должна быть больше 6</h2>")
        person.save()
    return HttpResponseRedirect(f"http://localhost:8000/prime/{person.Name}")


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

        if person.Name == PersonName and person.Password == PersonPassword:
            return HttpResponseRedirect(f'http://localhost:8000/prime/{person.Name}')
    return render(request, "login.html")


def delete(request, Name):
    person = Person.objects.get(Name=Name)
    tasks = Tasks.objects.all().filter(Name=Name)
    tasks.delete()
    person.delete()
    return HttpResponseRedirect("http://localhost:8000/register/")





def createTask(request, Name):
    person = Person.objects.get(Name=Name)
    person = Person.objects.all().last()
    if request.method == "POST":
        tasks = Tasks()
        tasks.TaskName = request.POST.get("TaskName")
        tasks.TaskDoing = request.POST.get("TaskDoing")
        tasks.TaskTime = request.POST.get("TaskTime")
        tasks.Name = person.Name
        if ' ' in tasks.TaskName or ' ' in tasks.TaskDoing or ' ' in tasks.TaskTime:
            return HttpResponse("<h2>Пробел в поле(ях)</h2>")
        if len(tasks.TaskName) > 20 or len(tasks.TaskDoing) > 40:
            return HttpResponse("<h2>Длина поля(ей) превышена</h2>")
        tasks.save()
    return HttpResponseRedirect(f'http://localhost:8000/prime/{person.Name}')