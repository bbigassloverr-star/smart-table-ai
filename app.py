from flask import Flask, jsonify, render_template
from threading import Lock

app = Flask(__name__)

# สถานะโต๊ะที่ AI ส่งเข้ามา
table_status = {
    "A1": "free",
    "A2": "free",
    "B1": "free",
    "B2": "free"
}

status_lock = Lock()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/status")
def status():
    with status_lock:
        return jsonify(table_status)


@app.route("/api/update", methods=["POST"])
def update_status():
    from flask import request

    data = request.get_json()

    if not isinstance(data, dict):
        return jsonify({"error": "invalid data"}), 400

    with status_lock:
        for table in table_status:
            if table in data and data[table] in ["free", "occupied"]:
                table_status[table] = data[table]

    return jsonify({
        "success": True,
        "tables": table_status
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)