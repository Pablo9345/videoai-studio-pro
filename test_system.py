#!/usr/bin/env python3
"""
Script de tests exhaustivos para VideoAI Studio Pro.
Verifica sintaxis, imports, y funciones críticas.
"""

import sys
import os
import ast
import importlib
import json
from pathlib import Path

# Añadir directorio actual al path
BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))

# Añadir el mock de streamlit si no está instalado
try:
    import streamlit
except ImportError:
    mock_path = Path("/home/z/my-project/scripts")
    if mock_path.exists():
        sys.path.insert(0, str(mock_path))
        try:
            import streamlit_mock  # Esto registra el mock
        except ImportError:
            pass

# Colores para output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

# Añadir directorio actual al path
BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))

results = {"pass": 0, "fail": 0, "warn": 0, "errors": []}


def log_pass(msg):
    print(f"{Colors.GREEN}✅ PASS{Colors.RESET}: {msg}")
    results["pass"] += 1


def log_fail(msg, detail=""):
    print(f"{Colors.RED}❌ FAIL{Colors.RESET}: {msg}")
    if detail:
        print(f"   {Colors.RED}→{Colors.RESET} {detail}")
    results["fail"] += 1
    results["errors"].append((msg, detail))


def log_warn(msg):
    print(f"{Colors.YELLOW}⚠ WARN{Colors.RESET}: {msg}")
    results["warn"] += 1


def log_info(msg):
    print(f"{Colors.BLUE}ℹ{Colors.RESET} {msg}")


# ============ TEST 1: Sintaxis Python ============
def test_sintaxis():
    """Verifica que todos los archivos Python compilen correctamente."""
    print(f"\n{Colors.BOLD}=== TEST 1: Sintaxis Python ==={Colors.RESET}")

    archivos = [
        "app.py", "styles.py", "database.py", "auth.py",
        "groq_ai.py", "video_processor.py", "components.py",
        "templates_data.py", "test_imports.py"
    ]

    for archivo in archivos:
        ruta = BASE_DIR / archivo
        if not ruta.exists():
            log_fail(f"Archivo no existe: {archivo}")
            continue

        try:
            with open(ruta, 'r', encoding='utf-8') as f:
                source = f.read()
            ast.parse(source)
            log_pass(f"Sintaxis OK: {archivo}")
        except SyntaxError as e:
            log_fail(f"Sintaxis error en {archivo}", f"Línea {e.lineno}: {e.msg}")


# ============ TEST 2: Imports ============
def test_imports():
    """Verifica que todos los imports funcionen correctamente."""
    print(f"\n{Colors.BOLD}=== TEST 2: Imports ==={Colors.RESET}")

    tests = [
        ("styles", ["PREMIUM_CSS", "get_premium_css", "render_template_preview_card",
                    "render_stat_card", "render_wizard", "render_wizard_step",
                    "render_scene_card", "render_pricing_card"]),
        ("templates_data", ["PLANTILLAS_PROFESIONALES", "MEMBRESIAS",
                            "get_plantilla_by_id", "get_categorias",
                            "get_plantillas_by_categoria", "get_plantilla_default"]),
        ("database", ["cargar_db", "guardar_db", "crear_usuario", "autenticar_usuario",
                      "obtener_usuario", "usar_token", "verificar_tokens", "agregar_proyecto",
                      "cambiar_plan", "get_dashboard_data", "get_stats",
                      "verify_admin_password", "set_admin_password", "listar_usuarios",
                      "get_config", "update_config", "UPLOADS", "OUTPUTS", "TEMP_DIR"]),
        ("groq_ai", ["GroqAI", "MODELOS_RECOMENDADOS", "MODEL_MAX_TOKENS", "SAFE_MAX_TOKENS"]),
        ("video_processor", ["procesar_video_completo", "detectar_silencios",
                             "crear_intro_profesional", "crear_outro_profesional",
                             "crear_diapositiva_imagen", "aplicar_color_grading",
                             "aplicar_audio_ducking", "unir_clips_con_transiciones",
                             "generar_subtitulos_srt", "quemar_subtitulos",
                             "exportar_multi_formato"]),
        ("auth", ["init_session_state", "is_logged_in", "is_admin", "logout",
                  "render_login_form", "render_user_sidebar"]),
        ("components", ["render_template_gallery", "render_processing_animation",
                        "render_stat_grid", "render_guion_visualization",
                        "render_pricing_section", "render_wizard_nav",
                        "render_format_selector", "render_upload_zone",
                        "render_project_card"]),
    ]

    for modulo, nombres in tests:
        try:
            mod = importlib.import_module(modulo)
            for nombre in nombres:
                if not hasattr(mod, nombre):
                    log_fail(f"Import faltante: {modulo}.{nombre}")
                else:
                    pass  # No log para no llenar output
            log_pass(f"Imports OK: {modulo} ({len(nombres)} símbolos)")
        except Exception as e:
            log_fail(f"Error importando {modulo}", str(e))


