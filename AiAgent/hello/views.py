from django.shortcuts import render, redirect
import requests
from bs4 import BeautifulSoup
from ddgs import DDGS
import subprocess


def search_web(query, max_results=6):
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results): results.append(r["href"])
    return results

def parse_page(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=1)

        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style"]): tag.decompose()

        text = soup.get_text(separator=" ")
        text = " ".join(text.split())

        return text[:5000]
    except: return ""


def ask_local_llm(prompt):
    response = requests.post(
        "http://host.docker.internal:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()["response"]


def ai_agent(query):
    links = search_web(query)

    collected_text = ""

    for link in links:
        content = parse_page(link)

        if len(content) > 300:
            collected_text += content + "\n\n"

    collected_text = collected_text[:5000]
    prompt = f"""Ответь кратко и понятно. Вопрос: {query} Данные из интернета:{collected_text}"""

    return ask_local_llm(prompt)


if __name__ == "__main__":
    user_query = input("Введи запрос: ")
    answer = ai_agent(user_query)
    print("\nОтвет:\n", answer)




def prime(request):
    if request.method == "POST":
        user_query = request.POST.get("query")
        answer = ai_agent(user_query)

        request.session["answer"] = answer
        return redirect("/")

    answer = request.session.pop("answer", "")
    return render(request, "prime.html", {"answer": answer})