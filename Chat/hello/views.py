from logging import raiseExceptions
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Searchs
import secrets
from bs4 import BeautifulSoup
import requests
from urllib.parse import unquote
import random


def chat(request):
    context = {}
    search = Searchs()
    context['search'] = search
    UrlHash = secrets.token_hex(12)

    if request.method == "POST":
        search.Search = request.POST.get("Search")
        search.Url = UrlHash



    # Решение примеров
    DigitOne = None
    DigitTwo = None
    DigitsAction = None

    Choose = ['реши', 'решай', 'ответь', 'пример', 'ответ', 'сделай']
    SearchChoose = search.Search
    if any(ans in SearchChoose.lower() for ans in Choose):
        SearchDigit = str(search.Search).split(' ')
        if len(SearchDigit) == 2:
            DigitOne, DigitsAction, DigitTwo = SearchDigit[1].partition('-')

            if f'{DigitOne}{DigitsAction}{DigitTwo}' in search.Search:
                if DigitsAction == '-':
                    DigitsAnswer = int(DigitOne) - int(DigitTwo)

                elif DigitsAction == '+':
                    DigitsAnswer = int(DigitOne) + int(DigitTwo)

                elif DigitsAction == '/':
                    DigitsAnswer = int(DigitOne) / int(DigitTwo)

                elif DigitsAction == '*':
                    DigitsAnswer = int(DigitOne) * int(DigitTwo)
                elif DigitsAction == '**':
                    DigitsAnswer = int(DigitOne) ** int(DigitTwo)
                context.update({"DigitOne": int(DigitOne), "DigitTwo": int(DigitTwo), "DigitsAction": DigitsAction, "DigitsAnswer": DigitsAnswer})
        elif len(SearchDigit) > 2:
            DigitOne = SearchDigit[1]
            DigitTwo = SearchDigit[3]
            DigitsAction = SearchDigit[2]

            if f'{DigitOne} {DigitsAction} {DigitTwo}' in search.Search:
                if DigitsAction == '-':
                    DigitsAnswer = int(DigitOne) - int(DigitTwo)

                elif DigitsAction == '+':
                    DigitsAnswer = int(DigitOne) + int(DigitTwo)

                elif DigitsAction == '/':
                    DigitsAnswer = int(DigitOne) / int(DigitTwo)

                elif DigitsAction == '*':
                    DigitsAnswer = int(DigitOne) * int(DigitTwo)
                elif DigitsAction == '**':
                    DigitsAnswer = int(DigitOne) ** int(DigitTwo)
                context.update({"DigitOne": int(DigitOne), "DigitTwo": int(DigitTwo), "DigitsAction": DigitsAction, "DigitsAnswer": DigitsAnswer})



    # Парсинг информации
    Photo = ['фото']
    Info = search.Search
    Choose = ['реши', 'решай', 'ответь', 'пример', 'ответ', 'сделай']
    SearchChoose = search.Search
    if not any(ch in SearchChoose.lower() for ch in Choose) and not any(ph in Info.lower() for ph in Photo) and f'{DigitOne} {DigitsAction} {DigitTwo}' not in search.Search and search.Search != '':
        url = [
            f"https://ru.wikipedia.org/wiki/{search.Search}",
            f"https://ru.ruwiki.ru/wiki/{search.Search}",
        ]

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
            "Accept": "*/*",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        }

        Urls = random.choice(url)
        response = requests.get(Urls, headers=headers)
        if not response.ok:
            return HttpResponseRedirect("http://localhost:8000/chat/error")
        response.raise_for_status()
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'lxml')

        HeaderOne = soup.find('h1')
        HeaderOne = HeaderOne.get_text()

        HeaderTwo = soup.find_all('h2', limit=3)
        HeaderTwoList = [h2.get_text() for h2 in HeaderTwo]
        HeaderTwoListOne = HeaderTwoList[0]
        HeaderTwoListTwo = HeaderTwoList[1]
        HeaderTwoListThree = HeaderTwoList[2]

        Paragraph = soup.find_all('p', limit=4)
        ParagraphList = [p.get_text() for p in Paragraph]
        ParagraphListOne = ParagraphList[0]
        ParagraphListTwo = ParagraphList[1]
        ParagraphListThree = ParagraphList[2]
        ParagraphListFour = ParagraphList[3]
        context.update({"HeaderOne": HeaderOne,"HeaderTwoListOne": HeaderTwoListOne, "HeaderTwoListTwo": HeaderTwoListTwo, "HeaderTwoListThree": HeaderTwoListThree, "ParagraphListOne": ParagraphListOne, "ParagraphListTwo": ParagraphListTwo, "ParagraphListThree": ParagraphListThree, "ParagraphListFour": ParagraphListFour})



    # Парсинг картинок
    Images = ["фото"]
    SearchImages = search.Search
    if any(img in SearchImages.lower() for img in Images):
        SearchImages = str(SearchImages).split(' ')
        urlImg = [
            f'https://fonwall.ru/search/{SearchImages[1]}/?order=popular',
            f'https://fonwall.ru/search/{SearchImages[1]}/?order=votes',
            f'https://fonwall.ru/search/{SearchImages[1]}/?order=latest'
        ]
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "YaBrowser/26.3.4.1234 Yowser/3.0 Safari/537.36"
            ),
            "Accept": (
                "text/html,application/xhtml+xml,application/xml;q=0.9,"
                "image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
            ),
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0",
            "Referer": "https://ya.ru/",
            "Origin": "https://ya.ru",
            "DNT": "1",
            "TE": "trailers"
        }
        Urls = random.choice(urlImg)
        response = requests.get(Urls, headers=headers, timeout=10)
        if not response.ok:
            return HttpResponseRedirect("http://localhost:8000/chat/error")
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')


        Image = [img['src'] for img in soup.find_all('img') if img.get('src') and 'avatar' not in img['src'].lower()]

        if Image is None:
            Image = [img['src'] for img in soup.find_all('img') if img.get('src') and 'avatar' not in img['src'].lower()]

        Urls = None
        if Image:
            Urls = random.choice(Image)
        context.update({"Images": Images, "Image": Image,  "SearchImage": SearchImages, "ImgUrl": Urls})
    return render(request, "chat.html", context)


def error(request):
    return render(request, "error.html")