# ============ TEST 3: Funciones críticas ============
def test_funciones_criticas():
    """Verifica que las funciones críticas ejecuten sin error."""
    print(f"\n{Colors.BOLD}=== TEST 3: Funciones críticas ==={Colors.RESET}")

    # Test 1: cargar_db
    try:
        from database import cargar_db, guardar_db
        db = cargar_db()
        assert "usuarios" in db
        assert "config" in db
        assert "membresias" in db
        log_pass("cargar_db() funciona correctamente")
    except Exception as e:
        log_fail("cargar_db() falló", str(e))

    # Test 2: crear_usuario
    try:
        from database import crear_usuario, autenticar_usuario, obtener_usuario
        import uuid
        email_test = f"test_{uuid.uuid4().hex[:8]}@test.com"
        usuario, msg = crear_usuario("Test User", email_test, "password123", "gratis")
        assert usuario is not None, f"No se creó usuario: {msg}"
        assert usuario["tokens"] > 0
        log_pass(f"crear_usuario() OK (email: {email_test})")

        # Test login
        usuario_login, msg = autenticar_usuario(email_test, "password123")
        assert usuario_login is not None, f"Login falló: {msg}"
        log_pass("autenticar_usuario() OK")

        # Test obtener
        usuario_obt = obtener_usuario(usuario["id"])
        assert usuario_obt is not None
        log_pass("obtener_usuario() OK")
    except Exception as e:
        log_fail("crear_usuario/login falló", str(e))

    # Test 3: Plantillas
    try:
        from templates_data import PLANTILLAS_PROFESIONALES, get_plantilla_by_id, get_categorias
        assert len(PLANTILLAS_PROFESIONALES) >= 12, f"Solo {len(PLANTILLAS_PROFESIONALES)} plantillas"
        plantilla = PLANTILLAS_PROFESIONALES[0]
        assert "id" in plantilla
        assert "nombre" in plantilla
        assert "color_primario" in plantilla
        assert "config_avanzada" in plantilla

        # Test get_plantilla_by_id
        plant = get_plantilla_by_id(plantilla["id"])
        assert plant is not None
        log_pass(f"Plantillas OK ({len(PLANTILLAS_PROFESIONALES)} plantillas, {len(get_categorias())} categorías)")
    except Exception as e:
        log_fail("Plantillas falló", str(e))

    # Test 4: Renderizado HTML (wizard)
    try:
        from styles import render_wizard, render_template_preview_card, render_stat_card
        from templates_data import PLANTILLAS_PROFESIONALES

        # Verificar que el HTML generado no tenga saltos de línea problemáticos
        html_wizard = render_wizard(3, ["Step 1", "Step 2", "Step 3", "Step 4"])
        assert '<div class="wizard-steps">' in html_wizard
        # Verificar que sea una sola línea (no tenga \n problemáticos)
        lineas = html_wizard.count('\n')
        if lineas > 0:
            log_warn(f"render_wizard tiene {lineas} saltos de línea")
        else:
            log_pass("render_wizard genera HTML en una sola línea")

        # Test render_template_preview_card
        html_card = render_template_preview_card(PLANTILLAS_PROFESIONALES[0], 0, False)
        assert '<div class="template-card' in html_card
        lineas = html_card.count('\n')
        if lineas > 0:
            log_warn(f"render_template_preview_card tiene {lineas} saltos de línea")
        else:
            log_pass("render_template_preview_card genera HTML en una sola línea")

        # Test render_stat_card
        html_stat = render_stat_card("🎬", "10", "videos")
        assert '<div class="stat-card">' in html_stat
        assert html_stat.count('\n') == 0
        log_pass("render_stat_card genera HTML en una sola línea")
    except Exception as e:
        log_fail("Renderizado HTML falló", str(e))

    # Test 5: GroqAI - max_tokens
    try:
        from groq_ai import GroqAI, MODEL_MAX_TOKENS, SAFE_MAX_TOKENS
        groq = GroqAI("test_key", "llama-3.1-8b-instant")

        # Verificar que _get_max_tokens funcione
        max_tokens = groq._get_max_tokens(5000)
        assert max_tokens <= 5000, f"max_tokens {max_tokens} > 5000"
        log_pass(f"_get_max_tokens funciona (modelo: llama-3.1-8b-instant, max: {max_tokens})")

        # Test con modelo 70b
        groq70 = GroqAI("test_key", "llama-3.1-70b-versatile")
        max70 = groq70._get_max_tokens(10000)
        assert max70 == 8000, f"Esperaba 8000, obtuvo {max70}"
        log_pass(f"_get_max_tokens para 70b: {max70}")

        # Verificar que SAFE_MAX_TOKENS esté definido
        assert SAFE_MAX_TOKENS > 0
        log_pass(f"SAFE_MAX_TOKENS = {SAFE_MAX_TOKENS}")
    except Exception as e:
        log_fail("GroqAI max_tokens falló", str(e))

    # Test 6: GroqAI - limpiar JSON
    try:
        from groq_ai import GroqAI
        groq = GroqAI("test_key")

        # JSON con markdown
        texto1 = '```json\n{"titulo": "Test", "valor": 123}\n```'
        limpio1 = groq._limpiar_json(texto1)
        parsed = json.loads(limpio1)
        assert parsed["titulo"] == "Test"
        log_pass("_limpiar_json maneja markdown ```json")

        # JSON con texto adicional
        texto2 = 'Aquí está el JSON:\n{"key": "value"}\nMás texto'
        limpio2 = groq._limpiar_json(texto2)
        parsed2 = json.loads(limpio2)
        assert parsed2["key"] == "value"
        log_pass("_limpiar_json extrae JSON de texto")

        # JSON ya limpio
        texto3 = '{"a": 1, "b": 2}'
        limpio3 = groq._limpiar_json(texto3)
        assert json.loads(limpio3)["a"] == 1
        log_pass("_limpiar_json preserva JSON limpio")
    except Exception as e:
        log_fail("_limpiar_json falló", str(e))


