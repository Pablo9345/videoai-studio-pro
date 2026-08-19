# 🎬 VideoAI Studio Pro

Plataforma de producción de video profesional con inteligencia artificial.
Genera videos listos para YouTube, TikTok e Instagram con guiones inteligentes,
plantillas premium y edición automática.

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Cloud-FF4B4B)
![License](https://img.shields.io/badge/License-MIT-green)

## ✨ Características

### 🎨 12+ Plantillas Profesionales
- **Tecnología**: Modern Tech, Startup Pitch
- **Corporativo**: Corporate Pro, Institucional Classic
- **Marketing**: Ad Impact, E-commerce Showcase
- **Social Media**: Viral TikTok, Instagram Aesthetic
- **Educación**: Tutorial Education
- **Entretenimiento**: Cinematic Vlog, Podcast Pro
- **Minimalista**: Minimal Clean

Cada plantilla incluye:
- Vista previa visual en vivo
- Paleta de colores optimizada
- Tipografía y transiciones
- Configuración avanzada (intro, outro, subtítulos, color grading)

### 🤖 IA Integrada (Groq + Llama 3.1)
- **Guiones completos**: Hook, escenas estructuradas, CTA, narración
- **Metadata social**: Títulos SEO, hashtags, descripciones por plataforma
- **Generador de ideas**: 3-15 ideas virales por nicho
- **Conceptos de miniatura**: Ideas visuales para portadas

### 🎬 Pipeline de Video Profesional
- Detección automática de silencios y cortes de escena
- Efecto Ken Burns en imágenes (zoom suave)
- Transiciones cinematográficas (fade, slide, zoom, wipe)
- **Color grading**: cinemático, cálido, frío, vibrante, neutro
- **Audio ducking**: la música baja automáticamente con la voz
- Subtítulos automáticos con Whisper (estilo personalizable)
- Exportación multi-formato simultánea (YouTube, TikTok, Instagram)

### 💎 Planes y Membresías
- **Starter** (Gratis): 3 videos/mes, 4 plantillas básicas
- **Creator Pro** ($19.99/mes): 50 videos, todas las plantillas, 1080p
- **Business** ($49.99/mes): 200 videos, plantillas personalizadas, 4K, API

## 🚀 Despliegue en Streamlit Cloud

### 1. Sube el repositorio a GitHub
```bash
git init
git add .
git commit -m "VideoAI Studio Pro"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/videoai-studio-pro.git
git push -u origin main
```

### 2. Configura Streamlit Cloud
1. Ve a [share.streamlit.io](https://share.streamlit.io)
2. Conecta tu cuenta de GitHub
3. Selecciona el repositorio `videoai-studio-pro`
4. Archivo principal: `app.py`
5. Streamlit Cloud instalará automáticamente las dependencias desde `requirements.txt`

### 3. Configura las dependencias del sistema
**Importante**: Streamlit Cloud necesita `ffmpeg` y `fontconfig`. Crea un archivo `packages.txt`:

```
ffmpeg
fonts-dejavu
fonts-dejavu-core
fonts-dejavu-extra
```

### 4. Configura la API Key de Groq
- Obtén tu API key gratuita en [console.groq.com](https://console.groq.com)
- Como administrador, accede con la contraseña por defecto: `admin123`
- Ve a "Configuración IA" e ingresa tu API key
- **Cambia la contraseña de admin** por seguridad

Alternativamente, configura la variable de entorno:
```bash
GROQ_API_KEY=tu_api_key_aqui
```

## 🛠 Desarrollo Local

### Requisitos
- Python 3.9+
- FFmpeg instalado en el sistema
- API key de Groq (gratis)

### Instalación
```bash
# Clonar repo
git clone https://github.com/TU_USUARIO/videoai-studio-pro.git
cd videoai-studio-pro

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt

# Instalar FFmpeg (Ubuntu/Debian)
sudo apt-get install ffmpeg

# Ejecutar
streamlit run app.py
```

La aplicación estará disponible en `http://localhost:8501`

## 📁 Estructura del Proyecto

```
videoai-studio-pro/
├── app.py                  # Punto de entrada y routing
├── styles.py              # Sistema de diseño CSS premium
├── database.py            # Capa de datos JSON
├── auth.py                # Autenticación y sesiones
├── groq_ai.py             # Integración IA con Groq
├── video_processor.py     # Pipeline de procesamiento FFmpeg
├── components.py           # Componentes UI reutilizables
├── templates_data.py      # Catálogo de plantillas
├── requirements.txt
├── packages.txt            # Dependencias del sistema (Streamlit Cloud)
├── .streamlit/
│   └── config.toml        # Tema y configuración
├── .gitignore
└── README.md
```

## 🎯 Casos de Uso

### Para Creadores de Contenido
- Genera videos virales para TikTok y Reels
- Optimiza tus publicaciones con metadata generada por IA
- Mantén consistencia visual con plantillas profesionales

### Para Agencias y Freelancers
- Produce videos para múltiples clientes rápidamente
- Mantén un estándar de calidad profesional
- Exporta a múltiples formatos en un solo proceso

### Para Empresas
- Crea contenido institucional con plantillas corporativas
- Genera videos formativos y tutoriales
- Mantén tu brand kit consistente

## 🔐 Seguridad

- Contraseñas hasheadas con SHA-256 + salt
- Backups automáticos de la base de datos
- Verificación de sesión en cada operación
- Tokens limitados por plan para evitar abuso

**Importante**: Cambia la contraseña de admin por defecto (`admin123`) después del primer despliegue.

## 🛣 Roadmap

- [ ] Integración con servicios de almacenamiento (S3, GCS)
- [ ] API REST para integraciones externas
- [ ] Editor visual de plantillas
- [ ] Soporte para más idiomas en subtítulos
- [ ] Integración con plataformas de publicación directa
- [ ] Analytics avanzados de rendimiento

## 📄 Licencia

MIT License - Libre uso comercial y personal.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 💬 Soporte

- 📧 Email: soporte@videoai.studio
- 🐛 Issues: [GitHub Issues](https://github.com/TU_USUARIO/videoai-studio-pro/issues)
- 📖 Docs: [Wiki](https://github.com/TU_USUARIO/videoai-studio-pro/wiki)

---

Hecho con ❤️ usando Streamlit, Groq IA y FFmpeg
