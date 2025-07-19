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
            "mensagem": mensagem,
            "apiKey": API_KEY
        }

        response = requests.post(ZAPWORK_API_URL, json=payload)

        if response.status_code == 200:
            return jsonify({"status": "sucesso", "zapwork": response.json()})
        else:
            return jsonify({"status": "erro", "detalhes": response.text}), response.status_code

    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