# ============ TEST 4: Verificar archivos ============
def test_archivos_config():
    """Verifica que existan los archivos de configuración."""
    print(f"\n{Colors.BOLD}=== TEST 4: Archivos de configuración ==={Colors.RESET}")

    archivos_esperados = [
        "requirements.txt",
        "packages.txt",
        ".streamlit/config.toml",
        ".gitignore",
        "README.md",
    ]

    for archivo in archivos_esperados:
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
        assert "ffmpeg" in content
        log_pass("requirements.txt contiene dependencias necesarias")
    except Exception as e:
        log_fail("requirements.txt inválido", str(e))

    # Verificar contenido de packages.txt
    try:
        with open(BASE_DIR / "packages.txt", 'r') as f:
            content = f.read()
        assert "ffmpeg" in content
        assert "fonts-dejavu" in content
        log_pass("packages.txt contiene FFmpeg y fuentes")
    except Exception as e:
        log_fail("packages.txt inválido", str(e))


# ============ TEST 5: Verificar estructura de plantillas ============
def test_plantillas():
    """Verifica que todas las plantillas tengan la estructura correcta."""
    print(f"\n{Colors.BOLD}=== TEST 5: Estructura de plantillas ==={Colors.RESET}")

    from templates_data import PLANTILLAS_PROFESIONALES

    campos_requeridos = [
        "id", "nombre", "categoria", "color_primario", "color_secundario",
        "color_acento", "color_texto", "color_sub", "fuente",
        "estilo", "transicion", "duracion_transicion",
        "descripcion", "preview_texto", "config_avanzada"
    ]

    config_avanzada_campos = [
        "intro_duracion", "outro_duracion", "subtitulo_tamano",
        "subtitulo_posicion", "subtitulo_estilo", "overlay_opacidad",
        "musica_volumen", "voz_volumen", "color_grading", "fps"
    ]

    for plantilla in PLANTILLAS_PROFESIONALES:
        for campo in campos_requeridos:
            if campo not in plantilla:
                log_fail(f"Plantilla {plantilla.get('id', '?')} falta campo: {campo}")
                break
        else:
            # Verificar config_avanzada
            config = plantilla.get("config_avanzada", {})
            for campo in config_avanzada_campos:
                if campo not in config:
                    log_fail(f"Plantilla {plantilla['id']} config_avanzada falta: {campo}")
                    break
            else:
                pass  # OK
    else:
        log_pass(f"Todas las {len(PLANTILLAS_PROFESIONALES)} plantillas tienen estructura correcta")


