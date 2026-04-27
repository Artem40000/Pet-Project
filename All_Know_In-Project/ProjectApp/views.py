from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.db import connection
import secrets
import string
from .models import Person, Tasks
import json
import os
import ollama


def register(request):
    if request.method == "POST":
        person = Person()
        person.Name = request.POST.get("Name")
        person.Password = request.POST.get("Password")
        person.ConfirmPassword = request.POST.get("ConfirmPassword")
        ValidateName = Person.objects.filter(Name=person.Name)
        if person.Password == person.ConfirmPassword:
            if not person.Name.isalpha(): return HttpResponse("<h1>Некорректное имя</h1>")
            if ' ' in person.Name or ' ' in person.Password: return HttpResponse("<h1>Пробел в поле(ях)</h1>")
            if ValidateName:
                return HttpResponse("<h1>Такой пользователь существует</h1>")
            else:
                person.save()
        else:
            return HttpResponse("<h2>Пароли не совпадают</h2>")
        return HttpResponseRedirect(f"http://localhost:8000/prime/{person.Name}")
    return render(request, 'register.html')


def login(request):
    if request.method == "POST":
        name = request.POST.get("Name")
        password = request.POST.get("Password")

        person = Person.objects.filter(Name=name).first()
        if not person:
            return HttpResponse("<h2>Такого пользователя нет</h2>")

        if person.Password != password:
            return HttpResponse("<h2>Неверный пароль</h2>")

        return HttpResponseRedirect(f"http://localhost:8000/prime/{name}")
    return render(request, 'login.html')




def EditAccount(request, Name):
    person = Person.objects.get(Name=Name)
    if request.method == "POST":
        new_Name = request.POST.get("Name")
        new_Password = request.POST.get("Password")
        ValidateName = Person.objects.filter(Name=new_Name)
        if ' ' in new_Name or ' ' in new_Password: return HttpResponse("<h2>Пробел в поле(ях)</h2>")
        if not new_Name.isalpha(): return HttpResponse("<h1>Некорректное имя</h1>")

        Tasks.objects.filter(Person=Name).update(Person=new_Name)
        if ValidateName:
            return HttpResponse("<h2>Такой пользователь существует</h2>")
        else:
            person.Name = new_Name
            person.Password = new_Password
            person.save()
        return redirect('Prime', Name=new_Name)


def DeleteAccount(request, Name):
    person = Person.objects.get(Name=Name)
    person.delete()
    tasks = Tasks.objects.filter(Person=Name)
    tasks.delete()
    return HttpResponseRedirect(f'http://localhost:8000/register/')




def CreateTask(request, Name):
    person = Person.objects.get(Name=Name)
    count = Tasks.objects.filter(Person=Name).count()
    if request.method == "POST":
        task = Tasks()
        task.Task_Name = request.POST.get("Task_Name")
        task.Task_Descriptions = request.POST.get("Task_Descriptions")
        task.Task_Time = request.POST.get("Task_Time")
        task.Person = person.Name
        if count >= 5: return HttpResponse("<h1>Максимум 5 задач</h1>")
        else: task.save()
        return redirect('CreateTask', Name=person.Name)
    return HttpResponseRedirect(f"http://localhost:8000/prime/{person.Name}")


def DeleteTask(request, Id):
    task = Tasks.objects.get(id=Id)
    task.delete()
    return redirect('Prime', Name=task.Person)




def PasswordGenerate(request, Name):
    person = Person.objects.get(Name=Name)
    Password = None

    if request.method == "POST":
        Long = request.POST.get('PasswordLong')
        StateCharacter = request.POST.get("character_state")
        StateDigits = request.POST.get("digits_state")

        if Long == '':
            Long = 4

        if StateDigits == 'on' and StateCharacter == 'on':
            Character = string.digits + string.ascii_letters
        elif StateDigits == 'off' and StateCharacter == 'on':
            Character = string.ascii_letters
        elif StateDigits == 'on' and StateCharacter == 'off':
            Character = string.digits
        elif StateDigits == 'off' and StateCharacter == 'off':
            return HttpResponse(f"<h2>Обязательно должен быть 1 параметр</h2>")

        Password = "".join(secrets.choice(Character) for i in range(int(Long)))
    return render(request, 'prime.html', {"Password": Password, "person": person})





def prime(request, Name):
    person = Person.objects.get(Name=Name)
    tasks = Tasks.objects.filter(Person=Name)

    answer = ""
    code = ""
    mode = ""
    theory = ""
    language = ""

    client = ollama.Client(host=os.getenv("OLLAMA_HOST"))
    if request.method == "POST":
        UserInput = request.POST.get("query", "").strip()
        router_messages = [{"role": "system", "content":
            """
            Определи тип запроса пользователя.
            ОТВЕТЬ МНЕ ОДНИМ СЛОВОМ НА ВЫБОР НИЖЕ, ЭТО МОЖЕТ БЫТЬ code / chat .
            code -> если пользователь просит написать код, исправить код,объяснить программирование, Python, JS, цикл, ии, функцию и т.д.
            chat -> если обычный вопрос, приветствие, разговор, факты.
            """}, {"role": "user", "content": UserInput}]

        router_response = client.chat(model='mistral:7b', messages=router_messages)
        mode = router_response["message"]["content"].strip().lower()

        if mode == "code":
            Messages = [{"role": "system", "content":
                """
                Ты программист.

                Отвечай ТОЛЬКО в JSON:
                {
                    "theory": "объяснение на русском",
                    "code": [Массив строк],
                    "language": "Определи какой это язык программирования",
                }

                Правила:
                - никаких HTML
                - никаких markdown
                - code это массив строк
                - ничего вне JSON
                """
                }, {"role": "user", "content": UserInput}]

            response = client.chat(model='mistral:7b', messages=Messages)
            raw_answer = response["message"]["content"]

            try:
                data = json.loads(raw_answer)

                theory = data.get("theory", "")
                code_lines = data.get("code", [])
                language = data.get("language", "")

                if isinstance(code_lines, list):
                    code = "\n".join(code_lines)
                else:
                    code = ""

            except:
                theory = "Ошибка чтения JSON."
                code = ""
                language = ""


        elif mode == "chat":
            Messages = [{"role": "system", "content":
                """
                Ты дружелюбный ассистент.

                Отвечай обычным текстом.
                Без JSON.
                Без HTML.
                """}, {"role": "user", "content": UserInput}]

            response = client.chat(model='mistral:7b', messages=Messages)
            answer = response["message"]["content"]
    return render(request, 'prime.html', {"person": person, "tasks": tasks, "answer": answer, "mode": mode, "code": code, "theory": theory, "language": language})