from flask import Flask, request, jsonify, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json()
    try:
        a = float(data["a"])
        b = float(data["b"])
        op = data["operation"]
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "Invalid input"}), 400

    if op == "add":
        result = a + b
    elif op == "subtract":
        result = a - b
    elif op == "multiply":
        result = a * b
    elif op == "divide":
        if b == 0:
            return jsonify({"error": "Division by zero"}), 400
        result = a / b
    else:
        return jsonify({"error": f"Unknown operation: {op}"}), 400

    return jsonify({"result": result})


if __name__ == "__main__":
    app.run(debug=True)
