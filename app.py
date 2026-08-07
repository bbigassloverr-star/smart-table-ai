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

# ฟังก์ชันสุ่มสถานะโต๊ะ
def auto_simulation():
    while True:
        for table in table_status:
            table_status[table] = random.choice(["free", "occupied"])

        print("สุ่มสถานะใหม่:", table_status)
        time.sleep(5)

# เริ่ม Thread ทันที
simulation_thread = threading.Thread(target=auto_simulation)
simulation_thread.daemon = True
simulation_thread.start()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/status")
def status():
    return jsonify(table_status)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)