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

# ฟังก์ชันสุ่มสถานะแบบสมจริง
def auto_simulation():
    tables = list(table_status.keys())

    while True:
        # เริ่มจากว่างทั้งหมดก่อน
        for table in tables:
            table_status[table] = "free"

        # สุ่มว่าจะมีคนนั่งกี่โต๊ะ (1-3 โต๊ะ)
        occupied_count = random.randint(1, 3)

        # สุ่มเลือกโต๊ะที่จะมีคนนั่ง
        occupied_tables = random.sample(tables, occupied_count)

        for table in occupied_tables:
            table_status[table] = "occupied"

        print("สถานะใหม่:", table_status)

        # เปลี่ยนทุก 5 วินาที
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