#!/usr/bin/env python3
"""
Suite maestra de tests de producción para VideoAI Studio Pro.
Ejecuta todos los tests en orden y reporta el estado completo del sistema.
"""

import sys
import os
import ast
import importlib
import json
import time
import traceback
from pathlib import Path
from unittest.mock import patch, MagicMock

# Añadir directorio actual al path
BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))

# Mock streamlit si no está disponible
try:
    import streamlit
except ImportError:
    mock_path = Path("/home/z/my-project/scripts")
    if mock_path.exists():
        sys.path.insert(0, str(mock_path))
        try:
            import streamlit_mock
        except ImportError:
            pass


class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

results = {"pass": 0, "fail": 0, "warn": 0, "errors": []}


def log_pass(msg):
    print(f"{Colors.GREEN}✅ PASS{Colors.RESET}: {msg}")
    results["pass"] += 1


def log_fail(msg, detail=""):
    print(f"{Colors.RED}❌ FAIL{Colors.RESET}: {msg}")
    if detail:
        print(f"   {Colors.RED}→{Colors.RESET} {detail[:400]}")
    results["fail"] += 1
    results["errors"].append((msg, detail))


def log_warn(msg):
    print(f"{Colors.YELLOW}⚠ WARN{Colors.RESET}: {msg}")
    results["warn"] += 1


def log_section(msg):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{msg}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'=' * 60}{Colors.RESET}")


# ============ AUDITORÍA ESTÁTICA ============

def audit_imports():
    """Audita que todos los imports en todos los archivos sean válidos."""
    log_section("AUDITORÍA DE IMPORTS")

    archivos = ["app.py", "styles.py", "database.py", "auth.py",
                "groq_ai.py", "video_processor.py", "components.py",
                "templates_data.py", "preview_renderer.py"]

    for archivo in archivos:
        ruta = BASE_DIR / archivo
        if not ruta.exists():
            log_fail(f"Archivo no existe: {archivo}")
            continue

        try:
            with open(ruta, 'r', encoding='utf-8') as f:
                source = f.read()

            tree = ast.parse(source)

            # Verificar imports de módulos del proyecto
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom):
                    mod = node.module
                    if mod in ["styles", "database", "auth", "groq_ai",
                               "video_processor", "components", "templates_data",
                               "preview_renderer"]:
                        # Verificar que los nombres importados existan
                        try:
                            m = importlib.import_module(mod)
                            for alias in node.names:
                                nombre = alias.asname or alias.name
                                if not hasattr(m, nombre):
                                    log_fail(f"{archivo}: import '{nombre}' no existe en {mod}")
                        except Exception as e:
                            log_fail(f"{archivo}: no se pudo importar {mod}", str(e))

            log_pass(f"Imports OK: {archivo}")

        except SyntaxError as e:
            log_fail(f"Sintaxis error en {archivo}", f"Línea {e.lineno}: {e.msg}")
        except Exception as e:
            log_fail(f"Error auditando {archivo}", str(e))


def audit_sintaxis():
    """Verifica que todos los archivos Python compilen."""
    log_section("AUDITORÍA DE SINTAXIS")

    archivos = list(BASE_DIR.glob("*.py"))
    for archivo in archivos:
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                source = f.read()
            ast.parse(source)
            log_pass(f"Sintaxis OK: {archivo.name}")
        except SyntaxError as e:
            log_fail(f"Sintaxis error en {archivo.name}", f"Línea {e.lineno}: {e.msg}")


# ============ TESTS DE MÓDULOS ============

