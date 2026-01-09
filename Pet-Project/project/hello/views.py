from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Person
from django.db import connection
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiResponse
from .serializers import PersonSerializer


def registration(request):
    people = Person.objects.all()
    return render(request, "registration.html", {"people": people})

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
        if len(person.name) > 25:
            return HttpResponse("<h2>Длина имени не должна быть больше 25 символов</h2>")

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
    return HttpResponseRedirect("http://127.0.0.1:8000/hello/")

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
            printPasswords = cursor.fetchone()

            if printPasswords:
                Password = printPasswords[0]
            else:
                return HttpResponse("<h2>Неверный пароль</h2>")


        if person.name == Name and person.password == Password:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT email FROM hello_person WHERE password = '{person.password}' AND name = '{person.name}'")
                printEmail = cursor.fetchone()
                person.email = printEmail[0]

                cursor.execute(f"SELECT age FROM hello_person WHERE password = '{person.password}' AND name = '{person.name}'")
                printAge = cursor.fetchone()
                person.age = printAge[0]
        return render(request, "HelloLogin.html", {"person": person})
    return render(request, "login.html")


def delete(request, Id):
    person = Person.objects.get(id=Id)
    person.delete()
    return HttpResponseRedirect("http://127.0.0.1:8000/register/")


def hello(request):
    person = Person.objects.all().last()
    return render(request, "Hello.html", {"person": person})


def edit(request, id):
    person = Person.objects.get(id=id)
    if request.method == "POST":
        person.name = request.POST.get("name")
        person.age = request.POST.get("age")
        person.email = request.POST.get("email")
        person.password = request.POST.get("password")
        ValidName = Person.objects.filter(name=person.name)

        if person.name == '' or person.email == '' or person.password == '':
            return HttpResponse("<h2>Заполните все поля</h2>")

        if len(person.name) < 3:
            return HttpResponse("<h2>Длина имени должна быть больше 2 символов</h2>")

        if len(person.name) > 25:
            return HttpResponse("<h2>Длина имени не должна быть больше 25 символов</h2>")

        for symbol in person.name:
            if symbol.isalpha() or symbol.isdigit():
                pass
            else:
                return HttpResponse("<h2>В имени должны быть только буквы или цифры</h2>")

        if len(person.email) < 6:
            return HttpResponse("<h2>Длины почты не должна быть меньше 6 символов</h2>")

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

        if ValidName:
            return HttpResponse("<h2>Такой пользователь уже есть</h2>")
        person.save()
        return HttpResponseRedirect('http://127.0.0.1:8000/hello/')
    return render(request, "edit.html", {"person": person})


def loginedit(request, id):
    person = Person.objects.get(id=id)
    if request.method == "POST":
        person.name = request.POST.get("name")
        person.age = request.POST.get("age")
        person.email = request.POST.get("email")
        person.password = request.POST.get("password")
        VName = Person.objects.filter(name=person.name)

        if person.name == '' or person.email == '' or person.password == '':
            return HttpResponse("<h2>Заполните все поля</h2>")

        if len(person.name) < 3:
            return HttpResponse("<h2>Длина имени должна быть больше 2 символов</h2>")

        if len(person.name) > 25:
            return HttpResponse("<h2>Длина имени не должна быть больше 25 символов</h2>")

        for symbol in person.name:
            if symbol.isalpha() or symbol.isdigit():
                pass
            else:
                return HttpResponse("<h2>В имени должны быть только буквы или цифры</h2>")

        if int(person.age) < 1:
            return HttpResponse("<h2>Возраст не должен быть меньше 1</h2>")
        if int(person.age) > 110:
            return HttpResponse("<h2>Возраст не должен превышать 110</h2>")

        if person.password == '':
            return HttpResponse("<h2>Заполните поле Пароль</h2>")
        if len(person.password) < 6:
            return HttpResponse("<h2>Длина пароль не должна быть меньше 6 символов</h2>")
        if ' ' in person.password:
            return HttpResponse("<h2>Пароль не должен содержать пробелы</h2>")
        if len(person.password) > 24:
            return HttpResponse("<h2>Длина пароля не должна превышать 24 символа</h2>")

        if VName:
            return HttpResponse("<h2>Такой пользователь уже есть</h2>")
        person.save()
        return HttpResponseRedirect('http://127.0.0.1:8000/login/')
    return render(request, "edit.html", {"person": person})


class PersonList(APIView):
    @extend_schema(
        summary="Получение информации обо всех пользователях",
        description="Возвращает список всех зарегистрированных пользователей.",
        responses={
            200: OpenApiResponse(response=PersonSerializer(many=True), description="Список всех пользователей")
        }
    )
    def get(self, request):
        users = Person.objects.all()
        serializer = PersonSerializer(users, many=True)
        return Response(serializer.data)


class PersonDetail(APIView):
    @extend_schema(
        summary="Получение информации о пользователе",
        description="Возвращает информацию о пользователе по его ID.",
        responses={
            200: OpenApiResponse(response=PersonSerializer, description="Информация о пользователе"),
            404: OpenApiResponse(description="Пользователь не найден")
        }
    )
    def get(self, request, user_id):
        try:
            user = Person.objects.get(id=user_id)
        except Person.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = PersonSerializer(user)
        return Response(serializer.data)


class PersonDelete(APIView):
    @extend_schema(
        summary="Удаление пользователя",
        description="Удаляет пользователя по его ID. Если пользователь не найден, возвращает ошибку.",
        responses={
            200: OpenApiResponse(description="Пользователь успешно удалён"),
            404: OpenApiResponse(description="Пользователь не найден"),
            400: OpenApiResponse(description="ID пользователя не предоставлен")
        }
    )
    def delete(self, request, user_id):
        if user_id:
            try:
                user = Person.objects.get(id=user_id)
                user.delete()
                return Response({"status": "User deleted"}, status=status.HTTP_200_OK)
            except Person.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "User ID not provided"}, status=status.HTTP_400_BAD_REQUEST)


class PersonDeleteAll(APIView):
    @extend_schema(
        summary="Удаление всех пользователей",
        description="Удаляет всех пользователей из базы данных.",
        responses={
            200: OpenApiResponse(description="Все пользователи успешно удалены")
        }
    )
    def delete(self, request):
        Person.objects.all().delete()
        return Response({"status": "All users deleted"}, status=status.HTTP_200_OK)


class PersonRegistration(APIView):
    @extend_schema(
        summary="Регистрация пользователя",
        description="Создаёт нового пользователя с уникальным email, именем, возрастом и паролем. "
                    "Возраст должен быть в пределах от 16 до 99 лет.",
        request=PersonSerializer,
        responses={
            201: OpenApiResponse(response=PersonSerializer, description="Пользователь успешно создан"),
            400: OpenApiResponse(description="Ошибки валидации")
        }
    )
    def post(self, request):
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"status": "User created", "id": user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PersonEdit(APIView):
    @extend_schema(
        summary="Изменение данных пользователя",
        description="Изменяет данные пользователя по его ID",
        request=PersonSerializer,
        responses={
            200: OpenApiResponse(description="Данные успешно изменены"),
            404: OpenApiResponse(description="Пользователь не найден"),
            400: OpenApiResponse(description="ID пользователя не предоставлен"),
        }
    )
    def post(self, request, user_id):
        try:
            user = Person.objects.get(id=user_id)
            serializer = PersonSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "User edit"}, status=status.HTTP_200_OK)
        except Person.DoesNotExist:
            return Response({"status": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"status": "User ID not provided"}, status=status.HTTP_400_BAD_REQUEST)