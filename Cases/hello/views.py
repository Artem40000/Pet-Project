from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Person, Items, ItemsTwo, ItemsThree, InvItem
from django.db import connection
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiResponse
from .serializers import ItemsSerializer, ItemsTwoSerializer, ItemsThreeSerializer
import random


def prime(request, Name):
    context = {}
    person = Person.objects.get(Name=Name)
    persons = Person.objects.all().last()
    context.update({'person': person, 'persons': person})
    items = InvItem.objects.all().filter(Name=person.Name)
    if items is not None:
        with connection.cursor() as cursor:
            cursor.execute(f'SELECT * FROM hello_InvItem WHERE "Name" = \'{Name}\'')
            All = cursor.fetchone()
            if All:
                pOne = All[1]
                pTwo = All[2]
                Url = All[3]
                context.update({"pOne": pOne, "pTwo": pTwo, "Url": Url, "items": items})

    if request.method == "POST":
        person.Name = request.POST.get("Name")
        person.Email = request.POST.get("Email")
        person.Password = request.POST.get("Password")
        ValidName = Person.objects.filter(Name=person.Name)
        if len(person.Name) > 30:
            return HttpResponse("<h2>!Имя слишком длинное</h2>")
        if len(person.Email) < 10:
            return HttpResponse("<h2>!Почта слишком короткая</h2>")
        if len(person.Password) < 6:
            return HttpResponse("<h2>!Пароль слишком короткий</h2>")
        if len(person.Password) > 48:
            return HttpResponse("<h2>!Пароль слишком длинный</h2>")
        if str(person.Name).isalpha() == False:
            return HttpResponse("<h2>!Имя неккоректно</h2>")
        if ' ' in person.Password:
            return HttpResponse("<h2>!Пароль содержит пробелы</h2>")
        if ValidName:
            return HttpResponse("<h2>!Такой пользователь уже существует</h2>")
        else:
            with connection.cursor() as cursor:
                cursor.execute(f'DELETE FROM hello_InvItem WHERE "Name" = \'{person.Name}\'')
                person.save()
                context.update({"person": person, "persons": persons})
        return HttpResponseRedirect(f"http://localhost:8000/prime/{person.Name}")
    return render(request, 'prime.html', context)


def register(request):
    return render(request, 'register.html')

def create(request):
    if request.method == "POST":
        person = Person()
        person.Name = request.POST.get("Name")
        person.Email = request.POST.get("Email")
        person.Password = request.POST.get("Password")
        ValidName = Person.objects.filter(Name=person.Name)

        if person.Name == '' or person.Email == '' or person.Password == '':
            return HttpResponse("<h2>!Заполните все поля</h2>")
        if len(person.Name) > 30:
            return HttpResponse("<h2>!Имя слишком длинное</h2>")
        if len(person.Email) < 10:
            return HttpResponse("<h2>!Почта слишком короткая</h2>")
        if len(person.Password) < 6:
            return HttpResponse("<h2>!Пароль слишком короткий</h2>")
        if len(person.Password) > 48:
            return HttpResponse("<h2>!Пароль слишком длинный</h2>")
        if str(person.Name).isalpha() == False:
            return HttpResponse("<h2>!Имя неккоректно</h2>")
        if ' ' in person.Password:
            return HttpResponse("<h2>!Пароль содержит пробелы</h2>")
        if ValidName:
            return HttpResponse("<h2>!Такой пользователь уже существует</h2>")
        else:
            person.save()
    return HttpResponseRedirect(f'http://localhost:8000/prime/{person.Name}')


def login(request):
    if request.method == "POST":
        person = Person.objects.all()
        person.Name = request.POST.get("Name")
        person.Password = request.POST.get("Password")
        if person.Name == '' or person.Password == '':
            return HttpResponse("<h2>!Заполните все поля</h2>")

        with connection.cursor() as cursor:
            cursor.execute(f'SELECT "Name" FROM hello_person WHERE "Name" = \'{person.Name}\'')
            NameConfirm = cursor.fetchone()
            if NameConfirm:
                Name = NameConfirm[0]
            else:
                return HttpResponse("<h2>Такого пользователя не существует</h2>")


            cursor.execute(f'SELECT "Password" FROM hello_person WHERE "Password" = \'{person.Password}\'')
            PasswordConfirm = cursor.fetchone()
            if PasswordConfirm:
                Password = PasswordConfirm[0]
            else:
                return HttpResponse("<h2>Неверный пароль</h2>")
        return HttpResponseRedirect(f"http://localhost:8000/prime/{person.Name}")
    return render(request, 'login.html')


