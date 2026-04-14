from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django import forms
from django.db import connection
from .models import Person, Tasks
import requests
from bs4 import BeautifulSoup
from ddgs import DDGS
import subprocess


def register(request):
    person = Person.objects.all(); person.delete()
    task = Tasks.objects.all(); task.delete()
    if request.method == "POST":
        person = Person()
        person.Name = request.POST.get("Name")
        person.Password = request.POST.get("Password")
        ValidateName = Person.objects.filter(Name=person.Name)
        if not person.Name.isalpha(): return HttpResponse("<h1>Некорректное имя</h1>")
        if ' ' in person.Name or ' ' in person.Password: return HttpResponse("<h1>Пробел в поле(ях)</h1>")
        if ValidateName: return HttpResponse("<h1>Такой пользователь существует</h1>")
        else: person.save()
        return HttpResponseRedirect(f"http://localhost:8000/prime/{person.Name}")
    return render(request, 'register.html')


def login(request):
    if request.method == "POST":
        person = Person()
        person.Name = request.POST.get("Name")
        person.Password = request.POST.get("Password")

        with connection.cursor() as cursor:
            cursor.execute(f'SELECT "Name" FROM hello_Person WHERE "Name" = \'{person.Name}\'')
            PersonName = cursor.fetchone()
            if PersonName: PersonName = PersonName[0]
            else: return HttpResponse("<h2>Такого пользователя нет</h2>")

            cursor.execute(f'SELECT "Password" FROM hello_Person WHERE "Password" = \'{person.Password}\'')
            PersonPassword = cursor.fetchone()
            if PersonPassword: PersonPassword = PersonPassword[0]
            else: return HttpResponse("<h2>Неверный пароль</h2>")

            if person.Name == PersonName and person.Password == PersonPassword: return HttpResponseRedirect(f"http://localhost:8000/prime/{person.Name}")
    return render(request, 'login.html')


def edit(request, Name):
    person = Person.objects.get(Name=Name)
    if request.method == "POST":
        person.Name = request.POST.get("Name")
        person.Password = request.POST.get("Password")
        ValidateName = Person.objects.filter(Name=person.Name)
        if ' ' in person.Name or ' ' in person.Password: return HttpResponse("<h2>Пробел в поле(ях)</h2>")
        if not person.Name.isalpha(): return HttpResponse("<h1>Некорректное имя</h1>")
        if ValidateName: return HttpResponse("<h2>Такой пользователь существует</h2>")
        else: person.save()
        return redirect('Prime', Name=person.Name)


def delete(request, Name):
    person = Person.objects.get(Name=Name)
    person.delete()
    tasks = Tasks.objects.filter(PersonName=Name)
    tasks.delete()
    return HttpResponseRedirect("http://localhost:8000/register/")


def createTask(request, Name):
    person = Person.objects.get(Name=Name)
    count = Tasks.objects.filter(PersonName=person.Name).count()

    if request.method == "POST":
        task = Tasks()
        task.Name = request.POST.get("Name")
        task.Description = request.POST.get("Description")
        task.Time = request.POST.get("Time")
        task.PersonName = person.Name
        if count >= 3:
            return HttpResponse("<h1>Максимум 3 задачи</h1>")
        else:
            task.save()
        return redirect('CreateTask', Name=person.Name)
    return HttpResponseRedirect(f"http://localhost:8000/prime/{person.Name}")


def deleteTask(request, id):
    task = Tasks.objects.get(id=id)
    task.delete()
    return redirect('Prime', Name=task.PersonName)





def search_web(query, max_results=3):
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results): results.append(r["href"])
    return results

def parse_page(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=3)

        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style"]): tag.decompose()

        text = soup.get_text(separator=" ")
        text = " ".join(text.split())

        return text[:3000]
    except: return ""


def ask_local_llm(prompt):
    response = requests.post(
        "http://host.docker.internal:11434/api/chat",
        json={
            "model": "llama3",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "stream": False
        }
    )
    return response.json()["message"]["content"]


def ai_agent(query):
    links = search_web(query)
    collected_text = ""

    for link in links:
        content = parse_page(link)

        if len(content) > 300: collected_text += content + "\n\n"

    collected_text = collected_text[:3000]
    prompt = f"""Ответь кратко и понятно. Вопрос: {query} Данные из интернета:{collected_text}"""

    return ask_local_llm(prompt)



def prime(request, Name):
    person = Person.objects.get(Name=Name)
    tasks = Tasks.objects.filter(PersonName=Name)

    if request.method == "POST":
        user_query = request.POST.get("query")
        answer = ai_agent(user_query)
        request.session["answer"] = answer
        return redirect("Prime", Name=person.Name)

    answer = request.session.pop("answer", "")
    return render(request, "prime.html", {"person": person, "tasks": tasks, "answer": answer})