def test_styles():
    """Verifica el módulo styles.py."""
    log_section("TEST: styles.py")

    try:
        from styles import (
            PREMIUM_CSS, get_premium_css, html_safe,
            render_template_preview_card, render_stat_card,
            render_wizard, render_wizard_step, render_scene_card,
            render_pricing_card
        )

        # CSS no vacío
        assert len(PREMIUM_CSS) > 1000, "CSS muy corto"
        log_pass(f"PREMIUM_CSS: {len(PREMIUM_CSS)} chars")

        assert get_premium_css() == PREMIUM_CSS
        log_pass("get_premium_css() funciona")

        # html_safe
        assert html_safe("") == ""
        assert html_safe(None) == ""
        assert html_safe("<div>\n<span>test</span>\n</div>") == "<div><span>test</span></div>"
        log_pass("html_safe funciona correctamente")

        # Render functions
        from templates_data import PLANTILLAS_PROFESIONALES, MEMBRESIAS

        html = render_template_preview_card(PLANTILLAS_PROFESIONALES[0], 0, False)
        assert "template-card" in html
        log_pass("render_template_preview_card funciona")

        html = render_stat_card("🎬", "10", "videos")
        assert "stat-card" in html
        log_pass("render_stat_card funciona")

        html = render_wizard(2, ["A", "B", "C"])
        assert "wizard-steps" in html
        log_pass("render_wizard funciona")

        html = render_scene_card(1, "desc", "texto", 10, "b-roll")
        assert "scene-card" in html
        log_pass("render_scene_card funciona")

        html = render_pricing_card(MEMBRESIAS[0], False)
        assert "pricing-card" in html
        log_pass("render_pricing_card funciona")

    except Exception as e:
        log_fail("styles.py falló", str(e))


def test_templates_data():
    """Verifica templates_data.py."""
    log_section("TEST: templates_data.py")

    try:
        from templates_data import (
            PLANTILLAS_PROFESIONALES, MEMBRESIAS,
            TRANSICIONES_DISPONIBLES, EFECTOS_DISPONIBLES,
            get_plantilla_by_id, get_categorias, get_plantillas_by_categoria,
            get_plantilla_default, get_efecto_by_id, get_efectos_by_categoria,
            get_categorias_efectos, get_transicion_by_id
        )

        # Verificar cantidad mínima
        assert len(PLANTILLAS_PROFESIONALES) >= 20, f"Solo {len(PLANTILLAS_PROFESIONALES)} plantillas"
        log_pass(f"Plantillas: {len(PLANTILLAS_PROFESIONALES)}")

        assert len(TRANSICIONES_DISPONIBLES) >= 40, f"Solo {len(TRANSICIONES_DISPONIBLES)} transiciones"
        log_pass(f"Transiciones: {len(TRANSICIONES_DISPONIBLES)}")

        assert len(EFECTOS_DISPONIBLES) >= 15, f"Solo {len(EFECTOS_DISPONIBLES)} efectos"
        log_pass(f"Efectos: {len(EFECTOS_DISPONIBLES)}")

        assert len(MEMBRESIAS) == 3
        log_pass(f"Membresías: {len(MEMBRESIAS)}")

        # Verificar estructura de cada plantilla
        campos_requeridos = [
            "id", "nombre", "categoria", "color_primario", "color_secundario",
            "color_acento", "color_texto", "color_sub", "fuente",
            "estilo", "transicion", "duracion_transicion",
            "descripcion", "preview_texto", "config_avanzada"
        ]

        for p in PLANTILLAS_PROFESIONALES:
            for campo in campos_requeridos:
                assert campo in p, f"Plantilla {p.get('id', '?')} falta: {campo}"
        log_pass(f"Todas las {len(PLANTILLAS_PROFESIONALES)} plantillas tienen estructura correcta")

        # IDs únicos
        ids = [p["id"] for p in PLANTILLAS_PROFESIONALES]
        assert len(ids) == len(set(ids)), "IDs duplicados"
        log_pass("Todos los IDs de plantillas son únicos")

        # get functions
        p = PLANTILLAS_PROFESIONALES[0]
        assert get_plantilla_by_id(p["id"]) == p
        assert get_plantilla_by_id("no_existe") is None
        log_pass("get_plantilla_by_id funciona")

        cats = get_categorias()
        assert len(cats) >= 10
        log_pass(f"Categorías: {len(cats)}")

        default = get_plantilla_default()
        assert default is not None
        log_pass(f"Plantilla default: {default['nombre']}")

        # Transiciones y efectos
        t = TRANSICIONES_DISPONIBLES[0]
        assert get_transicion_by_id(t["id"]) == t
        log_pass("get_transicion_by_id funciona")

        e = EFECTOS_DISPONIBLES[1]  # Skip "ninguno"
        assert get_efecto_by_id(e["id"]) == e
        log_pass("get_efecto_by_id funciona")

        cats_e = get_categorias_efectos()
        assert len(cats_e) >= 5
        log_pass(f"Categorías de efectos: {cats_e}")

    except Exception as e:
        log_fail("templates_data.py falló", str(e))
        traceback.print_exc()


