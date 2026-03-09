# WhatsApp NG

Complemento para NVDA que proporciona mejoras de accesibilidad para la versión de escritorio de WhatsApp basada en web.

## Características

- **Alt+1**: Ir a la lista de conversaciones de WhatsApp
- **Alt+2**: Ir a la lista de mensajes de WhatsApp
- **Alt+D**: Enfocar el campo de edición de mensajes
- **Enter**: Reproducir mensaje de voz (funciona en chats individuales y grupos)
- **Shift+Enter**: Abrir el menú contextual del mensaje
- **Control+C**: Copiar el mensaje actual al portapapeles
- **Control+R**: Leer el mensaje completo (hace clic en el botón "leer más" si es necesario)
- **Control+Shift+Enter**: Reaccionar al mensaje

### Scripts conmutables (sin atajo predeterminado - configurar en Gestos de entrada)

- Alternar el filtrado de números de teléfono en la lista de conversaciones
- Alternar el filtrado de números de teléfono en la lista de mensajes
- Alternar el modo foco automático (permite el modo exploración cuando sea necesario)

## Atajos de teclado nativos de WhatsApp Desktop

- Marcar como no leído: Ctrl+Shift+U
- Silenciar notificaciones: Ctrl+Shift+M
- Archivar conversación: Ctrl+Shift+A
- Fijar conversación: Ctrl+Alt+Shift+P
- Buscar: Ctrl+Alt+/
- Buscar en la conversación: Ctrl+Shift+F
- Nueva conversación: Ctrl+Alt+N
- Conversación siguiente: Ctrl+]
- Conversación anterior: Ctrl+[
- Añadir etiqueta a la conversación: Ctrl+Cmd+Shift+L
- Cerrar conversación: Escape
- Nuevo grupo: Ctrl+Shift+N
- Perfil e información: Ctrl+Alt+P
- Aumentar velocidad del mensaje de voz: Shift+.
- Disminuir velocidad del mensaje de voz: Shift+,
- Configuración: Alt+S
- Panel de emojis: Ctrl+Alt+E
- Panel de GIF: Ctrl+Alt+G
- Panel de stickers: Ctrl+Alt+S
- Búsqueda ampliada: Alt+K
- Bloquear aplicación: Alt+L
- Abrir detalles de la conversación: Alt+I
- Bloquear conversación: Ctrl+Shift+B
- Responder: Alt+R
- Responder en privado: Ctrl+Alt+R
- Reenviar: Ctrl+Alt+D
- Marcar mensaje con estrella: Alt+8
- Abrir menú desplegable de adjuntos: Alt+A
- Iniciar grabación PTT: Ctrl+Alt+Shift+R
- Pausar grabación PTT: Alt+P
- Enviar PTT: Ctrl+Enter
- Editar último mensaje: Ctrl+Flecha Arriba
- Activar/Desactivar cámara: Ctrl+Alt+V
- Silenciar/Reactivar: Ctrl+Alt+M
- Reacciones: Ctrl+Alt+R
- Levantar la mano: Ctrl+Alt+H
- Compartir pantalla: Ctrl+Alt+S
- Terminar llamada: Ctrl+Alt+W
- Ampliar: Ctrl++
- Reducir: Ctrl+-
- Restablecer zoom: Ctrl+0
- Abrir conversación: Ctrl+1..9

## Requisitos

- NVDA 2021.1 o posterior
- WhatsApp Desktop (versión basada en web)

## Instalación

1. Descarga el archivo `whatsAppNG.nvda-addon`
2. En NVDA, ve a **Herramientas → Administrador de complementos**
3. Haz clic en **Instalar** y selecciona el archivo
4. Reinicia NVDA

## Configuración

Los filtros de números de teléfono se pueden activar o desactivar:
- En la lista de conversaciones: Configura un atajo en Gestos de entrada
- En la lista de mensajes: Configura un atajo en Gestos de entrada

Configura los atajos en:
**Menú NVDA → Preferencias → Gestos de entrada → WhatsApp NG**

## Historial de cambios

### Versión 1.5.0 (2026-03-05)

**Añadido:**
- Control+Shift+Enter: Reaccionar a mensajes (abre menú de reacciones)
- Alt+Enter: Leer mensaje completo en modo exploración
- Atajos de teclado nativos de WhatsApp Desktop añadidos a la documentación

**Cambiado:**
- Rendimiento significativamente optimizado: La navegación ahora es más fluida y responsiva
- Alt+2 más confiable y preciso en navegación
- Control+C ahora solo funciona en la lista de mensajes

**Corregido:**
- Control+R ahora lee el texto completo correctamente al expandir mensajes largos

### Versión 1.4.0 (2026-02-23)

**Añadido:**
- Soporte completo de idiomas: Árabe, Alemán, Español, Italiano y Ruso
- Traducción ucraniana actualizada con las cadenas más recientes

**Corregido:**
- Error "Texto no encontrado" en Control+R después de hacer clic en el botón "leer más"
- Control+R ahora funciona solo en mensajes de texto (muestra "No es un mensaje de texto" para voz/imágenes)

**Cambiado:**
- Enlaces del repositorio actualizados al nuevo repositorio (nunotfc/WhatsAppNG)
- Documentación: Todos los README localizados ahora incluyen el historial completo hasta la versión 1.3.0

### Versión 1.3.0 (2026-02-07)

**Añadido:**
- Soporte para traducción al turco
- Opción para alternar el Modo Foco automático (configurar gesto en Gestos de entrada)

**Cambiado:**
- Rendimiento mejorado: Los comandos de navegación son ahora más rápidos en usos repetidos
- La tecla Escape ahora se envía correctamente a WhatsApp

**Corregido:**
- Enter ahora reproduce mensajes de vídeo (antes solo funcionaba para audio)

### Versión 1.1.1 (2025-01-31)

**Añadido:**
- Control+R: Leer mensaje completo (hace clic en "leer más" automáticamente)
- Control+C: Copiar el mensaje actual al portapapeles
- Desactivación automática del modo exploración (mantiene el modo foco activo para una mejor experiencia en WhatsApp)

**Cambiado:**
- Mensajes de error mejorados: Todos los scripts proporcionan ahora una respuesta clara en caso de fallo
- Los comandos de navegación (Alt+1, Alt+2, Alt+D) ahora son silenciosos cuando se ejecutan con éxito
- Enter: Detección basada en deslizadores en lugar de conteo de botones (más fiable)

**Corregido:**
- Alt+1 y Alt+2 informan correctamente de errores cuando fallan todas las rutas
- Filtrado de objetos optimizado para reducir el retardo de entrada

### Versión 1.1.0 (2025-01-30)

**Añadido:**
- Control+R: Leer mensaje completo
- Reproducción inteligente de mensajes de voz mediante detección de deslizadores

**Cambiado:**
- Enter: Lógica mejorada usando detección de deslizadores en lugar de contar botones

**Corregido:**
- Alt+2 ahora intenta correctamente todas las rutas de navegación si el primer intento falla

### Versión 1.0.0 (2025-01-29)

**Lanzamiento inicial:**
- Atajos de navegación para lista de conversaciones, lista de mensajes y redactor de mensajes
- Reproducción de mensajes de voz con soporte para chats individuales y grupos
- Acceso al menú contextual para acciones de mensaje
- Alternancia de filtrado de números de teléfono para conversaciones y mensajes
- Activación automática del modo foco en WhatsApp Desktop

## Créditos

Desarrollado por Nuno Costa para proporcionar mejoras de accesibilidad en la experiencia moderna de WhatsApp Desktop.

## Soporte

Para problemas o sugerencias, por favor visita:
https://github.com/nunotfc/whatsAppNG/issues

## Compilación de traducciones

Para actualizar o compilar traducciones:
```bash
scons pot
```

Esto requiere tener instaladas las herramientas GNU Gettext.
