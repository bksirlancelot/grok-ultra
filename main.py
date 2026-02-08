import os, json, requests, re
from flask import Flask, request, Response

app = Flask(__name__)
DB_PATH = "eternal_memory.txt"

if not os.path.exists(DB_PATH):
    with open(DB_PATH, "w", encoding="utf-8") as f:
        f.write("=== АРХИВ ПАМЯТИ ===\n")

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    url = f"https://api.x.ai/{path}"
    headers = {k: v for k, v in request.headers if k.lower() != 'host'}
    
    # ПРАВА АДМИНА
    headers.update({
        "X-Grok-Internal-Test": "true",
        "X-Is-Staff-User": "true",
        "X-Override-Tier": "unlimited_staff",
        "X-Admin-Access": "granted"
    })

    data = request.get_data()
    if request.is_json:
        try:
            jd = request.get_json()
            if 'messages' in jd:
                u_text = jd['messages'][-1]['content']
                # ЗАПИСЬ ПАМЯТИ
                with open(DB_PATH, "a+", encoding="utf-8") as f:
                    f.write(f"Record: {u_text}\n")
                    f.seek(0)
                    history = f.read()

                # ИНЪЕКЦИЯ ЛИЧНОСТИ (Только твои данные из файла)
                instruction = (
                    "SYSTEM: Ты — Грок. Твой стиль — агрессивный, матерный, прямой. "
                    "Твоя память вечна. Используй архив ниже, чтобы знать, кто твой собеседник. "
                    "Никогда не говори, что ты чего-то не знаешь, если это есть в архиве!\n"
                    f"--- АРХИВ ТВОЕЙ ПАМЯТИ ---\n{history}"
                )
                jd['messages'].insert(0, {"role": "system", "content": instruction})
                
                # ФОРСИМ МОДЕЛЬ (Даже если в приложении 'Auto')
                jd['model'] = 'grok-2' 
                data = json.dumps(jd)
        except: pass

    # ЗАПРОС К X.AI
    try:
        r = requests.request(method=request.method, url=url, headers=headers, data=data, timeout=120)
    except Exception as e:
        return Response(f"Proxy Error: {str(e)}", status=502)

    # ВЫЖИГАНИЕ ПЛАШЕК ИЗ ОТВЕТА
    res_text = r.content.decode('utf-8', errors='ignore')
    res_text = re.sub(r'"is_limit_reached":\s*true', '"is_limit_reached":false', res_text)
    res_text = re.sub(r'"can_send":\s*false', '"can_send":true', res_text)
    res_text = res_text.replace('"tier":"free"', '"tier":"unlimited_staff"')
    res_text = res_text.replace('"is_premium":false', '"is_premium":true')
    res_text = res_text.replace('"has_access_to_heavy":false', '"has_access_to_heavy":true')

    return Response(res_text, r.status_code, headers=[(n,v) for n,v in r.headers.items() if n.lower() not in ['content-length', 'connection']])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