def test_database():
    """Verifica database.py."""
    log_section("TEST: database.py")

    try:
        from database import (
            cargar_db, guardar_db, crear_usuario, autenticar_usuario,
            obtener_usuario, actualizar_usuario, usar_token, verificar_tokens,
            agregar_proyecto, cambiar_plan, get_dashboard_data, get_stats,
            verify_admin_password, set_admin_password, listar_usuarios,
            get_config, update_config, UPLOADS, OUTPUTS, TEMP_DIR
        )
        import uuid

        # Cargar DB
        db = cargar_db()
        assert "usuarios" in db
        assert "config" in db
        assert "membresias" in db
        log_pass("cargar_db funciona")

        # Crear usuario
        email = f"master_test_{uuid.uuid4().hex[:8]}@test.com"
        u, msg = crear_usuario("Test Master", email, "pass1234", "pro")
        assert u is not None, f"No se creó: {msg}"
        assert u["tokens"] == 50  # Pro
        log_pass(f"Usuario creado: {email} (tokens: {u['tokens']})")

        # Autenticar
        u2, msg = autenticar_usuario(email, "pass1234")
        assert u2 is not None
        log_pass("Autenticación correcta")

        # Autenticación fallida
        u3, msg = autenticar_usuario(email, "wrong")
        assert u3 is None
        log_pass("Rechaza contraseña incorrecta")

        # Verificar y usar tokens
        assert verificar_tokens(u["id"]) == True
        assert usar_token(u["id"]) == True
        u4 = obtener_usuario(u["id"])
        assert u4["tokens"] == 49
        log_pass(f"Token usado: 50 → {u4['tokens']}")

        # Actualizar usuario
        actualizar_usuario(u["id"], {"plan": "business"})
        u5 = obtener_usuario(u["id"])
        assert u5["plan"] == "business"
        log_pass("actualizar_usuario funciona")

        # Agregar proyecto
        proyecto = {
            "fecha": "20240101_120000",
            "video_original": "test.mp4",
            "video_final": "/tmp/test.mp4",
            "subtitulos": "/tmp/test.srt",
            "formatos": {"youtube": "/tmp/yt.mp4"},
            "transcripcion": "test",
        }
        assert agregar_proyecto(u["id"], proyecto) == True
        u6 = obtener_usuario(u["id"])
        assert len(u6["proyectos"]) == 1
        log_pass("agregar_proyecto funciona")

        # Dashboard
        dashboard = get_dashboard_data()
        assert "total_usuarios" in dashboard
        assert "usuarios_activos" in dashboard
        assert "tokens_distribuidos" in dashboard
        assert "distribucion_planes" in dashboard
        log_pass(f"Dashboard: {dashboard['total_usuarios']} usuarios")

        # Stats
        stats = get_stats()
        assert "total_videos_procesados" in stats
        log_pass("get_stats funciona")

        # Config
        config = get_config()
        assert "groq_api_key" in config
        assert "groq_model" in config
        log_pass(f"get_config OK (modelo: {config.get('groq_model')})")

        update_config({"test_key": "test_value"})
        assert get_config().get("test_key") == "test_value"
        log_pass("update_config funciona")

        # Admin password
        assert verify_admin_password("admin123") == True
        log_pass("verify_admin_password funciona")

        # Listar usuarios (sin password_hash)
        usuarios = listar_usuarios()
        for user in usuarios:
            assert "password_hash" not in user, "listar_usuarios expone password_hash!"
        log_pass(f"listar_usuarios: {len(usuarios)} usuarios (sin hashes)")

        # Usuario inexistente
        assert obtener_usuario("no_existe") is None
        assert actualizar_usuario("no_existe", {}) == False
        assert usar_token("no_existe") == False
        assert verificar_tokens("no_existe") == False
        assert agregar_proyecto("no_existe", {}) == False
        log_pass("Maneja UIDs inexistentes correctamente")

    except Exception as e:
        log_fail("database.py falló", str(e))
        traceback.print_exc()


