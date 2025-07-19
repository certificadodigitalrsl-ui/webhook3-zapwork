from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

ZAPWORK_API_URL = "https://app.zapwork.com.br/painel/notificacoes"
API_KEY = os.getenv("API_KEY")

@app.route("/", methods=["GET"])
def home():
    return "Servidor Webhook Zapwork ativo!"

@app.route("/webhook", methods=["POST"])
def receber_webhook():
    try:
        data = request.json
        nome = data.get("nome")
        telefone = data.get("telefone")
        mensagem = data.get("mensagem")

        payload = {
            "nome": nome,
            "telefone": telefone,
            "mensagem": mensagem
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": API_KEY
        }

        response = requests.post(ZAPWORK_API_URL, json=payload, headers=headers)

        return jsonify({
            "status": "ok",
            "zapwork_status": response.status_code,
            "zapwork_response": response.json()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
