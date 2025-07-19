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

        if not all([nome, telefone, mensagem]):
            return jsonify({"erro": "Campos obrigatórios ausentes"}), 400

        payload = {
            "numero": telefone,
            "mensagem": mensagem,
            "nome": nome
        }
        headers = {
            "Content-Type": "application/json",
            "x-api-key": API_KEY
        }
        response = requests.post(ZAPWORK_API_URL, json=payload, headers=headers)
        response.raise_for_status()

        return jsonify({"status": "Mensagem enviada com sucesso!"}), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
