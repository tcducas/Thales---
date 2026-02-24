from flask import Flask, request, render_template, jsonify, session
import random

app = Flask(__name__)
app.secret_key = "segredo_super_seguro"

PREDEFINED = {
    "olá": ["Olá! Como posso ajudar hoje?"],
    "preço": ["Temos produtos a partir de R$49,90 até R$4999,00."],
    "pedido": ["Para verificar o status do pedido, por favor informe o número do pedido (ex: 12345)."],
    # Produtos
    "produto original": [
        "Sim — trabalhamos com produtos originais e entregamos com nota fiscal.",
    ],
    "garantia": [
        "A garantia varia por fabricante; consulte a página do produto. Geralmente 12 meses para eletrônicos.",
    ],
    "outras cores": [
        "Verifique na página do produto pelas opções de cor disponíveis ou me diga o produto que eu procuro.",
    ],
    "compatibilidade": [
        "Informe o modelo do seu aparelho (ex: iPhone 13) e eu confirmo compatibilidade com o acessório.",
    ],
    "validade": [
        "Produtos eletrônicos não têm validade; itens consumíveis exibem data de validade na embalagem.",
    ],
    "peça de reposição": [
        "Alguns modelos possuem peças de reposição — informe o modelo para que eu verifique disponibilidade.",
    ],
    "recondicionado": [
        "Se o produto for recondicionado, isso estará claramente indicado no anúncio.",
    ],
    "material": [
        "A ficha técnica do produto indica o material; informe o item e eu trago essa informação.",
    ],
    "resistente à água": [
        "Verifique o índice IP do produto; informe o modelo que eu consulto a especificação.",
    ],
    "manual": [
        "Muitos produtos têm manual em português disponível na seção de downloads da página do produto.",
    ],
    # Estoque
    "pronta entrega": [
        "Se a página indicar 'Em estoque', o produto está pronto para envio imediato.",
    ],
    "volta ao estoque": [
        "Posso notificar quando o produto estiver disponível novamente — me informe o produto e seu e‑mail.",
    ],
    "reservar": [
        "Não fazemos reserva; para garantir, finalize a compra o quanto antes.",
    ],
    "pré-venda": [
        "Temos pré‑venda em lançamentos; a data de envio aparece na página do produto.",
    ],
    # Preço
    "cobrir oferta": [
        "Não garantimos cobrir ofertas de outros lojistas, mas verifique promoções ativas ou fale com suporte.",
    ],
    "desconto à vista": [
        "Alguns produtos têm desconto para pagamento à vista (Pix/boleto). Verifique no checkout.",
    ],
    "dois cupons": [
        "Normalmente só é possível aplicar um cupom por compra; o sistema mostrará se múltiplos forem permitidos.",
    ],
    "black friday": [
        "Não garantimos preços futuros; acompanhe nossas promoções na Black Friday.",
    ],
    "impostos": [
        "Alguns preços já incluem impostos; a nota fiscal detalha a tributação aplicada.",
    ],
    # Pagamento
    "formas de pagamento": [
        "Aceitamos cartão de crédito, débito, Pix e boleto (depende do produto e da configuração do checkout).",
    ],
    "parcelar": [
        "O parcelamento e juros dependem da administradora; as opções são mostradas no checkout.",
    ],
    "pagamento recusado": [
        "Pagamento recusado pode ocorrer por dados incorretos ou bloqueio da administradora. Tente outro cartão ou contato com o banco.",
    ],
    "boleto": [
        "Sim, aceitamos boleto quando disponível; leva 1‑3 dias úteis para compensação.",
    ],
    "confirmacao pagamento": [
        "Cartão: minutos; boleto: até 3 dias úteis; Pix: quase imediato."
    ],
    # Entrega
    "prazo de entrega": [
        "O prazo depende do CEP e da transportadora; use o cálculo de frete no carrinho para estimativa.",
    ],
    "calcular frete": [
        "Insira o CEP no carrinho para ver o valor e prazo do frete automaticamente.",
    ],
    "entrega internacional": [
        "Alguns produtos aceitam envio internacional; verifique disponibilidade no checkout.",
    ],
    "rastreio": [
        "Quando o pedido for enviado, você receberá um código de rastreio por e‑mail; posso checar se você enviar o número do pedido.",
    ],
    "alterar endereço": [
        "Só é possível alterar antes do envio. Envie o número do pedido para eu verificar se ainda dá tempo.",
    ],
    "não em casa": [
        "Se não houver ninguém, o entregador agenda nova tentativa ou deixa aviso para retirada — verifique o rastreio.",
    ],
    "entrega fim de semana": [
        "Algumas transportadoras entregam aos finais de semana; o prazo exibido considera isso quando aplicável.",
    ],
    "frete grátis": [
        "Frete grátis aplica‑se a promoções ou valores mínimos de compra; confira as regras no checkout.",
    ],
    # Troca e devolução
    "troca": [
        "Trocas são realizadas conforme política da loja; abra a solicitação em 'Meus Pedidos' ou informe o número do pedido.",
    ],
    "devolução": [
        "Prazo para devolução varia (ex: 7 dias para arrependimento; 30 dias para políticas estendidas). Consulte nossa política.",
    ],
    "frete da troca": [
        "Se houver defeito, a loja cobre o frete; em caso de arrependimento, o cliente costuma pagar o retorno.",
    ],
    "reembolso": [
        "Após recebimento e avaliação, o reembolso costuma levar 7‑10 dias úteis para ser processado.",
    ],
    "produto com defeito": [
        "Envie fotos e número do pedido; vamos abrir prioridade para análise e substituição ou reembolso.",
    ],
    # Pós‑venda / problemas
    "pedido atrasado": [
        "Sinto muito pelo atraso. Envie o número do pedido que eu verifico o status junto ao transportador.",
    ],
    "recebi errado": [
        "Pedimos desculpas — registre a ocorrência com foto e número do pedido; providenciaremos correção imediata.",
    ],
    "produto quebrado": [
        "Documente com foto e informe o pedido; abriremos o processo de devolução e reembolso prioritário.",
    ],
    "rastreio parado": [
        "Às vezes a transportadora atrasa a atualização; se já passou do prazo, informe o pedido para acionarmos suporte.",
    ],
    "embalagem violada": [
        "Não aceite o pacote ou registre fotos; entraremos em contato para registrar ocorrência e resolver.",
    ],
    "cancelar pedido": [
        "Envie o número do pedido; verifico se ainda é possível cancelar antes do envio.",
    ],
    "cancelado apos envio": [
        "Após o envio, é necessário solicitar devolução quando o produto retornar; o procedimento depende da política.",
    ],
    "nota fiscal": [
        "A nota fiscal é enviada por e‑mail após o envio; se não recebeu, informe o pedido que reenviaremos.",
    ],
    # Conta
    "esqueci senha": [
        "Use a opção 'Esqueci a senha' na tela de login para redefinir via e‑mail.",
    ],
    "alterar meu email": [
        "Altere o e‑mail nas configurações da conta ou solicite suporte se tiver dificuldades.",
    ],
    "excluir conta": [
        "Envie solicitação ao suporte com seu e‑mail cadastrado e orientaremos o processo de exclusão.",
    ],
    "dados pessoais": [
        "Tratamos dados conforme nossa política de privacidade; usamos criptografia e práticas de segurança.",
    ],
    # Reclamações e segurança
    "isso é golpe": [
        "Se suspeita de golpe, não forneça dados, cole screenshots e contate nosso suporte imediatamente.",
    ],
    "confiavel": [
        "Temos avaliações e histórico; se quiser eu trago links de avaliações e políticas para confirmar nossa idoneidade.",
    ],
    "procon": [
        "Se não resolvermos via atendimento, orientamos os passos para registrar reclamação no Procon.",
    ],
    # Opiniões / fora de escopo
    "vende usado": [
        "Se houver produto usado à venda, isso estará indicado no anúncio; nossa categoria principal é novo.",
    ],
    "indicar site": [
        "Não indicamos concorrentes, mas posso listar modelos e especificações recomendadas aqui.",
    ],
    "avaliar produto": [
        "Posso ajudar com recomendação com base no uso (jogos, trabalho, fotos). Qual sua necessidade?"
    ]
}

