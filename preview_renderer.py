"""
Sistema de preview animado para plantillas.
Genera HTML/CSS que simula cómo se verá el video final con la plantilla seleccionada.
Incluye: animación de intro, escenas con transiciones, y outro.
"""

from typing import Dict, Any, Optional


def generar_preview_animado(plantilla: Dict[str, Any],
                              titulo_video: str = "Mi Video",
                              tipo_contenido: str = "Publicitario",
                              duracion_seg: int = 3) -> str:
    """
    Genera HTML animado que simula cómo se verá el video con esta plantilla.
    El preview muestra: intro, escenas y outro con la paleta/tipografía real.

    Args:
        plantilla: Dict con la configuración de la plantilla
        titulo_video: Título del video para mostrar en la animación
        tipo_contenido: Tipo de contenido
        duracion_seg: Duración del video objetivo

    Returns:
        HTML string con animación lista para st.components.v1.html()
    """

    color_primario = plantilla.get("color_primario", "#6366F1")
    color_secundario = plantilla.get("color_secundario", "#1E1B4B")
    color_acento = plantilla.get("color_acento", "#FFFFFF")
    color_texto = plantilla.get("color_texto", "#FFFFFF")
    color_sub = plantilla.get("color_sub", "#E0E7FF")
    fuente = plantilla.get("fuente", "Inter")
    estilo = plantilla.get("estilo", "minimalista")
    transicion = plantilla.get("transicion", "fade")
    preview_texto = plantilla.get("preview_texto", "Tu texto aparecerá aquí")
    config = plantilla.get("config_avanzada", {})
    intro_dur = config.get("intro_duracion", 3)
    outro_dur = config.get("outro_duracion", 3)
    fps = config.get("fps", 30)
    color_grading = config.get("color_grading", "neutro")

    # Determinar gradiente según color_grading
    grading_filter = ""
    if color_grading == "cinematico":
        grading_filter = "sepia(0.15) contrast(1.05) brightness(0.95)"
    elif color_grading == "calido":
        grading_filter = "sepia(0.2) saturate(1.1) brightness(1.05)"
    elif color_grading == "frio":
        grading_filter = "hue-rotate(180deg) saturate(0.9) brightness(0.98)"
    elif color_grading == "vibrante":
        grading_filter = "saturate(1.4) contrast(1.1)"

    # Determinar tipo de transición CSS
    transition_css = _get_transition_css(transicion)

    # ID único para esta animación
    template_id = plantilla.get("id", "preview").replace("-", "_")

    # Total de escenas simuladas (3 escenas representativas)
    escenas_simuladas = [
        {"titulo": "01", "subtitulo": "Introducción", "texto": preview_texto, "duracion": 2},
        {"titulo": "02", "subtitulo": "Desarrollo", "texto": "Contenido principal", "duracion": 2},
        {"titulo": "03", "subtitulo": "Cierre", "texto": "Conclusión + CTA", "duracion": 2},
    ]

    # Construir HTML
    html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Montserrat:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&family=Poppins:wght@400;500;600;700;800&family=Lato:wght@400;700;900&display=swap');

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    background: #0a0e1a;
    font-family: '{fuente}', sans-serif;
    overflow: hidden;
    padding: 20px;
}}

.preview-container {{
    max-width: 720px;
    margin: 0 auto;
    background: #0f172a;
    border-radius: 18px;
    overflow: hidden;
    box-shadow: 0 24px 60px rgba(0,0,0,0.6), 0 0 0 1px rgba(99,102,241,0.2);
}}

.preview-header {{
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    padding: 14px 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(99,102,241,0.2);
}}

.preview-title {{
    color: #f8fafc;
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}}

.preview-badge {{
    background: linear-gradient(135deg, {color_primario}, {color_secundario});
    color: {color_texto};
    padding: 4px 12px;
    border-radius: 100px;
    font-size: 11px;
    font-weight: 600;
}}

.video-frame {{
    position: relative;
    width: 100%;
    aspect-ratio: 16/9;
    background: linear-gradient(135deg, {color_primario} 0%, {color_secundario} 100%);
    overflow: hidden;
    filter: {grading_filter};
}}

.scene {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    opacity: 0;
    animation: sceneAnimation_{template_id} 12s infinite;
    background: linear-gradient(135deg, {color_primario} 0%, {color_secundario} 100%);
}}

/* Escena 1 - INTRO */
.scene:nth-child(1) {{
    animation-delay: 0s;
    background: linear-gradient(135deg, {color_secundario} 0%, {color_primario} 100%);
}}

/* Escena 2 - Desarrollo */
.scene:nth-child(2) {{
    animation-delay: 4s;
    background: linear-gradient(135deg, {color_primario} 0%, {color_acento} 100%);
}}

