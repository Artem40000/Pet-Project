from django.shortcuts import render
import ollama
import os
import markdown
import json
import re
from urllib.parse import unquote


def prime(request):
    answer = ""
    code = ""
    mode = ""
    theory = ""
    language = ""

    Model = "llama3"
    client = ollama.Client(host=os.getenv("OLLAMA_HOST"))

    selected = request.GET.get("selected")
    if selected == 'llama':
        Model = "llama3"
    elif selected == 'qwen':
        Model = "qwen2.5:7b"

    if request.method == "POST":
        UserInput = request.POST.get("query", "").strip()
        router_messages = [{"role": "system", "content":
                """
                Определи тип запроса пользователя.
                code -> если пользователь просит написать код, исправить код,объяснить программирование, Python, JS, цикл, функцию и т.д.
                chat -> если обычный вопрос, приветствие, разговор, факты.
                ОТВЕТЬ МНЕ ОДНИМ СЛОВОМ НА ВЫБОР ВЫШЕ, ЭТО МОЖЕТ БЫТЬ code / chat .
                """
            }, {"role": "user","content": UserInput}]

        router_response = client.chat(model=Model, messages=router_messages)
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

            response = client.chat(model=Model, messages=Messages)
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

            response = client.chat(model=Model, messages=Messages)
            answer = response["message"]["content"]
    return render(request, 'prime.html', {"answer": answer, "Model": Model, "mode": mode, "code": code, "theory": theory, "language": language})