def delete(request, Name):
    items = InvItem.objects.all()
    items.delete()
    person = Person.objects.get(Name=Name)
    person.delete()
    return HttpResponseRedirect('http://localhost:8000/register/')



def yeti(request):
    Item = Items.objects.all()
    person = Person.objects.all().last()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM hello_Items")
        All = cursor.fetchone()
        pOne = All[1]
        pTwo = All[2]
        Url = All[3]

        AllAll = cursor.fetchall()
        if AllAll:
            Random = random.choice(AllAll)
            pOneR = Random[1]
            pTwoR = Random[2]
            UrlR = Random[3]
            with connection.cursor() as cursor:
                cursor.execute(f'INSERT INTO hello_InvItem ("pOne", "pTwo", "Url", "Name") VALUES(\'{pOneR}\',\'{pTwoR}\',\'{UrlR}\',\'{person.Name}\')')
    return render(request, 'case_yeti.html', {"person": person, "pOneR": pOneR, "pTwoR": pTwoR, "UrlR": UrlR, "Random": Random, "Item": Item, "pOne": pOne, "pTwo": pTwo, "Url": Url})

def cracken(request):
    ItemTw = ItemsTwo.objects.all()
    person = Person.objects.all().last()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM hello_ItemsTwo")
        All = cursor.fetchone()
        pOne = All[1]
        pTwo = All[2]
        Url = All[3]

        AllAll = cursor.fetchall()
        if AllAll:
            Random = random.choice(AllAll)
            pOneR = Random[1]
            pTwoR = Random[2]
            UrlR = Random[3]
            with connection.cursor() as cursor:
                cursor.execute(f'INSERT INTO hello_InvItem ("pOne", "pTwo", "Url", "Name") VALUES(\'{pOneR}\',\'{pTwoR}\',\'{UrlR}\',\'{person.Name}\')')
    return render(request, 'case_cracken.html', {"person": person, "pOneR": pOneR, "pTwoR": pTwoR, "UrlR": UrlR, "Random": Random, "Item": ItemTw, "pOne": pOne, "pTwo": pTwo, "Url": Url})

def dastin(request):
    ItemTh = ItemsThree.objects.all()
    person = Person.objects.all().last()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM hello_ItemsThree")
        All = cursor.fetchone()
        pOne = All[1]
        pTwo = All[2]
        Url = All[3]

        AllAll = cursor.fetchall()
        if AllAll:
            Random = random.choice(AllAll)
            pOneR = Random[1]
            pTwoR = Random[2]
            UrlR = Random[3]
            with connection.cursor() as cursor:
                cursor.execute(f'INSERT INTO hello_InvItem ("pOne", "pTwo", "Url", "Name") VALUES(\'{pOneR}\',\'{pTwoR}\',\'{UrlR}\',\'{person.Name}\')')
    return render(request, 'case_dastin.html', {"person": person, "pOneR": pOneR, "pTwoR": pTwoR, "UrlR": UrlR, "Random": Random, "Item": ItemTh, "pOne": pOne, "pTwo": pTwo, "Url": Url})





class ItemAdd(APIView):
    @extend_schema(
        request = ItemsSerializer, #| ItemsTwoSerializer | ItemsThreeSerializer |,
        responses={
            201: OpenApiResponse(response=ItemsSerializer, description="Item успешно создан"),
            400: OpenApiResponse(description="Ошибки валидации")
        }
    )
    def post(self, request):
        serializer = ItemsSerializer(data=request.data)
        if serializer.is_valid():
            Item = serializer.save()
            return Response({"status": "Item created", "id": Item.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ItemDelete(APIView):
    @extend_schema(
        responses={
            200: OpenApiResponse(description="Item успешно удалён"),
            404: OpenApiResponse(description="Item не найден"),
            400: OpenApiResponse(description="ID Item не предоставлен")
        }
    )
    def delete(self, request, item_id):
        if item_id:
            try:
                Item = Items.objects.get(id=item_id)
                Item.delete()
                return Response({"status": "Item deleted"}, status=status.HTTP_200_OK)
            except Items.DoesNotExist:
                return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "Item ID not provided"}, status=status.HTTP_400_BAD_REQUEST)