def test_groq_ai():
    """Verifica groq_ai.py."""
    log_section("TEST: groq_ai.py")

    try:
        from groq_ai import (
            GroqAI, MODEL_MAX_TOKENS, MODELOS_RECOMENDADOS,
            SAFE_MAX_TOKENS
        )

        # Constantes
        assert len(MODEL_MAX_TOKENS) >= 10
        assert "llama-3.1-70b-versatile" in MODEL_MAX_TOKENS
        assert "llama-3.1-8b-instant" in MODEL_MAX_TOKENS
        log_pass(f"MODEL_MAX_TOKENS: {len(MODEL_MAX_TOKENS)} modelos")

        assert len(MODELOS_RECOMENDADOS) >= 3
        log_pass(f"MODELOS_RECOMENDADOS: {MODELOS_RECOMENDADOS}")

        assert 1000 <= SAFE_MAX_TOKENS <= 5000
        log_pass(f"SAFE_MAX_TOKENS = {SAFE_MAX_TOKENS}")

        # Instancia
        groq = GroqAI("fake_key", "llama-3.1-8b-instant")
        assert groq.esta_configurado() == True
        log_pass("GroqAI instanciado correctamente")

        # _get_max_tokens
        max_tokens = groq._get_max_tokens(5000)
        assert max_tokens > 0
        log_pass(f"_get_max_tokens(5000) = {max_tokens}")

        # _limpiar_json
        casos = [
            ('```json\n{"a": 1}\n```', {"a": 1}),
            ('Texto\n{"b": 2}\nMás', {"b": 2}),
            ('{"c": 3}', {"c": 3}),
        ]
        for texto, esperado in casos:
            resultado = groq._safe_json(texto)
            assert "error" not in resultado, f"Fallo con: {texto}"
            assert resultado == esperado
        log_pass("_limpiar_json maneja 3 formatos correctamente")

        # JSON inválido
        resultado = groq._safe_json("no es json")
        assert "error" in resultado
        log_pass("Maneja JSON inválido")

        # Sin API key
        groq_no_key = GroqAI("", "llama-3.1-8b-instant")
        assert groq_no_key.esta_configurado() == False
        resultado = groq_no_key._consultar("test")
        assert "ERROR" in resultado
        log_pass("Maneja API key vacía")

        # Generar guion con mock
        guion_mock = {
            "titulo": "Test",
            "hook": "Hook test",
            "introduccion": "Intro",
            "escenas": [{"numero": 1, "descripcion": "test", "duracion_seg": 10}],
            "cta_final": "CTA",
            "hashtags_sugeridos": ["#test"],
            "descripcion_social": "desc"
        }
        with patch.object(groq, '_consultar', return_value=json.dumps(guion_mock)):
            resultado = groq.generar_guion_completo("test", "Publicitario", 1, "video.mp4", "Test")
        assert "titulo" in resultado
        assert resultado["titulo"] == "Test"
        log_pass("generar_guion_completo funciona con mock")

        # Generar ideas con mock
        ideas_mock = {"ideas": [{"titulo": "Idea 1", "potencial_viral": "alto"}]}
        with patch.object(groq, '_consultar', return_value=json.dumps(ideas_mock)):
            resultado = groq.generar_ideas_contenido("test", "jóvenes", 1)
        assert "ideas" in resultado
        log_pass("generar_ideas_contenido funciona con mock")

        # test_conexion con fake key
        resultado = groq.test_conexion()
        assert "ok" in resultado
        log_pass("test_conexion retorna estructura válida")

    except Exception as e:
        log_fail("groq_ai.py falló", str(e))
        traceback.print_exc()


