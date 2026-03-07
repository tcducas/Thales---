const form = document.getElementById('form')
const input = document.getElementById('input')
const messages = document.getElementById('messages')

const conversation = []

function appendMessage(text, cls) {
  const el = document.createElement('div')
  el.className = 'message ' + cls
  el.textContent = text
  messages.appendChild(el)
  messages.scrollTop = messages.scrollHeight
  return el
}

function showTyping() {
  const typing = document.createElement('div')
  typing.className = 'message bot typing'
  typing.textContent = 'IA está digitando...'
  typing.id = 'typing'
  messages.appendChild(typing)
  messages.scrollTop = messages.scrollHeight
}

function removeTyping() {
  const typing = document.getElementById('typing')
  if (typing) typing.remove()
}

form.addEventListener('submit', async (e) => {
  e.preventDefault()

  const text = input.value.trim()
  if (!text) return

  appendMessage(text, 'user')
  conversation.push({ role: 'user', content: text })
  input.value = ''

  showTyping()

  try {
    const payload = { messages: conversation }
    console.log('Payload enviado para /chat:', payload)

    const res = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })

    const data = await res.json()
    console.log('Resposta do backend:', data)

    removeTyping()

    const reply = data.response || 'Desculpe, não consegui responder agora.'
    appendMessage(reply, 'bot')
    conversation.push({ role: 'assistant', content: reply })

  } catch (error) {
    removeTyping()
    appendMessage('Desculpe, ocorreu um erro ao processar sua solicitação.', 'bot')
    console.error('Erro no chat:', error)
  }
})

appendMessage('Sou o assistente da loja. Como posso ajudar?', 'bot')