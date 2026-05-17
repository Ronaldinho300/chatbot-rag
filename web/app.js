// ==========================
// URL API
// ==========================
const API_BASE_URL = 'https://chatbot-rag-2-tzn4.onrender.com';

// ==========================
// Estado del documento actual
// null = sin documento cargado → backend usa solo identidad
// ==========================
let currentDocument = null;

// ==========================
// Elementos DOM
// ==========================
const sendBtn   = document.getElementById('send-btn');
const input     = document.getElementById('user-input');
const chatBox   = document.getElementById('chat-content');
const fileInput = document.getElementById('file-upload');
const statusDot = document.getElementById('status-dot');
const statusTxt = document.getElementById('status-text');

// ==========================
// Estado de la API
// ==========================
function setStatus(estado) {
    // estado: 'online' | 'offline' | 'loading'
    const labels = {
        online:  'En línea',
        offline: 'No disponible',
        loading: 'Conectando…'
    };
    if (statusDot) statusDot.dataset.status = estado;
    if (statusTxt) statusTxt.textContent = labels[estado] ?? estado;
}

// ==========================
// Agregar mensajes al chat
// ==========================
function addMessage(text, isUser = false) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `msg ${isUser ? 'user' : 'bot'}`;
    msgDiv.innerHTML = text;
    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
    return msgDiv;
}

// ==========================
// Parse JSON seguro
// ==========================
async function safeJson(res) {
    const text = await res.text();
    try {
        return JSON.parse(text);
    } catch {
        return { error: 'Respuesta inválida del servidor' };
    }
}

// ==========================
// Enviar mensaje al chat
// ==========================
async function enviar() {
    const texto = input.value.trim();
    if (!texto) return;

    addMessage(texto, true);
    input.value = '';

    const loadingMsg = addMessage('🤔 Pensando...', false);

    // Body: si no hay documento cargado, no se envía el campo
    // para que el backend use solo la identidad del bot.
    const body = { pregunta: texto };
    if (currentDocument) body.documento = currentDocument;

    try {
        const res = await fetch(`${API_BASE_URL}/chat`, {
            method:  'POST',
            headers: { 'Content-Type': 'application/json' },
            body:    JSON.stringify(body)
        });

        const data = await safeJson(res);
        loadingMsg.remove();

        if (!res.ok) {
            addMessage(`❌ Error: ${data.error || 'Error del servidor'}`, false);
            return;
        }

        addMessage(data.respuesta || 'Sin respuesta.', false);

    } catch (err) {
        console.error('[CHAT ERROR]', err);
        loadingMsg.remove();
        addMessage(
            '❌ No se pudo conectar con el servidor.<br>' +
            'Puede que la API esté iniciando (Render free tarda ~30 s). Intenta de nuevo.',
            false
        );
    }
}

// ==========================
// Subir archivo
// ==========================
async function uploadFile(file) {
    if (!file) return;

    const uploadMsg = addMessage(`📄 Subiendo <b>${file.name}</b>…`, true);

    const formData = new FormData();
    formData.append('archivo', file);

    try {
        const res = await fetch(`${API_BASE_URL}/upload`, {
            method: 'POST',
            body:   formData
            // ⚠️ NO pongas Content-Type aquí; el navegador lo pone
            //    automáticamente con el boundary correcto para multipart.
        });

        const data = await safeJson(res);

        if (!res.ok) {
            uploadMsg.innerHTML =
                `❌ No se pudo procesar: ${data.error || 'Error del servidor'}`;
            return;
        }

        // Guardar nombre base del documento (sin extensión)
        currentDocument = file.name.replace(/\.[^/.]+$/, '');

        uploadMsg.innerHTML =
            `✅ <b>${file.name}</b> cargado correctamente.<br>` +
            `Ahora puedes hacerme preguntas sobre este documento.`;

    } catch (err) {
        console.error('[UPLOAD ERROR]', err);
        uploadMsg.innerHTML =
            '❌ Error al subir el archivo.<br>' +
            'Verifica que la API esté activa e inténtalo de nuevo.';
    }

    chatBox.scrollTop = chatBox.scrollHeight;
}

// ==========================
// Eventos de la interfaz
// ==========================
sendBtn.onclick = enviar;

input.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') enviar();
});

fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) uploadFile(file);
    fileInput.value = ''; // permite volver a subir el mismo archivo
});

// ==========================
// Wake-up Render al cargar
// Render free duerme tras 15 min de inactividad.
// Este ping inicial lo despierta y actualiza el indicador.
// ==========================
window.addEventListener('load', async () => {
    setStatus('loading');
    try {
        const res = await fetch(`${API_BASE_URL}/health`);
        if (res.ok) {
            setStatus('online');
            console.log('✅ API activa');
        } else {
            setStatus('offline');
            console.warn('⚠️ API respondió con error:', res.status);
        }
    } catch {
        setStatus('offline');
        console.warn('⚠️ API no disponible');
    }
});
