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
        },
        "variacion_de": "institucional",
        "elementos_visuales": {
            "titular": True,
            "subtitulo": True,
            "logo_institucional": True,
            "graficos_decorativos": ["barra_superior", "sello_institucional"],
            "bloques_informativos": True,
        }
    },
    {
        "id": "institucional-modern",
        "nombre": "Institucional Modern",
        "categoria": "Corporativo",
        "color_primario": "#0F766E",
        "color_secundario": "#134E4A",
        "color_acento": "#F59E0B",
        "color_texto": "#FFFFFF",
        "color_sub": "#CCFBF1",
        "fuente": "Inter",
        "fuente_secundaria": "Lato",
        "estilo": "institucional-moderno",
        "transicion": "slide",
        "duracion_transicion": 0.4,
        "descripcion": "Versión moderna del institucional. Limpia, fresca y contemporánea para instituciones que buscan renovar su imagen.",
        "preview_texto": "Innovación al servicio de la comunidad",
        "config_avanzada": {
            "intro_duracion": 4,
            "outro_duracion": 3,
            "subtitulo_tamano": 22,
            "subtitulo_posicion": "bottom",
            "subtitulo_estilo": "bold-outline",
            "overlay_opacidad": 0.20,
            "musica_volumen": 0.12,
            "voz_volumen": 1.0,
            "color_grading": "calido",
            "fps": 30,
        },
        "variacion_de": "institucional",
        "elementos_visuales": {
            "titular": True,
            "subtitulo": True,
            "logo_institucional": True,
            "graficos_decorativos": ["lineas_geometricas", "puntos_destacados"],
            "bloques_informativos": True,
        }
    },
    {
        "id": "institucional-executive",
        "nombre": "Institucional Executive",
        "categoria": "Corporativo",
        "color_primario": "#1E293B",
        "color_secundario": "#0F172A",
        "color_acento": "#D4AF37",
        "color_texto": "#FFFFFF",
        "color_sub": "#FDE68A",
        "fuente": "Montserrat",
        "fuente_secundaria": "Inter",
        "estilo": "ejecutivo-premium",
        "transicion": "fade",
        "duracion_transicion": 0.7,
        "descripcion": "Versión ejecutiva premium. Sofisticada y elegante para directivos, reportes anuales y presentaciones de alto nivel.",
        "preview_texto": "Excelencia en cada decisión",
        "config_avanzada": {
            "intro_duracion": 5,
            "outro_duracion": 4,
            "subtitulo_tamano": 20,
            "subtitulo_posicion": "bottom",
            "subtitulo_estilo": "outline",
            "overlay_opacidad": 0.40,
            "musica_volumen": 0.10,
            "voz_volumen": 1.0,
            "color_grading": "cinematico",
            "fps": 30,
        },
        "variacion_de": "institucional",
        "elementos_visuales": {
            "titular": True,
            "subtitulo": True,
            "logo_institucional": True,
            "graficos_decorativos": ["borde_dorado", "sello_ejecutivo"],
            "bloques_informativos": True,
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


# ============ FILTROS Y EFECTOS PROFESIONALES (FFmpeg) ============
# Catálogo amplio basado en https://ffmpeg.org/ffmpeg-filters.html
# Organizado por categorías de uso profesional
# Cada filtro incluye: id, nombre, descripción, filtro_ffmpeg, intensidad_default, categoria

EFECTOS_DISPONIBLES = [
    # ============ GENERAL ============
    {
        "id": "ninguno", "nombre": "Ninguno",
        "descripcion": "Sin efectos adicionales",
        "filtro_ffmpeg": "", "intensidad_default": 0, "categoria": "general"
    },
    {
        "id": "sharpen", "nombre": "Sharpen",
        "descripcion": "Aumenta la nitidez del video (unsharp)",
        "filtro_ffmpeg": "unsharp=5:5:1.0:5:5:0.0",
        "intensidad_default": 0.5, "categoria": "general"
    },
    {
        "id": "soft_focus", "nombre": "Soft Focus",
        "descripcion": "Enfoque suave para look romántico (gblur)",
        "filtro_ffmpeg": "gblur=sigma=0.8,eq=brightness=0.05",
        "intensidad_default": 0.3, "categoria": "general"
    },
    {
        "id": "denoise", "nombre": "Denoise",
        "descripcion": "Reduce ruido digital del video (hqdn3d)",
        "filtro_ffmpeg": "hqdn3d=1.5:1.5:6:6",
        "intensidad_default": 0.4, "categoria": "general"
    },
    {
        "id": "deband", "nombre": "Deband",
        "descripcion": "Elimina bandas de color (deband)",
        "filtro_ffmpeg": "deband=1thr=0.02:2thr=0.02:3thr=0.02",
        "intensidad_default": 0.3, "categoria": "general"
    },

    # ============ CINEMÁTICO ============
    {
        "id": "vignette", "nombre": "Viñeta",
        "descripcion": "Oscurece bordes para enfocar el centro (vignette)",
        "filtro_ffmpeg": "vignette=PI/5",
        "intensidad_default": 0.5, "categoria": "cinematico"
    },
    {
        "id": "film_grain", "nombre": "Film Grain",
        "descripcion": "Grano de película cinematográfica (noise)",
        "filtro_ffmpeg": "noise=alls=8:allf=t+u",
        "intensidad_default": 0.3, "categoria": "cinematico"
    },
    {
        "id": "light_leaks", "nombre": "Light Leaks",
        "descripcion": "Fugas de luz para look analógico",
        "filtro_ffmpeg": "eq=brightness=0.08:saturation=1.15,vignette=PI/6",
        "intensidad_default": 0.5, "categoria": "cinematico"
    },
    {
        "id": "noir", "nombre": "Film Noir",
        "descripcion": "Blanco y negro de alto contraste (hue+eq+vignette)",
        "filtro_ffmpeg": "hue=s=0,eq=contrast=1.4:brightness=-0.05:saturation=0,vignette=PI/4",
        "intensidad_default": 0.8, "categoria": "cinematico"
    },
    {
        "id": "cinematic_bars", "nombre": "Cinematic Bars",
        "descripcion": "Barras negras cinematográficas 2.39:1 (crop)",
        "filtro_ffmpeg": "crop=iw:ih*0.75:0:ih*0.125",
        "intensidad_default": 1.0, "categoria": "cinematico"
    },
    {
        "id": "cinematic_look", "nombre": "Cinematic Look",
        "descripcion": "Look cinematográfico completo (teal-orange)",
        "filtro_ffmpeg": "eq=contrast=1.1:saturation=1.1,curves=r='0 0.1 0.5 0.55 1 0.9':b='0 0 0.5 0.5 1 0.85',vignette=PI/5",
        "intensidad_default": 0.6, "categoria": "cinematico"
    },
    {
        "id": "anamorphic", "nombre": "Anamorphic",
        "descripcion": "Look anamórfico con flare y streaks",
        "filtro_ffmpeg": "eq=contrast=1.1:saturation=0.95,vignette=PI/6,unsharp=3:3:0.5:3:3:0.0",
        "intensidad_default": 0.5, "categoria": "cinematico"
    },
    {
        "id": "teal_orange", "nombre": "Teal & Orange",
        "descripcion": "El famoso look teal-orange de Hollywood",
        "filtro_ffmpeg": "curves=r='0 0.1 0.5 0.6 1 0.95':g='0 0 0.5 0.5 1 0.9':b='0 0.05 0.5 0.55 1 1',eq=saturation=1.15:contrast=1.05",
        "intensidad_default": 0.7, "categoria": "cinematico"
    },

    # ============ COLOR ============
    {
        "id": "warm_sunset", "nombre": "Warm Sunset",
        "descripcion": "Tonos cálidos de atardecer",
        "filtro_ffmpeg": "eq=brightness=0.05:saturation=1.2,curves=r='0 0.05 0.5 0.55 1 0.95':g='0 0.02 0.5 0.55 1 0.97':b='0 0 0.5 0.5 1 0.85'",
        "intensidad_default": 0.5, "categoria": "color"
    },
    {
        "id": "cold_winter", "nombre": "Cold Winter",
        "descripcion": "Tonos fríos azules para ambiente invernal",
        "filtro_ffmpeg": "eq=saturation=0.85,curves=r='0 0 0.5 0.45 1 0.85':b='0 0.05 0.5 0.55 1 1'",
        "intensidad_default": 0.5, "categoria": "color"
    },
    {
        "id": "sepia", "nombre": "Sepia",
        "descripcion": "Tono sepia clásico (colorchannelmixer)",
        "filtro_ffmpeg": "colorchannelmixer=.393:.769:.189:0:.349:.686:.168:0:.272:.534:.131:0",
        "intensidad_default": 0.8, "categoria": "color"
    },
    {
        "id": "high_contrast", "nombre": "High Contrast",
        "descripcion": "Alto contraste para impacto visual (eq)",
        "filtro_ffmpeg": "eq=contrast=1.5:saturation=1.1",
        "intensidad_default": 0.6, "categoria": "color"
    },
    {
        "id": "low_saturation", "nombre": "Low Saturation",
        "descripcion": "Saturación reducida para look sutil",
        "filtro_ffmpeg": "eq=saturation=0.6:contrast=1.1",
        "intensidad_default": 0.5, "categoria": "color"
    },
    {
        "id": "high_saturation", "nombre": "High Saturation",
        "descripcion": "Saturación intensa para contenido vibrante",
        "filtro_ffmpeg": "eq=saturation=1.8:contrast=1.1",
        "intensidad_default": 0.6, "categoria": "color"
    },
    {
        "id": "golden_hour", "nombre": "Golden Hour",
        "descripcion": "Look de hora dorada con tonos cálidos",
        "filtro_ffmpeg": "eq=brightness=0.08:saturation=1.25:contrast=1.05,curves=r='0 0.1 0.5 0.6 1 1':g='0 0.02 0.5 0.52 1 0.9':b='0 0 0.5 0.45 1 0.7'",
        "intensidad_default": 0.6, "categoria": "color"
    },
    {
        "id": "blue_hour", "nombre": "Blue Hour",
        "descripcion": "Look de hora azul con tonos fríos",
        "filtro_ffmpeg": "eq=brightness=-0.03:saturation=0.9:contrast=1.1,curves=r='0 0 0.5 0.45 1 0.8':b='0 0.1 0.5 0.6 1 1'",
        "intensidad_default": 0.6, "categoria": "color"
    },
    {
        "id": "vibrant_pop", "nombre": "Vibrant Pop",
        "descripcion": "Colores vibrantes que saltan (eq)",
        "filtro_ffmpeg": "eq=saturation=1.5:contrast=1.15:brightness=0.03",
        "intensidad_default": 0.7, "categoria": "color"
    },
    {
        "id": "pastel_dream", "nombre": "Pastel Dream",
        "descripcion": "Tonos pastel suaves y soñadores",
        "filtro_ffmpeg": "eq=saturation=0.75:brightness=0.08:contrast=0.95,curves=r='0 0.05 0.5 0.55 1 0.95':b='0 0.03 0.5 0.55 1 0.95'",
        "intensidad_default": 0.5, "categoria": "color"
    },

    # ============ RETRO ============
    {
        "id": "vintage", "nombre": "Vintage",
        "descripcion": "Aspecto retro con tonos cálidos y viñeta",
        "filtro_ffmpeg": "curves=r='0 0.3 0.6 1':g='0 0.3 0.6 1':b='0 0.4 0.7 1',vignette=PI/4,eq=saturation=0.8",
        "intensidad_default": 0.7, "categoria": "retro"
    },
    {
        "id": "vhs", "nombre": "VHS",
        "descripcion": "Efecto cinta VHS con glitch y noise",
        "filtro_ffmpeg": "noise=alls=20:allf=t+u,eq=brightness=0.05:saturation=0.7",
        "intensidad_default": 0.6, "categoria": "retro"
    },
    {
        "id": "8mm_film", "nombre": "8mm Film",
        "descripcion": "Look de película 8mm antigua",
        "filtro_ffmpeg": "noise=alls=12:allf=t+u,eq=saturation=0.7:contrast=1.2:brightness=-0.03,vignette=PI/3,curves=r='0 0.2 0.5 0.6 1 0.95':b='0 0 0.5 0.55 1 0.8'",
        "intensidad_default": 0.7, "categoria": "retro"
    },
    {
        "id": "polaroid", "nombre": "Polaroid",
        "descripcion": "Look instantáneo Polaroid con tonos cálidos",
        "filtro_ffmpeg": "eq=brightness=0.05:saturation=0.9:contrast=0.95,curves=r='0 0.05 0.5 0.6 1 0.95':b='0 0 0.5 0.5 1 0.85',vignette=PI/4",
        "intensidad_default": 0.6, "categoria": "retro"
    },
    {
        "id": "super8", "nombre": "Super 8",
        "descripcion": "Look de cámara Super 8 con flicker",
        "filtro_ffmpeg": "noise=alls=15:allf=t+u,eq=saturation=0.85:contrast=1.15:brightness=0.02,vignette=PI/3",
        "intensidad_default": 0.6, "categoria": "retro"
    },

    # ============ DIGITAL ============
    {
        "id": "glitch", "nombre": "Glitch",
        "descripcion": "Efecto digital glitch para contenido tech/gaming",
        "filtro_ffmpeg": "noise=alls=15:allf=t+u,eq=saturation=1.3",
        "intensidad_default": 0.5, "categoria": "digital"
    },
    {
        "id": "neon", "nombre": "Neon Glow",
        "descripcion": "Brillo neón para contenido gaming/urbano",
        "filtro_ffmpeg": "eq=saturation=1.8:contrast=1.2,unsharp=5:5:1.5:3:3:0.0",
        "intensidad_default": 0.6, "categoria": "digital"
    },
    {
        "id": "cyberpunk", "nombre": "Cyberpunk",
        "descripcion": "Look cyberpunk con neón rosa-cyan",
        "filtro_ffmpeg": "eq=saturation=1.6:contrast=1.2,curves=r='0 0.05 0.5 0.6 1 1':b='0 0.1 0.5 0.55 1 1',vignette=PI/5",
        "intensidad_default": 0.7, "categoria": "digital"
    },
    {
        "id": "matrix", "nombre": "Matrix",
        "descripcion": "Filtro verde Matrix",
        "filtro_ffmpeg": "colorchannelmixer=0:0:0:0:0:0:0:0:0:0.3:0:0,hue=s=1.5,eq=contrast=1.2:saturation=1.5",
        "intensidad_default": 0.8, "categoria": "digital"
    },
    {
        "id": "digital_noise", "nombre": "Digital Noise",
        "descripcion": "Ruido digital para look tech",
        "filtro_ffmpeg": "noise=alls=10:allf=t+u,eq=saturation=1.2:contrast=1.1",
        "intensidad_default": 0.4, "categoria": "digital"
    },
    {
        "id": "pixelate", "nombre": "Pixelate",
        "descripcion": "Efecto pixelado retro digital",
        "filtro_ffmpeg": "scale=iw/8:ih/8,scale=iw:ih:flags=neighbor",
        "intensidad_default": 0.5, "categoria": "digital"
    },

    # ============ DRAMÁTICO ============
    {
        "id": "zoom_blur", "nombre": "Zoom Blur",
        "descripcion": "Motion blur radial para dramatismo (gblur)",
        "filtro_ffmpeg": "gblur=sigma=2",
        "intensidad_default": 0.4, "categoria": "dramatico"
    },
    {
        "id": "dramatic", "nombre": "Dramatic",
        "descripcion": "Alto contraste para escenas dramáticas",
        "filtro_ffmpeg": "eq=contrast=1.5:saturation=1.1,vignette=PI/4",
        "intensidad_default": 0.7, "categoria": "dramatico"
    },
    {
        "id": "horror", "nombre": "Horror",
        "descripcion": "Look de terror con alto contraste y viñeta",
        "filtro_ffmpeg": "eq=contrast=1.6:brightness=-0.1:saturation=0.5,vignette=PI/3,noise=alls=5:allf=t+u",
        "intensidad_default": 0.7, "categoria": "dramatico"
    },
    {
        "id": "suspense", "nombre": "Suspense",
        "descripcion": "Tensión visual con tonos oscuros",
        "filtro_ffmpeg": "eq=brightness=-0.08:contrast=1.3:saturation=0.85,vignette=PI/3",
        "intensidad_default": 0.6, "categoria": "dramatico"
    },
    {
        "id": "epic", "nombre": "Epic",
        "descripcion": "Look épico con alta saturación y contraste",
        "filtro_ffmpeg": "eq=contrast=1.3:saturation=1.4:brightness=0.03,vignette=PI/5,unsharp=3:3:0.8:3:3:0.0",
        "intensidad_default": 0.6, "categoria": "dramatico"
    },

    # ============ ARTÍSTICO ============
    {
        "id": "dreamy", "nombre": "Dreamy",
        "descripcion": "Aspecto suave y soñador",
        "filtro_ffmpeg": "gblur=sigma=0.5,eq=brightness=0.1:saturation=1.1",
        "intensidad_default": 0.4, "categoria": "artistico"
    },
    {
        "id": "watercolor", "nombre": "Watercolor",
        "descripcion": "Efecto de acuarela artística",
        "filtro_ffmpeg": "hqdn3d=4:4:6:6,eq=saturation=1.3:contrast=1.1,bilateral=sigma_spatial=5",
        "intensidad_default": 0.5, "categoria": "artistico"
    },
    {
        "id": "oil_painting", "nombre": "Oil Painting",
        "descripcion": "Efecto de pintura al óleo",
        "filtro_ffmpeg": "hqdn3d=10:10:8:8,eq=saturation=1.4:contrast=1.15",
        "intensidad_default": 0.6, "categoria": "artistico"
    },
    {
        "id": "sketch", "nombre": "Sketch",
        "descripcion": "Efecto de boceto a lápiz",
        "filtro_ffmpeg": "hue=s=0,eq=contrast=2:brightness=-0.1,unsharp=10:10:2:10:10:0",
        "intensidad_default": 0.7, "categoria": "artistico"
    },
    {
        "id": "negative", "nombre": "Negative",
        "descripcion": "Invierte colores (negativo fotográfico)",
        "filtro_ffmpeg": "negate",
        "intensidad_default": 1.0, "categoria": "artistico"
    },
    {
        "id": "emboss", "nombre": "Emboss",
        "descripcion": "Efecto de relieve tridimensional",
        "filtro_ffmpeg": "unsharp=10:10:3:10:10:0,eq=contrast=1.5:brightness=-0.1",
        "intensidad_default": 0.6, "categoria": "artistico"
    },

    # ============ PERIODISMO AUDIOVISUAL ============
    {
        "id": "news_professional", "nombre": "News Professional",
        "descripcion": "Look profesional para noticias y reportajes",
        "filtro_ffmpeg": "eq=contrast=1.15:saturation=1.05:brightness=0.02,unsharp=3:3:0.5:3:3:0.0",
        "intensidad_default": 0.4, "categoria": "periodismo"
    },
    {
        "id": "documentary", "nombre": "Documentary",
        "descripcion": "Look documental natural y realista",
        "filtro_ffmpeg": "eq=contrast=1.05:saturation=0.95:brightness=0.01,vignette=PI/8",
        "intensidad_default": 0.3, "categoria": "periodismo"
    },
    {
        "id": "field_report", "nombre": "Field Report",
        "descripcion": "Look de reportaje de campo con ligero grano",
        "filtro_ffmpeg": "noise=alls=4:allf=t+u,eq=contrast=1.1:saturation=1.05,vignette=PI/7",
        "intensidad_default": 0.4, "categoria": "periodismo"
    },
    {
        "id": "breaking_news", "nombre": "Breaking News",
        "descripcion": "Look urgente de última hora con alto contraste",
        "filtro_ffmpeg": "eq=contrast=1.3:saturation=1.1:brightness=0.03,unsharp=3:3:0.8:3:3:0.0",
        "intensidad_default": 0.5, "categoria": "periodismo"
    },
    {
        "id": "interview_soft", "nombre": "Interview Soft",
        "descripcion": "Suaviza la piel para entrevistas (beauty)",
        "filtro_ffmpeg": "hqdn3d=2:2:4:4,eq=saturation=0.95:contrast=1.05:brightness=0.03",
        "intensidad_default": 0.3, "categoria": "periodismo"
    },
    {
        "id": "archive_footage", "nombre": "Archive Footage",
        "descripcion": "Look de material de archivo histórico",
        "filtro_ffmpeg": "noise=alls=8:allf=t+u,eq=saturation=0.6:contrast=1.2:brightness=-0.02,vignette=PI/4,curves=r='0 0.1 0.5 0.55 1 0.9':b='0 0 0.5 0.5 1 0.8'",
        "intensidad_default": 0.6, "categoria": "periodismo"
    },
    {
        "id": "satellite_feed", "nombre": "Satellite Feed",
        "descripcion": "Look de transmisión satelital con ruido",
        "filtro_ffmpeg": "noise=alls=6:allf=t+u,eq=contrast=1.15:saturation=1.0:brightness=-0.02,unsharp=2:2:0.3:2:2:0",
        "intensidad_default": 0.5, "categoria": "periodismo"
    },

    # ============ BLOQUES Y OVERLAYS ============
    {
        "id": "lower_third_bg", "nombre": "Lower Third",
        "descripcion": "Bloque inferior para nombres y títulos (drawbox)",
        "filtro_ffmpeg": "drawbox=x=0:y=ih-80:w=iw*0.6:h=60:color=black@0.7:t=fill",
        "intensidad_default": 1.0, "categoria": "overlays"
    },
    {
        "id": "top_bar", "nombre": "Top Bar",
        "descripcion": "Barra superior para logos y branding",
        "filtro_ffmpeg": "drawbox=x=0:y=0:w=iw:h=50:color=black@0.5:t=fill",
        "intensidad_default": 1.0, "categoria": "overlays"
    },
    {
        "id": "side_bar_left", "nombre": "Side Bar Left",
        "descripcion": "Barra lateral izquierda para información",
        "filtro_ffmpeg": "drawbox=x=0:y=0:w=80:h=ih:color=black@0.5:t=fill",
        "intensidad_default": 1.0, "categoria": "overlays"
    },
    {
        "id": "vignette_strong", "nombre": "Vignette Strong",
        "descripcion": "Viñeta fuerte para enfocar atención",
        "filtro_ffmpeg": "vignette=PI/3",
        "intensidad_default": 0.8, "categoria": "overlays"
    },
    {
        "id": "frame_border", "nombre": "Frame Border",
        "descripcion": "Marco decorativo alrededor del video",
        "filtro_ffmpeg": "drawbox=x=5:y=5:w=iw-10:h=ih-10:color=white@0.3:t=2",
        "intensidad_default": 0.5, "categoria": "overlays"
    },
    {
        "id": "gradient_overlay", "nombre": "Gradient Overlay",
        "descripcion": "Overlay con gradiente para legibilidad de texto",
        "filtro_ffmpeg": "drawbox=x=0:y=ih-150:w=iw:h=150:color=black@0.4:t=fill",
        "intensidad_default": 0.6, "categoria": "overlays"
    },

    # ============ AUDIO Y SINCRONIZACIÓN ============
    {
        "id": "audio_normalize", "nombre": "Audio Normalize",
        "descripcion": "Normaliza el audio para nivel consistente (loudnorm)",
        "filtro_ffmpeg": "loudnorm=I=-16:TP=-1.5:LRA=11",
        "intensidad_default": 0.8, "categoria": "audio",
        "tipo": "audio"
    },
    {
        "id": "audio_compress", "nombre": "Audio Compress",
        "descripcion": "Compresión de audio para voz clara (acompressor)",
        "filtro_ffmpeg": "acompressor=threshold=0.5:ratio=4:attack=5:release=50",
        "intensidad_default": 0.6, "categoria": "audio",
        "tipo": "audio"
    },
    {
        "id": "audio_enhance_voice", "nombre": "Voice Enhance",
        "descripcion": "Realza la voz humana y reduce ruido de fondo (highpass+lowpass)",
        "filtro_ffmpeg": "highpass=f=80,lowpass=f=12000,acompressor=threshold=0.4:ratio=3",
        "intensidad_default": 0.7, "categoria": "audio",
        "tipo": "audio"
    },
    {
        "id": "audio_denoise", "nombre": "Audio Denoise",
        "descripcion": "Reduce ruido de fondo del audio (afftdn)",
        "filtro_ffmpeg": "afftdn=nr=12:nf=-25",
        "intensidad_default": 0.5, "categoria": "audio",
        "tipo": "audio"
    },
    {
        "id": "audio_bass_boost", "nombre": "Bass Boost",
        "descripcion": "Refuerza graves para impacto dramático (bass)",
        "filtro_ffmpeg": "bass=g=5:f=80:t=q:w=1",
        "intensidad_default": 0.4, "categoria": "audio",
        "tipo": "audio"
    },
    {
        "id": "audio_treble_boost", "nombre": "Treble Boost",
        "descripcion": "Refuerza agudos para claridad de voz (treble)",
        "filtro_ffmpeg": "treble=g=3:f=3000:t=q:w=1",
        "intensidad_default": 0.4, "categoria": "audio",
        "tipo": "audio"
    },

    # ============ DETECCIÓN Y EFECTOS TEMPORALES ============
    {
        "id": "edge_detect", "nombre": "Edge Detect",
        "descripcion": "Detecta bordes para look técnico (edgedetect)",
        "filtro_ffmpeg": "edgedetect=low=0.1:high=0.4",
        "intensidad_default": 0.5, "categoria": "tecnico"
    },
    {
        "id": "motion_blur", "nombre": "Motion Blur",
        "descripcion": "Motion blur para sensación de movimiento (tmix)",
        "filtro_ffmpeg": "tmix=frames=4:weights=1 2 4 2 1",
        "intensidad_default": 0.4, "categoria": "tecnico"
    },
    {
        "id": "frame_interp", "nombre": "Frame Interpolation",
        "descripcion": "Interpolación de frames para video fluido (minterpolate)",
        "filtro_ffmpeg": "minterpolate=fps=60:mi_mode=mci",
        "intensidad_default": 0.5, "categoria": "tecnico"
    },
    {
        "id": "stabilize", "nombre": "Stabilize",
        "descripcion": "Estabiliza video tembloroso (deshake)",
        "filtro_ffmpeg": "deshake=rx=4:ry=4",
        "intensidad_default": 0.6, "categoria": "tecnico"
    },
    {
        "id": "deinterlace", "nombre": "Deinterlace",
        "descripcion": "Desentrelaza video antiguo (yadif)",
        "filtro_ffmpeg": "yadif=mode=0",
        "intensidad_default": 0.8, "categoria": "tecnico"
    },
    {
        "id": "deflicker", "nombre": "Deflicker",
        "descripcion": "Elimina parpadeo del video (deflicker)",
        "filtro_ffmpeg": "deflicker=mode=am:size=10",
        "intensidad_default": 0.5, "categoria": "tecnico"
    },
    {
        "id": "lens_correction", "nombre": "Lens Correction",
        "descripcion": "Corrige distorsión de lente (lenscorrection)",
        "filtro_ffmpeg": "lenscorrection=k1=-0.1:k2=0.01",
        "intensidad_default": 0.4, "categoria": "tecnico"
    },
    {
        "id": "perspective", "nombre": "Perspective",
        "descripcion": "Corrige perspectiva (perspective)",
        "filtro_ffmpeg": "perspective=x0=0:y0=0:x1=W:y1=0:x2=0:y2=H:x3=W:y3=H",
        "intensidad_default": 0.3, "categoria": "tecnico"
    },

    # ============ LOOKS ESPECIALES ============
    {
        "id": "drone_aerial", "nombre": "Drone Aerial",
        "descripcion": "Optimiza video de drone con alta saturación y nitidez",
        "filtro_ffmpeg": "eq=saturation=1.3:contrast=1.1:brightness=0.02,unsharp=5:5:0.8:5:5:0.0,vignette=PI/8",
        "intensidad_default": 0.5, "categoria": "look_especial"
    },
    {
        "id": "go_pro", "nombre": "GoPro",
        "descripcion": "Look de cámara GoPro con colores vivos",
        "filtro_ffmpeg": "eq=saturation=1.35:contrast=1.12:brightness=0.03,unsharp=3:3:0.5:3:3:0.0,fisheye=f=0.3",
        "intensidad_default": 0.5, "categoria": "look_especial"
    },
    {
        "id": "night_vision", "nombre": "Night Vision",
        "descripcion": "Look de visión nocturna verde",
        "filtro_ffmpeg": "hue=s=1.5:h=120,eq=contrast=1.4:brightness=0.1:saturation=2.0,noise=alls=5:allf=t+u",
        "intensidad_default": 0.7, "categoria": "look_especial"
    },
    {
        "id": "thermal", "nombre": "Thermal Camera",
        "descripcion": "Efecto de cámara térmica (pseudocolor)",
        "filtro_ffmpeg": "format=gray,eq=contrast=1.5,scale=256:1,scale=iw:ih:flags=neighbor",
        "intensidad_default": 0.8, "categoria": "look_especial"
    },
    {
        "id": "infrared", "nombre": "Infrared",
        "descripcion": "Efecto infrarrojo con tonos invertidos",
        "filtro_ffmpeg": "negate,eq=saturation=0.3:contrast=1.3,curves=r='0 0.5 1 1':b='0 0 1 0.5'",
        "intensidad_default": 0.7, "categoria": "look_especial"
    },
    {
        "id": "underwater", "nombre": "Underwater",
        "descripcion": "Look de grabación submarina con tonos azul-verde",
        "filtro_ffmpeg": "eq=saturation=0.8:contrast=0.95:brightness=0.02,curves=r='0 0 0.5 0.4 1 0.7':g='0 0.05 0.5 0.55 1 0.95':b='0 0.1 0.5 0.6 1 1',gblur=sigma=0.3",
        "intensidad_default": 0.5, "categoria": "look_especial"
    },
    {
        "id": "old_tv", "nombre": "Old TV",
        "descripcion": "Look de televisión antigua con scanlines",
        "filtro_ffmpeg": "noise=alls=8:allf=t+u,eq=saturation=0.8:contrast=1.15,vignette=PI/4",
        "intensidad_default": 0.6, "categoria": "look_especial"
    },
    {
        "id": "security_cam", "nombre": "Security Cam",
        "descripcion": "Look de cámara de seguridad en blanco y negro",
        "filtro_ffmpeg": "hue=s=0,eq=contrast=1.4:brightness=-0.05,noise=alls=10:allf=t+u,vignette=PI/3",
        "intensidad_default": 0.7, "categoria": "look_especial"
    },
]


# ============ FILTROS RECOMENDADOS POR CATEGORÍA DE PLANTILLA ============
FILTROS_POR_CATEGORIA = {
    "Tecnología": ["cinematic_look", "teal_orange", "glitch", "neon", "cyberpunk"],
    "Corporativo": ["news_professional", "documentary", "interview_soft", "sharpen", "denoise"],
    "Marketing": ["vibrant_pop", "golden_hour", "high_saturation", "epic", "warm_sunset"],
    "Social Media": ["vibrant_pop", "neon", "vintage", "vhs", "glow"],
    "Educación": ["documentary", "sharpen", "denoise", "news_professional", "interview_soft"],
    "Entretenimiento": ["cinematic_look", "teal_orange", "dramatic", "epic", "vibrant_pop"],
    "Gaming": ["neon", "cyberpunk", "glitch", "matrix", "digital_noise"],
    "Belleza": ["interview_soft", "soft_focus", "pastel_dream", "dreamy", "warm_sunset"],
    "Gastronomía": ["warm_sunset", "golden_hour", "vibrant_pop", "high_saturation", "sharpen"],
    "Viajes": ["drone_aerial", "golden_hour", "vibrant_pop", "cinematic_look", "epic"],
    "Fitness": ["high_contrast", "epic", "dramatic", "high_saturation", "neon"],
    "Música": ["neon", "cyberpunk", "glitch", "vibrant_pop", "high_saturation"],
    "Noticias": ["news_professional", "breaking_news", "field_report", "archive_footage", "satellite_feed"],
    "Premium": ["cinematic_look", "teal_orange", "anamorphic", "light_leaks", "film_grain"],
    "Minimalista": ["documentary", "low_saturation", "soft_focus", "denoise", "sharpen"],
}


def get_filtros_recomendados(categoria_plantilla: str) -> list:
    """Retorna los filtros recomendados para una categoría de plantilla."""
    ids_recomendados = FILTROS_POR_CATEGORIA.get(categoria_plantilla, [])
    return [e for e in EFECTOS_DISPONIBLES if e["id"] in ids_recomendados]


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
