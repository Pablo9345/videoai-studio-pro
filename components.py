"""
Componentes UI reutilizables para VideoAI Studio Pro.
Incluye: galería de plantillas con vista previa, wizard de pasos,
tarjetas de estadísticas, y componentes decorativos.
"""

import streamlit as st
from styles import (
    render_template_preview_card,
    render_stat_card,
    render_wizard,
    render_scene_card,
    render_pricing_card
)
from templates_data import (
    PLANTILLAS_PROFESIONALES,
    get_plantilla_by_id,
    get_categorias,
    get_plantillas_by_categoria,
    MEMBRESIAS
)


def render_template_gallery(selected_id=None, categorias_filter=None):
    """
    Renderiza la galería completa de plantillas con vista previa.
    Permite filtrar por categoría y seleccionar.
    """
    # Filtro de categorías
    categorias = ["Todas"] + get_categorias()
    cols_filtros = st.columns([2, 1])
    with cols_filtros[0]:
        cat_sel = st.selectbox("🗂 Filtrar por categoría", categorias, key="cat_filter")
    with cols_filtros[1]:
        st.markdown(f"""
        <div style="margin-top: 28px; text-align: right; color: var(--text-muted) !important;">
            📊 {len(PLANTILLAS_PROFESIONALES)} plantillas disponibles
        </div>
        """, unsafe_allow_html=True)

    # Filtrar plantillas
    if cat_sel == "Todas":
        plantillas_a_mostrar = PLANTILLAS_PROFESIONALES
    else:
        plantillas_a_mostrar = get_plantillas_by_categoria(cat_sel)

    # Renderizar grid
    st.markdown('<div class="template-gallery">', unsafe_allow_html=True)

    cols = st.columns(3)
    for i, plantilla in enumerate(plantillas_a_mostrar):
        with cols[i % 3]:
            selected = (selected_id == plantilla["id"])
            st.markdown(
                render_template_preview_card(plantilla, i, selected),
                unsafe_allow_html=True
            )
            # Botón oculto + visible
            btn_label = "✓ Seleccionada" if selected else f"Usar {plantilla['nombre']}"
            if st.button(btn_label, key=f"tpl_btn_{plantilla['id']}",
                         use_container_width=True,
                         type="primary" if selected else "secondary"):
                st.session_state.plantilla_elegida = plantilla
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


