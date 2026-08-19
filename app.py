"""
VideoAI Studio Pro - Aplicación principal
Plataforma de producción de video profesional con IA.
Diseñada para Streamlit Cloud + GitHub.
"""

import streamlit as st
import os
import json
from datetime import datetime
from pathlib import Path

# Configuración de página (debe ser lo primero)
st.set_page_config(
    page_title="VideoAI Studio Pro - Producción de Video con IA",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/tu-usuario/videoai-studio-pro',
        'Report a bug': 'https://github.com/tu-usuario/videoai-studio-pro/issues',
        'About': "VideoAI Studio Pro - Plataforma de producción de video profesional con IA"
    }
)

# Imports del proyecto
from styles import PREMIUM_CSS, html_safe
from database import (
    cargar_db, guardar_db, get_config, update_config,
    obtener_usuario, usar_token, verificar_tokens, agregar_proyecto,
    cambiar_plan, get_dashboard_data, get_stats, verify_admin_password,
    set_admin_password, listar_usuarios
)
from auth import (
    init_session_state, is_logged_in, is_admin, logout,
    render_login_form, render_user_sidebar
)
from groq_ai import GroqAI, MODELOS_RECOMENDADOS
from video_processor import procesar_video_completo
from components import (
    render_template_gallery, render_processing_animation,
    render_stat_grid, render_guion_visualization,
    render_pricing_section, render_wizard_nav,
    render_format_selector, render_upload_zone,
    render_project_card,
    render_transiciones_selector, render_efectos_selector,
    render_preview_modal
)
from templates_data import (
    PLANTILLAS_PROFESIONALES, get_plantilla_by_id, get_plantilla_default,
    MEMBRESIAS
)
from database import UPLOADS, OUTPUTS, TEMP_DIR

# ============ ESTILOS GLOBALES ============
st.markdown(PREMIUM_CSS, unsafe_allow_html=True)

# ============ INICIALIZACIÓN ============
init_session_state()


