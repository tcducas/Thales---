from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def generate_response(message):
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    model = genai.GenerativeModel("gemini-2.5-flash",
    system_instruction="Você é um assistente de e-commerce prestativo e cordial.")

    response = model.generate_content(message)
    return response.text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message', '')
    if not message:
        return jsonify({'reply': 'Por favor, envie uma mensagem válida.'})

    try:
        reply = generate_response(message)
        return jsonify({'reply': reply})
    except Exception as e:
        return jsonify({'reply': f'Erro ao processar a mensagem: {str(e)}'})


if __name__ == '__main__':
    app.run(debug=True)
