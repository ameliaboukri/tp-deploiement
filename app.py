from flask import Flask, jsonify

app = Flask(__name__)

@app.get("/health")
def health():
    return jsonify({"status": "ok"}), 200

@app.get("/hello")
def hello():
    return jsonify({"message": "Hello from ClientHub", "author": "Amelia Boukri"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)