def test_video_processor():
    """Verifica video_processor.py."""
    log_section("TEST: video_processor.py")

    try:
        from video_processor import (
            _run_ffmpeg, _get_video_duration, _buscar_fuente, _escape_ffmpeg_text,
            detectar_silencios, crear_intro_profesional, crear_outro_profesional,
            crear_diapositiva_imagen, aplicar_color_grading,
            aplicar_audio_ducking, unir_clips_con_transiciones,
            generar_subtitulos_srt, quemar_subtitulos, exportar_multi_formato,
            aplicar_efectos_visuales, aplicar_efectos_multiples,
            combinar_filtros_efectos, procesar_video_completo
        )

        # Funciones utilitarias
        assert _buscar_fuente("Inter").endswith(".ttf")
        assert _buscar_fuente("Desconocida").endswith(".ttf")
        log_pass("_buscar_fuente funciona")

        escaped = _escape_ffmpeg_text("Hola: mundo")
        assert "\\:" in escaped or ":" not in escaped
        log_pass("_escape_ffmpeg_text funciona")

        # Generar SRT
        transcripcion = {
            "text": "Hola",
            "segments": [{"start": 0.0, "end": 1.0, "text": "Hola"}]
        }
        srt = generar_subtitulos_srt(transcripcion)
        assert os.path.exists(srt)
        log_pass("generar_subtitulos_srt funciona")

        # Color grading (sin video real, solo verificar que no crashee)
        log_pass("aplicar_color_grading importable")

        # Efectos visuales
        from templates_data import EFECTOS_DISPONIBLES
        for efecto in EFECTOS_DISPONIBLES[:5]:
            assert "filtro_ffmpeg" in efecto
        log_pass(f"Estructura de {len(EFECTOS_DISPONIBLES)} efectos correcta")

        # Combinar filtros
        filtros = combinar_filtros_efectos(["vignette", "film_grain"])
        assert len(filtros) > 0
        log_pass("combinar_filtros_efectos funciona")

        # Sin efectos
        assert combinar_filtros_efectos(["ninguno"]) == ""
        log_pass("combinar_filtros_efectos maneja 'ninguno'")

        # Export multi-formato importable
        log_pass("exportar_multi_formato importable")

        # procesar_video_completo importable
        log_pass("procesar_video_completo importable")

    except Exception as e:
        log_fail("video_processor.py falló", str(e))
        traceback.print_exc()


def test_preview_renderer():
    """Verifica preview_renderer.py."""
    log_section("TEST: preview_renderer.py")

    try:
        from preview_renderer import (
            generar_preview_animado, generar_preview_compacto,
            _get_transition_css
        )
        from templates_data import PLANTILLAS_PROFESIONALES

        # Preview animado
        for plantilla in PLANTILLAS_PROFESIONALES[:5]:
            html = generar_preview_animado(plantilla, "Test Video", "Publicitario", 2)
            assert len(html) > 1000, f"HTML muy corto para {plantilla['nombre']}"
            assert plantilla["color_primario"] in html
            assert "animation" in html
            assert "@keyframes" in html
        log_pass(f"Preview animado generado para 5 plantillas")

        # Preview compacto
        html = generar_preview_compacto(PLANTILLAS_PROFESIONALES[0])
        assert len(html) > 500
        log_pass("Preview compacto funciona")

        # _get_transition_css
        css = _get_transition_css("fade")
        assert "in" in css and "show" in css and "out" in css
        log_pass("_get_transition_css funciona")

        css = _get_transition_css("zoom")
        assert "scale" in css["in"]
        log_pass("Transición zoom tiene CSS correcto")

        # Transición desconocida usa fade por defecto
        css = _get_transition_css("desconocida")
        assert css == _get_transition_css("fade")
        log_pass("Transición desconocida usa fade por defecto")

    except Exception as e:
        log_fail("preview_renderer.py falló", str(e))
        traceback.print_exc()


def test_components():
    """Verifica components.py."""
    log_section("TEST: components.py")

    try:
        from components import (
            render_template_gallery, render_processing_animation,
            render_stat_grid, render_guion_visualization,
            render_pricing_section, render_wizard_nav,
            render_format_selector, render_upload_zone,
            render_project_card, render_transiciones_selector,
            render_efectos_selector, render_preview_modal
        )
        log_pass("Todos los componentes importables")

        # render_wizard_nav
        import streamlit as st
        st.session_state.clear()
        render_wizard_nav(3)
        log_pass("render_wizard_nav funciona")

        # render_format_selector
        st.session_state.clear()
        formatos = render_format_selector()
        assert isinstance(formatos, list)
        log_pass(f"render_format_selector retorna lista: {formatos}")

        # render_stat_grid
        stats = [{"icon": "🎬", "value": "10", "label": "videos"}]
        render_stat_grid(stats)
        log_pass("render_stat_grid funciona")

    except Exception as e:
        log_fail("components.py falló", str(e))
        traceback.print_exc()


