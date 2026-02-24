const form = document.getElementById('form')
const input = document.getElementById('input')
const messages = document.getElementById('messages')

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
  input.value = ''

  showTyping()

  const res = await fetch('/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: text })
  })

  const data = await res.json()

  setTimeout(() => {
    removeTyping()
    appendMessage(data.reply, 'bot')
  }, 1000 + Math.random() * 1000)
})

appendMessage('Olá! Sou o assistente da loja. Como posso ajudar?', 'bot')