/* Escena 3 - Cierre */
.scene:nth-child(3) {{
    animation-delay: 8s;
    background: linear-gradient(135deg, {color_acento} 0%, {color_primario} 100%);
}}

@keyframes sceneAnimation_{template_id} {{
    0% {{ opacity: 0; transform: {transition_css['in']}; }}
    5% {{ opacity: 1; transform: {transition_css['show']}; }}
    30% {{ opacity: 1; transform: {transition_css['show']}; }}
    33% {{ opacity: 0; transform: {transition_css['out']}; }}
    100% {{ opacity: 0; transform: {transition_css['out']}; }}
}}

.scene-content {{
    text-align: center;
    padding: 20px;
    z-index: 2;
    color: {color_texto};
}}

.scene-number {{
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.2em;
    color: {color_acento};
    margin-bottom: 8px;
    opacity: 0.9;
    text-transform: uppercase;
}}

.scene-title {{
    font-size: 28px;
    font-weight: 900;
    margin-bottom: 8px;
    text-shadow: 0 4px 12px rgba(0,0,0,0.5);
    line-height: 1.1;
    color: {color_texto};
}}

.scene-subtitle {{
    font-size: 14px;
    opacity: 0.85;
    margin-bottom: 16px;
    color: {color_sub};
}}

.scene-cta {{
    display: inline-block;
    padding: 6px 18px;
    background: {color_acento};
    color: {color_secundario};
    border-radius: 100px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}}

/* Overlay decorativo */
.overlay {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.2);
    z-index: 1;
    pointer-events: none;
}}

/* Animación de elementos dentro de cada escena */
.scene-content > * {{
    animation: fadeInUp_{template_id} 0.8s ease-out;
    animation-fill-mode: both;
}}

.scene-content > *:nth-child(1) {{ animation-delay: 0.2s; }}
.scene-content > *:nth-child(2) {{ animation-delay: 0.4s; }}
.scene-content > *:nth-child(3) {{ animation-delay: 0.6s; }}
.scene-content > *:nth-child(4) {{ animation-delay: 0.8s; }}

@keyframes fadeInUp_{template_id} {{
    from {{
        opacity: 0;
        transform: translateY(20px);
    }}
    to {{
        opacity: 1;
        transform: translateY(0);
    }}
}}

/* Elementos decorativos según estilo */
.deco-circle {{
    position: absolute;
    border-radius: 50%;
    pointer-events: none;
    animation: float 6s ease-in-out infinite;
}}

.deco-circle:nth-child(1) {{
    width: 200px;
    height: 200px;
    background: {color_acento};
    opacity: 0.1;
    top: -50px;
    right: -50px;
}}

.deco-circle:nth-child(2) {{
    width: 150px;
    height: 150px;
    background: {color_primario};
    opacity: 0.15;
    bottom: -30px;
    left: -30px;
    animation-delay: 2s;
}}

@keyframes float {{
    0%, 100% {{ transform: translateY(0) rotate(0deg); }}
    50% {{ transform: translateY(-20px) rotate(180deg); }}
}}

/* Timeline de progreso */
.timeline {{
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 4px;
    background: rgba(0,0,0,0.3);
    z-index: 10;
}}

.timeline-progress {{
    height: 100%;
    background: linear-gradient(90deg, {color_acento}, {color_primario});
    width: 0%;
    animation: timelineProgress 12s linear infinite;
}}

@keyframes timelineProgress {{
    0% {{ width: 0%; }}
    100% {{ width: 100%; }}
}}

/* Info footer */
.info-footer {{
    background: #1e293b;
    padding: 16px 24px;
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    border-top: 1px solid rgba(99,102,241,0.2);
}}

.info-item {{
    text-align: center;
}}

.info-label {{
    font-size: 10px;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-weight: 600;
    margin-bottom: 4px;
}}

.info-value {{
    font-size: 13px;
    color: #f8fafc;
    font-weight: 700;
}}

.info-value.accent {{
    color: {color_acento};
}}

/* Etiqueta de escena activa */
.scene-indicators {{
    position: absolute;
    top: 16px;
    right: 16px;
    display: flex;
    gap: 6px;
    z-index: 10;
}}

.scene-dot {{
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: rgba(255,255,255,0.3);
    animation: dotPulse 12s infinite;
}}

.scene-dot:nth-child(1) {{ animation-delay: 0s; }}
.scene-dot:nth-child(2) {{ animation-delay: 4s; }}
.scene-dot:nth-child(3) {{ animation-delay: 8s; }}

