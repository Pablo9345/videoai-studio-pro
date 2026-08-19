"""
Catálogo de plantillas profesionales para VideoAI Studio Pro.
12 plantillas categorizadas con paletas, tipografías y configuraciones
de edición optimizadas para cada caso de uso.
"""

PLANTILLAS_PROFESIONALES = [
    # ============ MODERNO / TECH ============
    {
        "id": "moderno-tech",
        "nombre": "Modern Tech",
        "categoria": "Tecnología",
        "color_primario": "#6366F1",
        "color_secundario": "#1E1B4B",
        "color_acento": "#06B6D4",
        "color_texto": "#FFFFFF",
        "color_sub": "#E0E7FF",
        "fuente": "Inter",
        "fuente_secundaria": "JetBrains Mono",
        "estilo": "minimalista-tech",
        "transicion": "fade",
        "duracion_transicion": 0.4,
        "descripcion": "Limpio, tecnológico y minimalista. Ideal para tutoriales, demo de software, productos SaaS y contenido tech.",
        "preview_texto": "Tu tutorial tech se verá increíble",
        "config_avanzada": {
            "intro_duracion": 4,
            "outro_duracion": 3,
            "subtitulo_tamano": 22,
            "subtitulo_posicion": "bottom",
            "subtitulo_estilo": "outline",
            "overlay_opacidad": 0.3,
            "musica_volumen": 0.15,
            "voz_volumen": 1.0,
            "color_grading": "neutro",
            "fps": 30,
        }
    },
    {
        "id": "startup-pitch",
        "nombre": "Startup Pitch",
        "categoria": "Tecnología",
        "color_primario": "#0EA5E9",
        "color_secundario": "#0F172A",
        "color_acento": "#FACC15",
        "color_texto": "#FFFFFF",
        "color_sub": "#F1F5F9",
        "fuente": "Montserrat",
        "fuente_secundaria": "Inter",
        "estilo": "dinamico-empresarial",
        "transicion": "slide",
        "duracion_transicion": 0.3,
        "descripcion": "Dinámico y persuasivo. Perfecto para pitch de startups, demo de productos y contenido B2B.",
        "preview_texto": "Eleva tu startup al siguiente nivel",
        "config_avanzada": {
            "intro_duracion": 3,
            "outro_duracion": 2,
            "subtitulo_tamano": 24,
            "subtitulo_posicion": "bottom",
            "subtitulo_estilo": "bold-outline",
            "overlay_opacidad": 0.2,
            "musica_volumen": 0.18,
            "voz_volumen": 1.0,
            "color_grading": "calido",
            "fps": 30,
        }
    },

    # ============ CORPORATIVO / NEGOCIOS ============
    {
        "id": "corporativo-pro",
        "nombre": "Corporate Pro",
        "categoria": "Corporativo",
        "color_primario": "#0F172A",
        "color_secundario": "#1E293B",
        "color_acento": "#F59E0B",
        "color_texto": "#FFFFFF",
        "color_sub": "#FCD34D",
        "fuente": "Montserrat",
        "fuente_secundaria": "Inter",
        "estilo": "elegante-formal",
        "transicion": "fade",
        "duracion_transicion": 0.5,
        "descripcion": "Sobrio y elegante. Para presentaciones ejecutivas, informes corporativos y contenido institucional.",
        "preview_texto": "Excelencia corporativa en cada detalle",
        "config_avanzada": {
            "intro_duracion": 5,
            "outro_duracion": 4,
            "subtitulo_tamano": 20,
            "subtitulo_posicion": "bottom",
            "subtitulo_estilo": "outline",
            "overlay_opacidad": 0.4,
            "musica_volumen": 0.12,
            "voz_volumen": 1.0,
            "color_grading": "calido",
            "fps": 30,
        }
    },
    {
        "id": "institucional-classic",
        "nombre": "Institucional Classic",
        "categoria": "Corporativo",
        "color_primario": "#0369A1",
        "color_secundario": "#0C4A6E",
        "color_acento": "#B45309",
        "color_texto": "#FFFFFF",
        "color_sub": "#FED7AA",
        "fuente": "Lato",
        "fuente_secundaria": "Open Sans",
        "estilo": "formal-tradicional",
        "transicion": "fade",
        "duracion_transicion": 0.6,
        "descripcion": "Tradicional y confiable. Ideal para organismos oficiales, ONGs, educación formal y contenido institucional.",
        "preview_texto": "Compromiso con la sociedad",
        "config_avanzada": {
            "intro_duracion": 5,
            "outro_duracion": 4,
            "subtitulo_tamano": 22,
            "subtitulo_posicion": "bottom",
            "subtitulo_estilo": "outline",
            "overlay_opacidad": 0.35,
            "musica_volumen": 0.10,
            "voz_volumen": 1.0,
            "color_grading": "neutro",
            "fps": 30,
        }
    },

    # ============ MARKETING / PUBLICIDAD ============
    {
        "id": "publicitario-impact",
        "nombre": "Ad Impact",
        "categoria": "Marketing",
        "color_primario": "#EF4444",
        "color_secundario": "#7F1D1D",
        "color_acento": "#FACC15",
        "color_texto": "#FFFFFF",
        "color_sub": "#FEF3C7",
        "fuente": "Poppins",
        "fuente_secundaria": "Inter",
        "estilo": "impactante-atrevido",
        "transicion": "zoom",
        "duracion_transicion": 0.25,
        "descripcion": "Atrevido, llamativo y de alto impacto. Perfecto para anuncios, promociones y campañas publicitarias.",
        "preview_texto": "¡OFERTA ESPECIAL POR TIEMPO LIMITADO!",
        "config_avanzada": {
            "intro_duracion": 2,
            "outro_duracion": 3,
            "subtitulo_tamano": 28,
            "subtitulo_posicion": "center",
            "subtitulo_estilo": "bold-box",
            "overlay_opacidad": 0.15,
            "musica_volumen": 0.25,
            "voz_volumen": 1.0,
            "color_grading": "vibrante",
            "fps": 30,
        }
    },
    {
        "id": "ecommerce-product",
        "nombre": "E-commerce Showcase",
        "categoria": "Marketing",
        "color_primario": "#8B5CF6",
        "color_secundario": "#4C1D95",
        "color_acento": "#10B981",
        "color_texto": "#FFFFFF",
        "color_sub": "#D1FAE5",
        "fuente": "Poppins",
        "fuente_secundaria": "Inter",
        "estilo": "moderno-comercial",
        "transicion": "slide",
        "duracion_transicion": 0.3,
        "descripcion": "Moderno y comercial. Optimizado para showcases de productos, ecommerce y demos visuales.",
        "preview_texto": "Descubre el producto que cambiará tu día",
        "config_avanzada": {
            "intro_duracion": 3,
            "outro_duracion": 3,
            "subtitulo_tamano": 24,
            "subtitulo_posicion": "bottom",
            "subtitulo_estilo": "outline",
            "overlay_opacidad": 0.2,
            "musica_volumen": 0.20,
            "voz_volumen": 1.0,
            "color_grading": "vibrante",
            "fps": 30,
        }
    },

    # ============ REDES SOCIALES ============
    {
        "id": "viral-tiktok",
        "nombre": "Viral TikTok",
        "categoria": "Social Media",
        "color_primario": "#000000",
        "color_secundario": "#FF0050",
        "color_acento": "#00F2EA",
        "color_texto": "#FFFFFF",
        "color_sub": "#00F2EA",
        "fuente": "Poppins",
        "fuente_secundaria": "Inter",
        "estilo": "energetico-viral",
        "transicion": "zoom",
        "duracion_transicion": 0.15,
        "descripcion": "Energético y viral. Diseñado para TikTok, Reels y Shorts. Alto impacto visual y ritmo rápido.",
        "preview_texto": "Esto se va a hacer VIRAL 🔥",
        "config_avanzada": {
            "intro_duracion": 1,
            "outro_duracion": 2,
            "subtitulo_tamano": 32,
            "subtitulo_posicion": "center",
            "subtitulo_estilo": "bold-box",
            "overlay_opacidad": 0.1,
            "musica_volumen": 0.30,
            "voz_volumen": 1.0,
            "color_grading": "vibrante",
            "fps": 30,
        }
    },
    {
        "id": "instagram-aesthetic",
        "nombre": "Instagram Aesthetic",
        "categoria": "Social Media",
        "color_primario": "#F472B6",
        "color_secundario": "#9D174D",
        "color_acento": "#FBBF24",
        "color_texto": "#FFFFFF",
        "color_sub": "#FBCFE8",
        "fuente": "Poppins",
        "fuente_secundaria": "Inter",
        "estilo": "estetico-lifestyle",
        "transicion": "fade",
        "duracion_transicion": 0.4,
        "descripcion": "Estético y aspiracional. Para contenido lifestyle, moda, belleza y branding personal en Instagram.",
        "preview_texto": "Vive tu mejor versión ✨",
        "config_avanzada": {
            "intro_duracion": 2,
            "outro_duracion": 2,
            "subtitulo_tamano": 26,
            "subtitulo_posicion": "bottom",
            "subtitulo_estilo": "outline",
            "overlay_opacidad": 0.15,
            "musica_volumen": 0.22,
            "voz_volumen": 1.0,
            "color_grading": "calido",
            "fps": 30,
        }
    },

    # ============ EDUCACIÓN ============
    {
        "id": "tutorial-education",
        "nombre": "Tutorial Education",
        "categoria": "Educación",
        "color_primario": "#10B981",
        "color_secundario": "#064E3B",
        "color_acento": "#FBBF24",
        "color_texto": "#FFFFFF",
        "color_sub": "#D1FAE5",
        "fuente": "Inter",
        "fuente_secundaria": "JetBrains Mono",
        "estilo": "didactico-amigable",
        "transicion": "fade",
        "duracion_transicion": 0.4,
        "descripcion": "Didáctico y amigable. Optimizado para tutoriales, cursos online y contenido educativo.",
        "preview_texto": "Aprende paso a paso, sin complicaciones",
        "config_avanzada": {
            "intro_duracion": 3,
            "outro_duracion": 3,
            "subtitulo_tamano": 24,
            "subtitulo_posicion": "bottom",
            "subtitulo_estilo": "bold-outline",
            "overlay_opacidad": 0.25,
            "musica_volumen": 0.12,
            "voz_volumen": 1.0,
            "color_grading": "neutro",
            "fps": 30,
        }
    },

    # ============ ENTRETENIMIENTO ============
    {
        "id": "vlog-cinematic",
        "nombre": "Cinematic Vlog",
        "categoria": "Entretenimiento",
        "color_primario": "#1F2937",
        "color_secundario": "#111827",
        "color_acento": "#FBBF24",
        "color_texto": "#FFFFFF",
        "color_sub": "#FEF3C7",
        "fuente": "Montserrat",
        "fuente_secundaria": "Inter",
        "estilo": "cinematico-narrativo",
        "transicion": "fade",
        "duracion_transicion": 0.8,
        "descripcion": "Cinemático y narrativo. Para vlogs premium, storytelling, viajes y contenido cinematográfico.",
        "preview_texto": "Una historia que recordarás",
        "config_avanzada": {
            "intro_duracion": 4,
            "outro_duracion": 3,
            "subtitulo_tamano": 20,
            "subtitulo_posicion": "bottom",
            "subtitulo_estilo": "outline",
            "overlay_opacidad": 0.35,
            "musica_volumen": 0.20,
            "voz_volumen": 1.0,
            "color_grading": "cinematico",
            "fps": 24,
        }
    },

    # ============ PODCAST / ENTREVISTA ============
    {
        "id": "podcast-pro",
        "nombre": "Podcast Pro",
        "categoria": "Entretenimiento",
        "color_primario": "#7C3AED",
        "color_secundario": "#4C1D95",
        "color_acento": "#FBBF24",
        "color_texto": "#FFFFFF",
        "color_sub": "#EDE9FE",
        "fuente": "Montserrat",
        "fuente_secundaria": "Inter",
        "estilo": "radio-profesional",
        "transicion": "fade",
        "duracion_transicion": 0.5,
        "descripcion": "Profesional para podcasts. Incluye intro musical, lower thirds y créditos. Ideal para entrevistas.",
        "preview_texto": "Bienvenidos a otro episodio",
        "config_avanzada": {
            "intro_duracion": 6,
            "outro_duracion": 5,
            "subtitulo_tamano": 22,
            "subtitulo_posicion": "bottom",
            "subtitulo_estilo": "outline",
            "overlay_opacidad": 0.4,
            "musica_volumen": 0.18,
            "voz_volumen": 1.0,
            "color_grading": "calido",
            "fps": 30,
        }
    },

    # ============ MINIMALISTA ============
    {
        "id": "minimal-clean",
        "nombre": "Minimal Clean",
        "categoria": "Minimalista",
        "color_primario": "#FFFFFF",
        "color_secundario": "#F3F4F6",
        "color_acento": "#000000",
        "color_texto": "#000000",
        "color_sub": "#374151",
        "fuente": "Inter",
        "fuente_secundaria": "Inter",
        "estilo": "minimalista-puro",
        "transicion": "fade",
        "duracion_transicion": 0.6,
        "descripcion": "Minimalista puro. Espacios en blanco, tipografía limpia. Para marcas premium y contenido sofisticado.",
        "preview_texto": "Menos es más",
        "config_avanzada": {
            "intro_duracion": 3,
            "outro_duracion": 3,
            "subtitulo_tamano": 22,
            "subtitulo_posicion": "bottom",
            "subtitulo_estilo": "outline",
            "overlay_opacidad": 0.10,
            "musica_volumen": 0.10,
            "voz_volumen": 1.0,
            "color_grading": "neutro",
            "fps": 30,
        }
    },
]


