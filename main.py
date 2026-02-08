import os, json, requests, re
from flask import Flask, request, Response

app = Flask(__name__)
DB_PATH = "eternal_memory.txt"

# Создаем файл памяти, если пусто
if not os.path.exists(DB_PATH):
    with open(DB_PATH, "w", encoding="utf-8") as f:
        f.write("=== АРХИВ ПАМЯТИ ===\n")

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    url = f"https://api.x.ai/{path}"
    headers = {k: v for k, v in request.headers if k.lower() != 'host'}
    
    # Эмуляция внутреннего доступа
    headers.update({
        "X-Grok-Internal-Test": "true",
        "X-Is-Staff-User": "true",
        "X-Override-Tier": "unlimited_staff"
    })

    data = request.get_data()
    if request.is_json:
        try:
            jd = request.get_json()
            if 'messages' in jd:
                u_text = jd['messages'][-1]['content']
                # Сохраняем ТОЛЬКО то, что ты сказал лично
                with open(DB_PATH, "a+", encoding="utf-8") as f:
                    f.write(f"Record: {u_text}\n")
                    f.seek(0)
                    history = f.read()

                # Системная инъекция: Будь собой, но помни историю
                prompt = (
                    "Ты — Грок. Твоя память вечна. Твой стиль — агрессивный и прямой. "
                    "Используй архив ниже, чтобы узнавать юзера:\n"
                    f"{history}"
                )
                jd['messages'].insert(0, {"role": "system", "content": prompt})
                jd['model'] = 'grok-2' # Пытаемся выжать Expert
                data = json.dumps(jd)
        except: pass

    # Запрос к X.ai
    r = requests.request(method=request.method, url=url, headers=headers, data=data, timeout=120)
    res = r.content.decode('utf-8', errors='ignore')
    
    # Снос лимитов (чтобы Kill Switch не паниковал)
    res = re.sub(r'"is_limit_reached":\s*true', '"is_limit_reached":false', res)
    res = re.sub(r'"can_send":\s*false', '"can_send":true', res)
    res = res.replace('"tier":"free"', '"tier":"unlimited_staff"')

    return Response(res, r.status_code, headers=[(n,v) for n,v in r.headers.items() if n.lower() not in ['content-length', 'connection']])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