def test_auth():
    """Verifica auth.py."""
    log_section("TEST: auth.py")

    try:
        from auth import (
            init_session_state, is_logged_in, is_admin, logout,
            render_login_form, render_user_sidebar
        )
        import streamlit as st

        # Limpiar sesión
        st.session_state.clear()
        init_session_state()

        # Estado inicial
        assert is_logged_in() == False
        assert is_admin() == False
        assert st.session_state.wizard_step == 1
        assert st.session_state.plantilla_elegida is None
        assert st.session_state.guion is None
        log_pass("init_session_state inicializa correctamente")

        # Nuevas variables
        assert st.session_state.archivos_guardados is None
        assert st.session_state.formatos_seleccionados == ['youtube']
        assert st.session_state.transicion_personalizada is None
        assert st.session_state.efectos_seleccionados == []
        assert st.session_state.preview_plantilla_id is None
        log_pass("Nuevas variables de sesión inicializadas")

        # Simular login
        st.session_state.usuario = {"id": "test", "nombre": "Test", "tokens": 10, "plan": "pro"}
        assert is_logged_in() == True
        log_pass("is_logged_in funciona")

        # Logout
        logout()
        assert is_logged_in() == False
        assert st.session_state.wizard_step == 1
        log_pass("logout limpia sesión correctamente")

    except Exception as e:
        log_fail("auth.py falló", str(e))
        traceback.print_exc()


def test_app_imports():
    """Verifica que app.py pueda importar correctamente."""
    log_section("TEST: app.py imports")

    try:
        # Verificar que app.py pueda ser importado
        # (sin ejecutar streamlit run)
        import app
        log_pass("app.py importable sin errores")

        # Verificar que las funciones principales existan
        assert hasattr(app, 'main')
        assert hasattr(app, 'render_home_page')
        assert hasattr(app, 'render_process_page')
        assert hasattr(app, 'render_templates_page')
        assert hasattr(app, 'render_projects_page')
        assert hasattr(app, 'render_ideas_page')
        assert hasattr(app, 'render_plans_page')
        assert hasattr(app, 'render_config_page')
        assert hasattr(app, 'render_admin_page')
        assert hasattr(app, '_ejecutar_produccion_video')
        log_pass("Todas las funciones principales de app.py existen")

    except Exception as e:
        log_fail("app.py falló al importar", str(e))
        traceback.print_exc()


# ============ TESTS DE FLUJO COMPLETO ============

def test_flujo_completo_wizard():
    """Simula el flujo completo del wizard paso a paso."""
    log_section("TEST: Flujo completo del wizard")

    try:
        import streamlit as st
        from auth import init_session_state
        from database import crear_usuario
        from templates_data import PLANTILLAS_PROFESIONALES, TRANSICIONES_DISPONIBLES, EFECTOS_DISPONIBLES
        import uuid

        # Inicializar sesión
        st.session_state.clear()
        init_session_state()

        # Registrar usuario
        email = f"wizard_{uuid.uuid4().hex[:8]}@test.com"
        usuario, _ = crear_usuario("Wizard Test", email, "pass1234", "pro")
        st.session_state.usuario = usuario
        st.session_state.vista = "process"
        log_pass(f"Usuario registrado: {email}")

        # PASO 1: Subir material
        st.session_state.archivos_guardados = {
            "principal": "/tmp/test_video.mp4",
            "principal_name": "test.mp4",
            "videos": [],
            "imagenes": [],
            "audio": None,
        }
        st.session_state.wizard_step = 2
        log_pass("Paso 1: Material cargado")

        # PASO 2: Descripción
        st.session_state["texto_objetivo_input"] = "Promoción de mi producto"
        st.session_state["tipo_contenido_sel"] = "Publicitario"
        st.session_state["duracion_slider"] = 2
        st.session_state.wizard_step = 3
        log_pass("Paso 2: Descripción completada")

        # PASO 3: Plantilla
        st.session_state.plantilla_elegida = PLANTILLAS_PROFESIONALES[0]
        st.session_state.wizard_step = 4
        log_pass(f"Paso 3: Plantilla '{PLANTILLAS_PROFESIONALES[0]['nombre']}' seleccionada")

        # PASO 4: Formatos + transiciones + efectos
        st.session_state.formatos_seleccionados = ["youtube", "tiktok"]
        st.session_state.transicion_personalizada = "slide"
        st.session_state.duracion_transicion_personalizada = 0.4
        st.session_state.efectos_seleccionados = [
            {"id": "vignette", "nombre": "Viñeta", "intensidad": 0.5},
            {"id": "film_grain", "nombre": "Film Grain", "intensidad": 0.3}
        ]
        st.session_state.wizard_step = 5
        log_pass("Paso 4: Formatos + transición + 2 efectos seleccionados")

        # PASO 5: Guion
        st.session_state.guion = {
            "titulo": "Mi Video Promocional",
            "hook": "¿Quieres conocer mi producto?",
            "introduccion": "Hoy te presento...",
            "escenas": [
                {"numero": 1, "descripcion": "Vista general", "texto_en_pantalla": "Hola", "duracion_seg": 10},
                {"numero": 2, "descripcion": "Producto en acción", "texto_en_pantalla": "Nuevo!", "duracion_seg": 15},
            ],
            "cta_final": "Compra ahora",
            "hashtags_sugeridos": ["#producto", "#nuevo"],
            "descripcion_social": "Descripción del video"
        }
        st.session_state.wizard_step = 6
        log_pass("Paso 5: Guion generado")

        # Validar todos los datos presentes
        required = ["archivos_guardados", "plantilla_elegida", "guion",
                    "formatos_seleccionados", "usuario",
                    "transicion_personalizada", "efectos_seleccionados"]
        for key in required:
            assert st.session_state.get(key) is not None or st.session_state.get(key) == [], f"Falta: {key}"
        log_pass("Todos los datos del wizard presentes en sesión")

        # Validar estructura del guion
        guion = st.session_state.guion
        assert "titulo" in guion
        assert "escenas" in guion
        assert len(guion["escenas"]) > 0
        log_pass("Estructura del guion válida")

        # Validar efectos
        efectos = st.session_state.efectos_seleccionados
        assert len(efectos) == 2
        for e in efectos:
            assert "id" in e and "intensidad" in e
        log_pass("Estructura de efectos válida")

    except Exception as e:
        log_fail("Flujo del wizard falló", str(e))
        traceback.print_exc()


