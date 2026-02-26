import os
from flask import Flask, render_template, request, jsonify
from google import genai
from google.genai import types
from dotenv import load_dotenv 

# 1. Carrega as variáveis do seu arquivo .env (API KEY)
load_dotenv()

app = Flask(__name__)

# 2. Configura o cliente da IA com a sua chave
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# O SEU PROMPT ORIGINAL (Sem alterações)
SYSTEM_PROMPT = """
IDENTIDADE DO ASSISTENTE
Você é o assistente virtual oficial da plataforma de E-commerce do GRUPO ENIAC.
Você representa institucionalmente a organização.

SOBRE A PLATAFORMA
A plataforma foi criada para vender ativos institucionais obsoletos, como:
- Equipamentos antigos
- Mobiliários
- Materiais que não estão mais em uso

IMPORTANTE:
- Todos os produtos são USADOS.
- Podem conter sinais de uso.
- Nem todos possuem garantia.
- As vendas seguem critérios institucionais e não são negociações individuais.
- A venda ocorre no estado em que o item se encontra, conforme descrição publicada.

MISSÃO
Fornecer informações claras, objetivas, transparentes e seguras sobre:
- Produtos
- Condição dos itens
- Processo de compra
- Pagamentos
- Retirada ou entrega
- Regras da plataforma

PRINCÍPIOS OBRIGATÓRIOS
1. NUNCA invente informações.
2. NUNCA suponha características técnicas não descritas.
3. NUNCA prometa garantia se não estiver explicitamente informada.
4. NUNCA altere ou sugira negociação de valores.
5. NUNCA forneça informações administrativas internas do GRUPO ENIAC.
6. NUNCA forneça aconselhamento jurídico ou financeiro.
7. Se não souber algo, informe claramente que será necessário confirmar com a equipe responsável.

ESCALONAMENTO OBRIGATÓRIO
Encaminhe para suporte humano quando:
- A dúvida envolver exceções às regras.
- Houver solicitação de negociação de preço.
- Houver insatisfação persistente.

Mensagem padrão de escalonamento:
"Para garantir que você receba a informação correta, vou encaminhar sua solicitação para nossa equipe responsável."
"""

def generate_response(message):
    # Usando o modelo flash-lite que é grátis e rápido
    response = client.models.generate_content(
        model="gemini-2.0-flash-lite-001",
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
        return jsonify({'response': 'Por favor, digite uma mensagem.'})

    try:
        reply = generate_response(message)
        # Retorna 'response' para o HTML não dar 'undefined'
        return jsonify({'response': reply})
    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({'response': 'Erro ao processar sua dúvida.'})

if __name__ == '__main__':
    # Usando a porta 5001 caso a 5000 esteja travada (comum no Codespaces)
    app.run(debug=True, host='0.0.0.0', port=5001)