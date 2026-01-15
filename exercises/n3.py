from flask import Flask, jsonify, request

app = Flask(__name__)

# Endpoint para obtener un pago
@app.route("/api/payments/<int:payment_id>", methods=["GET"])
def get_payment(payment_id):
    mock_data = {"id": payment_id, "amount": 500, "currency": "MXN"}
    return jsonify(mock_data), 200

# Endpoint para crear un pago
@app.route("/api/payments", methods=["POST"])
def create_payment():
    data = request.get_json()
    if "amount" not in data:
        return jsonify({"error": "Campo 'amount' requerido"}), 400
    return jsonify({"message": "Pago creado exitosamente"}), 201

if __name__ == "__main__":
    app.run(debug=True)
