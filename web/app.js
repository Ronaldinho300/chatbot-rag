const sendBtn = document.getElementById('send-btn');
const input = document.getElementById('user-input');
const chatBox = document.getElementById('chat-content');

async function enviar() {
    const texto = input.value.trim();
    if (!texto) return;

    // Agregar burbuja del usuario
    chatBox.innerHTML += `<div class="msg user">${texto}</div>`;
    input.value = '';
    chatBox.scrollTop = chatBox.scrollHeight;

    try {
        // Se comunica con el backend de Python (Puerto 5000)
        const res = await fetch('http://127.0.0.1:5000/ask', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ pregunta: texto })
        });
        const data = await res.json();
        
        // Agregar respuesta del Bot
        chatBox.innerHTML += `<div class="msg bot">${data.respuesta}</div>`;
    } catch (e) {
        chatBox.innerHTML += `<div class="msg bot">⚠️ Error: Inicia el servidor de Python primero.</div>`;
    }
    chatBox.scrollTop = chatBox.scrollHeight;
}

sendBtn.onclick = enviar;
input.onkeypress = (e) => { if(e.key === 'Enter') enviar(); };
// Lógica para el selector de archivos
document.getElementById('file-upload').addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        const chatContent = document.getElementById('chat-content');
        
        // Crear una burbuja de mensaje indicando que se subió un archivo
        const fileMsg = document.createElement('div');
        fileMsg.className = 'msg user';
        fileMsg.innerHTML = `📄 <b>Archivo seleccionado:</b> ${file.name}`;
        
        chatContent.appendChild(fileMsg);
        
        // Auto-scroll hacia abajo
        chatContent.scrollTop = chatContent.scrollHeight;
        
        console.log("Archivo listo para procesar:", file.name);
    }
});