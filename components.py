"""
Componentes UI reutilizables para VideoAI Studio Pro.
Incluye: galería de plantillas con vista previa, wizard de pasos,
tarjetas de estadísticas, y componentes decorativos.
"""

from typing import Dict, Any, List, Optional
import streamlit as st
import streamlit.components.v1 as components
from styles import (
    render_template_preview_card,
    render_stat_card,
    render_wizard,
    render_scene_card,
    render_pricing_card,
    html_safe
)
from templates_data import (
    PLANTILLAS_PROFESIONALES,
    get_plantilla_by_id,
    get_categorias,
    get_plantillas_by_categoria,
    TRANSICIONES_DISPONIBLES,
    EFECTOS_DISPONIBLES,
    get_efectos_by_categoria,
    get_categorias_efectos,
    MEMBRESIAS
)
from preview_renderer import generar_preview_animado, generar_preview_compacto


def render_template_gallery(selected_id=None, categorias_filter=None):
    """
    Renderiza la galería completa de plantillas con vista previa INLINE.
    - El preview se muestra en el MISMO recuadro (expandible)
    - Botón para abrir popup con animación completa
    - Se puede cerrar el popup
    """
    # Header con instrucciones
    st.markdown("""
    <div style="background: var(--bg-glass); border: 1px solid var(--border-glass);
                border-radius: 12px; padding: 1rem; margin-bottom: 1rem;">
        <p style="margin: 0; color: var(--text-secondary) !important; font-size: 0.9rem;">
            👆 <strong>Haz clic en "📋 Seleccionar" para elegir una plantilla</strong> ·
            Usa <strong>"▶ Preview"</strong> para ver la animación en el mismo recuadro
        </p>
    </div>
    """, unsafe_allow_html=True)

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

    # Renderizar grid - cada plantilla con su preview INLINE
    cols = st.columns(3)
    for i, plantilla in enumerate(plantillas_a_mostrar):
        with cols[i % 3]:
            selected = (selected_id == plantilla["id"])
            plantilla_id = plantilla["id"]

            # Tarjeta visual de la plantilla
            html_card = render_template_preview_card(plantilla, i, selected)
            st.markdown(html_safe(html_card), unsafe_allow_html=True)

            # Botón SELECCIONAR (siempre activo)
            btn_label = "✓ SELECCIONADA" if selected else "📋 Seleccionar"
            if st.button(btn_label, key=f"tpl_btn_{plantilla_id}",
                         use_container_width=True,
                         type="primary" if selected else "secondary"):
                st.session_state.plantilla_elegida = plantilla
                st.rerun()

            # Botón PREVIEW INLINE (toggle)
            preview_expandido = st.session_state.get(f"preview_inline_{plantilla_id}", False)
            btn_preview_label = "▼ Ocultar Preview" if preview_expandido else "▶ Preview"
            if st.button(btn_preview_label, key=f"tpl_prev_{plantilla_id}",
                         use_container_width=True,
                         help="Ver animación de la plantilla aquí mismo"):
                st.session_state[f"preview_inline_{plantilla_id}"] = not preview_expandido
                st.rerun()

            # Mostrar preview INLINE si está expandido
            if preview_expandido:
                with st.container(border=True):
                    # Preview visual simple con CSS inline (sin dependencias externas)
                    color_p = plantilla.get("color_primario", "#6366F1")
                    color_s = plantilla.get("color_secundario", "#1E1B4B")
                    color_a = plantilla.get("color_acento", "#FFFFFF")
                    color_t = plantilla.get("color_texto", "#FFFFFF")
                    preview_texto = plantilla.get("preview_texto", "Tu texto aquí")
                    nombre = plantilla.get("nombre", "Plantilla")
                    estilo = plantilla.get("estilo", "")
                    transicion = plantilla.get("transicion", "fade")

                    # HTML del preview con animación CSS simple
                    preview_html = f"""
                    <div style="width:100%; aspect-ratio:16/9;
                                background: linear-gradient(135deg, {color_p} 0%, {color_s} 100%);
                                border-radius:10px; display:flex; align-items:center;
                                justify-content:center; flex-direction:column;
                                color:{color_t}; text-align:center; padding:12px;
                                position:relative; overflow:hidden;">
                        <div style="position:absolute; top:8px; right:8px;
                                    background:{color_a}33; color:{color_t};
                                    padding:2px 8px; border-radius:10px; font-size:9px;
                                    border:1px solid {color_a}80;">● LIVE</div>
                        <div style="font-size:18px; font-weight:900;
                                    text-shadow:0 2px 8px rgba(0,0,0,0.5);
                                    margin-bottom:6px;">{preview_texto}</div>
                        <div style="background:{color_a}; color:{color_s};
                                    padding:3px 10px; border-radius:10px;
                                    font-size:10px; font-weight:700;">▶ {nombre}</div>
                        <div style="position:absolute; bottom:6px; left:8px;
                                    font-size:9px; opacity:0.7;">{estilo} · {transicion}</div>
                    </div>
                    """
                    st.markdown(preview_html, unsafe_allow_html=True)

                    # Información rápida de la plantilla
                    st.caption(f"🎨 Colores: {color_p} / {color_s} / {color_a}")

                    # Botón para abrir popup con preview completo
                    if st.button("🍿 Ver Preview Animado Completo", key=f"popup_{plantilla_id}",
                                 use_container_width=True):
                        st.session_state.preview_plantilla_id = plantilla_id
                        st.rerun()

    # Mostrar modal de popup si se solicitó
    if "preview_plantilla_id" in st.session_state and st.session_state.preview_plantilla_id:
        plantilla_preview = get_plantilla_by_id(st.session_state.preview_plantilla_id)
        if plantilla_preview:
            render_preview_modal(plantilla_preview)


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
        html = render_stat_card(stat['icon'], stat['value'], stat['label'])
        st.markdown(html_safe(html), unsafe_allow_html=True)
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
            html = render_scene_card(
                escena.get("numero", 0),
                escena.get("descripcion", "") + (f"\n\n🎙 **Narración:** {escena.get('narracion', '')}" if escena.get("narracion") else ""),
                escena.get("texto_en_pantalla", ""),
                escena.get("duracion_seg", 0),
                escena.get("b_roll_sugerido", "")
            )
            st.markdown(html_safe(html), unsafe_allow_html=True)

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

            st.markdown(html_safe(render_pricing_card(plan, featured)), unsafe_allow_html=True)

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
    html = render_wizard(current_step, steps)
    # Usar html_safe para asegurar que el HTML se renderice correctamente
    st.markdown(html_safe(html), unsafe_allow_html=True)


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


