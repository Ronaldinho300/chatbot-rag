// ==========================
// URL API
// ==========================
const API_BASE_URL =
    'https://chatbot-rag-1-u4jn.onrender.com';

// ==========================
// Documento actual
// ==========================
let currentDocument = 'documento';

// ==========================
// Elementos DOM
// ==========================
const sendBtn =
    document.getElementById('send-btn');

const input =
    document.getElementById('user-input');

const chatBox =
    document.getElementById('chat-content');

const fileInput =
    document.getElementById('file-upload');

// ==========================
// Agregar mensajes
// ==========================
function addMessage(
    text,
    isUser = false
) {

    const msgDiv =
        document.createElement('div');

    msgDiv.className =
        `msg ${isUser ? 'user' : 'bot'}`;

    msgDiv.innerHTML = text;

    chatBox.appendChild(msgDiv);

    chatBox.scrollTop =
        chatBox.scrollHeight;

    return msgDiv;
}

// ==========================
// Validar respuesta JSON
// ==========================
async function safeJson(res) {

    const text = await res.text();

    try {
        return JSON.parse(text);
    }

    catch {

        return {
            error:
                'Respuesta inválida del servidor'
        };
    }
}

// ==========================
// Enviar mensaje
// ==========================
async function enviar() {

    const texto =
        input.value.trim();

    if (!texto) return;

    addMessage(texto, true);

    input.value = '';

    // ==========================
    // Loading
    // ==========================
    const loadingMsg =
        addMessage(
            '🤔 Pensando...',
            false
        );

    try {

        const res = await fetch(
            `${API_BASE_URL}/chat`,
            {
                method: 'POST',

                headers: {
                    'Content-Type':
                        'application/json'
                },

                body: JSON.stringify({
                    pregunta: texto,
                    documento: currentDocument
                })
            }
        );

        const data =
            await safeJson(res);

        loadingMsg.remove();

        // ==========================
        // Error servidor
        // ==========================
        if (!res.ok) {

            addMessage(
                `❌ Error: ${
                    data.error ||
                    'Error interno servidor'
                }`,
                false
            );

            return;
        }

        // ==========================
        // Mostrar respuesta
        // ==========================
        addMessage(
            data.respuesta ||
            'No se obtuvo respuesta.',
            false
        );
    }

    catch (error) {

        console.error(error);

        loadingMsg.remove();

        addMessage(
            `
            ❌ Error de conexión.

            Posibles causas:
            <br><br>

            • API caída
            <br>
            • Error CORS
            <br>
            • Backend en Render dormido
            <br>
            • Error interno Flask
            `,
            false
        );
    }
}

// ==========================
// Subir archivo
// ==========================
async function uploadFile(file) {

    if (!file) return;

    // ==========================
    // Mostrar subida
    // ==========================
    const uploadMsg =
        addMessage(
            `📄 Subiendo <b>${file.name}</b>...`,
            true
        );

    // ==========================
    // FormData
    // ==========================
    const formData = new FormData();

    formData.append(
        'archivo',
        file
    );

    try {

        const res = await fetch(
            `${API_BASE_URL}/upload`,
            {
                method: 'POST',
                body: formData
            }
        );

        const data =
            await safeJson(res);

        // ==========================
        // Error backend
        // ==========================
        if (!res.ok) {

            uploadMsg.innerHTML =
                `
                ❌ Error:
                ${data.error ||
                'No se pudo procesar'}
                `;

            return;
        }

        // ==========================
        // Documento actual
        // ==========================
        const baseName =
            file.name.replace(
                /\.[^/.]+$/,
                ''
            );

        currentDocument =
            baseName;

        // ==========================
        // Éxito
        // ==========================
        uploadMsg.innerHTML =
            `
            ✅ Documento
            <b>${file.name}</b>
            procesado correctamente.
            <br><br>
            Ahora puedes hacer preguntas.
            `;
    }

    catch (error) {

        console.error(error);

        uploadMsg.innerHTML =
            `
            ❌ Error al subir archivo.

            <br><br>

            Posibles causas:
            <br>

            • API caída
            <br>
            • Error CORS
            <br>
            • Archivo demasiado grande
            <br>
            • Backend dormido
            `;
    }

    chatBox.scrollTop =
        chatBox.scrollHeight;
}

// ==========================
// Eventos
// ==========================
sendBtn.onclick = enviar;

// Enter enviar
input.addEventListener(
    'keypress',
    (e) => {

        if (e.key === 'Enter') {
            enviar();
        }
    }
);

// Subir archivo
fileInput.addEventListener(
    'change',
    (e) => {

        const file =
            e.target.files[0];

        if (file) {
            uploadFile(file);
        }

        // Permite volver subir mismo archivo
        fileInput.value = '';
    }
);

// ==========================
// Wake up Render
// ==========================
window.addEventListener(
    'load',
    async () => {

        try {

            await fetch(
                `${API_BASE_URL}/health`
            );

            console.log(
                '✅ API activa'
            );
        }

        catch {

            console.log(
                '⚠️ API dormida o caída'
            );
        }
    }
);
