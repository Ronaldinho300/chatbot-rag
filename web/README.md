#🖥️ AsisBot - Interfaz de Usuario (Frontend)
Este repositorio contiene el desarrollo de la interfaz profesional para el proyecto AsisBot, un asistente inteligente para SENATI. El diseño se centra en la usabilidad, la rapidez y una estética moderna.


🎨 Características de la Interfaz
Diseño Responsivo: Optimizado para visualización en computadoras y dispositivos móviles.

Iconografía Moderna: Sustitución de emojis tradicionales por iconos vectoriales de Google Material Symbols para un acabado más técnico.

Gestión de Archivos: Inclusión de un botón de acción rápida (+) para adjuntar documentos .pdf o .txt.

Feedback Visual: Indicador de estado "En línea" y burbujas de chat diferenciadas por colores (Azul para usuario, Gris para el bot).

🛠️ Tecnologías Utilizadas
HTML5: Estructura semántica del chat.

CSS3: Estilos personalizados, incluyendo:

Flexbox para el alineamiento de mensajes.

Efectos de transición (hover) en botones.

Diseño circular para el botón de envío.

JavaScript (Vanilla):

Manipulación del DOM para insertar mensajes en tiempo real.

Uso de la API Fetch para comunicación asíncrona con el backend (Puerto 5000).

Lógica de autoscroll para mantener el mensaje más reciente a la vista.

📂 Estructura de Archivos
Plaintext
web/
├── index.html   # Estructura principal y enlace a librerías de iconos.
├── styles.css   # Definición de colores institucionales y diseño de burbujas.
└── app.js       # Captura de eventos (clics, teclas) y conexión con la API.
🚀 Cómo visualizar la interfaz
Clonar este repositorio o descargar la carpeta web.

Asegurarse de tener conexión a internet (para cargar los iconos de Google).

Abrir el archivo index.html en cualquier navegador moderno (Chrome, Edge, Firefox).

📡 Conexión con el Backend
La interfaz está pre-configurada para conectarse a un servidor local. Para que los mensajes reciban respuesta, el backend debe estar activo en:
http://127.0.0.1:5000/ask

💡 Nota para el Instructor
Esta interfaz ha sido diseñada siguiendo los estándares de calidad de SENATI 2026, priorizando una experiencia de usuario (UX) fluida y profesional.

¿Cómo guardarlo?
Abre tu archivo README.md en VS Code.

Borra todo lo que tenga y pega este texto.

Guarda y sube a GitHub:

Bash
git add README.md
git commit -m "Documentacion técnica de la interfaz completada"
git push origin web-sites