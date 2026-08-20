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
    """Página de inicio. Orden: Hero → Funcionalidades → Botón → Stats al final."""
    # ============ HERO ============
    st.markdown("""
    <div class="hero-section">
        <div class="hero-title">VideoAI Studio Pro</div>
        <div class="hero-subtitle">
            La plataforma todo-en-uno para crear videos profesionales con inteligencia artificial.
            Guiones inteligentes, plantillas premium y exportación multi-formato.
        </div>
        <div class="hero-badges">
            <span class="hero-badge hero-badge-accent">✨ 20 Plantillas Pro</span>
            <span class="hero-badge">🎬 Multi-formato (YT, TT, IG)</span>
            <span class="hero-badge">📝 Subtítulos Automáticos</span>
            <span class="hero-badge">🎨 Color Grading</span>
            <span class="hero-badge">🎵 Audio Ducking</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align: center; margin-bottom: 1rem;">
        <p style="color: var(--accent-tertiary) !important; font-style: italic; font-size: 1rem;">
            "La creación de videos profesionales nunca fue tan fácil y entretenida"
        </p>
        <p style="color: var(--text-muted) !important; font-size: 0.85rem;">
            Desarrollado por <strong style="color: var(--accent-primary) !important;">Comunicaciones Integrales</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ============ FUNCIONALIDADES (sobre Potencia) ============
    st.markdown("### 🚀 Funcionalidades profesionales")
    st.markdown("Haz clic en cada funcionalidad para conocer más detalles.")

    features = [
        ("🧠", "Guion IA", "Generación automática de guiones",
         "**¿Qué hace?** Genera guiones técnicos completos con IA: hook, escenas con B-roll, CTA y hashtags.\n\n**Importancia:** Un guion estructurado aumenta la retención hasta 80%.\n\n**Capacidades:**\n- Análisis del objetivo\n- B-roll sugerido\n- Hashtags optimizados\n- Descripción lista para publicar"),
        ("🎨", "20 Plantillas Pro", "Diseños categorizados",
         "**¿Qué hace?** 20 plantillas en 15 categorías: Gaming, Belleza, Gastronomía, Noticias, Premium y más.\n\n**Importancia:** Consistencia visual de marca y ahorro de horas de diseño.\n\n**Capacidades:**\n- Preview animado en vivo\n- Guardar plantillas personalizadas\n- Logo en posición configurable\n- Marcar como corporativa"),
        ("🎬", "Edición Pro", "Transiciones y efectos",
         "**¿Qué hace?** 47 transiciones (fade, slide, zoom) y 80 efectos visuales (vintage, glitch, noir).\n\n**Importancia:** La calidad de edición diferencia amateur de profesional.\n\n**Capacidades:**\n- 47 transiciones XFade\n- 80 filtros con intensidad ajustable\n- Color grading cinematográfico\n- Efecto Ken Burns\n- Filtros de audio profesional"),
        ("📝", "Subtítulos Auto", "Transcripción con Whisper",
         "**¿Qué hace?** Transcribe audio con Whisper y quema subtítulos con estilo de la plantilla.\n\n**Importancia:** 85% de videos en redes se ven sin sonido.\n\n**Capacidades:**\n- Detección de idioma\n- Estilo adaptado a plantilla\n- Posición configurable\n- Exportación SRT"),
        ("📱", "Multi-Formato", "YouTube, TikTok, Instagram",
         "**¿Qué hace?** Exporta a 3 formatos simultáneos: 1920×1080, 1080×1920, 1080×1080.\n\n**Importancia:** Maximiza alcance en todas las plataformas.\n\n**Capacidades:**\n- 3 formatos con un clic\n- Calidad 1080p Full HD\n- Descargas independientes\n- Faststart para streaming"),
        ("📅", "Agenda", "Programa publicaciones",
         "**¿Qué hace?** Agenda y programa publicaciones desde un calendario centralizado.\n\n**Importancia:** La consistencia es clave para crecer.\n\n**Capacidades:**\n- Calendario visual\n- Estados: borrador/programada/publicada\n- Multi-plataforma"),
        ("📊", "Análisis", "Mide y mejora tu estrategia",
         "**¿Qué hace?** Analiza efectividad de posteos, lee comentarios, propone nuevas piezas.\n\n**Importancia:** Lo que no se mide, no se mejora.\n\n**Capacidades:**\n- Análisis de efectividad\n- Lectura de comentarios\n- Detección de patrones\n- Propuestas de contenido"),
        ("📱", "Redes Sociales", "SEO y preview de posts",
         "**¿Qué hace?** Genera contenido SEO editable y preview de cómo se verá publicado.\n\n**Importancia:** SEO aumenta descubrimiento orgánico 5x.\n\n**Capacidades:**\n- Caption optimizado\n- Hashtags y keywords\n- Preview visual por plataforma\n- Programar publicación"),
    ]

    # Grid de funcionalidades con desplegables
    for i in range(0, len(features), 4):
        batch = features[i:i+4]
        cols = st.columns(4)
        for j, (icon, title, short, detalle) in enumerate(batch):
            with cols[j]:
                st.markdown(f"""
                <div class="glass-card-feature">
                    <div class="feature-icon">{icon}</div>
                    <div class="feature-title">{title}</div>
                    <div class="feature-desc">{short}</div>
                </div>
                """, unsafe_allow_html=True)
                with st.expander("ℹ️ Detalles", expanded=False):
                    st.markdown(detalle)

    # ============ BOTÓN EMPEZAR A CREAR (sobre Potencia) ============
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Empezar a crear ahora", type="primary", use_container_width=True,
                     key="btn_empezar_crear"):
            if st.session_state.get('usuario'):
                st.session_state.vista = "process"
                st.session_state.wizard_step = 1
            else:
                st.session_state.vista = "auth"
                st.session_state._show_login = True
            st.rerun()

    # Si se solicitó mostrar login
    if st.session_state.get("_show_login") and not st.session_state.get('usuario'):
        st.markdown("---")
        st.markdown("## 🔐 Acceder al sistema")
        render_login_form()

    # ============ POTENCIA DE LA PLATAFORMA (al final, horizontal) ============
    st.markdown("---")
    st.markdown("""
    <style>
    .stats-h { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.8rem; margin: 1rem 0; }
    .stat-h { background: var(--bg-glass); border: 1px solid var(--border-glass);
              border-radius: 12px; padding: 1rem 0.5rem; text-align: center;
              backdrop-filter: blur(20px); transition: all 0.3s; }
    .stat-h:hover { border-color: var(--accent-primary); transform: translateY(-2px); }
    .stat-h-icon { font-size: 1.5rem; margin-bottom: 0.3rem; }
    .stat-h-val { font-size: 1.4rem; font-weight: 800; color: var(--text-primary) !important; }
    .stat-h-lbl { font-size: 0.75rem; color: var(--text-muted) !important; margin-top: 0.3rem;
                  text-transform: uppercase; letter-spacing: 0.05em; }
    </style>
    <div class="stats-h">
        <div class="stat-h"><div class="stat-h-icon">🎬</div><div class="stat-h-val">20</div><div class="stat-h-lbl">Plantillas Pro</div></div>
        <div class="stat-h"><div class="stat-h-icon">⚡</div><div class="stat-h-val">&lt;5min</div><div class="stat-h-lbl">Tiempo promedio</div></div>
        <div class="stat-h"><div class="stat-h-icon">📱</div><div class="stat-h-val">3</div><div class="stat-h-lbl">Formatos simultáneos</div></div>
        <div class="stat-h"><div class="stat-h-icon">🤖</div><div class="stat-h-val">100%</div><div class="stat-h-lbl">Automatizado por IA</div></div>
    </div>
    """, unsafe_allow_html=True)

    # Branding final
    st.markdown("""
    <div style="text-align: center; margin-top: 1.5rem; padding-top: 1rem;
                border-top: 1px solid rgba(99, 102, 241, 0.2);">
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

            # SELECCIÓN DE NARRADOR
            st.markdown("---")
            st.markdown("### 🎙️ Narrador / Voz del video")

            tipo_narrador = st.radio(
                "Selecciona el tipo de narrador:",
                ["IA (voz automática)", "Grabar mi voz", "Sin narrador (solo música)"],
                key="tipo_narrador_sel",
                horizontal=True
            )

            if tipo_narrador == "IA (voz automática)":
                col_voz1, col_voz2 = st.columns(2)
                with col_voz1:
                    voz_idioma = st.selectbox(
                        "🌐 Idioma de la voz",
                        ["Español", "Inglés", "Portugués", "Francés"],
                        key="voz_idioma"
                    )
                with col_voz2:
                    voz_genero = st.selectbox(
                        "👤 Género de voz",
                        ["Femenina", "Masculina", "Neutra"],
                        key="voz_genero"
                    )
                velocidad_voz = st.slider(
                    "⚡ Velocidad de narración",
                    min_value=0.5, max_value=2.0, value=1.0, step=0.1,
                    key="voz_velocidad"
                )
                st.session_state.narrador_config = {
                    "tipo": "ia",
                    "idioma": voz_idioma,
                    "genero": voz_genero,
                    "velocidad": velocidad_voz
                }

            elif tipo_narrador == "Grabar mi voz":
                st.info("🎤 Sube una muestra de tu voz (mínimo 10 segundos) para que la IA la clone de manera natural.")
                archivo_voz = st.file_uploader(
                    "🎵 Sube tu muestra de voz (WAV, MP3)",
                    type=['wav', 'mp3', 'm4a'],
                    key="voz_muestra_upload"
                )
                if archivo_voz:
                    st.success(f"✅ Muestra de voz cargada: {archivo_voz.name}")
                    # Guardar archivo
                    from database import UPLOADS
                    timestamp_voz = datetime.now().strftime("%Y%m%d_%H%M%S")
                    ruta_voz = UPLOADS / f"{timestamp_voz}_voz_{archivo_voz.name}"
                    with open(ruta_voz, 'wb') as f:
                        f.write(archivo_voz.getbuffer())
                    st.session_state.narrador_config = {
                        "tipo": "clonar_voz",
                        "ruta_muestra": str(ruta_voz),
                        "nombre_archivo": archivo_voz.name
                    }
                else:
                    st.session_state.narrador_config = {"tipo": "clonar_voz", "ruta_muestra": None}

            else:  # Sin narrador
                st.info("🎵 El video tendrá solo música de fondo, sin narración.")
                st.session_state.narrador_config = {"tipo": "sin_narrador"}

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
            st.markdown("### ✨ Filtros y efectos")
            st.info("🎯 Selecciona filtros para tu video. Los filtros recomendados están basados en tu plantilla. "
                    "Puedes ajustar la intensidad de cada filtro individualmente.")

            # Obtener categoría de la plantilla para recomendaciones
            categoria_plantilla = ""
            if st.session_state.get('plantilla_elegida'):
                categoria_plantilla = st.session_state.plantilla_elegida.get('categoria', '')

            efectos_sel = render_efectos_selector(categoria_plantilla)
            st.session_state.efectos_seleccionados = efectos_sel

            if efectos_sel:
                # Separar video y audio para mostrar
                efectos_video = [e for e in efectos_sel if e.get("tipo", "video") == "video"]
                efectos_audio = [e for e in efectos_sel if e.get("tipo") == "audio"]

                if efectos_video:
                    st.success(f"🎬 {len(efectos_video)} filtro(s) de video: " +
                               ", ".join([e["nombre"] for e in efectos_video]))
                if efectos_audio:
                    st.info(f"🎵 {len(efectos_audio)} filtro(s) de audio: " +
                            ", ".join([e["nombre"] for e in efectos_audio]))
            else:
                st.warning("⚠ No has seleccionado ningún filtro. El video se producirá sin filtros adicionales.")

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

                # Construir descripción del material real del usuario
                archivos_guardados = st.session_state.get("archivos_guardados", {})
                if archivos_guardados:
                    material_desc = f"Video principal: {archivos_guardados.get('principal_name', 'video.mp4')}"
                    if archivos_guardados.get("videos"):
                        material_desc += f", {len(archivos_guardados['videos'])} video(s) extra de B-roll"
                    if archivos_guardados.get("imagenes"):
                        material_desc += f", {len(archivos_guardados['imagenes'])} imagen(es)"
                    if archivos_guardados.get("audio"):
                        material_desc += ", música/audio de fondo"
                else:
                    material_desc = "Solo video principal disponible"

                # Pasar archivos_extra al generador de guion
                archivos_extra_guion = {
                    "videos": archivos_guardados.get("videos", []),
                    "imagenes": archivos_guardados.get("imagenes", []),
                    "audio": archivos_guardados.get("audio"),
                }

                guion = groq.generar_guion_completo(
                    texto_objetivo, tipo, duracion, material_desc, plantilla_nombre,
                    archivos_extra_guion
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

    # Pasar efectos seleccionados al pipeline (se aplican dentro del proceso)
    efectos_seleccionados = st.session_state.get('efectos_seleccionados', [])

    resultado = procesar_video_completo(
        ruta_video,
        st.session_state.guion,
        plantilla_procesar,
        archivos_extra,
        st.session_state.formatos_seleccionados,
        progress_callback,
        efectos_seleccionados  # NUEVO: se aplican dentro del pipeline
    )

    if "error" not in resultado:
        # Descontar token
        usar_token(st.session_state.usuario["id"])
        st.session_state.usuario = obtener_usuario(st.session_state.usuario["id"])

        # Determinar el video a mostrar: el del primer formato seleccionado
        formatos_seleccionados = st.session_state.formatos_seleccionados
        video_mostrar = resultado["video_final"]  # Por defecto el base

        # Si hay formatos exportados, usar el primero seleccionado
        if resultado.get("formatos"):
            for fmt in formatos_seleccionados:
                if fmt in resultado["formatos"]:
                    video_mostrar = resultado["formatos"][fmt]
                    break

        # Guardar proyecto
        proyecto = {
            "fecha": timestamp,
            "video_original": video_principal_name,
            "video_final": video_mostrar,  # Guardar el formato correcto
            "video_base": resultado["video_final"],  # Guardar también el base
            "subtitulos": resultado["subtitulos"],
            "formatos": resultado["formatos"],
            "transcripcion": resultado["transcripcion"][:500],
            "plantilla_usada": st.session_state.plantilla_elegida["nombre"],
            "tipo_contenido": st.session_state.get("tipo_contenido_sel", ""),
            "formato_principal": formatos_seleccionados[0] if formatos_seleccionados else "youtube",
        }
        agregar_proyecto(st.session_state.usuario["id"], proyecto)
        st.session_state.usuario = obtener_usuario(st.session_state.usuario["id"])

        st.balloons()
        st.markdown(f"""
        <div class="custom-alert custom-alert-success">
            <strong>¡Video producido exitosamente! 🎉</strong>
            <div style="margin-top: 0.5rem;">
                Formato principal: <strong>{formatos_seleccionados[0].upper() if formatos_seleccionados else 'YOUTUBE'}</strong>
                <br>Tu video está listo. Puedes reproducirlo y descargarlo en los formatos seleccionados.
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Mostrar video en el formato seleccionado
        st.video(video_mostrar)

        # Descargas - PRIORIZAR VIDEOS, SRT opcional
        st.markdown("### ⬇ Descargar tu video")
        st.markdown("📥 Descarga tu video en el formato que necesites:")

        # Botones de descarga de video PRIMERO
        video_cols = st.columns(max(len(resultado["formatos"]), 1))
        for i, (nombre_fmt, ruta_fmt) in enumerate(resultado["formatos"].items()):
            with video_cols[i]:
                try:
                    with open(ruta_fmt, 'rb') as f:
                        # Etiqueta más descriptiva según formato
                        fmt_labels = {
                            "youtube": "📺 YouTube (16:9 HD)",
                            "tiktok": "📱 TikTok (9:16 Vertical)",
                            "instagram": "⬜ Instagram (1:1 Cuadrado)"
                        }
                        label = fmt_labels.get(nombre_fmt, f"🎬 {nombre_fmt.upper()}")
                        st.download_button(
                            label,
                            f,
                            file_name=f"{nombre_fmt}_{timestamp}.mp4",
                            mime="video/mp4",
                            use_container_width=True,
                            type="primary"
                        )
                except (FileNotFoundError, IOError):
                    st.error(f"Formato {nombre_fmt} no disponible")

        # SRT como opcional, en expander
        if resultado.get("subtitulos"):
            with st.expander("📝 Descargar subtítulos (opcional)"):
                try:
                    with open(resultado["subtitulos"], 'rb') as f:
                        st.download_button(
                            "📝 Descargar subtítulos SRT",
                            f,
                            file_name=f"subtitulos_{timestamp}.srt",
                            mime="text/plain",
                            help="Archivo de subtítulos para editar o subir por separado"
                        )
                except (FileNotFoundError, IOError):
                    pass

        # Transcripción
        with st.expander("📝 Ver transcripción completa"):
            st.write(resultado["transcripcion"])

        # Reset wizard
        if st.button("🎬 Crear otro video", type="primary"):
            st.session_state.wizard_step = 1
            st.session_state.guion = None
            st.session_state.plantilla_elegida = None
            st.session_state.archivos_guardados = None
            st.session_state.efectos_seleccionados = []
            st.session_state.transicion_personalizada = None
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
    """Página de galería de plantillas."""
    st.markdown("""
    <div class="hero-section">
        <h2 style="color: var(--text-primary) !important;">🎨 Galería de Plantillas</h2>
        <p style="color: var(--text-secondary) !important;">
            12+ plantillas profesionales categorizadas para cada caso de uso.
            Cada plantilla incluye paleta de colores, tipografía, transiciones y configuración optimizada.
        </p>
    </div>
    """, unsafe_allow_html=True)

    selected_id = None
    if st.session_state.plantilla_elegida:
        selected_id = st.session_state.plantilla_elegida.get("id")

    render_template_gallery(selected_id=selected_id)

    if st.session_state.plantilla_elegida:
        st.markdown("---")
        plantilla = st.session_state.plantilla_elegida
        st.markdown(f"""
        <div class="glass-card">
            <h3 style="color: var(--text-primary) !important;">
                📋 Configuración: {plantilla['nombre']}
            </h3>
            <pre style="background: var(--bg-tertiary); padding: 1rem; border-radius: 8px; overflow: auto;">
{json.dumps(plantilla, indent=2, ensure_ascii=False)}
            </pre>
        </div>
        """, unsafe_allow_html=True)

        if st.button("📤 Usar esta plantilla para producir", type="primary"):
            st.session_state.vista = "process"
            st.rerun()


def render_projects_page():
    """Página de proyectos del usuario."""
    usuario = st.session_state.usuario
    proyectos = usuario.get("proyectos", [])

    st.markdown("""
    <div class="hero-section">
        <h2 style="color: var(--text-primary) !important;">📊 Mis Proyectos</h2>
        <p style="color: var(--text-secondary) !important;">
            Gestiona y descarga tus videos producidos.
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
    """Página de generación de ideas con IA."""
    st.markdown("""
    <div class="hero-section">
        <h2 style="color: var(--text-primary) !important;">💡 Generador de Ideas IA</h2>
        <p style="color: var(--text-secondary) !important;">
            ¿Sin inspiración? Deja que la IA genere ideas virales para tu nicho.
        </p>
    </div>
    """, unsafe_allow_html=True)

    config = get_config()
    groq = GroqAI(config.get("groq_api_key", ""),
                  model=config.get("groq_model", "llama-3.1-70b-versatile"))

    if not groq.esta_configurado():
        st.warning("API de Groq no configurada. Contacta al administrador.")
        return

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            nicho = st.text_input("🎯 Tu nicho o industria",
                                    placeholder="Ej: Marketing digital, Fitness, Cocina, Tecnología...")
        with col2:
            publico = st.text_input("👥 Público objetivo",
                                     placeholder="Ej: Jóvenes 18-30, Padres, Emprendedores...")

        cantidad = st.slider("💡 Número de ideas", 3, 15, 8)

    if st.button("✨ Generar Ideas", type="primary", use_container_width=True):
        if not nicho:
            st.warning("Escribe tu nicho para generar ideas")
            return

        with st.spinner("💡 Generando ideas creativas..."):
            resultado = groq.generar_ideas_contenido(nicho, publico, cantidad)

            if "error" in resultado:
                st.error(f"Error: {resultado['error']}")
            elif "ideas" in resultado:
                st.markdown(f"### 🎯 {len(resultado['ideas'])} ideas para tu nicho")

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
                    </div>
                    """, unsafe_allow_html=True)


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

        # Acceso admin discreto en el footer del sidebar
        if not is_admin():
            with st.sidebar.expander("🔐 Acceso administrador", expanded=False):
                admin_pass = st.text_input("Contraseña admin", type="password", key="admin_pass_input")
                if st.button("🔑 Ingresar", type="primary", use_container_width=True):
                    if verify_admin_password(admin_pass):
                        st.session_state.admin_mode = True
                        st.success("✅ Modo admin activado")
                        st.rerun()
                    else:
                        st.error("❌ Contraseña incorrecta")

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
        # La portada ya tiene el botón "Empezar a crear" que muestra login
        render_home_page()


if __name__ == "__main__":
    main()
