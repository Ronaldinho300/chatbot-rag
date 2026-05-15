# 🖥️ AsisBot - Interfaz de Usuario (Frontend)

Este repositorio contiene el desarrollo de la interfaz profesional para el proyecto **AsisBot**, un asistente inteligente para SENATI. El diseño se centra en la usabilidad, la rapidez y una estética moderna.

## 🎨 Características de la Interfaz

* **Diseño Responsivo:** Optimizado para visualización en computadoras y dispositivos móviles.
* **Iconografía Moderna:** Sustitución de emojis tradicionales por iconos vectoriales de **Google Material Symbols** para un acabado más técnico.
* **Gestión de Archivos:** Inclusión de un botón de acción rápida **(+)** para adjuntar documentos `.pdf` o `.txt`.
* **Feedback Visual:** Indicador de estado "En línea" y burbujas de chat diferenciadas por colores (Azul para usuario, Gris para el bot).

## 🛠️ Tecnologías Utilizadas

* **HTML5:** Estructura semántica del chat.
* **CSS3:** Estilos personalizados, incluyendo:
    * Flexbox para el alineamiento de mensajes.
    * Efectos de transición (*hover*) en botones.
    * Diseño circular para el botón de envío.
* **JavaScript (Vanilla):**
    * Manipulación del DOM para insertar mensajes en tiempo real.
    * Uso de la **API Fetch** para comunicación asíncrona con el backend (Puerto 5000).
    * Lógica de *autoscroll* para mantener el mensaje más reciente a la vista.

## 📂 Estructura de Archivos

```text
web/
├── index.html   # Estructura principal y enlace a librerías de iconos.
├── styles.css   # Definición de colores institucionales y diseño de burbujas.
└── app.js       # Captura de eventos (clics, teclas) y conexión con la API.