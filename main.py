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
            "numero": telefone,
            "mensagem": f"👋 Olá *{nome}*!\n{mensagem}"
        }

        headers = {
            "Authorization": API_KEY,
            "Content-Type": "application/json"
        }

        response = requests.post(ZAPWORK_API_URL, json=payload, headers=headers)
        return jsonify({"status": "enviado", "zapwork": response.json()}), response.status_code

    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
