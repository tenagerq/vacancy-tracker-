from flask import Flask, request, jsonify, send_from_directory
import json, os
from datetime import datetime

app = Flask(__name__, static_folder="static")
DATA_FILE = "vacancies.json"

def load():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/api/vacancies", methods=["GET"])
def get_vacancies():
    return jsonify(load())

@app.route("/api/vacancies", methods=["POST"])
def add_vacancy():
    data = request.json
    vacancies = load()
    vacancy = {
        "id": int(datetime.now().timestamp() * 1000),
        "date": datetime.now().strftime("%d.%m.%Y"),
        "company": data.get("company", "").strip(),
        "position": data.get("position", "").strip(),
        "status": data.get("status", "Applied")
    }
    if not vacancy["company"] or not vacancy["position"]:
        return jsonify({"error": "Заполните компанию и должность"}), 400
    vacancies.insert(0, vacancy)
    save(vacancies)
    return jsonify(vacancy), 201

@app.route("/api/vacancies/<int:vid>", methods=["DELETE"])
def delete_vacancy(vid):
    vacancies = load()
    vacancies = [v for v in vacancies if v["id"] != vid]
    save(vacancies)
    return jsonify({"ok": True})

if __name__ == "__main__":
    os.makedirs("static", exist_ok=True)
    print("\n✅  Трекер вакансий запущен!")
    print("👉  Откройте в браузере: http://localhost:5000\n")
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
