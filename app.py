from flask import Flask, jsonify, render_template

app = Flask(__name__)

table_status = {
    "A1": "free",
    "A2": "free"
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/status")
def status():
    return jsonify(table_status)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)