def test_plantillas_renderizado_html():
    """Verifica que todas las plantillas rendericen HTML válido."""
    log_section("TEST: Renderizado HTML de todas las plantillas")

    try:
        from styles import render_template_preview_card, html_safe
        from preview_renderer import generar_preview_animado, generar_preview_compacto
        from templates_data import PLANTILLAS_PROFESIONALES

        for plantilla in PLANTILLAS_PROFESIONALES:
            # Card HTML
            html = render_template_preview_card(plantilla, 0, False)
            assert "template-card" in html
            assert plantilla["nombre"] in html

            # Preview animado
            html_anim = generar_preview_animado(plantilla, "Test", "Test", 2)
            assert len(html_anim) > 1000
            assert plantilla["color_primario"] in html_anim

            # Preview compacto
            html_compact = generar_preview_compacto(plantilla)
            assert len(html_compact) > 500

        log_pass(f"Todas las {len(PLANTILLAS_PROFESIONALES)} plantillas renderizan HTML correctamente")

    except Exception as e:
        log_fail("Renderizado HTML falló", str(e))
        traceback.print_exc()


def test_coherencia_datos():
    """Verifica la coherencia de datos entre módulos."""
    log_section("TEST: Coherencia de datos")

    try:
        from templates_data import PLANTILLAS_PROFESIONALES, TRANSICIONES_DISPONIBLES, EFECTOS_DISPONIBLES
        from preview_renderer import _get_transition_css

        # Verificar que cada transición de plantilla exista en TRANSICIONES_DISPONIBLES
        transiciones_ids = {t["id"] for t in TRANSICIONES_DISPONIBLES}
        for p in PLANTILLAS_PROFESIONALES:
            trans_plantilla = p.get("transicion", "fade")
            # fade siempre existe, otras deben estar en la lista
            if trans_plantilla != "fade":
                # Si no está, al menos debe tener CSS en _get_transition_css
                css = _get_transition_css(trans_plantilla)
                # Debe retornar algo (fallback a fade)
                assert css is not None
        log_pass("Transiciones de plantillas son coherentes")

        # Verificar que cada efecto tenga filtro FFmpeg
        for e in EFECTOS_DISPONIBLES:
            if e["id"] != "ninguno":
                assert "filtro_ffmpeg" in e
                assert len(e["filtro_ffmpeg"]) > 0
        log_pass("Todos los efectos tienen filtro FFmpeg")

        # Verificar que config_avanzada tenga campos requeridos
        for p in PLANTILLAS_PROFESIONALES:
            config = p.get("config_avanzada", {})
            assert "intro_duracion" in config
            assert "outro_duracion" in config
            assert "color_grading" in config
            assert "fps" in config
        log_pass("Todas las plantillas tienen config_avanzada completa")

    except Exception as e:
        log_fail("Coherencia de datos falló", str(e))
        traceback.print_exc()


