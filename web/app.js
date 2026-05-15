// 👇 CAMBIA ESTA URL POR LA DE TU API EN RENDER (sin barra al final)
const API_BASE_URL = 'https://chatbot-rag-1-u4jn.onrender.com';  // ← tu URL real

let currentDocument = 'documento'; // nombre por defecto (sin extensión)

const sendBtn = document.getElementById('send-btn');
const input = document.getElementById('user-input');
const chatBox = document.getElementById('chat-content');
const fileInput = document.getElementById('file-upload');

// Función para agregar mensajes al chat
function addMessage(text, isUser = false) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `msg ${isUser ? 'user' : 'bot'}`;
    msgDiv.innerHTML = text;
    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
    return msgDiv;
}

// Enviar pregunta al chatbot
async function enviar() {
    const texto = input.value.trim();
    if (!texto) return;

    addMessage(texto, true);
    input.value = '';

    // Indicador de carga
    const loadingMsg = addMessage('🤔 Pensando...', false);

    try {
        const res = await fetch(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                pregunta: texto,
                documento: currentDocument
            })
        });
        const data = await res.json();
        loadingMsg.remove();
        addMessage(data.respuesta || 'No se obtuvo respuesta.', false);
    } catch (error) {
        loadingMsg.remove();
        addMessage('⚠️ Error de conexión con el servidor. Verifica que la API esté activa.', false);
    }
}

// Subir archivo a la API
async function uploadFile(file) {
    if (!file) return;

    const uploadMsg = addMessage(`📄 Subiendo <b>${file.name}</b> ...`, true);

    const formData = new FormData();
    formData.append('archivo', file);

    try {
        const res = await fetch(`${API_BASE_URL}/upload`, {
            method: 'POST',
            body: formData
        });
        const data = await res.json();
        if (res.ok) {
            // Extraer nombre base sin extensión
            const baseName = file.name.replace(/\.[^/.]+$/, '');
            currentDocument = baseName;
            uploadMsg.innerHTML = `✅ Documento <b>${file.name}</b> procesado. Ahora puedes preguntar sobre él.`;
        } else {
            uploadMsg.innerHTML = `❌ Error: ${data.error || 'No se pudo procesar el archivo.'}`;
        }
    } catch (error) {
        uploadMsg.innerHTML = `❌ Error de conexión al subir el archivo.`;
    }
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Eventos
sendBtn.onclick = enviar;
input.onkeypress = (e) => { if (e.key === 'Enter') enviar(); };
fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) uploadFile(file);
    fileInput.value = ''; // permite volver a subir el mismo archivo
});