@keyframes dotPulse {{
    0%, 30% {{ background: {color_acento}; transform: scale(1.3); }}
    33%, 100% {{ background: rgba(255,255,255,0.3); transform: scale(1); }}
}}

/* Subtitle preview */
.subtitle-preview {{
    position: absolute;
    bottom: 30px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(0,0,0,0.7);
    color: {color_texto};
    padding: 6px 14px;
    border-radius: 6px;
    font-size: 13px;
    font-weight: 600;
    z-index: 5;
    text-shadow: 0 2px 4px rgba(0,0,0,0.5);
    border: 1px solid {color_acento};
    animation: subtitleFade 12s infinite;
    white-space: nowrap;
}}

@keyframes subtitleFade {{
    0%, 20% {{ opacity: 0; transform: translateX(-50%) translateY(10px); }}
    25%, 75% {{ opacity: 1; transform: translateX(-50%) translateY(0); }}
    80%, 100% {{ opacity: 0; transform: translateX(-50%) translateY(10px); }}
}}
</style>
</head>
<body>
<div class="preview-container">
    <div class="preview-header">
        <div class="preview-title">Preview Animado · {plantilla.get('nombre', 'Plantilla')}</div>
        <div class="preview-badge">● LIVE</div>
    </div>

    <div class="video-frame">
        <!-- Elementos decorativos -->
        <div class="deco-circle"></div>
        <div class="deco-circle"></div>

        <!-- Indicadores de escena -->
        <div class="scene-indicators">
            <div class="scene-dot"></div>
            <div class="scene-dot"></div>
            <div class="scene-dot"></div>
        </div>

        <!-- Escena 1: INTRO -->
        <div class="scene">
            <div class="overlay"></div>
            <div class="scene-content">
                <div class="scene-number">🎬 INTRO · {intro_dur}s</div>
                <div class="scene-title">{titulo_video}</div>
                <div class="scene-subtitle">{tipo_contenido}</div>
                <div class="scene-cta">▶ COMENZAR</div>
            </div>
        </div>

        <!-- Escena 2: DESARROLLO -->
        <div class="scene">
            <div class="overlay"></div>
            <div class="scene-content">
                <div class="scene-number">📍 ESCENA 01 · Desarrollo</div>
                <div class="scene-title">{preview_texto}</div>
                <div class="scene-subtitle">Narración del contenido principal</div>
                <div class="scene-cta">CONTINUAR</div>
            </div>
        </div>

        <!-- Escena 3: CIERRE -->
        <div class="scene">
            <div class="overlay"></div>
            <div class="scene-content">
                <div class="scene-number">🏁 OUTRO · {outro_dur}s</div>
                <div class="scene-title">¡Gracias por ver!</div>
                <div class="scene-subtitle">Suscríbete para más contenido</div>
                <div class="scene-cta">🔔 SUSCRÍBETE</div>
            </div>
        </div>

        <!-- Subtítulo preview -->
        <div class="subtitle-preview">Subtítulos aparecerán aquí</div>

        <!-- Timeline -->
        <div class="timeline">
            <div class="timeline-progress"></div>
        </div>
    </div>

    <div class="info-footer">
        <div class="info-item">
            <div class="info-label">Estilo</div>
            <div class="info-value">{estilo}</div>
        </div>
        <div class="info-item">
            <div class="info-label">Transición</div>
            <div class="info-value accent">{transicion}</div>
        </div>
        <div class="info-item">
            <div class="info-label">Color Grading</div>
            <div class="info-value">{color_grading}</div>
        </div>
        <div class="info-item">
            <div class="info-label">FPS</div>
            <div class="info-value">{fps}</div>
        </div>
    </div>