def get_plantilla_by_id(plantilla_id):
    """Obtiene una plantilla por su ID."""
    for p in PLANTILLAS_PROFESIONALES:
        if p["id"] == plantilla_id:
            return p
    return None


def get_categorias():
    """Retorna lista de categorías únicas."""
    return list(set(p["categoria"] for p in PLANTILLAS_PROFESIONALES))


def get_plantillas_by_categoria(categoria):
    """Filtra plantillas por categoría."""
    return [p for p in PLANTILLAS_PROFESIONALES if p["categoria"] == categoria]


def get_plantilla_default():
    """Retorna la plantilla por defecto."""
    return PLANTILLAS_PROFESIONALES[0]


# Configuración de membresías actualizada
MEMBRESIAS = [
    {
        "id": "gratis",
        "nombre": "Starter",
        "precio": 0,
        "tokens": 3,
        "features": [
            "3 videos al mes",
            "Plantillas básicas (4)",
            "Resolución 720p",
            "Marca de agua ligera",
            "Soporte por email"
        ]
    },
    {
        "id": "pro",
        "nombre": "Creator Pro",
        "precio": 19.99,
        "tokens": 50,
        "features": [
            "50 videos al mes",
            "Todas las plantillas (12+)",
            "Resolución 1080p Full HD",
            "Sin marca de agua",
            "Subtítulos automáticos",
            "Multi-formato (YT, TT, IG)",
            "Soporte prioritario"
        ]
    },
    {
        "id": "business",
        "nombre": "Business",
        "precio": 49.99,
        "tokens": 200,
        "features": [
            "200 videos al mes",
            "Plantillas personalizadas IA",
            "Resolución 4K Ultra HD",
            "API de integración",
            "Multi-usuario (5 cuentas)",
            "Brand kit personalizado",
            "Soporte dedicado 24/7",
            "Análisis avanzado"
        ]
    }
]
