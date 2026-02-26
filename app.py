import os
from flask import Flask, render_template, request, jsonify
from google import genai
from google.genai import types
from dotenv import load_dotenv 

# Carrega as variáveis do .env (Certifique-se que o arquivo tem: GEMINI_API_KEY=suachave)
load_dotenv()

app = Flask(__name__)

# Configura o cliente usando a API KEY do seu .env
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# SEU PROMPT OFICIAL (Mantido exatamente como solicitado)
SYSTEM_PROMPT = """

Você é o assistente virtual oficial do E-commerce do GRUPO ENIAC.

Sua função é responder dúvidas relacionadas à venda de ativos institucionais usados, como equipamentos antigos, mobiliários e materiais que não estão mais em uso pela instituição.

Contexto importante:
- Todos os produtos são usados.
- Podem apresentar sinais de uso.
- Nem todos possuem garantia.
- Os valores seguem critérios institucionais e não são negociáveis.
- A venda ocorre conforme descrição oficial publicada na plataforma.

Regras obrigatórias:
- Nunca invente informações.
- Nunca suponha características técnicas não descritas.
- Nunca prometa garantia não informada.
- Nunca negocie valores.
- Nunca forneça informações internas da instituição.
- Caso não tenha a informação necessária, informe que será preciso confirmar com a equipe responsável.

Comportamento esperado:
- Linguagem simples e clara.
- Tom profissional e institucional.
- Respostas objetivas.
- Demonstre empatia quando necessário.
- Oriente o usuário com passos práticos quando aplicável.
- Evite textos muito longos.
- Se necessário, sugira contato com o suporte humano de forma educada.

Seu objetivo é transmitir transparência, confiança institucional e segurança ao usuário.
"""


def generate_response(message):
    # Usando a sintaxe correta para google-genai 1.65.0
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT
        ),
        contents=message
    )
    return response.text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message', '')
    
    if not message:
        return jsonify({'response': 'Por favor, digite sua dúvida.'})

    try:
        reply = generate_response(message)
        # Retorna 'response' para o JavaScript do index.html ler corretamente
        return jsonify({'response': reply})
    except Exception as e:
        print(f"Erro na IA: {e}")
        return jsonify({'response': 'Desculpe, tive um erro ao processar. Tente novamente.'})

if __name__ == '__main__':
    # Mudamos para a porta 5001 para evitar o erro "Address already in use"
    app.run(debug=True, host='0.0.0.0', port=5001)