</div>
</body>
</html>
    """
    return html


def _get_transition_css(transicion: str) -> Dict[str, str]:
    """
    Retorna los CSS transforms para simular cada tipo de transición.
    """
    transitions = {
        "fade": {
            "in": "translateY(0)",
            "show": "translateY(0)",
            "out": "translateY(0)",
        },
        "slide": {
            "in": "translateX(100%)",
            "show": "translateX(0)",
            "out": "translateX(-100%)",
        },
        "slideleft": {
            "in": "translateX(100%)",
            "show": "translateX(0)",
            "out": "translateX(-100%)",
        },
        "slideright": {
            "in": "translateX(-100%)",
            "show": "translateX(0)",
            "out": "translateX(100%)",
        },
        "zoom": {
            "in": "scale(1.5)",
            "show": "scale(1)",
            "out": "scale(0.5)",
        },
        "zoomin": {
            "in": "scale(0.5)",
            "show": "scale(1)",
            "out": "scale(1.5)",
        },
        "wipeleft": {
            "in": "translateX(0) scaleX(0)",
            "show": "translateX(0) scaleX(1)",
            "out": "translateX(-100%) scaleX(1)",
        },
        "wiperight": {
            "in": "translateX(0) scaleX(0)",
            "show": "translateX(0) scaleX(1)",
            "out": "translateX(100%) scaleX(1)",
        },
        "circleopen": {
            "in": "scale(0) rotate(180deg)",
            "show": "scale(1) rotate(0deg)",
            "out": "scale(0) rotate(-180deg)",
        },
        "circleclose": {
            "in": "scale(1.5) rotate(0deg)",
            "show": "scale(1) rotate(0deg)",
            "out": "scale(0) rotate(180deg)",
        },
        "dissolve": {
            "in": "translateY(0) blur(10px)",
            "show": "translateY(0) blur(0)",
            "out": "translateY(0) blur(10px)",
        },
        "hblur": {
            "in": "blur(20px)",
            "show": "blur(0)",
            "out": "blur(20px)",
        },
        "smoothup": {
            "in": "translateY(100%)",
            "show": "translateY(0)",
            "out": "translateY(-100%)",
        },
        "smoothdown": {
            "in": "translateY(-100%)",
            "show": "translateY(0)",
            "out": "translateY(100%)",
        },
        "smoothleft": {
            "in": "translateX(100%)",
            "show": "translateX(0)",
            "out": "translateX(-100%)",
        },
        "smoothright": {
            "in": "translateX(-100%)",
            "show": "translateX(0)",
            "out": "translateX(100%)",
        },
    }
    return transitions.get(transicion, transitions["fade"])


def generar_preview_compacto(plantilla: Dict[str, Any]) -> str:
    """
    Genera un preview compacto (más pequeño) para mostrar en tarjetas.
    Útil cuando se quieren ver múltiples previews en simultáneo.
    """
    color_primario = plantilla.get("color_primario", "#6366F1")
    color_secundario = plantilla.get("color_secundario", "#1E1B4B")
    color_acento = plantilla.get("color_acento", "#FFFFFF")
    color_texto = plantilla.get("color_texto", "#FFFFFF")
    fuente = plantilla.get("fuente", "Inter")
    preview_texto = plantilla.get("preview_texto", "Tu texto aquí")
    nombre = plantilla.get("nombre", "Plantilla")
    template_id = plantilla.get("id", "preview").replace("-", "_")

    return f"""
<!DOCTYPE html>
<html>
<head>
<style>
@import url('https://fonts.googleapis.com/css2?family={fuente.replace(" ", "+")}:wght@400;700;900&display=swap');
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ background:transparent; font-family:'{fuente}',sans-serif; }}
.compact-preview {{
    width: 100%;
    aspect-ratio: 16/9;
    background: linear-gradient(135deg, {color_primario} 0%, {color_secundario} 100%);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    color: {color_texto};
    text-align: center;
    padding: 12px;
    position: relative;
    overflow: hidden;
    animation: compactPulse_{template_id} 4s ease-in-out infinite;
}}
@keyframes compactPulse_{template_id} {{
    0%, 100% {{ transform: scale(1); }}
    50% {{ transform: scale(1.02); }}
}}
.compact-title {{
    font-size: 14px;
    font-weight: 900;
    margin-bottom: 4px;
    text-shadow: 0 2px 8px rgba(0,0,0,0.4);
    animation: titleSlide_{template_id} 4s ease-in-out infinite;
}}
@keyframes titleSlide_{template_id} {{
    0%, 100% {{ opacity: 0.8; transform: translateY(0); }}
    50% {{ opacity: 1; transform: translateY(-3px); }}
}}
.compact-subtitle {{
    font-size: 10px;
    opacity: 0.9;
    background: {color_acento};
    color: {color_secundario};
    padding: 2px 10px;
    border-radius: 100px;
    font-weight: 700;
    display: inline-block;
    margin-top: 6px;
}}
.compact-name {{
    position: absolute;
    bottom: 6px;
    left: 8px;
    font-size: 9px;
    opacity: 0.7;
    color: {color_texto};
    font-weight: 600;
}}
.compact-badge {{
    position: absolute;
    top: 6px;
    right: 6px;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #10B981;
    animation: blink 1.5s infinite;
}}
@keyframes blink {{
    0%, 100% {{ opacity: 1; }}
    50% {{ opacity: 0.3; }}
}}
</style>
</head>
<body>
<div class="compact-preview">
    <div class="compact-badge"></div>
    <div class="compact-title">{preview_texto}</div>
    <div class="compact-subtitle">{nombre}</div>
    <div class="compact-name">{plantilla.get('categoria', '')}</div>
</div>
</body>
</html>
    """