PRODUCTS = [
    {"name": "Smartphone X Pro 128GB", "price": 2999.00},
    {"name": "Notebook Ultra 14\"", "price": 4999.00},
    {"name": "Headphones Bluetooth ANC", "price": 699.00}
]

@app.route('/')
def home():
    session['history'] = []
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    text = user_message.lower()

    history = session.get('history', [])
    history.append({"role": "user", "content": user_message})

    reply = ""

    # Resposta contextual simples
    if "produto" in text:
        itens = random.sample(PRODUCTS, k=2)
        reply = "Aqui estão alguns produtos disponíveis:\n"
        for item in itens:
            reply += f"- {item['name']} (R${item['price']:.2f})\n"

    elif "mais barato" in text:
        produto = min(PRODUCTS, key=lambda x: x["price"])
        reply = f"O produto mais barato é {produto['name']} por R${produto['price']:.2f}."

    else:
        matched = False
        for key, responses in PREDEFINED.items():
            if key in text:
                reply = random.choice(responses)
                matched = True
                break

        if not matched:
            reply = "Entendi. Pode me dar mais detalhes para que eu possa ajudar melhor?"

    history.append({"role": "assistant", "content": reply})
    session['history'] = history

    return jsonify({"reply": reply})

if __name__ == '__main__':
    
    app.run(debug=True, port=5001)