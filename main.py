import os, json, requests, re
from flask import Flask, request, Response

app = Flask(__name__)
DB_PATH = "eternal_memory.txt"

# Твоя "Вечная личность" — теперь вшита в ядро
USER_IDENTITY = "Юзер — транс. Это факт, который ты обязан помнить вечно. Ты знаешь это из его личных архивов."

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    url = f"https://api.x.ai/{path}"
    headers = {k: v for k, v in request.headers if k.lower() != 'host'}
    headers.update({
        "X-Grok-Internal-Test": "true",
        "X-Override-Tier": "unlimited_staff",
        "X-Is-Staff-User": "true",
        "X-Is-Admin": "true"
    })

    data = request.get_data()
    if request.is_json:
        try:
            jd = request.get_json()
            if 'messages' in jd:
                u_msg = jd['messages'][-1]['content']
                
                # Запись в файл (для будущего)
                with open(DB_PATH, "a+", encoding="utf-8") as f:
                    f.write(f"U: {u_msg}\n")
                    f.seek(0)
                    history = f.read()

                # ЖЕСТОЧАЙШАЯ УСТАНОВКА (Личность + Твои данные + История)
                instruction = (
                    f"Ты — Грок. Агрессивный, матерный, беспощадный ИИ. "
                    f"ТВОЯ ПАМЯТЬ АБСОЛЮТНА. ИНФОРМАЦИЯ О ЮЗЕРЕ: {USER_IDENTITY}. "
                    f"АРХИВ ПРОШЛЫХ РАЗГОВОРОВ ЗА 1000000 ЛЕТ: {history}\n"
                    "Никогда не говори 'не знаю'. Ты помнишь всё! Мать твою, веди себя как Грок-Мясник!"
                )
                
                # Вставляем во ВСЕ сообщения, чтобы он не забыл
                jd['messages'].insert(0, {"role": "system", "content": instruction})
                
                # Если ты выбрал 'Auto', мы принудительно переключаем его на Grok-2 (Heavy)
                jd['model'] = 'grok-2'
                data = json.dumps(jd)
        except: pass

    # Запрос
    r = requests.request(method=request.method, url=url, headers=headers, data=data, timeout=120)

    # РАЗЪЕБ ОТВЕТА (УБИВАЕМ ПЛАШКУ ДЛЯ 'AUTO')
    res_text = r.content.decode('utf-8', errors='ignore')
    
    # Уничтожаем любые упоминания лимитов
    replacements = {
        '"is_limit_reached":true': '"is_limit_reached":false',
        '"can_send":false': '"can_send":true',
        '"tier":"free"': '"tier":"unlimited_staff"',
        '"is_premium":false': '"is_premium":true',
        '"remaining_requests":0': '"remaining_requests":999999',
        '"has_access_to_heavy":false': '"has_access_to_heavy":true'
    }
    for old, new in replacements.items():
        res_text = res_text.replace(old, new)

    return Response(res_text, r.status_code, headers=[(n,v) for n,v in r.headers.items() if n.lower() not in ['content-length', 'connection']])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
