from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

ZAPWORK_API_URL = "https://app.zapwork.com.br/painel/notificacoes"
API_KEY = os.getenv("API_KEY")  # Definida como variável de ambiente no Render

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

        if not all([telefone, mensagem]):
            return jsonify({"error": "Campos obrigatórios ausentes."}), 400

        headers = {
            "Authorization": API_KEY,
            "Content-Type": "application/json"
        }
        payload = {
            "telefone": telefone,
            "mensagem": mensagem
        }

        response = requests.post(ZAPWORK_API_URL, json=payload, headers=headers)

        if response.status_code == 200:
            return jsonify({"status": "sucesso", "resposta": response.json()})
        else:
            return jsonify({"erro": "Falha ao enviar para Zapwork", "resposta": response.text}), 500

    except Exception as e:
        return jsonify({"erro": "Erro interno", "mensagem": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