def render_processing_animation(message="Procesando..."):
    """Muestra una animación de procesamiento premium."""
    st.markdown(f"""
    <div class="processing-container">
        <div class="spinner-glow"></div>
        <div class="processing-icon">🎬</div>
        <h3 style="color: var(--text-primary) !important;">{message}</h3>
        <p style="color: var(--text-secondary) !important;">
            Esto puede tomar varios minutos según la duración del video
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_stat_grid(stats):
    """
    Renderiza una grilla de estadísticas.
    stats: list of dicts [{icon, value, label}]
    """
    st.markdown('<div class="stats-grid">', unsafe_allow_html=True)
    for stat in stats:
        st.markdown(render_stat_card(stat['icon'], stat['value'], stat['label']),
                    unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def render_guion_visualization(guion):
    """Renderiza el guion generado de forma visual atractiva."""
    if not guion or "error" in guion:
        st.error("No hay guion válido para mostrar")
        return

    # Header del guion
    st.markdown(f"""
    <div class="glass-card" style="border-left: 4px solid var(--accent-primary);">
        <h2 style="color: var(--text-primary) !important; margin-bottom: 0.5rem;">
            🎬 {guion.get('titulo', 'Sin título')}
        </h2>
        {f'<p style="color: var(--accent-warning) !important; font-weight: 600; margin: 0.5rem 0;">🎯 Hook: {guion.get("hook", "")}</p>' if guion.get("hook") else ''}
        <p style="color: var(--text-secondary) !important;">{guion.get('introduccion', '')}</p>
    </div>
    """, unsafe_allow_html=True)

    # Escenas
    if "escenas" in guion:
        st.markdown("### 🎞 Escenas del video")
        for escena in guion["escenas"]:
            st.markdown(
                render_scene_card(
                    escena.get("numero", 0),
                    escena.get("descripcion", "") + (f"\n\n🎙 **Narración:** {escena.get('narracion', '')}" if escena.get("narracion") else ""),
                    escena.get("texto_en_pantalla", ""),
                    escena.get("duracion_seg", 0),
                    escena.get("b_roll_sugerido", "")
                ),
                unsafe_allow_html=True
            )

    # CTA final
    if guion.get("cta_final"):
        st.markdown(f"""
        <div class="custom-alert custom-alert-success">
            <strong>📣 Call to Action Final:</strong>
            <span style="margin-left: 0.5rem;">{guion['cta_final']}</span>
        </div>
        """, unsafe_allow_html=True)

    # Hashtags
    if guion.get("hashtags_sugeridos"):
        hashtags_html = " ".join(guion["hashtags_sugeridos"])
        st.markdown(f"""
        <div class="glass-card">
            <strong style="color: var(--text-primary) !important;">#️⃣ Hashtags sugeridos:</strong><br>
            <span style="color: var(--accent-primary) !important; font-size: 0.9rem;">{hashtags_html}</span>
        </div>
        """, unsafe_allow_html=True)


def render_pricing_section(current_plan="gratis"):
    """Renderiza la sección de planes de precios."""
    featured_plan = "pro"

    cols = st.columns(len(MEMBRESIAS))
    for i, plan in enumerate(MEMBRESIAS):
        with cols[i]:
            featured = (plan["id"] == featured_plan)
            current = (plan["id"] == current_plan)

            st.markdown(render_pricing_card(plan, featured), unsafe_allow_html=True)

            if current:
                st.success("✓ Tu plan actual")
            else:
                btn_label = "💳 Actualizar" if plan["precio"] > 0 else "⬇️ Empezar Gratis"
                if st.button(btn_label, key=f"plan_btn_{plan['id']}",
                             use_container_width=True,
                             type="primary" if featured else "secondary"):
                    if plan["precio"] == 0:
                        cambiar_plan(st.session_state.usuario["id"], plan["id"])
                        st.session_state.usuario = obtener_usuario(st.session_state.usuario["id"])
                        st.success(f"¡Plan cambiado a {plan['nombre']}!")
                        st.rerun()
                    else:
                        st.info(f"Para actualizar a {plan['nombre']}, contacta con soporte o configura tu método de pago.")
                        st.markdown("""
                        <div style="background: var(--bg-glass); padding: 1rem; border-radius: 12px; margin-top: 0.5rem;">
                            <p style="margin: 0; color: var(--text-secondary) !important;">
                                💳 <strong>Pago seguro vía PayPal:</strong><br>
                                <a href="https://www.paypal.com" target="_blank">
                                    Proceder al pago
                                </a>
                            </p>
                        </div>
                        """, unsafe_allow_html=True)


def render_wizard_nav(current_step):
    """Renderiza el wizard de navegación de pasos."""
    steps = [
        "Subir Material",
        "Describir Proyecto",
        "Elegir Plantilla",
        "Formatos",
        "Generar Guion",
        "Producir Video"
    ]
    st.markdown(render_wizard(current_step, steps), unsafe_allow_html=True)


def render_format_selector():
    """Renderiza el selector de formatos de salida con previews visuales."""
    formatos = [
        {"id": "youtube", "nombre": "YouTube", "ratio": "16:9",
         "resolucion": "1920×1080", "icon": "📺", "desc": "Horizontal HD"},
        {"id": "tiktok", "nombre": "TikTok / Reels", "ratio": "9:16",
         "resolucion": "1080×1920", "icon": "📱", "desc": "Vertical para móvil"},
        {"id": "instagram", "nombre": "Instagram Feed", "ratio": "1:1",
         "resolucion": "1080×1080", "icon": "⬜", "desc": "Cuadrado perfecto"},
    ]

    seleccionados = []
    cols = st.columns(len(formatos))

    for i, fmt in enumerate(formatos):
        with cols[i]:
            key = f"fmt_{fmt['id']}"
            checked = st.checkbox(fmt['nombre'], value=(fmt['id'] == 'youtube'),
                                  key=key)
            if checked:
                seleccionados.append(fmt['id'])

            st.markdown(f"""
            <div class="glass-card-feature" style="margin-top: 0.5rem; min-height: 130px;">
                <div class="feature-icon">{fmt['icon']}</div>
                <div class="feature-title">{fmt['ratio']}</div>
                <div class="feature-desc">{fmt['resolucion']}<br>{fmt['desc']}</div>
            </div>
            """, unsafe_allow_html=True)

    return seleccionados


def render_upload_zone():
    """Renderiza las zonas de subida de archivos."""
    st.markdown("""
    <div class="glass-card">
        <h3 style="color: var(--text-primary) !important; margin-bottom: 0.5rem;">
            📁 Sube tu material
        </h3>
        <p style="color: var(--text-secondary) !important; margin-bottom: 1rem;">
            Sube el video principal y, opcionalmente, material complementario.
            El sistema procesará todo automáticamente.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="custom-alert custom-alert-info">
            <strong>🎬 Video Principal</strong>
            <div style="margin-top: 0.3rem;">El video base con tu narración o contenido</div>
        </div>
        """, unsafe_allow_html=True)
        video_principal = st.file_uploader(
            "Video principal (MP4, MOV, AVI, MKV)",
            type=['mp4', 'mov', 'avi', 'mkv'],
            key="video_main"
        )

        st.markdown("""
        <div class="custom-alert custom-alert-info" style="margin-top: 1rem;">
            <strong>🎵 Música/Audio</strong>
            <div style="margin-top: 0.3rem;">Banda sonora de fondo (opcional)</div>
        </div>
        """, unsafe_allow_html=True)
        audio_musica = st.file_uploader(
            "Música o audio (MP3, WAV)",
            type=['mp3', 'wav'],
            key="audio_extra"
        )

    with col2:
        st.markdown("""
        <div class="custom-alert custom-alert-info">
            <strong>🎥 Videos Extra (B-roll)</strong>
            <div style="margin-top: 0.3rem;">Material adicional para intercalar</div>
        </div>
        """, unsafe_allow_html=True)
        videos_extra = st.file_uploader(
            "Videos adicionales B-roll",
            type=['mp4', 'mov', 'avi', 'mkv'],
            accept_multiple_files=True,
            key="videos_extra"
        )

        st.markdown("""
        <div class="custom-alert custom-alert-info" style="margin-top: 1rem;">
            <strong>🖼 Imágenes</strong>
            <div style="margin-top: 0.3rem;">Fotos o gráficos para insertar</div>
        </div>
        """, unsafe_allow_html=True)
        imagenes = st.file_uploader(
            "Imágenes de apoyo (PNG, JPG, WEBP)",
            type=['png', 'jpg', 'jpeg', 'webp'],
            accept_multiple_files=True,
            key="imgs_extra"
        )

    return video_principal, videos_extra, imagenes, audio_musica


def render_project_card(proyecto, index):
    """Renderiza una tarjeta de proyecto en la lista."""
    from datetime import datetime

    try:
        fecha = datetime.fromisoformat(proyecto.get('fecha', '')).strftime("%d/%m/%Y %H:%M")
    except (ValueError, TypeError):
        # Si es string de timestamp como "20240101_120000"
        fecha = proyecto.get('fecha', 'Fecha desconocida')

    with st.expander(f"🎬 {proyecto.get('video_original', 'Proyecto')} · {fecha}", expanded=(index == 0)):
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown(f"""
            <div class="glass-card">
                <p style="color: var(--text-secondary) !important; margin-bottom: 0.5rem;">
                    <strong style="color: var(--text-primary) !important;">📁 Archivo original:</strong>
                    {proyecto.get('video_original', 'N/A')}
                </p>
                {f'<p style="color: var(--text-secondary) !important; margin-bottom: 0.5rem;"><strong style="color: var(--text-primary) !important;">📝 Transcripción:</strong> {proyecto.get("transcripcion", "")[:200]}...</p>' if proyecto.get('transcripcion') else ''}
            </div>
            """, unsafe_allow_html=True)

            if proyecto.get("video_final") and st.session_state.get(f"show_video_{index}"):
                st.video(proyecto["video_final"])

        with col2:
            if st.button("▶ Ver", key=f"view_{index}", use_container_width=True):
                st.session_state[f"show_video_{index}"] = not st.session_state.get(f"show_video_{index}", False)
                st.rerun()

            if proyecto.get("formatos"):
                for fmt_name, fmt_path in proyecto["formatos"].items():
                    try:
                        with open(fmt_path, 'rb') as f:
                            st.download_button(
                                f"⬇ {fmt_name.upper()}",
                                f,
                                file_name=f"{fmt_name}_{proyecto.get('fecha', 'video')}.mp4",
                                mime="video/mp4",
                                key=f"dl_{index}_{fmt_name}",
                                use_container_width=True
                            )
                    except (FileNotFoundError, IOError):
                        st.caption(f"⚠ {fmt_name} no disponible")

            if proyecto.get("subtitulos"):
                try:
                    with open(proyecto["subtitulos"], 'rb') as f:
                        st.download_button(
                            "📝 Descargar SRT",
                            f,
                            file_name=f"subtitulos_{proyecto.get('fecha', 'subs')}.srt",
                            key=f"dl_sub_{index}",
                            use_container_width=True
                        )
                except (FileNotFoundError, IOError):
                    pass
