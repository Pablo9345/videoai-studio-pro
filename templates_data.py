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

    # ============ GAMING ============
    {
        "id": "gaming-stream",
        "nombre": "Gaming Stream",
        "categoria": "Gaming",
        "color_primario": "#7C3AED",
        "color_secundario": "#1E1B4B",
        "color_acento": "#10B981",
        "color_texto": "#FFFFFF",
        "color_sub": "#D1FAE5",
        "fuente": "JetBrains Mono",
        "fuente_secundaria": "Inter",
        "estilo": "gamer-neon",
        "transicion": "zoom",
        "duracion_transicion": 0.2,
        "descripcion": "Estilo gamer con neón vibrante. Perfecto para gameplay, reviews, streams y contenido gaming.",
        "preview_texto": "GAME ON 🎮 Next Level Gaming",
        "config_avanzada": {
            "intro_duracion": 3,
            "outro_duracion": 3,
            "subtitulo_tamano": 26,
            "subtitulo_posicion": "bottom",
            "subtitulo_estilo": "bold-box",
            "overlay_opacidad": 0.15,
            "musica_volumen": 0.25,
            "voz_volumen": 1.0,
            "color_grading": "vibrante",
            "fps": 60,
        }
    },

    # ============ BEAUTY ============
    {
        "id": "beauty-aesthetic",
        "nombre": "Beauty Aesthetic",
        "categoria": "Belleza",
        "color_primario": "#FBCFE8",
        "color_secundario": "#9D174D",
        "color_acento": "#F59E0B",
        "color_texto": "#FFFFFF",
        "color_sub": "#FCE7F3",
        "fuente": "Poppins",
        "fuente_secundaria": "Inter",
        "estilo": "soft-pastel",
        "transicion": "fade",
        "duracion_transicion": 0.5,
        "descripcion": "Suave y elegante. Para tutoriales de maquillaje, skincare, belleza y lifestyle premium.",
        "preview_texto": "Glow Up ✨ Tu mejor versión",
        "config_avanzada": {
            "intro_duracion": 3,
            "outro_duracion": 3,
            "subtitulo_tamano": 24,
            "subtitulo_posicion": "bottom",
            "subtitulo_estilo": "outline",
            "overlay_opacidad": 0.20,
            "musica_volumen": 0.15,
            "voz_volumen": 1.0,
            "color_grading": "calido",
            "fps": 30,
        }
    },

    # ============ FOOD ============
    {
        "id": "food-recipe",
        "nombre": "Food Recipe",
        "categoria": "Gastronomía",
        "color_primario": "#DC2626",
        "color_secundario": "#7F1D1D",
        "color_acento": "#FBBF24",
        "color_texto": "#FFFFFF",
        "color_sub": "#FEF3C7",
        "fuente": "Montserrat",
        "fuente_secundaria": "Inter",
        "estilo": "apetitoso-calido",
        "transicion": "slide",
        "duracion_transicion": 0.3,
        "descripcion": "Cálido y apetitoso. Para recetas, reseñas gastronómicas, cocina y food content.",
        "preview_texto": "¡Receta deliciosa en 60 segundos! 🍝",
        "config_avanzada": {
            "intro_duracion": 2,
            "outro_duracion": 3,
            "subtitulo_tamano": 22,
            "subtitulo_posicion": "bottom",
            "subtitulo_estilo": "bold-outline",
            "overlay_opacidad": 0.25,
            "musica_volumen": 0.18,
            "voz_volumen": 1.0,
            "color_grading": "calido",
            "fps": 30,
        }
    },

    # ============ TRAVEL ============
    {
        "id": "travel-wanderlust",
        "nombre": "Travel Wanderlust",
        "categoria": "Viajes",
        "color_primario": "#0EA5E9",
        "color_secundario": "#0C4A6E",
        "color_acento": "#FBBF24",
        "color_texto": "#FFFFFF",
        "color_sub": "#BAE6FD",
        "fuente": "Montserrat",
        "fuente_secundaria": "Inter",
        "estilo": "aventurero-inspirador",
        "transicion": "fade",
        "duracion_transicion": 0.6,
        "descripcion": "Inspirador y aventurero. Para vlogs de viaje, guías, paisajes y contenido wanderlust.",
        "preview_texto": "Descubre el mundo 🌍 Una aventura te espera",
        "config_avanzada": {
            "intro_duracion": 4,
            "outro_duracion": 3,
            "subtitulo_tamano": 22,
            "subtitulo_posicion": "bottom",
            "subtitulo_estilo": "outline",
            "overlay_opacidad": 0.30,
            "musica_volumen": 0.22,
            "voz_volumen": 1.0,
            "color_grading": "cinematico",
            "fps": 24,
        }
    },

    # ============ FITNESS ============
    {
        "id": "fitness-energy",
        "nombre": "Fitness Energy",
        "categoria": "Fitness",
        "color_primario": "#10B981",
        "color_secundario": "#064E3B",
        "color_acento": "#F97316",
        "color_texto": "#FFFFFF",
        "color_sub": "#A7F3D0",
        "fuente": "Poppins",
        "fuente_secundaria": "Inter",
        "estilo": "energico-motivacional",
        "transicion": "zoom",
        "duracion_transicion": 0.25,
        "descripcion": "Enérgico y motivacional. Para rutinas de ejercicio, motivación, transformaciones y fitness.",
        "preview_texto": "💪 NO RINDAS HOY Push Your Limits",
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

    # ============ MUSIC ============
    {
        "id": "music-visualizer",
        "nombre": "Music Visualizer",
        "categoria": "Música",
        "color_primario": "#1F2937",
        "color_secundario": "#000000",
        "color_acento": "#A855F7",
        "color_texto": "#FFFFFF",
        "color_sub": "#E9D5FF",
        "fuente": "Montserrat",
        "fuente_secundaria": "JetBrains Mono",
        "estilo": "musical-visual",
        "transicion": "dissolve",
        "duracion_transicion": 0.5,
        "descripcion": "Visual y rítmico. Para lyric videos, visualizadores musicales, beats y contenido de artistas.",
        "preview_texto": "♪ Now Playing 🎵 Artist - Track Title",
        "config_avanzada": {
            "intro_duracion": 4,
            "outro_duracion": 4,
            "subtitulo_tamano": 32,
            "subtitulo_posicion": "center",
            "subtitulo_estilo": "bold-box",
            "overlay_opacidad": 0.40,
            "musica_volumen": 0.50,
            "voz_volumen": 0.8,
            "color_grading": "cinematico",
            "fps": 30,
        }
    },

    # ============ NEWS ============
    {
        "id": "news-breaking",
        "nombre": "News Breaking",
        "categoria": "Noticias",
        "color_primario": "#1E40AF",
        "color_secundario": "#1E3A8A",
        "color_acento": "#DC2626",
        "color_texto": "#FFFFFF",
        "color_sub": "#DBEAFE",
        "fuente": "Lato",
        "fuente_secundaria": "Inter",
        "estilo": "informativo-profesional",
        "transicion": "slide",
        "duracion_transicion": 0.3,
        "descripcion": "Profesional e informativo. Para noticias, reportajes, breaking news y contenido periodístico.",
        "preview_texto": "ÚLTIMA HORA 📰 Noticias de hoy",
        "config_avanzada": {
            "intro_duracion": 5,
            "outro_duracion": 4,
            "subtitulo_tamano": 22,
            "subtitulo_posicion": "bottom",
            "subtitulo_estilo": "bold-outline",
            "overlay_opacidad": 0.30,
            "musica_volumen": 0.10,
            "voz_volumen": 1.0,
            "color_grading": "neutro",
            "fps": 30,
        }
    },

    # ============ LUXURY ============
    {
        "id": "luxury-elegance",
        "nombre": "Luxury Elegance",
        "categoria": "Premium",
        "color_primario": "#0F172A",
        "color_secundario": "#000000",
        "color_acento": "#D4AF37",
        "color_texto": "#FFFFFF",
        "color_sub": "#FDE68A",
        "fuente": "Montserrat",
        "fuente_secundaria": "Inter",
        "estilo": "lujo-exclusivo",
        "transicion": "fade",
        "duracion_transicion": 0.8,
        "descripcion": "Exclusivo y lujoso. Para productos premium, bienes raíces, joyería y marcas de alto valor.",
        "preview_texto": "Exquisite Living ✦ The Art of Luxury",
        "config_avanzada": {
            "intro_duracion": 5,
            "outro_duracion": 4,
            "subtitulo_tamano": 22,
            "subtitulo_posicion": "bottom",
            "subtitulo_estilo": "outline",
            "overlay_opacidad": 0.35,
            "musica_volumen": 0.15,
            "voz_volumen": 1.0,
            "color_grading": "cinematico",
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


# ============ TRANSICIONES DISPONIBLES (XFade de FFmpeg) ============
TRANSICIONES_DISPONIBLES = [
    {"id": "fade", "nombre": "Fade", "descripcion": "Transición suave de fundido", "duracion_default": 0.5},
    {"id": "fadeblack", "nombre": "Fade Black", "descripcion": "Fundido a negro", "duracion_default": 0.5},
    {"id": "fadewhite", "nombre": "Fade White", "descripcion": "Fundido a blanco", "duracion_default": 0.5},
    {"id": "dissolve", "nombre": "Dissolve", "descripcion": "Disolución suave", "duracion_default": 0.6},
    {"id": "wipeleft", "nombre": "Wipe Left", "descripcion": "Barrido hacia la izquierda", "duracion_default": 0.4},
    {"id": "wiperight", "nombre": "Wipe Right", "descripcion": "Barrido hacia la derecha", "duracion_default": 0.4},
    {"id": "wipeup", "nombre": "Wipe Up", "descripcion": "Barrido hacia arriba", "duracion_default": 0.4},
    {"id": "wipedown", "nombre": "Wipe Down", "descripcion": "Barrido hacia abajo", "duracion_default": 0.4},
    {"id": "slideleft", "nombre": "Slide Left", "descripcion": "Deslizamiento desde la izquierda", "duracion_default": 0.4},
    {"id": "slideright", "nombre": "Slide Right", "descripcion": "Deslizamiento desde la derecha", "duracion_default": 0.4},
    {"id": "slideup", "nombre": "Slide Up", "descripcion": "Deslizamiento desde abajo", "duracion_default": 0.4},
    {"id": "slidedown", "nombre": "Slide Down", "descripcion": "Deslizamiento desde arriba", "duracion_default": 0.4},
    {"id": "circlecrop", "nombre": "Circle Crop", "descripcion": "Recorte circular", "duracion_default": 0.5},
    {"id": "circleopen", "nombre": "Circle Open", "descripcion": "Apertura circular", "duracion_default": 0.5},
    {"id": "circleclose", "nombre": "Circle Close", "descripcion": "Cierre circular", "duracion_default": 0.5},
    {"id": "radial", "nombre": "Radial", "descripcion": "Radial wipes", "duracion_default": 0.5},
    {"id": "smoothleft", "nombre": "Smooth Left", "descripcion": "Suave desde la izquierda", "duracion_default": 0.5},
    {"id": "smoothright", "nombre": "Smooth Right", "descripcion": "Suave desde la derecha", "duracion_default": 0.5},
    {"id": "smoothup", "nombre": "Smooth Up", "descripcion": "Suave hacia arriba", "duracion_default": 0.5},
    {"id": "smoothdown", "nombre": "Smooth Down", "descripcion": "Suave hacia abajo", "duracion_default": 0.5},
    {"id": "zoom", "nombre": "Zoom", "descripcion": "Zoom in/out", "duracion_default": 0.3},
    {"id": "zoomin", "nombre": "Zoom In", "descripcion": "Zoom acercándose", "duracion_default": 0.3},
    {"id": "horzopen", "nombre": "Horizontal Open", "descripcion": "Apertura horizontal", "duracion_default": 0.4},
    {"id": "horzclose", "nombre": "Horizontal Close", "descripcion": "Cierre horizontal", "duracion_default": 0.4},
    {"id": "vertopen", "nombre": "Vertical Open", "descripcion": "Apertura vertical", "duracion_default": 0.4},
    {"id": "vertclose", "nombre": "Vertical Close", "descripcion": "Cierre vertical", "duracion_default": 0.4},
    {"id": "diagtl", "nombre": "Diagonal Top-Left", "descripcion": "Diagonal desde esquina superior izquierda", "duracion_default": 0.4},
    {"id": "diagtr", "nombre": "Diagonal Top-Right", "descripcion": "Diagonal desde esquina superior derecha", "duracion_default": 0.4},
    {"id": "diagbl", "nombre": "Diagonal Bottom-Left", "descripcion": "Diagonal desde esquina inferior izquierda", "duracion_default": 0.4},
    {"id": "diagbr", "nombre": "Diagonal Bottom-Right", "descripcion": "Diagonal desde esquina inferior derecha", "duracion_default": 0.4},
    {"id": "hlslice", "nombre": "HLSlice", "descripcion": "Slice horizontal", "duracion_default": 0.4},
    {"id": "hrslice", "nombre": "HRSlice", "descripcion": "Slice horizontal derecho", "duracion_default": 0.4},
    {"id": "vuslice", "nombre": "VUSlice", "descripcion": "Slice vertical superior", "duracion_default": 0.4},
    {"id": "vdslice", "nombre": "VDSlice", "descripcion": "Slice vertical inferior", "duracion_default": 0.4},
    {"id": "hblur", "nombre": "HBlur", "descripcion": "Blur horizontal", "duracion_default": 0.5},
    {"id": "fadegrays", "nombre": "Fade Grayscale", "descripcion": "Fundido en escala de grises", "duracion_default": 0.5},
    {"id": "wipetl", "nombre": "Wipe Top-Left", "descripcion": "Barrido desde esquina superior izquierda", "duracion_default": 0.4},
    {"id": "wipetr", "nombre": "Wipe Top-Right", "descripcion": "Barrido desde esquina superior derecha", "duracion_default": 0.4},
    {"id": "wipebl", "nombre": "Wipe Bottom-Left", "descripcion": "Barrido desde esquina inferior izquierda", "duracion_default": 0.4},
    {"id": "wipebr", "nombre": "Wipe Bottom-Right", "descripcion": "Barrido desde esquina inferior derecha", "duracion_default": 0.4},
    {"id": "squircles", "nombre": "Squircle", "descripcion": "Cierre en forma de cuadrado redondeado", "duracion_default": 0.5},
    {"id": "pixellize", "nombre": "Pixellize", "descripcion": "Pixelado en transición", "duracion_default": 0.5},
    {"id": "dissolve", "nombre": "Dissolve (pro)", "descripcion": "Disolución profesional", "duracion_default": 0.6},
    {"id": "h_cut", "nombre": "Cut Horizontal", "descripcion": "Corte horizontal brusco", "duracion_default": 0.1},
    {"id": "v_cut", "nombre": "Cut Vertical", "descripcion": "Corte vertical brusco", "duracion_default": 0.1},
    {"id": "smpte101", "nombre": "SMPTE 101", "descripcion": "Transición profesional SMPTE", "duracion_default": 0.5},
    {"id": "smpte102", "nombre": "SMPTE 102", "descripcion": "Transición profesional SMPTE 2", "duracion_default": 0.5},
]


# ============ EFECTOS VISUALES DISPONIBLES ============
EFECTOS_DISPONIBLES = [
    {
        "id": "ninguno",
        "nombre": "Ninguno",
        "descripcion": "Sin efectos adicionales",
        "filtro_ffmpeg": "",
        "intensidad_default": 0,
        "categoria": "general"
    },
    {
        "id": "vignette",
        "nombre": "Viñeta",
        "descripcion": "Oscurece los bordes para enfocar el centro",
        "filtro_ffmpeg": "vignette=PI/5",
        "intensidad_default": 0.5,
        "categoria": "fotografia"
    },
    {
        "id": "vintage",
        "nombre": "Vintage",
        "descripcion": "Aspecto retro con tonos cálidos y viñeta",
        "filtro_ffmpeg": "curves=r='0 0.3 0.6 1':g='0 0.3 0.6 1':b='0 0.4 0.7 1',vignette=PI/4,eq=saturation=0.8",
        "intensidad_default": 0.7,
        "categoria": "retro"
    },
    {
        "id": "vhs",
        "nombre": "VHS",
        "descripcion": "Efecto cinta VHS con glitch y noise",
        "filtro_ffmpeg": "noise=alls=20:allf=t+u,scale=960:540,scale=1920:1080:flags=neighbor,eq=brightness=0.05:saturation=0.7",
        "intensidad_default": 0.6,
        "categoria": "retro"
    },
    {
        "id": "film_grain",
        "nombre": "Film Grain",
        "descripcion": "Grano de película cinematográfica",
        "filtro_ffmpeg": "noise=alls=8:allf=t+u",
        "intensidad_default": 0.3,
        "categoria": "cinematico"
    },
    {
        "id": "light_leaks",
        "nombre": "Light Leaks",
        "descripcion": "Fugas de luz para look analógico",
        "filtro_ffmpeg": "eq=brightness=0.08:saturation=1.15,vignette=PI/6",
        "intensidad_default": 0.5,
        "categoria": "cinematico"
    },
    {
        "id": "zoom_blur",
        "nombre": "Zoom Blur",
        "descripcion": "Motion blur radial para dramatismo",
        "filtro_ffmpeg": "gblur=sigma=2",
        "intensidad_default": 0.4,
        "categoria": "dramatico"
    },
    {
        "id": "glitch",
        "nombre": "Glitch",
        "descripcion": "Efecto digital glitch para contenido tech/gaming",
        "filtro_ffmpeg": "noise=alls=15:allf=t+u,eq=saturation=1.3,scale=960:540,scale=1920:1080:flags=neighbor",
        "intensidad_default": 0.5,
        "categoria": "digital"
    },
    {
        "id": "neon",
        "nombre": "Neon Glow",
        "descripcion": "Brillo neón para contenido gaming/urbano",
        "filtro_ffmpeg": "eq=saturation=1.8:contrast=1.2,unsharp=5:5:1.5:3:3:0.0",
        "intensidad_default": 0.6,
        "categoria": "digital"
    },
    {
        "id": "noir",
        "nombre": "Film Noir",
        "descripcion": "Blanco y negro de alto contraste cinematográfico",
        "filtro_ffmpeg": "hue=s=0,eq=contrast=1.4:brightness=-0.05:saturation=0,vignette=PI/4",
        "intensidad_default": 0.8,
        "categoria": "cinematico"
    },
    {
        "id": "warm_sunset",
        "nombre": "Warm Sunset",
        "descripcion": "Tonos cálidos de atardecer",
        "filtro_ffmpeg": "eq=brightness=0.05:saturation=1.2,curves=r='0 0.05 0.5 0.55 1 0.95':g='0 0.02 0.5 0.55 1 0.97':b='0 0 0.5 0.5 1 0.85'",
        "intensidad_default": 0.5,
        "categoria": "color"
    },
    {
        "id": "cold_winter",
        "nombre": "Cold Winter",
        "descripcion": "Tonos fríos azules para ambiente invernal",
        "filtro_ffmpeg": "eq=saturation=0.85,curves=r='0 0 0.5 0.45 1 0.85':b='0 0.05 0.5 0.55 1 1'",
        "intensidad_default": 0.5,
        "categoria": "color"
    },
    {
        "id": "dramatic",
        "nombre": "Dramatic",
        "descripcion": "Alto contraste para escenas dramáticas",
        "filtro_ffmpeg": "eq=contrast=1.5:saturation=1.1,vignette=PI/4",
        "intensidad_default": 0.7,
        "categoria": "dramatico"
    },
    {
        "id": "dreamy",
        "nombre": "Dreamy",
        "descripcion": "Aspecto suave y soñador",
        "filtro_ffmpeg": "gblur=sigma=0.5:steps=3,eq=brightness=0.1:saturation=1.1",
        "intensidad_default": 0.4,
        "categoria": "artistico"
    },
    {
        "id": "sharpen",
        "nombre": "Sharpen",
        "descripcion": "Aumenta la nitidez del video",
        "filtro_ffmpeg": "unsharp=5:5:1.0:5:5:0.0",
        "intensidad_default": 0.5,
        "categoria": "general"
    },
    {
        "id": "soft_focus",
        "nombre": "Soft Focus",
        "descripcion": "Enfoque suave para look romántico",
        "filtro_ffmpeg": "gblur=sigma=0.8:steps=5,eq=brightness=0.05",
        "intensidad_default": 0.3,
        "categoria": "artistico"
    },
]


def get_efectos_by_categoria(categoria):
    """Filtra efectos por categoría."""
    return [e for e in EFECTOS_DISPONIBLES if e["categoria"] == categoria]


def get_efecto_by_id(efecto_id):
    """Obtiene un efecto por su ID."""
    for e in EFECTOS_DISPONIBLES:
        if e["id"] == efecto_id:
            return e
    return None


def get_categorias_efectos():
    """Retorna lista de categorías de efectos."""
    return list(set(e["categoria"] for e in EFECTOS_DISPONIBLES))


def get_transicion_by_id(transicion_id):
    """Obtiene una transición por su ID."""
    for t in TRANSICIONES_DISPONIBLES:
        if t["id"] == transicion_id:
            return t
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