# ============ MODAL DE PREVIEW ANIMADO ============
def render_preview_modal(plantilla: Dict[str, Any]):
    """Renderiza un modal con preview animado de la plantilla seleccionada."""
    from styles import html_safe

    plantilla_nombre = plantilla.get("nombre", "Plantilla")
    plantilla_id = plantilla.get("id", "unknown")

    # Container estilo modal
    st.markdown(f"""
    <div style="position: fixed; top: 0; left: 0; right: 0; bottom: 0;
                background: rgba(0,0,0,0.85); z-index: 9999;
                display: flex; align-items: center; justify-content: center;
                padding: 2rem; backdrop-filter: blur(8px);">
        <div style="background: var(--bg-secondary); border-radius: 18px;
                    max-width: 800px; width: 100%; max-height: 90vh; overflow-y: auto;
                    border: 1px solid var(--border-glass); box-shadow: 0 24px 60px rgba(0,0,0,0.5);">
            <div style="padding: 1rem 1.5rem; border-bottom: 1px solid var(--border-glass);
                        display: flex; justify-content: space-between; align-items: center;
                        background: var(--bg-glass); border-radius: 18px 18px 0 0;">
                <h3 style="color: var(--text-primary) !important; margin: 0;">
                    🎬 Preview: {plantilla_nombre}
                </h3>
            </div>
            <div style="padding: 1rem;">
                <p style="color: var(--text-secondary) !important; margin-bottom: 1rem;">
                    Esta es una simulación animada de cómo se verá tu video con la plantilla seleccionada.
                    Incluye intro, escenas y outro con la paleta y tipografía real.
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Formulario para personalizar el preview
    st.markdown("### 🎨 Personaliza tu preview")
    col1, col2 = st.columns(2)
    with col1:
        titulo_preview = st.text_input("Título del video",
                                       value="Mi Video Increíble",
                                       key=f"prev_title_{plantilla_id}")
        tipo_preview = st.selectbox("Tipo de contenido",
                                    ["Publicitario", "Institucional", "Educativo",
                                     "Entretenimiento", "Tutorial", "Vlog"],
                                    key=f"prev_tipo_{plantilla_id}")
    with col2:
        duracion_preview = st.slider("Duración objetivo (min)", 1, 10, 2,
                                     key=f"prev_dur_{plantilla_id}")

    # Preview animado en vivo
    st.markdown("### ▶ Preview en vivo")
    try:
        html_preview = generar_preview_animado(
            plantilla, titulo_preview, tipo_preview, duracion_preview
        )
        # Usar components.html para renderizar HTML completo con animaciones
        components.html(html_preview, height=500, scrolling=True)
    except Exception as e:
        st.warning(f"El preview animado no pudo cargarse. Mostrando vista estática.")
        # Fallback: preview estático simple
        color_p = plantilla.get("color_primario", "#6366F1")
        color_s = plantilla.get("color_secundario", "#1E1B4B")
        color_a = plantilla.get("color_acento", "#FFFFFF")
        color_t = plantilla.get("color_texto", "#FFFFFF")
        st.markdown(f"""
        <div style="width:100%; aspect-ratio:16/9;
                    background: linear-gradient(135deg, {color_p} 0%, {color_s} 100%);
                    border-radius:12px; display:flex; align-items:center;
                    justify-content:center; flex-direction:column;
                    color:{color_t}; text-align:center; padding:20px;">
            <div style="font-size:28px; font-weight:900; margin-bottom:8px;">{titulo_preview}</div>
            <div style="font-size:14px; opacity:0.9; margin-bottom:12px;">{tipo_preview}</div>
            <div style="background:{color_a}; color:{color_s}; padding:6px 16px;
                        border-radius:20px; font-size:12px; font-weight:700;">▶ COMENZAR</div>
        </div>
        """, unsafe_allow_html=True)

    # Información detallada de la plantilla
    st.markdown("### 📋 Detalles de la plantilla")
    detalles_col1, detalles_col2 = st.columns(2)

    with detalles_col1:
        st.markdown(f"""
        **Nombre:** {plantilla.get('nombre', 'N/A')}  
        **Categoría:** {plantilla.get('categoria', 'N/A')}  
        **Estilo:** {plantilla.get('estilo', 'N/A')}  
        **Transición:** {plantilla.get('transicion', 'N/A')}  
        **Duración transición:** {plantilla.get('duracion_transicion', 0.5)}s  
        **Fuente:** {plantilla.get('fuente', 'N/A')}
        """)

    with detalles_col2:
        config = plantilla.get('config_avanzada', {})
        st.markdown(f"""
        **Color grading:** {config.get('color_grading', 'N/A')}  
        **FPS:** {config.get('fps', 30)}  
        **Duración intro:** {config.get('intro_duracion', 3)}s  
        **Duración outro:** {config.get('outro_duracion', 3)}s  
        **Subtítulo tamaño:** {config.get('subtitulo_tamano', 22)}px  
        **Posición subtítulo:** {config.get('subtitulo_posicion', 'bottom')}
        """)

    # Paleta de colores
    st.markdown("### 🎨 Paleta de colores")
    paleta_cols = st.columns(4)
    paleta = [
        ("Primario", plantilla.get('color_primario', '#000')),
        ("Secundario", plantilla.get('color_secundario', '#000')),
        ("Acento", plantilla.get('color_acento', '#FFF')),
        ("Texto", plantilla.get('color_texto', '#FFF')),
    ]
    for i, (nombre, color) in enumerate(paleta):
        with paleta_cols[i]:
            st.markdown(f"""
            <div style="background: {color}; padding: 20px; border-radius: 10px;
                        text-align: center; color: {'#000' if color in ['#FFFFFF', '#FBCFE8'] else '#FFF'};
                        font-weight: 700; border: 2px solid var(--border-glass);">
                <div style="font-size: 0.85rem; opacity: 0.8;">{nombre}</div>
                <div style="font-size: 0.9rem;">{color}</div>
            </div>
            """, unsafe_allow_html=True)

    # Acciones
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("✖ Cerrar", key=f"close_prev_{plantilla_id}", use_container_width=True):
            del st.session_state.preview_plantilla_id
            st.rerun()
    with col2:
        ya_seleccionada = st.session_state.get('plantilla_elegida', {}).get('id') == plantilla_id
        if ya_seleccionada:
            st.success("✓ Esta plantilla ya está seleccionada")
        else:
            if st.button(f"✓ Usar esta plantilla", type="primary",
                         key=f"use_prev_{plantilla_id}", use_container_width=True):
                st.session_state.plantilla_elegida = plantilla
                del st.session_state.preview_plantilla_id
                st.success(f"✅ Plantilla '{plantilla_nombre}' seleccionada!")
                st.rerun()
    with col3:
        # Espacio para equilibrio
        st.write("")


# ============ SELECTOR DE TRANSICIONES ============
def render_transiciones_selector(transicion_default: str = "fade") -> Dict[str, Any]:
    """
    Renderiza un selector de transiciones con preview.
    Retorna dict con 'id' y 'duracion' seleccionadas.
    """
    st.markdown("### 🎞 Selecciona la transición")

    # Filtrar por categoría rápida
    categorias_trans = ["Todas", "Suaves", "Deslizantes", "Circulares", "Zoom", "Profesionales"]

    # Mapping de transiciones a categorías visuales
    transiciones_categorias = {
        "Suaves": ["fade", "fadeblack", "fadewhite", "dissolve", "fadegrays"],
        "Deslizantes": ["slideleft", "slideright", "slideup", "slidedown",
                        "smoothleft", "smoothright", "smoothup", "smoothdown",
                        "wipeleft", "wiperight", "wipeup", "wipedown",
                        "wipetl", "wipetr", "wipebl", "wipebr"],
        "Circulares": ["circlecrop", "circleopen", "circleclose", "radial", "squircles"],
        "Zoom": ["zoom", "zoomin"],
        "Profesionales": ["hblur", "pixellize", "horzopen", "horzclose",
                          "vertopen", "vertclose", "h_cut", "v_cut",
                          "smpte101", "smpte102"],
    }

    cat_sel = st.selectbox("📂 Categoría", categorias_trans, key="trans_cat_sel")

    if cat_sel == "Todas":
        trans_a_mostrar = TRANSICIONES_DISPONIBLES
    else:
        ids_categoria = transiciones_categorias.get(cat_sel, [])
        trans_a_mostrar = [t for t in TRANSICIONES_DISPONIBLES if t["id"] in ids_categoria]

    # Grid de transiciones (5 por fila)
    cols = st.columns(5)
    seleccion = transicion_default

    for i, trans in enumerate(trans_a_mostrar[:20]):  # Mostrar hasta 20
        with cols[i % 5]:
            is_selected = trans["id"] == transicion_default
            label = trans["nombre"]
            if st.button(label, key=f"trans_btn_{trans['id']}",
                         use_container_width=True,
                         type="primary" if is_selected else "secondary"):
                seleccion = trans["id"]
                st.session_state.transicion_personalizada = trans["id"]

    # Duración personalizada
    dur_sel = st.slider("⏱ Duración de transición (segundos)",
                        min_value=0.1, max_value=2.0, value=0.5, step=0.1,
                        key="trans_dur_sel")

    return {
        "id": st.session_state.get("transicion_personalizada", transicion_default),
        "duracion": dur_sel,
    }


# ============ SELECTOR DE EFECTOS ============
def render_efectos_selector(categoria_plantilla: str = "") -> List[Dict[str, Any]]:
    """
    Renderiza un selector de filtros con multi-selección.
    Separa filtros de video y audio, y muestra recomendados según la plantilla.
    Retorna lista de efectos seleccionados con su intensidad.
    """
    # Tabs: Recomendados / Video / Audio / Todos
    tab_recom, tab_video, tab_audio, tab_todos = st.tabs([
        "⭐ Recomendados", "🎬 Filtros Video", "🎵 Filtros Audio", "📋 Todos"
    ])

    seleccionados = []

    with tab_recom:
        st.markdown("### ⭐ Filtros recomendados para tu plantilla")
        if categoria_plantilla:
            from templates_data import get_filtros_recomendados
            recomendados = get_filtros_recomendados(categoria_plantilla)
            if recomendados:
                st.info(f"Basado en la categoría **{categoria_plantilla}**, estos son los filtros más adecuados:")
                cols = st.columns(3)
                for i, efecto in enumerate(recomendados):
                    with cols[i % 3]:
                        key = f"recom_chk_{efecto['id']}"
                        checked = st.checkbox(
                            f"{efecto['nombre']}",
                            value=False,
                            key=key,
                            help=efecto.get("descripcion", "")
                        )
                        if checked:
                            intensidad = st.slider(
                                "Intensidad", 0.1, 1.0,
                                efecto.get("intensidad_default", 0.5), 0.1,
                                key=f"recom_int_{efecto['id']}"
                            )
                            seleccionados.append({
                                "id": efecto["id"],
                                "nombre": efecto["nombre"],
                                "intensidad": intensidad,
                                "tipo": efecto.get("tipo", "video")
                            })
            else:
                st.info("No hay filtros recomendados específicos para esta categoría.")
        else:
            st.warning("Selecciona una plantilla primero para ver filtros recomendados.")

    with tab_video:
        st.markdown("### 🎬 Filtros de video")
        cats_efectos = get_categorias_efectos()
        # Excluir categoría 'audio' del selector de video
        cats_video = [c for c in cats_efectos if c != "audio"]
        cat_sel = st.selectbox("📂 Categoría", ["Todas"] + cats_video, key="efecto_video_cat")

        if cat_sel == "Todas":
            efectos_video = [e for e in EFECTOS_DISPONIBLES if e.get("categoria") != "audio" and e["id"] != "ninguno"]
        else:
            efectos_video = [e for e in EFECTOS_DISPONIBLES if e.get("categoria") == cat_sel and e["id"] != "ninguno"]

        cols = st.columns(4)
        for i, efecto in enumerate(efectos_video):
            with cols[i % 4]:
                key = f"vchk_{efecto['id']}"
                checked = st.checkbox(
                    f"{efecto['nombre']}",
                    value=False,
                    key=key,
                    help=efecto.get("descripcion", "")
                )
                if checked:
                    intensidad = st.slider(
                        "Intensidad", 0.1, 1.0,
                        efecto.get("intensidad_default", 0.5), 0.1,
                        key=f"vint_{efecto['id']}"
                    )
                    seleccionados.append({
                        "id": efecto["id"],
                        "nombre": efecto["nombre"],
                        "intensidad": intensidad,
                        "tipo": "video"
                    })

    with tab_audio:
        st.markdown("### 🎵 Filtros de audio")
        st.info("Mejora la calidad del audio: normalización, compresión, reducción de ruido y más.")

        efectos_audio = [e for e in EFECTOS_DISPONIBLES if e.get("tipo") == "audio"]
        cols = st.columns(3)
        for i, efecto in enumerate(efectos_audio):
            with cols[i % 3]:
                key = f"achk_{efecto['id']}"
                checked = st.checkbox(
                    f"{efecto['nombre']}",
                    value=False,
                    key=key,
                    help=efecto.get("descripcion", "")
                )
                if checked:
                    intensidad = st.slider(
                        "Intensidad", 0.1, 1.0,
                        efecto.get("intensidad_default", 0.5), 0.1,
                        key=f"aint_{efecto['id']}"
                    )
                    seleccionados.append({
                        "id": efecto["id"],
                        "nombre": efecto["nombre"],
                        "intensidad": intensidad,
                        "tipo": "audio"
                    })

    with tab_todos:
        st.markdown("### 📋 Todos los filtros disponibles")
        cat_sel_all = st.selectbox("📂 Categoría", ["Todas"] + get_categorias_efectos(), key="efecto_all_cat")

        if cat_sel_all == "Todas":
            efectos_all = EFECTOS_DISPONIBLES
        else:
            efectos_all = get_efectos_by_categoria(cat_sel_all)

        cols = st.columns(4)
        for i, efecto in enumerate(efectos_all):
            with cols[i % 4]:
                if efecto["id"] == "ninguno":
                    continue
                key = f"allchk_{efecto['id']}"
                checked = st.checkbox(
                    f"{efecto['nombre']}",
                    value=False,
                    key=key,
                    help=efecto.get("descripcion", "")
                )
                if checked:
                    intensidad = st.slider(
                        "Intensidad", 0.1, 1.0,
                        efecto.get("intensidad_default", 0.5), 0.1,
                        key=f"allint_{efecto['id']}"
                    )
                    seleccionados.append({
                        "id": efecto["id"],
                        "nombre": efecto["nombre"],
                        "intensidad": intensidad,
                        "tipo": efecto.get("tipo", "video")
                    })

    # Eliminar duplicados (si se seleccionó el mismo filtro en diferentes tabs)
    seen = set()
    unique = []
    for s in seleccionados:
        if s["id"] not in seen:
            seen.add(s["id"])
            unique.append(s)

    return unique