def render_home_page():
    """Página de inicio moderna y atractiva."""
    # Hero section moderna con gradientes animados
    st.markdown("""
    <style>
    .hero-modern {
        position: relative;
        padding: 3rem 2rem;
        margin-bottom: 2rem;
        border-radius: 24px;
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
        overflow: hidden;
        border: 1px solid rgba(99, 102, 241, 0.2);
        text-align: center;
    }
    .hero-modern::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, #6366f1, #8b5cf6, #ec4899, #6366f1);
        background-size: 200% 100%;
        animation: shimmer 4s linear infinite;
    }
    @keyframes shimmer {
        0% { background-position: 0% 0%; }
        100% { background-position: 200% 0%; }
    }
    .hero-modern::after {
        content: '';
        position: absolute;
        top: -50%; right: -10%;
        width: 400px; height: 400px;
        background: radial-gradient(circle, rgba(139, 92, 246, 0.15) 0%, transparent 70%);
        border-radius: 50%;
        pointer-events: none;
    }
    .hero-tagline {
        display: inline-block;
        padding: 0.4rem 1.2rem;
        background: rgba(99, 102, 241, 0.15);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 100px;
        color: #a5b4fc !important;
        font-size: 0.85rem;
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 1.5rem;
    }
    .hero-title-main {
        font-size: 3.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #f8fafc 0%, #c7d2fe 50%, #f9a8d4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
        letter-spacing: -0.03em;
        line-height: 1.1;
    }
    .hero-subtitle-main {
        font-size: 1.2rem;
        color: #cbd5e1 !important;
        max-width: 700px;
        margin: 0 auto 1.5rem;
        line-height: 1.6;
    }
    .hero-premise {
        font-style: italic;
        color: #f9a8d4 !important;
        font-size: 1rem;
        margin-bottom: 2rem;
        opacity: 0.9;
    }
    .hero-cta-row {
        display: flex;
        gap: 1rem;
        justify-content: center;
        flex-wrap: wrap;
    }
    .brand-footer {
        text-align: center;
        margin-top: 1rem;
        color: #64748b !important;
        font-size: 0.85rem;
        letter-spacing: 0.05em;
    }
    .brand-footer strong {
        color: #a5b4fc !important;
        font-weight: 700;
    }
    </style>
    <div class="hero-modern">
        <div class="hero-tagline">🎬 Plataforma de Producción Audiovisual</div>
        <div class="hero-title-main">VideoAI Studio Pro</div>
        <div class="hero-subtitle-main">
            Tu estudio creativo impulsado por inteligencia artificial.
            Crea videos profesionales, optimiza tu contenido para redes sociales
            y construye tu narrativa de marca con herramientas profesionales.
        </div>
        <div class="hero-premise">
            "La creación de videos profesionales nunca fue tan fácil y entretenida"
        </div>
        <div class="hero-cta-row">
            <span style="display: inline-block; padding: 0.5rem 1rem; background: rgba(99, 102, 241, 0.2); border-radius: 8px; color: #c7d2fe !important; font-size: 0.9rem; font-weight: 600;">✨ 20 Plantillas Pro</span>
            <span style="display: inline-block; padding: 0.5rem 1rem; background: rgba(236, 72, 153, 0.2); border-radius: 8px; color: #f9a8d4 !important; font-size: 0.9rem; font-weight: 600;">🎨 Editor Visual</span>
            <span style="display: inline-block; padding: 0.5rem 1rem; background: rgba(16, 185, 129, 0.2); border-radius: 8px; color: #6ee7b7 !important; font-size: 0.9rem; font-weight: 600;">📈 Análisis IA</span>
        </div>
        <div class="brand-footer">
            Desarrollado por <strong>Comunicaciones Integrales</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ============ FUNCIONALIDADES PROFESIONALES (con desplegables) ============
    st.markdown("""
    <style>
    .features-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin: 1.5rem 0;
    }
    .feature-card-modern {
        background: rgba(26, 34, 56, 0.6);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 16px;
        padding: 1.2rem;
        backdrop-filter: blur(20px);
        transition: all 0.3s ease;
        text-align: center;
        min-height: 140px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .feature-card-modern:hover {
        border-color: rgba(99, 102, 241, 0.6);
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(99, 102, 241, 0.15);
    }
    .feature-icon-modern {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    .feature-title-modern {
        font-size: 1rem;
        font-weight: 700;
        color: #f8fafc !important;
        margin-bottom: 0.3rem;
    }
    .feature-short {
        font-size: 0.8rem;
        color: #94a3b8 !important;
        margin-bottom: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("### 🚀 Funcionalidades profesionales")
    st.markdown("Haz clic en cada funcionalidad para conocer más detalles.")

    features = [
        {
            "icon": "🧠",
            "title": "Guion Inteligente",
            "short": "Guiones con hook, escenas y CTA",
            "detalle": ("**¿Qué hace?** Genera guiones técnicos completos con IA, incluyendo hook para los primeros 3 segundos, "
                       "escenas estructuradas con B-roll sugerido, narración, texto en pantalla y CTA final.\n\n"
                       "**Importancia:** Un guion bien estructurado aumenta la retención de audiencia hasta un 80% y multiplica las vistas orgánicas.\n\n"
                       "**Capacidades:**\n"
                       "- Análisis del objetivo del video\n"
                       "- Sugerencia de música y ambiente sonoro\n"
                       "- Hashtags optimizados para cada plataforma\n"
                       "- Descripción lista para publicar")
        },
        {
            "icon": "🎨",
            "title": "20 Plantillas Pro",
            "short": "Diseños profesionales categorizados",
            "detalle": ("**¿Qué hace?** Ofrece 20 plantillas profesionales organizadas por categoría: Gaming, Belleza, Gastronomía, "
                       "Viajes, Fitness, Música, Noticias, Premium, Corporativo, Marketing, Educación y más.\n\n"
                       "**Importancia:** Mantén consistencia visual en tu marca y ahorra horas de diseño.\n\n"
                       "**Capacidades:**\n"
                       "- Vista previa animada en vivo\n"
                       "- Personalización de colores y tipografía\n"
                       "- Guardar plantillas personalizadas\n"
                       "- Reutilizar como imagen corporativa\n"
                       "- Logo personalizado en posición configurable")
        },
        {
            "icon": "🎬",
            "title": "Edición Pro",
            "short": "Transiciones y efectos cinematográficos",
            "detalle": ("**¿Qué hace?** Aplica transiciones profesionales (47 disponibles: fade, slide, zoom, circle, etc.) "
                       "y efectos visuales (16 efectos: vintage, glitch, film grain, noir, etc.).\n\n"
                       "**Importancia:** La calidad de edición diferencia el contenido amateur del profesional.\n\n"
                       "**Capacidades:**\n"
                       "- 47 transiciones XFade de FFmpeg\n"
                       "- 16 efectos visuales con intensidad ajustable\n"
                       "- Color grading cinematográfico\n"
                       "- Efecto Ken Burns en imágenes\n"
                       "- Audio ducking automático")
        },
        {
            "icon": "📝",
            "title": "Subtítulos Auto",
            "short": "Transcripción con Whisper",
            "detalle": ("**¿Qué hace?** Transcribe automáticamente el audio del video usando Whisper de OpenAI, "
                       "y quema subtítulos con estilo personalizable según la plantilla.\n\n"
                       "**Importancia:** El 85% de los videos en redes sociales se ven sin sonido.\n\n"
                       "**Capacidades:**\n"
                       "- Detección automática de idioma\n"
                       "- Estilo de subtítulos adaptado a plantilla\n"
                       "- Posición configurable\n"
                       "- Exportación a SRT para edición externa")
        },
        {
            "icon": "📱",
            "title": "Multi-Formato",
            "short": "YouTube, TikTok, Instagram simultáneo",
            "detalle": ("**¿Qué hace?** Exporta tu video en 3 formatos simultáneos: YouTube (1920×1080), "
                       "TikTok/Reels (1080×1920) e Instagram Feed (1080×1080).\n\n"
                       "**Importancia:** Maximiza el alcance publicando en todas las plataformas con un solo procesamiento.\n\n"
                       "**Capacidades:**\n"
                       "- 3 formatos con un solo clic\n"
                       "- Calidad 1080p Full HD\n"
                       "- Descargas independientes\n"
                       "- Presets optimizados por plataforma")
        },
        {
            "icon": "🤖",
            "title": "Metadata IA",
            "short": "Títulos SEO, hashtags, descripciones",
            "detalle": ("**¿Qué hace?** Genera metadata optimizada por SEO: títulos, descripciones, hashtags y tags "
                       "personalizados para cada plataforma social.\n\n"
                       "**Importancia:** El SEO en redes sociales aumenta el descubrimiento orgánico hasta 5x.\n\n"
                       "**Capacidades:**\n"
                       "- Títulos SEO por plataforma\n"
                       "- Hashtags optimizados\n"
                       "- Descripción con keywords\n"
                       "- Mejor horario de publicación\n"
                       "- Concepto de miniatura")
        },
        {
            "icon": "📅",
            "title": "Agenda de Publicaciones",
            "short": "Programa tus posts",
            "detalle": ("**¿Qué hace?** Agenda y programa tus publicaciones en redes sociales desde un calendario centralizado.\n\n"
                       "**Importancia:** La consistencia en la publicación es clave para el crecimiento.\n\n"
                       "**Capacidades:**\n"
                       "- Calendario visual\n"
                       "- Programación por plataforma\n"
                       "- Recordatorios\n"
                       "- Mejor horario sugerido por IA")
        },
        {
            "icon": "📊",
            "title": "Análisis y Estrategia",
            "short": "Mide, analiza y mejora",
            "detalle": ("**¿Qué hace?** Analiza la efectividad de tus posteos, lee comentarios para extraer ideas, "
                       "detecta críticas reales y propone nuevas piezas que contribuyan a tu relato.\n\n"
                       "**Importancia:** Lo que no se mide, no se mejora.\n\n"
                       "**Capacidades:**\n"
                       "- Análisis de efectividad de posteos\n"
                       "- Lectura inteligente de comentarios\n"
                       "- Detección de patrones exitosos\n"
                       "- Propuestas de contenido basadas en tu narrativa\n"
                       "- Recomendación de estrategia")
        },
    ]

    # Grid de funcionalidades (4 columnas)
    for i in range(0, len(features), 4):
        batch = features[i:i+4]
        cols = st.columns(4)
        for j, feature in enumerate(batch):
            with cols[j]:
                st.markdown(f"""
                <div class="feature-card-modern">
                    <div class="feature-icon-modern">{feature['icon']}</div>
                    <div class="feature-title-modern">{feature['title']}</div>
                    <div class="feature-short">{feature['short']}</div>
                </div>
                """, unsafe_allow_html=True)
                # Botón con desplegable
                with st.expander(f"ℹ️ Detalles", expanded=False):
                    st.markdown(feature['detalle'])

    # CTA principal - lleva directamente a producción
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Empezar a crear ahora", type="primary", use_container_width=True,
                     help="Comienza tu primer video profesional en menos de 5 minutos"):
            if st.session_state.get('usuario'):
                # Si ya está logueado, ir directo a producción
                st.session_state.vista = "process"
                st.session_state.wizard_step = 1
                st.rerun()
            else:
                # Si no está logueado, ir a auth
                st.session_state.vista = "auth"
                st.rerun()

    # ============ POTENCIA DE LA PLATAFORMA (al final, horizontal) ============
    st.markdown("""
    <style>
    .stats-horizontal {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 0.8rem;
        margin: 1.5rem 0;
    }
    .stat-card-mini {
        background: rgba(26, 34, 56, 0.6);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 12px;
        padding: 1rem 0.5rem;
        backdrop-filter: blur(20px);
        text-align: center;
        transition: all 0.3s ease;
    }
    .stat-card-mini:hover {
        border-color: rgba(99, 102, 241, 0.6);
        transform: translateY(-2px);
    }
    .stat-icon-mini {
        font-size: 1.5rem;
        margin-bottom: 0.3rem;
    }
    .stat-value-mini {
        font-size: 1.4rem;
        font-weight: 800;
        color: #f8fafc !important;
        line-height: 1;
        font-family: 'Montserrat', sans-serif;
    }
    .stat-label-mini {
        font-size: 0.75rem;
        color: #64748b !important;
        margin-top: 0.3rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="stats-horizontal">
        <div class="stat-card-mini">
            <div class="stat-icon-mini">🎬</div>
            <div class="stat-value-mini">20</div>
            <div class="stat-label-mini">Plantillas Pro</div>
        </div>
        <div class="stat-card-mini">
            <div class="stat-icon-mini">⚡</div>
            <div class="stat-value-mini">&lt;5min</div>
            <div class="stat-label-mini">Tiempo promedio</div>
        </div>
        <div class="stat-card-mini">
            <div class="stat-icon-mini">📱</div>
            <div class="stat-value-mini">3</div>
            <div class="stat-label-mini">Formatos simultáneos</div>
        </div>
        <div class="stat-card-mini">
            <div class="stat-icon-mini">🤖</div>
            <div class="stat-value-mini">100%</div>
            <div class="stat-label-mini">Automatizado por IA</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Branding final
    st.markdown("""
    <div style="text-align: center; margin-top: 2rem; padding-top: 1.5rem; border-top: 1px solid rgba(99, 102, 241, 0.2);">
        <p style="color: #64748b !important; font-size: 0.85rem; margin: 0;">
            © 2025 VideoAI Studio Pro · Desarrollado por
            <strong style="color: #a5b4fc !important;">Comunicaciones Integrales</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_process_page():
    """Página principal de producción de video con wizard."""
    usuario = st.session_state.usuario

    # Hero compacto
    st.markdown("""
    <div class="glass-card" style="border-left: 4px solid var(--accent-primary); margin-bottom: 1.5rem;">
        <h2 style="color: var(--text-primary) !important; margin: 0;">
            📤 Producción de Video Profesional
        </h2>
        <p style="color: var(--text-secondary) !important; margin: 0.5rem 0 0 0;">
            Sigue los pasos para crear tu video profesional con IA
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Verificar tokens
    if usuario['tokens'] <= 0:
        st.markdown("""
        <div class="custom-alert custom-alert-warning">
            <strong>⚠ Sin tokens disponibles</strong>
            <div style="margin-top: 0.3rem;">
                Has agotado tus tokens. Actualiza tu plan para continuar creando videos.
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("💎 Ver planes", type="primary"):
            st.session_state.vista = "plans"
            st.rerun()
        return

    # Wizard
    render_wizard_nav(st.session_state.wizard_step)

    # ============ PASO 1: SUBIR MATERIAL ============
    if st.session_state.wizard_step == 1:
        st.markdown("### 📁 Paso 1: Sube tu material")
        video_principal, videos_extra, imagenes, audio_musica = render_upload_zone()

        # Guardar archivos inmediatamente en disco cuando se suben
        # Esto evita que se pierdan al navegar entre pasos del wizard
        timestamp_preview = datetime.now().strftime("%Y%m%d_%H%M%S")
        archivos_guardados = {"videos": [], "imagenes": [], "audio": None, "principal": None}

        if video_principal is not None:
            ruta_v = UPLOADS / f"{timestamp_preview}_main_{video_principal.name}"
            with open(ruta_v, 'wb') as f:
                f.write(video_principal.getbuffer())
            archivos_guardados["principal"] = str(ruta_v)
            archivos_guardados["principal_name"] = video_principal.name

        if videos_extra:
            for v in videos_extra:
                ruta_v = UPLOADS / f"{timestamp_preview}_extra_{v.name}"
                with open(ruta_v, 'wb') as f:
                    f.write(v.getbuffer())
                archivos_guardados["videos"].append(str(ruta_v))

        if imagenes:
            for img in imagenes:
                ruta_img = UPLOADS / f"{timestamp_preview}_img_{img.name}"
                with open(ruta_img, 'wb') as f:
                    f.write(img.getbuffer())
                archivos_guardados["imagenes"].append(str(ruta_img))

        if audio_musica:
            ruta_audio = UPLOADS / f"{timestamp_preview}_audio_{audio_musica.name}"
            with open(ruta_audio, 'wb') as f:
                f.write(audio_musica.getbuffer())
            archivos_guardados["audio"] = str(ruta_audio)

        # Guardar en session state
        st.session_state.archivos_guardados = archivos_guardados

        # Mostrar resumen de archivos cargados
        if archivos_guardados["principal"] or archivos_guardados["videos"] or archivos_guardados["imagenes"] or archivos_guardados["audio"]:
            st.markdown("""
            <div class="glass-card" style="border-left: 4px solid var(--accent-success);">
                <strong style="color: var(--accent-success) !important;">✅ Archivos cargados:</strong>
            """, unsafe_allow_html=True)
            if archivos_guardados["principal"]:
                st.write(f"🎬 Video principal: **{archivos_guardados['principal_name']}**")
            if archivos_guardados["videos"]:
                st.write(f"🎥 Videos extra: **{len(archivos_guardados['videos'])}** archivos")
            if archivos_guardados["imagenes"]:
                st.write(f"🖼 Imágenes: **{len(archivos_guardados['imagenes'])}** archivos")
            if archivos_guardados["audio"]:
                st.write(f"🎵 Audio: **cargado**")
            st.markdown("</div>", unsafe_allow_html=True)

        col1, col2 = st.columns([1, 2])
        with col1:
            if st.button("⏭ Siguiente", type="primary", use_container_width=True):
                if not archivos_guardados["principal"]:
                    st.warning("Debes subir al menos un video principal")
                else:
                    st.session_state.wizard_step = 2
                    st.rerun()
        with col2:
            if st.button("🔄 Limpiar", use_container_width=True):
                st.session_state.archivos_guardados = None
                st.rerun()

    # ============ PASO 2: DESCRIBIR PROYECTO ============
    elif st.session_state.wizard_step == 2:
        st.markdown("### 📝 Paso 2: Describe tu proyecto")

        with st.container():
            texto_objetivo = st.text_area(
                "🎯 ¿Qué mensaje quieres transmitir?",
                height=120,
                placeholder="Ej: Quiero promocionar mi curso online de marketing digital. Mi público objetivo son emprendedores de 25-40 años interesados en aumentar sus ventas online. El tono debe ser motivador y profesional...",
                key="texto_objetivo_input"
            )

            col1, col2 = st.columns(2)
            with col1:
                tipo_contenido = st.selectbox(
                    "📂 Tipo de contenido",
                    ["Publicitario", "Institucional", "Educativo", "Entretenimiento",
                     "Tutorial", "Vlog", "Review de producto", "Storytelling"],
                    key="tipo_contenido_sel"
                )
            with col2:
                duracion_objetivo = st.slider(
                    "⏱ Duración aproximada (minutos)",
                    min_value=1, max_value=15, value=3, step=1,
                    key="duracion_slider"
                )

            publico_objetivo = st.text_input(
                "👥 Público objetivo (opcional)",
                placeholder="Ej: Emprendedores, estudiantes, profesionales tech...",
                key="publico_input"
            )

        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅ Anterior", use_container_width=True):
                st.session_state.wizard_step = 1
                st.rerun()
        with col2:
            if st.button("⏭ Siguiente", type="primary", use_container_width=True):
                if not texto_objetivo:
                    st.warning("Escribe una descripción del proyecto")
                else:
                    st.session_state.wizard_step = 3
                    st.rerun()

    # ============ PASO 3: ELEGIR PLANTILLA ============
    elif st.session_state.wizard_step == 3:
        st.markdown("### 🎨 Paso 3: Elige una plantilla profesional")

        selected_id = None
        if st.session_state.plantilla_elegida:
            selected_id = st.session_state.plantilla_elegida.get("id")

        render_template_gallery(selected_id=selected_id)

        if st.session_state.plantilla_elegida:
            st.success(f"✅ Plantilla seleccionada: **{st.session_state.plantilla_elegida['nombre']}**")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅ Anterior", use_container_width=True):
                st.session_state.wizard_step = 2
                st.rerun()
        with col2:
            if not st.session_state.plantilla_elegida:
                st.info("👆 Selecciona una plantilla para continuar")
            elif st.button("⏭ Siguiente", type="primary", use_container_width=True):
                st.session_state.wizard_step = 4
                st.rerun()

    # ============ PASO 4: FORMATOS ============
    elif st.session_state.wizard_step == 4:
        st.markdown("### 📱 Paso 4: Formatos y personalización")
        st.markdown("Selecciona para qué plataformas exportar y personaliza el estilo del video.")

        # Sub-pestañas: Formatos / Transiciones / Efectos
        tab_fmt, tab_trans, tab_efc = st.tabs(["📱 Formatos", "🎞 Transiciones", "✨ Efectos"])

        with tab_fmt:
            formatos_seleccionados = render_format_selector()

        with tab_trans:
            st.markdown("Personaliza las transiciones entre clips (opcional).")
            usar_transicion_personalizada = st.checkbox(
                "Usar transición personalizada (en lugar de la de la plantilla)",
                value=False,
                key="usar_trans_custom"
            )
            if usar_transicion_personalizada:
                transicion_sel = render_transiciones_selector(
                    st.session_state.plantilla_elegida.get("transicion", "fade")
                    if st.session_state.plantilla_elegida else "fade"
                )
                st.session_state.transicion_personalizada = transicion_sel["id"]
                st.session_state.duracion_transicion_personalizada = transicion_sel["duracion"]
            else:
                st.session_state.transicion_personalizada = None
                st.session_state.duracion_transicion_personalizada = None
                plantilla_trans = st.session_state.plantilla_elegida.get("transicion", "fade") if st.session_state.plantilla_elegida else "fade"
                st.info(f"Se usará la transición de la plantilla: **{plantilla_trans}**")

        with tab_efc:
            st.markdown("Aplica efectos visuales adicionales a tu video (opcional).")
            usar_efectos = st.checkbox(
                "Aplicar efectos visuales adicionales",
                value=False,
                key="usar_efectos_visuales"
            )
            if usar_efectos:
                efectos_sel = render_efectos_selector()
                st.session_state.efectos_seleccionados = efectos_sel
                if efectos_sel:
                    st.success(f"✅ {len(efectos_sel)} efectos seleccionados")
                else:
                    st.warning("No has seleccionado ningún efecto")
            else:
                st.session_state.efectos_seleccionados = []

        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅ Anterior", use_container_width=True):
                st.session_state.wizard_step = 3
                st.rerun()
        with col2:
            if not formatos_seleccionados:
                st.warning("Selecciona al menos un formato en la pestaña 'Formatos'")
            elif st.button("⏭ Siguiente", type="primary", use_container_width=True):
                st.session_state.formatos_seleccionados = formatos_seleccionados
                st.session_state.wizard_step = 5
                st.rerun()

    # ============ PASO 5: GENERAR GUION ============
    elif st.session_state.wizard_step == 5:
        st.markdown("### 🧠 Paso 5: Generar guion con IA")

        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("⬅ Anterior", use_container_width=True):
                st.session_state.wizard_step = 4
                st.rerun()

        config = get_config()
        groq = GroqAI(config.get("groq_api_key", ""),
                      model=config.get("groq_model", "llama-3.1-70b-versatile"))

        if not groq.esta_configurado():
                        st.markdown("""
            <div class="custom-alert custom-alert-warning">
                <strong>⚠ API Key de Groq no configurada</strong>
                <div style="margin-top: 0.3rem;">
                    Un administrador debe configurar la API key de Groq.
                    Puedes obtenerla gratis en <a href="https://console.groq.com" target="_blank">console.groq.com</a>
                </div>
            </div>
            """, unsafe_allow_html=True)

        if st.button("🧠 Generar Guion Profesional", type="primary",
                     use_container_width=True, disabled=not groq.esta_configurado()):
            with st.spinner("🎬 Generando guion profesional con IA..."):
                texto_objetivo = st.session_state.get("texto_objetivo_input", "")
                tipo = st.session_state.get("tipo_contenido_sel", "Publicitario")
                duracion = st.session_state.get("duracion_slider", 3)
                plantilla_nombre = st.session_state.plantilla_elegida.get("nombre", "")

                material_desc = "Material multimedia disponible"

                guion = groq.generar_guion_completo(
                    texto_objetivo, tipo, duracion, material_desc, plantilla_nombre
                )

                if "error" in guion:
                    st.error(f"Error al generar guion: {guion.get('error', 'desconocido')}")
                    if "raw" in guion:
                        with st.expander("🔍 Respuesta recibida"):
                            st.code(guion["raw"])
                else:
                    st.session_state.guion = guion
                    st.success("✅ Guion generado exitosamente")
                    st.rerun()

        # Mostrar guion generado
        if st.session_state.guion:
            st.markdown("---")
            st.markdown("### 📜 Guion generado")
            render_guion_visualization(st.session_state.guion)

            # Editor avanzado
            with st.expander("✏ Editar guion (avanzado)"):
                guion_json = st.text_area(
                    "Edita el JSON del guion",
                    value=json.dumps(st.session_state.guion, indent=2, ensure_ascii=False),
                    height=300,
                    key="guion_editor"
                )
                if st.button("💾 Guardar cambios del guion"):
                    try:
                        st.session_state.guion = json.loads(guion_json)
                        st.success("Guion actualizado")
                        st.rerun()
                    except json.JSONDecodeError as e:
                        st.error(f"JSON inválido: {e}")

            # Botón siguiente
            if st.button("⏭ Continuar a producción", type="primary",
                         use_container_width=True):
                st.session_state.wizard_step = 6
                st.rerun()

    # ============ PASO 6: PRODUCIR VIDEO ============
    elif st.session_state.wizard_step == 6:
        st.markdown("### 🚀 Paso 6: Producir video")

        # Validar que existan los datos requeridos
        if not st.session_state.get('plantilla_elegida'):
            st.error("❌ No se ha seleccionado una plantilla. Vuelve al paso 3.")
            if st.button("⬅ Volver al paso 3"):
                st.session_state.wizard_step = 3
                st.rerun()
            return

        if not st.session_state.get('guion'):
            st.error("❌ No se ha generado el guion. Vuelve al paso 5.")
            if st.button("⬅ Volver al paso 5"):
                st.session_state.wizard_step = 5
                st.rerun()
            return

        if not st.session_state.get('formatos_seleccionados'):
            st.warning("⚠ No se seleccionaron formatos. Usando YouTube por defecto.")
            st.session_state.formatos_seleccionados = ['youtube']

        if not st.session_state.get('archivos_guardados'):
            st.error("❌ No se encontraron archivos. Vuelve al paso 1.")
            if st.button("⬅ Volver al paso 1"):
                st.session_state.wizard_step = 1
                st.rerun()
            return

        # Resumen
        plantilla_nombre = st.session_state.plantilla_elegida.get('nombre', 'N/A')
        tipo_cont = st.session_state.get('tipo_contenido_sel', 'N/A')
        duracion = st.session_state.get('duracion_slider', 3)
        formatos_str = ', '.join(st.session_state.formatos_seleccionados).upper()

        # Personalizaciones avanzadas
        transicion_personalizada = st.session_state.get('transicion_personalizada')
        duracion_trans = st.session_state.get('duracion_transicion_personalizada')
        efectos_seleccionados = st.session_state.get('efectos_seleccionados', [])

        # Construir string de transición para el resumen
        if transicion_personalizada:
            trans_str = f"{transicion_personalizada} ({duracion_trans:.1f}s) — Personalizada"
        else:
            plantilla_trans = st.session_state.plantilla_elegida.get('transicion', 'fade')
            trans_str = f"{plantilla_trans} — De la plantilla"

        # String de efectos
        if efectos_seleccionados:
            efectos_str = ', '.join([f"{e['nombre']} ({int(e['intensidad']*100)}%)" for e in efectos_seleccionados])
        else:
            efectos_str = 'Ninguno'

        st.markdown(f"""
        <div class="glass-card">
            <h4 style="color: var(--text-primary) !important;">📋 Resumen del proyecto</h4>
            <ul style="color: var(--text-secondary) !important;">
                <li><strong>Tipo:</strong> {tipo_cont}</li>
                <li><strong>Duración objetivo:</strong> {duracion} minutos</li>
                <li><strong>Plantilla:</strong> {plantilla_nombre}</li>
                <li><strong>Formatos:</strong> {formatos_str}</li>
                <li><strong>Transición:</strong> {trans_str}</li>
                <li><strong>Efectos visuales:</strong> {efectos_str}</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅ Anterior", use_container_width=True):
                st.session_state.wizard_step = 5
                st.rerun()
        with col2:
            if st.button("🚀 PRODUCIR VIDEO AHORA", type="primary",
                         use_container_width=True):
                # Ejecutar producción
                _ejecutar_produccion_video()


def _ejecutar_produccion_video():
    """Ejecuta el pipeline completo de producción de video."""
    from database import UPLOADS
    import streamlit as st

    # Recuperar archivos guardados en disco en el paso 1
    archivos_guardados = st.session_state.get("archivos_guardados")

    if not archivos_guardados or not archivos_guardados.get("principal"):
        st.error("No se encontró el video principal. Vuelve al paso 1 para subir el material.")
        if st.button("⬅ Volver al paso 1"):
            st.session_state.wizard_step = 1
            st.rerun()
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    progress = st.progress(0.0)
    status = st.empty()

    status.markdown("💾 Preparando archivos...")

    # Usar el video principal guardado
    ruta_video = archivos_guardados["principal"]
    video_principal_name = archivos_guardados.get("principal_name", "video.mp4")

    archivos_extra = {
        "videos": archivos_guardados.get("videos", []),
        "imagenes": archivos_guardados.get("imagenes", []),
        "audio": archivos_guardados.get("audio"),
    }

    # Aplicar personalizaciones de transición si el usuario las seleccionó
    transicion_personalizada = st.session_state.get('transicion_personalizada')
    duracion_transicion_personalizada = st.session_state.get('duracion_transicion_personalizada')

    # Crear una copia de la plantilla para no mutar la original
    plantilla_procesar = dict(st.session_state.plantilla_elegida)

    if transicion_personalizada:
        plantilla_procesar["transicion"] = transicion_personalizada
        if duracion_transicion_personalizada:
            plantilla_procesar["duracion_transicion"] = duracion_transicion_personalizada

    # Ejecutar pipeline
    def progress_callback(p, msg):
        progress.progress(p)
        status.markdown(f"⏳ {msg}")

    status.markdown("🎬 Iniciando pipeline de producción...")

    resultado = procesar_video_completo(
        ruta_video,
        st.session_state.guion,
        plantilla_procesar,
        archivos_extra,
        st.session_state.formatos_seleccionados,
        progress_callback
    )

    # Aplicar efectos visuales adicionales si fueron seleccionados
    efectos_seleccionados = st.session_state.get('efectos_seleccionados', [])
    if efectos_seleccionados and "error" not in resultado:
        from video_processor import aplicar_efectos_visuales
        status.markdown("✨ Aplicando efectos visuales...")
        video_base = resultado["video_final"]
        for efecto in efectos_seleccionados:
            video_base = aplicar_efectos_visuales(
                video_base,
                efecto["id"],
                efecto["intensidad"]
            )
        resultado["video_final"] = video_base

    if "error" not in resultado:
        # Descontar token
        usar_token(st.session_state.usuario["id"])
        st.session_state.usuario = obtener_usuario(st.session_state.usuario["id"])

        # Guardar proyecto
        proyecto = {
            "fecha": timestamp,
            "video_original": video_principal_name,
            "video_final": resultado["video_final"],
            "subtitulos": resultado["subtitulos"],
            "formatos": resultado["formatos"],
            "transcripcion": resultado["transcripcion"][:500],
            "plantilla_usada": st.session_state.plantilla_elegida["nombre"],
            "tipo_contenido": st.session_state.get("tipo_contenido_sel", ""),
        }
        agregar_proyecto(st.session_state.usuario["id"], proyecto)
        st.session_state.usuario = obtener_usuario(st.session_state.usuario["id"])

        st.balloons()
        st.markdown("""
        <div class="custom-alert custom-alert-success">
            <strong>¡Video producido exitosamente! 🎉</strong>
            <div style="margin-top: 0.5rem;">
                Tu video está listo. Puedes reproducirlo y descargarlo en los formatos seleccionados.
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Mostrar video
        st.video(resultado["video_final"])

        # Descargas
        st.markdown("### ⬇ Descargar resultados")
        cols = st.columns(max(len(resultado["formatos"]) + 1, 1))
        with cols[0]:
            if resultado.get("subtitulos"):
                try:
                    with open(resultado["subtitulos"], 'rb') as f:
                        st.download_button(
                            "📝 Subtítulos SRT",
                            f,
                            file_name=f"subtitulos_{timestamp}.srt",
                            mime="text/plain",
                            use_container_width=True
                        )
                except (FileNotFoundError, IOError):
                    pass

        for i, (nombre_fmt, ruta_fmt) in enumerate(resultado["formatos"].items(), 1):
            with cols[i]:
                try:
                    with open(ruta_fmt, 'rb') as f:
                        st.download_button(
                            f"🎬 {nombre_fmt.upper()}",
                            f,
                            file_name=f"{nombre_fmt}_{timestamp}.mp4",
                            mime="video/mp4",
                            use_container_width=True
                        )
                except (FileNotFoundError, IOError):
                    st.error(f"Formato {nombre_fmt} no disponible")

        # Transcripción
        with st.expander("📝 Ver transcripción completa"):
            st.write(resultado["transcripcion"])

        # Reset wizard
        if st.button("🎬 Crear otro video", type="primary"):
            st.session_state.wizard_step = 1
            st.session_state.guion = None
            st.session_state.plantilla_elegida = None
            st.session_state.archivos_guardados = None
            st.rerun()

    else:
        st.markdown(f"""
        <div class="custom-alert custom-alert-error">
            <strong>❌ Error en la producción</strong>
            <div style="margin-top: 0.3rem;">{resultado['error']}</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🔄 Reintentar"):
            st.rerun()


def render_templates_page():
    """Página de galería de plantillas con logo personalizado y guardado."""
    st.markdown("""
    <div class="hero-section">
        <h2 style="color: var(--text-primary) !important;">🎨 Galería de Plantillas</h2>
        <p style="color: var(--text-secondary) !important;">
            20 plantillas profesionales categorizadas para cada caso de uso.
            Las plantillas se adaptan a tu proyecto, cumplen estándares pero también crean identidad.
            Puedes guardarlas y reutilizarlas como imagen corporativa de tu institución.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Tabs: Plantillas / Mis Plantillas Guardadas / Logo Personalizado
    tab_galeria, tab_guardadas, tab_logo = st.tabs([
        "🎨 Galería de Plantillas",
        "💾 Mis Plantillas Guardadas",
        "🖼️ Logo Personalizado"
    ])

    with tab_galeria:
        selected_id = None
        if st.session_state.plantilla_elegida:
            selected_id = st.session_state.plantilla_elegida.get("id")

        render_template_gallery(selected_id=selected_id)

        if st.session_state.plantilla_elegida:
            st.markdown("---")
            plantilla = st.session_state.plantilla_elegida
            st.markdown(f"### 📋 Plantilla seleccionada: {plantilla['nombre']}")

            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📤 Usar para producir", type="primary", use_container_width=True):
                    st.session_state.vista = "process"
                    st.session_state.wizard_step = 1
                    st.rerun()
            with col2:
                if st.button("💾 Guardar como plantilla personalizada", use_container_width=True,
                             help="Guarda esta plantilla para reutilizarla como imagen corporativa"):
                    from database import guardar_plantilla_usuario
                    nombre_guardar = st.text_input("Nombre de la plantilla",
                                                    value=f"Mi {plantilla['nombre']}",
                                                    key="nombre_guardar_plantilla")
                    if st.button("✅ Confirmar guardado", type="primary"):
                        guardar_plantilla_usuario(
                            st.session_state.usuario["id"],
                            plantilla,
                            nombre_guardar
                        )
                        st.success(f"✅ Plantilla '{nombre_guardar}' guardada!")
            with col3:
                if st.button("⭐ Marcar como corporativa", use_container_width=True,
                             help="Usa esta plantilla por defecto en todos tus proyectos"):
                    st.session_state.plantilla_elegida["es_corporativa"] = True
                    st.success("⭐ Plantilla marcada como corporativa")

    with tab_guardadas:
        st.markdown("### 💾 Mis plantillas guardadas")
        st.info("Aquí aparecen las plantillas que has personalizado y guardado para reutilizar.")

        from database import listar_plantillas_usuario, eliminar_plantilla_usuario, marcar_plantilla_corporativa
        plantillas_guardadas = listar_plantillas_usuario(st.session_state.usuario["id"])

        if plantillas_guardadas:
            for pg in plantillas_guardadas:
                with st.container(border=True):
                    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                    with col1:
                        emoji_corp = "⭐" if pg.get("es_corporativa") else "📋"
                        st.markdown(f"**{emoji_corp} {pg.get('nombre', 'Sin nombre')}**")
                        st.caption(f"📅 Creada: {pg.get('fecha_creacion', 'N/A')[:10]}")
                    with col2:
                        if st.button("📂 Usar", key=f"use_saved_{pg['id']}"):
                            st.session_state.plantilla_elegida = pg.get("plantilla")
                            st.session_state.vista = "process"
                            st.rerun()
                    with col3:
                        if not pg.get("es_corporativa"):
                            if st.button("⭐", key=f"corp_{pg['id']}",
                                        help="Marcar como corporativa"):
                                marcar_plantilla_corporativa(pg["id"], True)
                                st.success("⭐ Marcada como corporativa")
                                st.rerun()
                        else:
                            st.caption("⭐ Corporativa")
                    with col4:
                        if st.button("🗑", key=f"del_saved_{pg['id']}"):
                            eliminar_plantilla_usuario(pg["id"])
                            st.rerun()
        else:
            st.info("📭 No tienes plantillas guardadas. "
                    "Selecciona una plantilla de la galería y guárdala para reutilizarla.")

    with tab_logo:
        st.markdown("### 🖼️ Logo Personalizado")
        st.info("Sube tu logo para incluirlo en tus videos. "
                "Puedes elegir la posición y tamaño.")

        # Subir logo
        logo_file = st.file_uploader(
            "📤 Sube tu logo (PNG, JPG, SVG)",
            type=['png', 'jpg', 'jpeg', 'svg', 'webp'],
            key="logo_upload"
        )

        # Configuración de posición
        col1, col2 = st.columns(2)
        with col1:
            posicion_logo = st.selectbox(
                "📍 Posición del logo",
                ["Esquina superior izquierda", "Esquina superior derecha",
                 "Esquina inferior izquierda", "Esquina inferior derecha",
                 "Centro superior", "Centro inferior", "Personalizado"],
                key="logo_posicion"
            )
        with col2:
            tamano_logo = st.slider(
                "📏 Tamaño del logo (% del ancho)",
                min_value=5, max_value=30, value=10, step=1,
                key="logo_tamano"
            )

        # Opacidad
        opacidad_logo = st.slider(
            "👻 Opacidad del logo (%)",
            min_value=20, max_value=100, value=100, step=5,
            key="logo_opacidad"
        )

        if logo_file is not None:
            # Guardar logo
            from database import UPLOADS
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            ruta_logo = UPLOADS / f"{timestamp}_logo_{logo_file.name}"
            with open(ruta_logo, 'wb') as f:
                f.write(logo_file.getbuffer())

            st.success(f"✅ Logo guardado: {logo_file.name}")

            # Guardar configuración en session state
            st.session_state.logo_config = {
                "path": str(ruta_logo),
                "posicion": posicion_logo,
                "tamano": tamano_logo,
                "opacidad": opacidad_logo,
            }

            # Preview del logo
            st.markdown("#### 👀 Vista previa del logo")
            st.image(str(ruta_logo), caption="Tu logo", width=200)

            # Mapear posición a coordenadas relativas
            pos_map = {
                "Esquina superior izquierda": (5, 5),
                "Esquina superior derecha": (85, 5),
                "Esquina inferior izquierda": (5, 85),
                "Esquina inferior derecha": (85, 85),
                "Centro superior": (45, 5),
                "Centro inferior": (45, 85),
            }

            # Preview de posición
            if posicion_logo != "Personalizado":
                x, y = pos_map.get(posicion_logo, (5, 5))
                st.markdown(f"""
                <div style="position: relative; width: 100%; aspect-ratio: 16/9;
                            background: linear-gradient(135deg, #1e1b4b, #0f172a);
                            border-radius: 12px; overflow: hidden; border: 2px solid #312e81;">
                    <div style="position: absolute; left: {x}%; top: {y}%;
                                transform: translate(-50%, -50%);
                                padding: 8px 16px;
                                background: rgba(255,255,255,0.2);
                                border: 2px dashed #a5b4fc;
                                border-radius: 8px;
                                color: white; font-size: 0.85rem; font-weight: 600;">
                        🏢 Tu Logo
                    </div>
                    <div style="position: absolute; top: 50%; left: 50%;
                                transform: translate(-50%, -50%);
                                color: #64748b; font-size: 0.9rem;">
                        Vista previa del video
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("👆 Sube un logo para configurarlo")


def render_projects_page():
    """Página de proyectos del usuario."""
    usuario = st.session_state.usuario
    proyectos = usuario.get("proyectos", [])

    st.markdown("""
    <div class="hero-section">
        <h2 style="color: var(--text-primary) !important;">🎬 Mis Proyectos</h2>
        <p style="color: var(--text-secondary) !important;">
            Gestiona y descarga tus videos producidos en múltiples formatos.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Stats del usuario
    stats = [
        {"icon": "🎬", "value": len(proyectos), "label": "Videos creados"},
        {"icon": "🪙", "value": usuario.get("tokens", 0), "label": "Tokens restantes"},
        {"icon": "✅", "value": usuario.get("tokens_usados", 0), "label": "Tokens usados"},
        {"icon": "📅", "value": usuario.get("plan", "gratis").upper(), "label": "Plan actual"},
    ]
    render_stat_grid(stats)

    st.markdown("---")

    if proyectos:
        st.markdown("### 📜 Historial de proyectos")
        for i, proyecto in enumerate(reversed(proyectos)):
            render_project_card(proyecto, i)
    else:
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 3rem;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">📭</div>
            <h3 style="color: var(--text-primary) !important;">No tienes proyectos aún</h3>
            <p style="color: var(--text-secondary) !important;">
                Crea tu primer video profesional con IA en minutos
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚀 Crear mi primer video", type="primary"):
            st.session_state.vista = "process"
            st.rerun()


def render_ideas_page():
    """Página de generación de ideas con IA adaptada al estilo del usuario."""
    st.markdown("""
    <div class="hero-section">
        <h2 style="color: var(--text-primary) !important;">💡 Generador de Ideas IA</h2>
        <p style="color: var(--text-secondary) !important;">
            Cuéntanos sobre tu área de interés y tu forma de comunicar.
            La IA reconocerá tu estilo y te propondrá ideas alineadas con tu misión.
        </p>
    </div>
    """, unsafe_allow_html=True)

    config = get_config()
    groq = GroqAI(config.get("groq_api_key", ""),
                  model=config.get("groq_model", "llama-3.1-8b-instant"))

    if not groq.esta_configurado():
        st.warning("API de IA no configurada. Contacta al administrador.")
        return

    # Wizard de 2 pasos: Área de interés + Estilo del usuario
    with st.container():
        st.markdown("### 1️⃣ Tu área de interés")
        area_interes = st.text_input(
            "🎯 Área de interés o industria",
            placeholder="Ej: Marketing digital, Fitness, Cocina, Tecnología, Educación financiera...",
            key="ideas_area"
        )
        publico = st.text_input(
            "👥 Público objetivo",
            placeholder="Ej: Jóvenes 18-30, Padres, Emprendedores, Estudiantes...",
            key="ideas_publico"
        )

        st.markdown("### 2️⃣ Tu estilo y misión")
        st.info("💡 Cada creador tiene una forma única de comunicar. "
                "Describe tu estilo para que las ideas se adapten a tu personalidad.")

        estilo_usuario = st.text_area(
            "🎨 Tu estilo de comunicación (cómo te expresas)",
            placeholder="Ej: Directo y motivador, uso humor sutil, me apasiona contar historias reales, "
            "mi tono es profesional pero cercano, me enfoco en datos y evidencia...",
            height=100,
            key="ideas_estilo"
        )
        mision = st.text_area(
            "🎯 Tu misión o relato (qué quieres lograr con tu contenido)",
            placeholder="Ej: Ayudar a emprendedores a escalar su negocio, "
            "democratizar el acceso a la educación financiera, "
            "inspirar a las personas a vivir más saludable...",
            height=80,
            key="ideas_mision"
        )

        cantidad = st.slider("💡 Número de ideas", 3, 10, 5)

    if st.button("✨ Generar Ideas Personalizadas", type="primary", use_container_width=True):
        if not area_interes:
            st.warning("Escribe tu área de interés para generar ideas")
            return

        with st.spinner("💡 Analizando tu estilo y generando ideas personalizadas..."):
            resultado = groq.generar_ideas_contenido(
                area_interes, publico, cantidad, estilo_usuario, mision
            )

            if "error" in resultado:
                st.error(f"Error: {resultado.get('error', 'desconocido')}")
                if "raw" in resultado:
                    with st.expander("🔍 Respuesta recibida (debug)"):
                        st.code(resultado["raw"][:1000])
            elif "ideas" in resultado:
                # Mostrar diagnóstico de estilo si está disponible
                if resultado.get("diagnostico_estilo"):
                    st.markdown("### 🎭 Análisis de tu estilo")
                    st.info(resultado["diagnostico_estilo"])

                st.markdown(f"### 🎯 {len(resultado['ideas'])} ideas personalizadas para ti")

                for i, idea in enumerate(resultado["ideas"], 1):
                    potencial_color = {
                        "alto": "var(--accent-success)",
                        "medio": "var(--accent-warning)",
                        "bajo": "var(--text-muted)"
                    }.get(idea.get("potencial_viral", "").lower(), "var(--accent-primary)")

                    st.markdown(f"""
                    <div class="glass-card" style="border-left: 4px solid {potencial_color};">
                        <div style="display: flex; justify-content: space-between; align-items: start;">
                            <h4 style="color: var(--text-primary) !important; margin: 0;">
                                {i}. {idea.get('titulo', 'Sin título')}
                            </h4>
                            <span class="template-tag" style="background: {potencial_color}33;
                                                                 color: {potencial_color} !important;">
                                🔥 {idea.get('potencial_viral', 'N/A').upper()}
                            </span>
                        </div>
                        <p style="color: var(--accent-warning) !important; margin: 0.5rem 0;">
                            🎯 Hook: "{idea.get('gancho', '')}"
                        </p>
                        <p style="color: var(--text-secondary) !important; margin: 0.3rem 0;">
                            {idea.get('descripcion', '')}
                        </p>
                        <div style="display: flex; gap: 0.5rem; flex-wrap: wrap; margin-top: 0.5rem;">
                            <span class="template-tag">📂 {idea.get('tipo', 'N/A')}</span>
                            <span class="template-tag">⏱ {idea.get('duracion_sugerida', 'N/A')}</span>
                        </div>
                        <p style="color: var(--text-muted) !important; font-size: 0.85rem; margin-top: 0.5rem;">
                            💭 {idea.get('razon', '')}
                        </p>
                        {f'<p style="color: var(--accent-primary) !important; font-size: 0.85rem; margin-top: 0.5rem; font-style: italic;">🎨 Adaptado a tu estilo: {idea.get("adaptado_a_estilo", "")}</p>' if idea.get('adaptado_a_estilo') else ''}
                    </div>
                    """, unsafe_allow_html=True)

                    # Botón para usar esta idea en producción
                    if st.button(f"🎬 Crear video con esta idea", key=f"use_idea_{i}",
                                 use_container_width=True):
                        st.session_state["texto_objetivo_input"] = idea.get('titulo', '')
                        st.session_state["tipo_contenido_sel"] = idea.get('tipo', 'Publicitario').capitalize()
                        st.session_state.vista = "process"
                        st.session_state.wizard_step = 2
                        st.rerun()


def render_redes_sociales_page():
    """Página de integración con redes sociales y SEO."""
    st.markdown("""
    <div class="hero-section">
        <h2 style="color: var(--text-primary) !important;">📱 Redes Sociales y SEO</h2>
        <p style="color: var(--text-secondary) !important;">
            Genera contenido optimizado para tus redes sociales y visualiza cómo se verá tu post publicado.
        </p>
    </div>
    """, unsafe_allow_html=True)

    config = get_config()
    groq = GroqAI(config.get("groq_api_key", ""),
                  model=config.get("groq_model", "llama-3.1-8b-instant"))

    if not groq.esta_configurado():
        st.warning("API de IA no configurada. Contacta al administrador.")
        return

    # Selección de proyecto creado
    usuario = st.session_state.usuario
    proyectos = usuario.get("proyectos", [])

    if not proyectos:
        st.info("Crea tu primer video en 'Producción' para generar contenido para redes sociales.")
        return

    with st.container():
        st.markdown("### 📹 Selecciona un video")
        opciones = [f"{p.get('video_original', 'Proyecto')} - {p.get('fecha', 'N/A')}" for p in reversed(proyectos)]
        proyecto_sel = st.selectbox("Video creado", opciones, key="rrss_proyecto")
        proyecto_idx = len(proyectos) - 1 - opciones.index(proyecto_sel)
        proyecto = proyectos[proyecto_idx]

        # Plataforma
        plataforma = st.selectbox(
            "📱 Plataforma de destino",
            ["Instagram", "TikTok", "Facebook", "Twitter/X", "LinkedIn", "YouTube"],
            key="rrss_plataforma"
        )

        # Información del video
        col1, col2 = st.columns(2)
        with col1:
            titulo_video = st.text_input(
                "🎬 Título del video",
                value=proyecto.get("video_original", "Mi video").replace(".mp4", ""),
                key="rrss_titulo"
            )
        with col2:
            descripcion_breve = st.text_input(
                "📝 Descripción breve",
                placeholder="De qué trata tu video...",
                key="rrss_descripcion"
            )

    if st.button("✨ Generar contenido optimizado por SEO", type="primary", use_container_width=True):
        with st.spinner("📱 Generando contenido optimizado..."):
            resultado = groq.generar_contenido_post_social(
                titulo_video, descripcion_breve, plataforma.lower()
            )

            if "error" in resultado:
                st.error(f"Error: {resultado.get('error')}")
            else:
                st.markdown("### 📝 Contenido generado (editable)")

                # Formulario editable
                col1, col2 = st.columns(2)
                with col1:
                    caption_editable = st.text_area(
                        "Caption principal",
                        value=resultado.get("caption", ""),
                        height=120,
                        key="rrss_caption_edit"
                    )
                    titulo_seo = st.text_input(
                        "Título SEO (máx 60 chars)",
                        value=resultado.get("titulo_seo", ""),
                        key="rrss_titulo_seo"
                    )
                    meta_desc = st.text_area(
                        "Meta descripción (máx 155 chars)",
                        value=resultado.get("meta_descripcion", ""),
                        height=70,
                        key="rrss_meta"
                    )

                with col2:
                    hashtags_str = ", ".join(resultado.get("hashtags", []))
                    hashtags_edit = st.text_area(
                        "Hashtags",
                        value=hashtags_str,
                        height=80,
                        key="rrss_hashtags"
                    )
                    keywords_str = ", ".join(resultado.get("keywords", []))
                    keywords_edit = st.text_input(
                        "Keywords",
                        value=keywords_str,
                        key="rrss_keywords"
                    )
                    cta = st.text_input(
                        "Call to Action",
                        value=resultado.get("call_to_action", ""),
                        key="rrss_cta"
                    )
                    horario = st.text_input(
                        "Mejor horario",
                        value=resultado.get("mejor_horario", ""),
                        key="rrss_horario"
                    )

                # Preview de cómo se verá publicado
                st.markdown("### 👀 Preview del post publicado")

                # Simular interfaz de la red social
                plataforma_lower = plataforma.lower()
                if plataforma_lower == "instagram":
                    preview_html = f"""
                    <div style="max-width: 400px; margin: 0 auto; background: white;
                                border-radius: 12px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.2);">
                        <div style="background: linear-gradient(135deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888);
                                    padding: 12px; display: flex; align-items: center; gap: 8px;">
                            <div style="width: 32px; height: 32px; border-radius: 50%;
                                        background: linear-gradient(45deg, #f09433, #dc2743);"></div>
                            <strong style="color: white;">tu_marca</strong>
                        </div>
                        <div style="background: #000; height: 200px; display: flex; align-items: center;
                                    justify-content: center; color: white; font-size: 0.9rem;">
                            🎬 Tu video aparecerá aquí
                        </div>
                        <div style="padding: 12px; background: white;">
                            <div style="display: flex; gap: 12px; margin-bottom: 8px;">
                                <span>❤️ 1.2k</span><span>💬 89</span><span>📤 45</span>
                            </div>
                            <p style="margin: 0; color: #000; font-size: 0.85rem;">
                                <strong>tu_marca</strong> {caption_editable[:100]}...
                            </p>
                            <p style="color: #00376b; font-size: 0.8rem; margin-top: 4px;">
                                {hashtags_edit[:80]}
                            </p>
                        </div>
                    </div>
                    """
                elif plataforma_lower == "tiktok":
                    preview_html = f"""
                    <div style="max-width: 300px; margin: 0 auto; background: #000;
                                border-radius: 12px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.4);
                                position: relative;">
                        <div style="height: 400px; background: linear-gradient(135deg, #25F4EE, #FE2C55);
                                    display: flex; align-items: center; justify-content: center; color: white;">
                            🎬 Tu video TikTok
                        </div>
                        <div style="position: absolute; right: 10px; bottom: 60px; text-align: center; color: white;">
                            <div>❤️</div><div>1.2k</div>
                            <div>💬</div><div>89</div>
                            <div>📤</div><div>45</div>
                        </div>
                        <div style="padding: 12px; color: white;">
                            <p style="margin: 0; font-size: 0.85rem;">@tu_marca</p>
                            <p style="margin: 4px 0; font-size: 0.8rem;">{caption_editable[:80]}...</p>
                            <p style="color: #25F4EE; font-size: 0.75rem; margin: 0;">{hashtags_edit[:60]}</p>
                        </div>
                    </div>
                    """
                else:
                    preview_html = f"""
                    <div style="max-width: 500px; margin: 0 auto; background: white;
                                border-radius: 8px; padding: 16px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                        <div style="display: flex; gap: 8px; margin-bottom: 12px;">
                            <div style="width: 40px; height: 40px; border-radius: 50%;
                                        background: #1877f2;"></div>
                            <div>
                                <strong>Tu Marca</strong>
                                <p style="margin: 0; font-size: 0.75rem; color: #65676b;">Just now · 🌐</p>
                            </div>
                        </div>
                        <p style="color: #000; margin: 8px 0;">{caption_editable[:200]}</p>
                        <div style="background: #000; height: 200px; display: flex; align-items: center;
                                    justify-content: center; color: white;">🎬 Tu video</div>
                        <div style="display: flex; gap: 16px; padding: 12px 0; color: #65676b;">
                            <span>👍 Me gusta</span><span>💬 Comentar</span><span>📤 Compartir</span>
                        </div>
                    </div>
                    """

                st.markdown(preview_html, unsafe_allow_html=True)

                # Botón para programar publicación
                st.markdown("---")
                if st.button("📅 Programar publicación en agenda", type="primary"):
                    # Guardar en agenda
                    from database import agregar_publicacion_agenda
                    agregar_publicacion_agenda(usuario["id"], {
                        "titulo": titulo_video,
                        "plataforma": plataforma,
                        "caption": caption_editable,
                        "hashtags": hashtags_edit,
                        "video_path": proyecto.get("video_final", ""),
                        "fecha_programada": None,  # A definir en agenda
                        "estado": "borrador",
                        "contenido_generado": {
                            "titulo_seo": titulo_seo,
                            "meta_descripcion": meta_desc,
                            "keywords": keywords_edit,
                            "cta": cta,
                            "mejor_horario": horario,
                        }
                    })
                    st.success("✅ Publicación guardada en la agenda. Visita 'Agenda' para programarla.")


def render_agenda_page():
    """Página de agenda de publicaciones."""
    st.markdown("""
    <div class="hero-section">
        <h2 style="color: var(--text-primary) !important;">📅 Agenda de Publicaciones</h2>
        <p style="color: var(--text-secondary) !important;">
            Programa tus publicaciones y mantén consistencia en tus redes sociales.
        </p>
    </div>
    """, unsafe_allow_html=True)

    usuario = st.session_state.usuario
    from database import (
        listar_agenda_usuario, eliminar_publicacion_agenda,
        actualizar_publicacion_agenda
    )
    from datetime import datetime, timedelta

    agenda = listar_agenda_usuario(usuario["id"])

    # Stats
    stats_cols = st.columns(4)
    stats_cols[0].metric("📅 Total publicaciones", len(agenda))
    stats_cols[1].metric("✅ Publicadas", sum(1 for p in agenda if p.get("estado") == "publicada"))
    stats_cols[2].metric("⏰ Programadas", sum(1 for p in agenda if p.get("estado") == "programada"))
    stats_cols[3].metric("📝 Borradores", sum(1 for p in agenda if p.get("estado") == "borrador"))

    st.markdown("---")

    # Lista de publicaciones
    if agenda:
        st.markdown("### 📋 Próximas publicaciones")
        for pub in reversed(agenda):
            estado = pub.get("estado", "borrador")
            estado_emoji = {"publicada": "✅", "programada": "⏰", "borrador": "📝"}.get(estado, "📝")
            estado_color = {"publicada": "var(--accent-success)",
                           "programada": "var(--accent-warning)",
                           "borrador": "var(--text-muted)"}.get(estado, "var(--text-muted)")

            with st.container(border=True):
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.markdown(f"**{estado_emoji} {pub.get('titulo', 'Sin título')}**")
                    st.caption(f"📱 {pub.get('plataforma', 'N/A')} · 📅 {pub.get('fecha_programada', 'Sin programar')}")
                    if pub.get("caption"):
                        st.text(pub["caption"][:120] + "..." if len(pub.get("caption", "")) > 120 else pub["caption"])
                with col2:
                    nuevo_estado = st.selectbox(
                        "Estado",
                        ["borrador", "programada", "publicada"],
                        index=["borrador", "programada", "publicada"].index(estado),
                        key=f"agenda_estado_{pub['id']}"
                    )
                    if nuevo_estado != estado:
                        actualizar_publicacion_agenda(pub["id"], {"estado": nuevo_estado})
                        st.success("✅ Actualizado")
                with col3:
                    if st.button("🗑 Eliminar", key=f"del_agenda_{pub['id']}"):
                        eliminar_publicacion_agenda(pub["id"])
                        st.rerun()
    else:
        st.info("📭 No tienes publicaciones en la agenda. "
                "Ve a 'Redes Sociales' para generar contenido y programarlo.")


def render_analisis_page():
    """Página de análisis de efectividad y comentarios."""
    st.markdown("""
    <div class="hero-section">
        <h2 style="color: var(--text-primary) !important;">📊 Análisis y Estrategia</h2>
        <p style="color: var(--text-secondary) !important;">
            Mide la efectividad de tus posteos, analiza comentarios y recibe recomendaciones de estrategia.
        </p>
    </div>
    """, unsafe_allow_html=True)

    config = get_config()
    groq = GroqAI(config.get("groq_api_key", ""),
                  model=config.get("groq_model", "llama-3.1-8b-instant"))

    if not groq.esta_configurado():
        st.warning("API de IA no configurada. Contacta al administrador.")
        return

    # Tabs para las diferentes funcionalidades
    tab_efectividad, tab_comentarios, tab_creaciones = st.tabs([
        "📈 Efectividad de Posteos",
        "💬 Análisis de Comentarios",
        "🎨 Análisis de Creaciones"
    ])

    with tab_efectividad:
        st.markdown("### 📈 Analiza la efectividad de tus publicaciones")
        st.info("Ingresa las métricas de tus últimos posteos para recibir análisis y recomendaciones.")

        # Formulario para ingresar métricas
        num_posteos = st.number_input("¿Cuántos posteos quieres analizar?", 1, 10, 3, key="num_posteos_eff")

        posteos = []
        for i in range(num_posteos):
            with st.expander(f"📊 Posteo {i+1}", expanded=(i == 0)):
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    titulo_p = st.text_input("Título", key=f"eff_titulo_{i}",
                                              placeholder=f"Posteo {i+1}")
                with col2:
                    likes = st.number_input("👍 Likes", 0, 1000000, 0, key=f"eff_likes_{i}")
                with col3:
                    comments = st.number_input("💬 Comentarios", 0, 100000, 0, key=f"eff_comments_{i}")
                with col4:
                    views = st.number_input("👁 Views", 0, 10000000, 0, key=f"eff_views_{i}")

                if titulo_p:
                    posteos.append({
                        "titulo": titulo_p,
                        "likes": likes,
                        "comments": comments,
                        "views": views,
                        "engagement": ((likes + comments) / views * 100) if views > 0 else 0
                    })

        if st.button("🔍 Analizar efectividad", type="primary") and posteos:
            with st.spinner("📈 Analizando métricas..."):
                resultado = groq.analizar_efectividad_posteos(posteos)

                if "error" in resultado:
                    st.error(f"Error: {resultado.get('error')}")
                else:
                    st.markdown("### 📊 Resultados del análisis")

                    if resultado.get("resumen_general"):
                        st.info(resultado["resumen_general"])

                    col1, col2 = st.columns(2)
                    with col1:
                        if resultado.get("mejor_posteo"):
                            st.success(f"🏆 **Mejor posteo:** {resultado['mejor_posteo']}")
                        if resultado.get("patrones_exitosos"):
                            st.markdown("**✅ Patrones exitosos:**")
                            for p in resultado["patrones_exitosos"]:
                                st.markdown(f"- {p}")
                    with col2:
                        if resultado.get("peor_posteo"):
                            st.warning(f"📉 **Posteo con menor rendimiento:** {resultado['peor_posteo']}")
                        if resultado.get("patrones_fallidos"):
                            st.markdown("**❌ Patrones a evitar:**")
                            for p in resultado["patrones_fallidos"]:
                                st.markdown(f"- {p}")

                    if resultado.get("recomendacion_estrategia"):
                        st.markdown("### 🎯 Recomendación de estrategia")
                        rec_color = "success" if "insistir" in resultado["recomendacion_estrategia"].lower() else "warning"
                        if rec_color == "success":
                            st.success(f"**{resultado['recomendacion_estrategia']}**")
                        else:
                            st.warning(f"**{resultado['recomendacion_estrategia']}**")
                        if resultado.get("razon_recomendacion"):
                            st.caption(resultado["razon_recomendacion"])

                    metricas = resultado.get("metricas_clave", {})
                    if metricas:
                        st.markdown("### 📊 Métricas clave")
                        cols = st.columns(len(metricas))
                        for i, (k, v) in enumerate(metricas.items()):
                            cols[i].metric(k.replace("_", " ").title(), v)

    with tab_comentarios:
        st.markdown("### 💬 Análisis inteligente de comentarios")
        st.info("Pega los comentarios de tus seguidores para extraer ideas importantes, "
                "detectar críticas reales y oportunidades de contenido.")

        comentarios_text = st.text_area(
            "📋 Comentarios de tus seguidores (uno por línea)",
            height=200,
            placeholder="Comentario 1...\nComentario 2...\nComentario 3...",
            key="comentarios_input"
        )

        if st.button("🔍 Analizar comentarios", type="primary") and comentarios_text:
            comentarios = [c.strip() for c in comentarios_text.split("\n") if c.strip()]
            with st.spinner("💬 Analizando comentarios..."):
                resultado = groq.analizar_comentarios(comentarios)

                if "error" in resultado:
                    st.error(f"Error: {resultado.get('error')}")
                else:
                    st.markdown("### 📊 Resultados del análisis")

                    if resultado.get("sentimiento_general"):
                        sent = resultado["sentimiento_general"]
                        sent_color = {"positivo": "success", "negativo": "error",
                                     "neutro": "info", "mixto": "warning"}.get(sent, "info")
                        getattr(st, sent_color)(f"**Sentimiento general:** {sent.upper()}")

                    col1, col2 = st.columns(2)
                    with col1:
                        if resultado.get("ideas_importantes"):
                            st.markdown("### 💡 Ideas importantes extraídas")
                            for idea in resultado["ideas_importantes"]:
                                st.markdown(f"- {idea}")
                        if resultado.get("oportunidades_contenido"):
                            st.markdown("### 🎯 Oportunidades de contenido")
                            for opp in resultado["oportunidades_contenido"]:
                                st.markdown(f"- {opp}")
                    with col2:
                        if resultado.get("criticas_reales"):
                            st.markdown("### ⚠️ Críticas reales detectadas")
                            for crit in resultado["criticas_reales"]:
                                st.warning(f"- {crit}")
                        if resultado.get("fallos_detectados"):
                            st.markdown("### ❌ Fallos detectados")
                            for fallo in resultado["fallos_detectados"]:
                                st.error(f"- {fallo}")

                    if resultado.get("sugerencias_mejora"):
                        st.markdown("### ✅ Sugerencias de mejora")
                        for sug in resultado["sugerencias_mejora"]:
                            st.markdown(f"- {sug}")

                    if resultado.get("alertas_urgentes"):
                        st.markdown("### 🚨 Alertas urgentes")
                        for alerta in resultado["alertas_urgentes"]:
                            if alerta and alerta != "alerta 1 si hay algo urgente":
                                st.error(f"⚠️ {alerta}")

    with tab_creaciones:
        st.markdown("### 🎨 Análisis de tus creaciones")
        st.info("Analizamos tus videos creados y te proponemos nuevas piezas que contribuyan a tu relato.")

        usuario = st.session_state.usuario
        proyectos = usuario.get("proyectos", [])

        if not proyectos:
            st.info("🎬 Aún no tienes creaciones. Crea tu primer video para recibir análisis y propuestas.")
        else:
            # Narrativa del usuario
            narrativa = st.text_area(
                "🎯 Tu narrativa o misión como creador",
                placeholder="Ej: Ayudar a emprendedores a través de contenido educativo...",
                height=80,
                key="narrativa_usuario"
            )

            if st.button("🔍 Analizar creaciones y proponer piezas", type="primary"):
                # Preparar datos de creaciones
                creaciones_data = [
                    {
                        "titulo": p.get("video_original", "Proyecto"),
                        "fecha": p.get("fecha", ""),
                        "plantilla": p.get("plantilla_usada", ""),
                        "tipo": p.get("tipo_contenido", ""),
                    }
                    for p in proyectos[-10:]  # Últimas 10
                ]

                with st.spinner("🎨 Analizando tus creaciones..."):
                    resultado = groq.analizar_creaciones_y_proponer(creaciones_data, narrativa)

                    if "error" in resultado:
                        st.error(f"Error: {resultado.get('error')}")
                    else:
                        if resultado.get("analisis_creaciones"):
                            st.markdown("### 📊 Análisis de tu estilo")
                            st.info(resultado["analisis_creaciones"])

                        if resultado.get("coherencia_narrativa"):
                            st.markdown("### 🎯 Coherencia con tu narrativa")
                            st.success(resultado["coherencia_narrativa"])

                        col1, col2 = st.columns(2)
                        with col1:
                            if resultado.get("fortalezas"):
                                st.markdown("### ✅ Fortalezas")
                                for f in resultado["fortalezas"]:
                                    st.markdown(f"- {f}")
                        with col2:
                            if resultado.get("areas_mejora"):
                                st.markdown("### 📈 Áreas de mejora")
                                for a in resultado["areas_mejora"]:
                                    st.markdown(f"- {a}")

                        if resultado.get("propuestas_piezas"):
                            st.markdown("### 🎬 Piezas propuestas para tu relato")
                            for i, pieza in enumerate(resultado["propuestas_piezas"], 1):
                                prioridad = pieza.get("prioridad", "media")
                                prioridad_color = {"alta": "error", "media": "warning", "baja": "info"}.get(prioridad, "info")

                                with st.container(border=True):
                                    st.markdown(f"**{i}. {pieza.get('titulo', 'Sin título')}**")
                                    st.caption(f"📂 {pieza.get('tipo', 'N/A')} · 🎯 Prioridad: {prioridad.upper()}")
                                    st.write(pieza.get("descripcion", ""))
                                    if pieza.get("conexion_relato"):
                                        st.info(f"🎨 **Conexión con tu relato:** {pieza['conexion_relato']}")

                        if resultado.get("estrategia_contenido"):
                            st.markdown("### 📋 Estrategia de contenido recomendada")
                            st.success(resultado["estrategia_contenido"])

                        if resultado.get("proximos_pasos"):
                            st.markdown("### ✅ Próximos pasos")
                            for i, paso in enumerate(resultado["proximos_pasos"], 1):
                                st.markdown(f"{i}. {paso}")


def render_plans_page():
    """Página de planes y membresías."""
    st.markdown("""
    <div class="hero-section">
        <h2 style="color: var(--text-primary) !important;">💎 Planes y Membresías</h2>
        <p style="color: var(--text-secondary) !important;">
            Elige el plan que mejor se adapte a tus necesidades de producción.
        </p>
    </div>
    """, unsafe_allow_html=True)

    usuario = st.session_state.usuario
    render_pricing_section(current_plan=usuario.get("plan", "gratis"))

    st.markdown("---")

    # FAQ
    st.markdown("### ❓ Preguntas frecuentes")
    faqs = [
        ("¿Qué son los tokens?", "Los tokens son créditos que se consumen al procesar cada video. Cada plan incluye un número determinado de tokens mensuales."),
        ("¿Puedo cambiar de plan?", "Sí, puedes actualizar o downgradear tu plan en cualquier momento desde esta sección."),
        ("¿Los tokens se acumulan?", "Los tokens no usados en un mes se reinician al inicio del siguiente período de facturación."),
        ("¿Qué formatos de video puedo exportar?", "Todos los planes permiten exportar a YouTube (16:9), TikTok (9:16) e Instagram (1:1)."),
        ("¿Necesito instalar algo?", "No, todo funciona en la nube. Solo necesitas un navegador moderno."),
    ]
    for pregunta, respuesta in faqs:
        with st.expander(f"❓ {pregunta}"):
            st.write(respuesta)


def render_config_page():
    """Página de configuración del usuario."""
    usuario = st.session_state.usuario

    st.markdown("""
    <div class="hero-section">
        <h2 style="color: var(--text-primary) !important;">⚙️ Configuración</h2>
        <p style="color: var(--text-secondary) !important;">
          Gestiona tu cuenta y preferencias.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Info de cuenta
    st.markdown("### 👤 Información de cuenta")
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Nombre", value=usuario.get("nombre", ""), disabled=True)
            st.text_input("Email", value=usuario.get("email", ""), disabled=True)
        with col2:
            st.text_input("Plan actual", value=usuario.get("plan", "").upper(), disabled=True)
            st.text_input("Tokens disponibles", value=str(usuario.get("tokens", 0)), disabled=True)

    st.markdown("---")

    # Preferencias
    st.markdown("### 🎨 Preferencias")
    config_personal = usuario.get("config_personal", {})

    plantilla_fav_id = st.selectbox(
        "Plantilla favorita por defecto",
        ["Ninguna"] + [p["id"] for p in PLANTILLAS_PROFESIONALES],
        format_func=lambda x: "Ninguna" if x == "Ninguna" else next((p["nombre"] for p in PLANTILLAS_PROFESIONALES if p["id"] == x), x)
    )

    formato_pref = st.selectbox("Formato preferido de salida",
                                ["youtube", "tiktok", "instagram"],
                                format_func=lambda x: {"youtube": "YouTube (16:9)",
                                                       "tiktok": "TikTok (9:16)",
                                                       "instagram": "Instagram (1:1)"}[x])

    notif = st.checkbox("Recibir notificaciones por email", value=config_personal.get("notificaciones", True))

    if st.button("💾 Guardar preferencias", type="primary"):
        cambios = {
            "config_personal": {
                "plantilla_favorita": None if plantilla_fav_id == "Ninguna" else plantilla_fav_id,
                "formato_preferido": formato_pref,
                "notificaciones": notif,
            }
        }
        from database import actualizar_usuario
        actualizar_usuario(usuario["id"], cambios)
        st.session_state.usuario = obtener_usuario(usuario["id"])
        st.success("✅ Preferencias guardadas")

    st.markdown("---")

    # Zona de peligro
    st.markdown("### ⚠ Zona de peligro")
    with st.expander("🗑 Cerrar cuenta"):
        st.warning("Esta acción eliminará todos tus proyectos y datos permanentemente.")
        confirm = st.checkbox("Entiendo que perderé toda mi información")
        if st.button("🗑 Eliminar mi cuenta", disabled=not confirm):
            from database import actualizar_usuario
            actualizar_usuario(usuario["id"], {"activo": False})
            logout()


def render_admin_page():
    """Panel de administración."""
    st.markdown("""
    <div class="hero-section">
        <h2 style="color: var(--text-primary) !important;">🔑 Panel de Administración</h2>
        <p style="color: var(--text-secondary) !important;">
            Gestiona el sistema, usuarios y configuración global.
        </p>
    </div>
    """, unsafe_allow_html=True)

    admin_vista = st.sidebar.radio("📍 Secciones",
                                    ["📊 Dashboard", "👥 Usuarios", "🔑 Configuración IA",
                                     "🎨 Plantillas", "💰 Membresías", "📈 Estadísticas"])

    db = cargar_db()

    if admin_vista == "📊 Dashboard":
        data = get_dashboard_data()
        st.markdown("### 📊 Dashboard general")

        stats = [
            {"icon": "👥", "value": data["total_usuarios"], "label": "Usuarios totales"},
            {"icon": "✅", "value": data["usuarios_activos"], "label": "Usuarios activos"},
            {"icon": "🎬", "value": data["videos_procesados"], "label": "Videos procesados"},
            {"icon": "🪙", "value": data["tokens_distribuidos"], "label": "Tokens distribuidos"},
        ]
        render_stat_grid(stats)

        st.markdown("### 📊 Distribución por planes")
        for plan_id, count in data["distribucion_planes"].items():
            plan_nombre = next((m["nombre"] for m in db["membresias"] if m["id"] == plan_id), plan_id)
            pct = (count / data["total_usuarios"] * 100) if data["total_usuarios"] > 0 else 0
            st.write(f"**{plan_nombre}**: {count} usuarios ({pct:.1f}%)")
            st.progress(pct / 100)

    elif admin_vista == "👥 Usuarios":
        st.markdown("### 👥 Gestión de usuarios")
        usuarios = listar_usuarios()

        if usuarios:
            for u in usuarios:
                with st.expander(f"👤 {u['nombre']} · {u['email']} · Plan: {u['plan'].upper()}"):
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col1:
                        st.write(f"**Tokens disponibles:** {u.get('tokens', 0)}")
                        st.write(f"**Tokens usados:** {u.get('tokens_usados', 0)}")
                        st.write(f"**Proyectos:** {len(u.get('proyectos', []))}")
                        st.write(f"**Estado:** {'✅ Activo' if u.get('activo', True) else '⛔ Suspendido'}")
                        st.write(f"**Registro:** {u.get('fecha_registro', 'N/A')[:10]}")
                    with col2:
                        add_tokens = st.number_input(f"Añadir tokens", 1, 100, 10,
                                                       key=f"tok_{u['id']}")
                        if st.button("➕ Añadir", key=f"add_{u['id']}"):
                            from database import actualizar_usuario
                            new_tokens = u.get("tokens", 0) + add_tokens
                            actualizar_usuario(u["id"], {"tokens": new_tokens})
                            st.success(f"✅ {add_tokens} tokens añadidos")
                            st.rerun()
                    with col3:
                        if u.get("activo", True):
                            if st.button("⛔ Suspender", key=f"sus_{u['id']}"):
                                from database import actualizar_usuario
                                actualizar_usuario(u["id"], {"activo": False})
                                st.rerun()
                        else:
                            if st.button("✅ Activar", key=f"act_{u['id']}"):
                                from database import actualizar_usuario
                                actualizar_usuario(u["id"], {"activo": True})
                                st.rerun()
        else:
            st.info("No hay usuarios registrados aún.")

    elif admin_vista == "🔑 Configuración IA":
        st.markdown("### 🔑 Configuración de IA (Groq)")

        api_key = st.text_input("API Key de Groq",
                                 value=db["config"].get("groq_api_key", ""),
                                 type="password",
                                 help="Obtén tu API key gratuita en https://console.groq.com")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Guardar API Key", type="primary"):
                update_config({"groq_api_key": api_key})
                st.success("✅ API Key guardada")
        with col2:
            if st.button("🧪 Probar conexión"):
                groq = GroqAI(api_key)
                with st.spinner("Probando conexión con Groq..."):
                    resultado = groq.test_conexion()

                if resultado.get("ok"):
                    st.success(f"✅ Conexión exitosa. Modelo: {resultado['modelo_activo']}")
                    st.info(f"Max tokens detectado: {resultado.get('max_tokens_detectado', 'N/A')}")

                    # Guardar el modelo detectado automáticamente
                    update_config({"groq_model": resultado["modelo_activo"]})

                    st.session_state.modelos_groq = resultado.get("modelos_disponibles", [])
                else:
                    st.error(f"❌ {resultado.get('error', 'Error desconocido')}")
                    if "modelos_disponibles" in resultado:
                        st.info("Modelos disponibles detectados.")

        # Selección manual de modelo
        if "modelos_groq" not in st.session_state:
            # Cargar modelos disponibles si hay API key
            if api_key:
                groq_temp = GroqAI(api_key)
                modelos_temp = groq_temp.listar_modelos()
                if modelos_temp:
                    st.session_state.modelos_groq = modelos_temp

        if "modelos_groq" in st.session_state and st.session_state.modelos_groq:
            st.markdown("#### 🤖 Selecciona modelo")
            modelo_actual = db["config"].get("groq_model", "llama-3.1-8b-instant")

            # Recomendar modelos de alta capacidad
            modelos_recomendados = [m for m in MODELOS_RECOMENDADOS
                                     if m in st.session_state.modelos_groq]

            if modelos_recomendados:
                st.info(f"💡 Recomendados (mayor capacidad): {', '.join(modelos_recomendados[:2])}")

            try:
                idx = st.session_state.modelos_groq.index(modelo_actual) if modelo_actual in st.session_state.modelos_groq else 0
            except ValueError:
                idx = 0

            modelo_sel = st.selectbox("Modelo de IA", st.session_state.modelos_groq,
                                       index=idx,
                                       help="Los modelos 70b tienen mayor capacidad. Los 8b son más rápidos pero con límite de tokens menor.")
            if st.button("💾 Guardar modelo seleccionado"):
                update_config({"groq_model": modelo_sel})
                st.success(f"✅ Modelo guardado: {modelo_sel}")

        st.markdown("---")
        st.markdown("### 🔐 Contraseña de Admin")
        new_pass = st.text_input("Nueva contraseña de admin", type="password")
        if st.button("💾 Cambiar contraseña admin", type="primary"):
            if len(new_pass) >= 8:
                set_admin_password(new_pass)
                st.success("✅ Contraseña actualizada")
            else:
                st.warning("La contraseña debe tener al menos 8 caracteres")

    elif admin_vista == "🎨 Plantillas":
        st.markdown("### 🎨 Plantillas del sistema")
        st.write(f"**{len(PLANTILLAS_PROFESIONALES)} plantillas predefinidas**")

        for p in PLANTILLAS_PROFESIONALES:
            with st.expander(f"🎨 {p['nombre']} - {p['categoria']}"):
                st.json(p)

    elif admin_vista == "💰 Membresías":
        st.markdown("### 💰 Configuración de planes")
        for m in db["membresias"]:
            with st.expander(f"💎 {m['nombre']} - ${m['precio']}/mes"):
                st.write(f"**Tokens incluidos:** {m['tokens']}")
                st.write("**Features:**")
                for f in m["features"]:
                    st.write(f"- {f}")

    elif admin_vista == "📈 Estadísticas":
        st.markdown("### 📈 Estadísticas del sistema")
        stats = get_stats()
        st.write(f"**Videos procesados totales:** {stats.get('total_videos_procesados', 0)}")
        st.write(f"**Fecha de inicio:** {stats.get('fecha_inicio', 'N/A')[:10]}")

        # Mostrar backups disponibles
        from database import DB_BACKUP_DIR
        if DB_BACKUP_DIR.exists():
            backups = list(DB_BACKUP_DIR.glob("sistema_*.json"))
            st.write(f"**Backups disponibles:** {len(backups)}")
            if backups:
                with st.expander("Ver backups"):
                    for b in sorted(backups, reverse=True)[:10]:
                        st.write(f"- {b.name}")


# ============ SIDEBAR ADMIN ============
def render_admin_sidebar():
    """Sidebar del modo admin."""
    st.sidebar.markdown("""
    <div class="sidebar-user-card" style="border-left: 4px solid var(--accent-warning);">
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <div style="font-size: 1.5rem;">🔑</div>
            <div>
                <div style="font-weight: 700; color: var(--accent-warning) !important;">MODO ADMIN</div>
                <div style="font-size: 0.8rem; color: var(--text-muted) !important;">Acceso completo</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.sidebar.button("🚪 Salir de admin", use_container_width=True):
        st.session_state.admin_mode = False
        st.rerun()


def render_admin_login():
    """Formulario de login admin."""
    with st.sidebar.expander("🔐 Acceso Admin", expanded=True):
        st.markdown("Para acceder al panel de administración, ingresa la contraseña.")
        admin_pass = st.text_input("Contraseña de admin", type="password", key="admin_pass_input")
        if st.button("🔑 Entrar como Admin", type="primary", use_container_width=True):
            if verify_admin_password(admin_pass):
                st.session_state.admin_mode = True
                st.success("✅ Modo admin activado")
                st.rerun()
            else:
                st.error("❌ Contraseña incorrecta")


# ============ MAIN ============
def main():
    """Función principal."""

    # Sidebar
    with st.sidebar:
        if is_admin():
            render_admin_sidebar()
        elif is_logged_in():
            render_user_sidebar()
        else:
            st.markdown("""
            <div style="text-align: center; padding: 1rem 0;">
                <h2 style="background: var(--gradient-primary);
                          -webkit-background-clip: text;
                          -webkit-text-fill-color: transparent;
                          background-clip: text;
                          font-weight: 800;
                          margin: 0;">🎬 VideoAI</h2>
                <p style="color: var(--text-muted) !important; font-size: 0.85rem; margin: 0;">
                    Studio Pro
                </p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("---")
            st.info("👆 Inicia sesión para empezar a crear videos profesionales con IA")

        # Acceso admin siempre disponible
        if not is_admin():
            render_admin_login()

    # Contenido principal
    if is_admin():
        render_admin_page()
    elif is_logged_in():
        vista = st.session_state.get("vista", "home")
        if vista == "home":
            render_home_page()
        elif vista == "process":
            render_process_page()
        elif vista == "templates":
            render_templates_page()
        elif vista == "projects":
            render_projects_page()
        elif vista == "ideas":
            render_ideas_page()
        elif vista == "redes":
            render_redes_sociales_page()
        elif vista == "agenda":
            render_agenda_page()
        elif vista == "analisis":
            render_analisis_page()
        elif vista == "plans":
            render_plans_page()
        elif vista == "config":
            render_config_page()
        elif vista == "auth":
            render_login_form()
        else:
            render_home_page()
    else:
        # Usuario no logueado - mostrar landing
        tab_landing = st.tabs(["🏠 Inicio", "🔐 Acceder"])

        with tab_landing[0]:
            render_home_page()

            st.markdown("---")
            st.markdown("### 🚀 ¿Listo para empezar?")
            if st.button("🔐 Iniciar sesión / Crear cuenta", type="primary", use_container_width=True):
                st.session_state.vista = "auth"
                st.rerun()

        with tab_landing[1]:
            render_login_form()


if __name__ == "__main__":
    main()
