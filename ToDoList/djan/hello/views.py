from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Tasks
from django.db import connection

def prime(request):
    Tasksss = Tasks.objects.all()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM hello_tasks")
        Task = cursor.fetchone()
        if Task != None:
            Name = Task[1]
            Taskss = Task[2]
            Time = Task[3]
        else:
            return render(request, "prime.html")
    return render(request, "prime.html", {"Name": Name, "Task": Taskss, "Time": Time, "Tasks": Tasksss})


def Task(request):
    Task = Tasks.objects.all()
    return render(request, "Task.html", {"Task": Task})


def CreateTask(request):
    if request.method == "POST":
        Task = Tasks()
        Task.Name = request.POST.get("Name")
        Task.Task = request.POST.get("Task")
        Task.Time = request.POST.get("Time")
        if Task.Name == '':
            return HttpResponse("<h2>Заполните поле Название</h2>")
        if len(Task.Name) > 40:
            return HttpResponse("<h2>Длина Названия не должна быть больше 40 символов</h2>")

        if Task.Task == '':
            return HttpResponse("<h2>Заполните поле Описание</h2>")
        if len(Task.Task) > 40:
            return HttpResponse("<h2>Длины Описания не должна быть больше 40 символов</h2>")
        Task.save()
        return HttpResponseRedirect(f"http://127.0.0.1:8000/prime")

def delete(request, id):
    try:
        Task = Tasks.objects.get(id=id)
        Task.delete()
        return HttpResponseRedirect("http://127.0.0.1:8000/prime/")
    except Tasks.DoesNotExist:
        return HttpResponseRedirect("<h2>Задача не найдена</h2>")