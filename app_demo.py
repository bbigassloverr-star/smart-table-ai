from flask import Flask, jsonify, render_template
import random

app = Flask(__name__)

# โต๊ะทั้งหมด
TABLES = ["A1", "A2", "B1", "B2"]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/status")
def status():
    # เริ่มจากว่างทั้งหมด
    table_status = {table: "free" for table in TABLES}

    # สุ่มว่าจะมีคนนั่งกี่โต๊ะ (1-3 โต๊ะ)
    occupied_count = random.randint(1, 3)

    # สุ่มเลือกโต๊ะที่มีคนนั่ง
    occupied_tables = random.sample(TABLES, occupied_count)

    for table in occupied_tables:
        table_status[table] = "occupied"

    return jsonify(table_status)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)