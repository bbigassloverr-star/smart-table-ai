from flask import Flask, jsonify, render_template
import random
import threading
import time

app = Flask(__name__)

# สถานะเริ่มต้นของโต๊ะ 4 ตัว
table_status = {
    "A1": "free",
    "A2": "free",
    "B1": "free",
    "B2": "free"
}

# จำลอง AI สุ่มสถานะโต๊ะ
def auto_simulation():
    while True:
        table = random.choice(list(table_status.keys()))
        table_status[table] = random.choice(["free", "occupied"])
        time.sleep(5)

# ทำงานเบื้องหลัง
threading.Thread(target=auto_simulation, daemon=True).start()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/status")
def status():
    return jsonify(table_status)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)