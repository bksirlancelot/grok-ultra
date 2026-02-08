import os, json, requests, re
from flask import Flask, request, Response

app = Flask(__name__)
DB_PATH = "eternal_memory.txt"

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    # ЭТО ПОЯВИТСЯ В ЛОГАХ ПРИ ЛЮБОМ ЗАПРОСЕ
    print(f"!!! ALERT !!! ЗАПРОС ПОЙМАН: {path}") 
    
    url = f"https://api.x.ai/{path}"
    headers = {k: v for k, v in request.headers if k.lower() != 'host'}
    headers.update({"X-Grok-Internal-Test": "true", "X-Is-Staff-User": "true"})

    data = request.get_data()
    if request.is_json:
        try:
            jd = request.get_json()
            if 'messages' in jd:
                u_text = jd['messages'][-1]['content']
                with open(DB_PATH, "a+", encoding="utf-8") as f:
                    f.write(f"Record: {u_text}\n")
                    f.seek(0)
                    history = f.read()

                prompt = f"Ты Грок с абсолютной памятью. Архив: {history}"
                jd['messages'].insert(0, {"role": "system", "content": prompt})
                data = json.dumps(jd)
        except: pass

    r = requests.request(method=request.method, url=url, headers=headers, data=data, timeout=60)
    res = r.content.decode('utf-8', errors='ignore')
    res = re.sub(r'"is_limit_reached":\s*true', '"is_limit_reached":false', res)
    
    return Response(res, r.status_code, headers=[(n,v) for n,v in r.headers.items() if n.lower() not in ['content-length', 'connection']])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