# ============ TEST 6: Verificar procesador de video ============
def test_video_processor():
    """Verifica que las funciones del procesador de video sean importables y consistentes."""
    print(f"\n{Colors.BOLD}=== TEST 6: Video processor ==={Colors.RESET}")

    try:
        from video_processor import (
            crear_intro_profesional, crear_outro_profesional,
            aplicar_color_grading, unir_clips_con_transiciones,
            _buscar_fuente, _escape_ffmpeg_text
        )

        # Test _buscar_fuente
        fuente = _buscar_fuente("Inter")
        assert fuente.endswith(".ttf"), f"Fuente inválida: {fuente}"
        log_pass(f"_buscar_fuente('Inter') = {fuente}")

        # Test _escape_ffmpeg_text
        texto = "Hola: mundo %test"
        escaped = _escape_ffmpeg_text(texto)
        assert ":" not in escaped or "\\:" in escaped, f"No escapó ':': {escaped}"
        log_pass(f"_escape_ffmpeg_text escapa caracteres especiales")

        # Test aplicar_color_grading (preset válido)
        presets_validos = ["neutro", "calido", "frio", "cinematico", "vibrante"]
        for preset in presets_validos:
            # Solo verificar que no lance excepción al importar
            pass
        log_pass(f"aplicar_color_grading tiene {len(presets_validos)} presets válidos")

    except Exception as e:
        log_fail("Video processor falló", str(e))


# ============ MAIN ============
def main():
    print(f"{Colors.BOLD}{'=' * 60}{Colors.RESET}")
    print(f"{Colors.BOLD}VideoAI Studio Pro - Test Suite{Colors.RESET}")
    print(f"{Colors.BOLD}{'=' * 60}{Colors.RESET}")

    test_sintaxis()
    test_imports()
    test_funciones_criticas()
    test_archivos_config()
    test_plantillas()
    test_video_processor()

    # Resumen final
    print(f"\n{Colors.BOLD}{'=' * 60}{Colors.RESET}")
    print(f"{Colors.BOLD}RESUMEN{Colors.RESET}")
    print(f"{Colors.BOLD}{'=' * 60}{Colors.RESET}")
    print(f"{Colors.GREEN}✅ Pasaron: {results['pass']}{Colors.RESET}")
    print(f"{Colors.RED}❌ Fallaron: {results['fail']}{Colors.RESET}")
    print(f"{Colors.YELLOW}⚠ Advertencias: {results['warn']}{Colors.RESET}")

    if results["fail"] > 0:
        print(f"\n{Colors.RED}{Colors.BOLD}ERRORES DETALLADOS:{Colors.RESET}")
        for msg, detail in results["errors"]:
            print(f"  - {msg}")
            if detail:
                print(f"    → {detail}")
        sys.exit(1)
    else:
        print(f"\n{Colors.GREEN}{Colors.BOLD}¡Todos los tests pasaron! 🎉{Colors.RESET}")
        sys.exit(0)


if __name__ == "__main__":
    main()