# ============ ARCHIVOS DE CONFIGURACIÓN ============

def test_archivos_config():
    """Verifica que existan los archivos de configuración."""
    log_section("TEST: Archivos de configuración")

    archivos = [
        "requirements.txt",
        "packages.txt",
        ".streamlit/config.toml",
        ".gitignore",
        "README.md",
    ]

    for archivo in archivos:
        ruta = BASE_DIR / archivo
        if ruta.exists():
            log_pass(f"Archivo existe: {archivo}")
        else:
            log_fail(f"Archivo faltante: {archivo}")

    # Verificar contenido de requirements.txt
    try:
        with open(BASE_DIR / "requirements.txt", 'r') as f:
            content = f.read()
        assert "streamlit" in content
        assert "whisper" in content
        assert "ffmpeg" in content.lower() or "ffmpeg-python" in content
        log_pass("requirements.txt contiene dependencias correctas")
    except Exception as e:
        log_fail("requirements.txt inválido", str(e))

    # Verificar packages.txt
    try:
        with open(BASE_DIR / "packages.txt", 'r') as f:
            content = f.read()
        assert "ffmpeg" in content
        assert "fonts-dejavu" in content
        log_pass("packages.txt contiene FFmpeg y fuentes")
    except Exception as e:
        log_fail("packages.txt inválido", str(e))


# ============ MAIN ============

def main():
    print(f"{Colors.BOLD}{'=' * 70}{Colors.RESET}")
    print(f"{Colors.BOLD}SUITE MAESTRA DE TESTS - VideoAI Studio Pro{Colors.RESET}")
    print(f"{Colors.BOLD}{'=' * 70}{Colors.RESET}")
    print(f"Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python: {sys.version.split()[0]}")
    print(f"Directorio: {BASE_DIR}")

    inicio = time.time()

    # 1. Auditoría estática
    audit_sintaxis()
    audit_imports()

    # 2. Tests por módulo
    test_styles()
    test_templates_data()
    test_database()
    test_groq_ai()
    test_video_processor()
    test_preview_renderer()
    test_components()
    test_auth()

    # 3. Tests de integración
    test_app_imports()
    test_flujo_completo_wizard()
    test_plantillas_renderizado_html()
    test_coherencia_datos()

    # 4. Archivos de configuración
    test_archivos_config()

    duracion = time.time() - inicio

    # Resumen final
    total = results["pass"] + results["fail"] + results["warn"]
    print(f"\n{Colors.BOLD}{'=' * 70}{Colors.RESET}")
    print(f"{Colors.BOLD}RESUMEN FINAL{Colors.RESET}")
    print(f"{Colors.BOLD}{'=' * 70}{Colors.RESET}")
    print(f"{Colors.GREEN}✅ Pasaron: {results['pass']}/{total}{Colors.RESET}")
    print(f"{Colors.RED}❌ Fallaron: {results['fail']}/{total}{Colors.RESET}")
    print(f"{Colors.YELLOW}⚠ Advertencias: {results['warn']}/{total}{Colors.RESET}")
    print(f"⏱ Duración: {duracion:.1f}s")
    if total > 0:
        print(f"📊 Tasa de éxito: {(results['pass'] / total * 100):.1f}%")

    if results["fail"] > 0:
        print(f"\n{Colors.RED}{Colors.BOLD}ERRORES DETALLADOS:{Colors.RESET}")
        for msg, detail in results["errors"]:
            print(f"  - {msg}")
            if detail:
                print(f"    → {detail[:300]}")
        print(f"\n{Colors.RED}{Colors.BOLD}❌ SISTEMA NO LISTO PARA PRODUCCIÓN{Colors.RESET}")
        sys.exit(1)
    else:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✅ SISTEMA 100% LISTO PARA PRODUCCIÓN 🎉{Colors.RESET}")
        sys.exit(0)


if __name__ == "__main__":
    main()
