from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["POST"])
def webhook():
    data = request.json
    name = data.get("name")
    whatsapp = data.get("whatsapp")

    print(f"📩 Novo agendamento recebido: {name} - WhatsApp: {whatsapp}")

    return jsonify({"status": "recebido", "name": name, "whatsapp": whatsapp}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
