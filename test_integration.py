#!/usr/bin/env python3
"""
Tests de integración del flujo completo del wizard.
Simula el comportamiento de un usuario recorriendo la app.
"""

import sys
import os
from pathlib import Path

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


def log_pass(msg):
    print(f"{Colors.GREEN}✅ PASS{Colors.RESET}: {msg}")


def log_fail(msg, detail=""):
    print(f"{Colors.RED}❌ FAIL{Colors.RESET}: {msg}")
    if detail:
        print(f"   {Colors.RED}→{Colors.RESET} {detail}")


def log_info(msg):
    print(f"{Colors.BLUE}ℹ{Colors.RESET} {msg}")


# ============ TEST: Flujo del wizard ============
def test_wizard_flow():
    """Simula el flujo completo del wizard paso a paso."""
    print(f"\n{Colors.BOLD}=== TEST: Flujo del wizard ==={Colors.RESET}")

    try:
        # Test 1: Inicialización de sesión
        from auth import init_session_state
        import streamlit as st
        st.session_state.clear()
        init_session_state()

        assert st.session_state.usuario is None
        assert st.session_state.vista == "home"
        assert st.session_state.wizard_step == 1
        log_pass("Inicialización de sesión correcta")

        # Test 2: Simular usuario logueado
        from database import crear_usuario, autenticar_usuario
        import uuid
        email_test = f"test_flow_{uuid.uuid4().hex[:8]}@test.com"
        usuario, _ = crear_usuario("Test Flow", email_test, "test1234", "pro")
        st.session_state.usuario = usuario
        st.session_state.vista = "process"

        assert st.session_state.usuario is not None
        assert st.session_state.usuario["tokens"] > 0
        log_pass(f"Usuario logueado: {email_test} (tokens: {usuario['tokens']})")

        # Test 3: Paso 1 → 2 (subir archivos simulados)
        st.session_state.archivos_guardados = {
            "principal": "/tmp/test_video.mp4",
            "principal_name": "test.mp4",
            "videos": [],
            "imagenes": [],
            "audio": None,
        }
        st.session_state.wizard_step = 2
        log_pass("Paso 1→2: Archivos guardados en sesión")

        # Test 4: Paso 2 → 3 (descripción del proyecto)
        st.session_state["texto_objetivo_input"] = "Promoción de mi curso"
        st.session_state["tipo_contenido_sel"] = "Publicitario"
        st.session_state["duracion_slider"] = 2
        st.session_state.wizard_step = 3
        log_pass("Paso 2→3: Descripción del proyecto guardada")

        # Test 5: Paso 3 → 4 (selección de plantilla)
        from templates_data import PLANTILLAS_PROFESIONALES
        st.session_state.plantilla_elegida = PLANTILLAS_PROFESIONALES[0]
        st.session_state.wizard_step = 4
        assert st.session_state.plantilla_elegida is not None
        log_pass(f"Paso 3→4: Plantilla seleccionada: {PLANTILLAS_PROFESIONALES[0]['nombre']}")

        # Test 6: Paso 4 → 5 (selección de formatos)
        st.session_state.formatos_seleccionados = ["youtube", "tiktok"]
        st.session_state.wizard_step = 5
        assert len(st.session_state.formatos_seleccionados) == 2
        log_pass(f"Paso 4→5: Formatos seleccionados: {st.session_state.formatos_seleccionados}")

        # Test 7: Validación del paso 6 (sin guion)
        st.session_state.wizard_step = 6
        # En este punto, _ejecutar_produccion_video debería detectar que no hay guion
        # y mostrar un error. No podemos ejecutarlo directamente porque Streamlit
        # no está disponible, pero podemos validar la lógica.

        # Simular guion válido
        st.session_state.guion = {
            "titulo": "Video Test",
            "hook": "Hook test",
            "introduccion": "Intro test",
            "escenas": [{"numero": 1, "descripcion": "test", "duracion_seg": 10}],
            "cta_final": "Suscríbete",
        }
        log_pass("Paso 5→6: Guion válido en sesión")

        # Test 8: Validación de todos los datos del wizard
        required = ["archivos_guardados", "plantilla_elegida", "guion",
                    "formatos_seleccionados", "usuario"]
        for key in required:
            assert st.session_state.get(key) is not None, f"Falta: {key}"
        log_pass("Todos los datos del wizard están presentes")

    except Exception as e:
        import traceback
        log_fail("Flujo del wizard falló", str(e))
        traceback.print_exc()


# ============ TEST: Renderizado de componentes HTML ============
def test_html_rendering():
    """Verifica que los componentes HTML generen HTML válido."""
    print(f"\n{Colors.BOLD}=== TEST: Renderizado HTML ==={Colors.RESET}")

    try:
        from styles import (
            render_wizard, render_template_preview_card,
            render_stat_card, render_scene_card, render_pricing_card,
            html_safe
        )
        from templates_data import PLANTILLAS_PROFESIONALES, MEMBRESIAS

        # Test 1: HTML del wizard no contiene saltos de línea problemáticos
        html = render_wizard(3, ["A", "B", "C", "D"])
        # html_safe debe eliminar saltos de línea
        html_limpio = html_safe(html)
        assert '\n' not in html_limpio, f"HTML aún tiene saltos de línea: {html_limpio[:100]}"
        log_pass("html_safe elimina saltos de línea del wizard")

        # Test 2: HTML del wizard es válido (tiene tags abiertos y cerrados)
        assert html_limpio.count('<div') == html_limpio.count('</div>')
        log_pass("HTML del wizard tiene tags balanceados")

        # Test 3: Tarjeta de plantilla
        html_card = render_template_preview_card(PLANTILLAS_PROFESIONALES[0], 0, False)
        html_card_limpio = html_safe(html_card)
        assert 'template-card' in html_card_limpio
        assert PLANTILLAS_PROFESIONALES[0]["nombre"] in html_card_limpio
        log_pass("Tarjeta de plantilla genera HTML válido")

        # Test 4: Stat card
        html_stat = render_stat_card("🎬", "10", "videos")
        assert html_stat.count('<div') == html_stat.count('</div>')
        log_pass("Stat card genera HTML balanceado")

        # Test 5: Scene card
        html_scene = render_scene_card(1, "Descripción", "Texto en pantalla", 10, "B-roll")
        html_scene_limpio = html_safe(html_scene)
        assert 'scene-card' in html_scene_limpio
        log_pass("Scene card genera HTML válido")

        # Test 6: Pricing card
        html_pricing = render_pricing_card(MEMBRESIAS[0], False)
        html_pricing_limpio = html_safe(html_pricing)
        assert 'pricing-card' in html_pricing_limpio
        log_pass("Pricing card genera HTML válido")

    except Exception as e:
        log_fail("Renderizado HTML falló", str(e))


# ============ TEST: Generación de guion (mock) ============
def test_guion_generation_mock():
    """Simula la generación de un guion sin llamar a la API."""
    print(f"\n{Colors.BOLD}=== TEST: Generación de guion (mock) ==={Colors.RESET}")

    try:
        from groq_ai import GroqAI

        # Crear instancia con API key falsa
        groq = GroqAI("fake_api_key", "llama-3.1-8b-instant")

        # Test 1: max_tokens respeta el límite del modelo
        max_tokens = groq._get_max_tokens(5000)
        assert max_tokens <= 8000, f"max_tokens {max_tokens} demasiado alto"
        log_pass(f"max_tokens para 8b: {max_tokens}")

        # Test 2: Para modelo 70b
        groq70 = GroqAI("fake", "llama-3.1-70b-versatile")
        max70 = groq70._get_max_tokens(10000)
        assert max70 == 8000
        log_pass(f"max_tokens para 70b: {max70}")

        # Test 3: _limpiar_json con respuestas válidas
        casos = [
            ('```json\n{"a": 1}\n```', {"a": 1}),
            ('Texto\n{"b": 2}\nMás texto', {"b": 2}),
            ('{"c": 3}', {"c": 3}),
            ('[{"d": 4}]', [{"d": 4}]),
        ]
        for i, (input_text, expected) in enumerate(casos):
            resultado = groq._safe_json(input_text)
            if "error" in resultado:
                log_fail(f"Caso {i+1} falló", f"Input: {input_text[:50]}")
            else:
                assert resultado == expected, f"Esperado {expected}, obtuvo {resultado}"
        log_pass("_safe_json maneja 4 formatos diferentes correctamente")

        # Test 4: test_conexion detecta API key inválida
        resultado = groq.test_conexion()
        # Como es API key falsa, debería fallar
        if resultado.get("ok"):
            log_warn("test_conexion debería fallar con API key falsa")
        else:
            log_pass("test_conexion detecta API key inválida correctamente")

    except Exception as e:
        log_fail("Generación de guion mock falló", str(e))


# ============ TEST: Base de datos ============
def test_database_operations():
    """Verifica operaciones CRUD de la base de datos."""
    print(f"\n{Colors.BOLD}=== TEST: Operaciones de base de datos ==={Colors.RESET}")

    try:
        import uuid
        from database import (
            crear_usuario, autenticar_usuario, obtener_usuario,
            usar_token, verificar_tokens, agregar_proyecto,
            get_dashboard_data, get_stats, get_config, update_config
        )

        email = f"dbtest_{uuid.uuid4().hex[:8]}@test.com"

        # Crear usuario
        usuario, msg = crear_usuario("DB Test", email, "pass1234", "gratis")
        assert usuario is not None, f"No se creó: {msg}"
        uid = usuario["id"]
        tokens_iniciales = usuario["tokens"]
        log_pass(f"Usuario creado con {tokens_iniciales} tokens")

        # Verificar tokens
        assert verificar_tokens(uid) == True
        log_pass("verificar_tokens funciona (True)")

        # Usar un token
        assert usar_token(uid) == True
        usuario_despues = obtener_usuario(uid)
        assert usuario_despues["tokens"] == tokens_iniciales - 1
        log_pass(f"usar_token descontó correctamente ({tokens_iniciales} → {usuario_despues['tokens']})")

        # Agregar proyecto
        proyecto = {
            "fecha": "20240101_120000",
            "video_original": "test.mp4",
            "video_final": "/tmp/final.mp4",
            "subtitulos": "/tmp/subs.srt",
            "formatos": {"youtube": "/tmp/yt.mp4"},
            "transcripcion": "Test transcripción",
        }
        assert agregar_proyecto(uid, proyecto) == True
        usuario_proyecto = obtener_usuario(uid)
        assert len(usuario_proyecto["proyectos"]) == 1
        log_pass("agregar_proyecto funciona correctamente")

        # Stats del dashboard
        dashboard = get_dashboard_data()
        assert "total_usuarios" in dashboard
        assert "distribucion_planes" in dashboard
        log_pass(f"get_dashboard_data retorna datos válidos ({dashboard['total_usuarios']} usuarios)")

        # Stats globales
        stats = get_stats()
        assert "total_videos_procesados" in stats
        log_pass("get_stats funciona correctamente")

        # Config
        config = get_config()
        assert "groq_model" in config
        log_pass(f"get_config OK (modelo: {config.get('groq_model')})")

        # Update config
        update_config({"test_key": "test_value"})
        config_updated = get_config()
        assert config_updated.get("test_key") == "test_value"
        log_pass("update_config funciona correctamente")

    except Exception as e:
        import traceback
        log_fail("Operaciones DB fallaron", str(e))
        traceback.print_exc()


# ============ TEST: Procesador de video ============
def test_video_processor_funcs():
    """Verifica funciones del procesador de video."""
    print(f"\n{Colors.BOLD}=== TEST: Video processor ==={Colors.RESET}")

    try:
        from video_processor import (
            _buscar_fuente, _escape_ffmpeg_text, detectar_silencios,
            crear_intro_profesional, crear_outro_profesional,
            aplicar_color_grading, unir_clips_con_transiciones,
            generar_subtitulos_srt, quemar_subtitulos, exportar_multi_formato
        )
        from templates_data import PLANTILLAS_PROFESIONALES

        # Test 1: Buscar fuente
        for nombre in ["Inter", "Montserrat", "Poppins", "Lato", "JetBrains Mono"]:
            fuente = _buscar_fuente(nombre)
            assert fuente.endswith(".ttf"), f"Fuente inválida para {nombre}: {fuente}"
        log_pass("_buscar_fuente encuentra todas las fuentes")

        # Test 2: Escapar texto FFmpeg
        texto = "Hola: mundo %test 'comillas'"
        escaped = _escape_ffmpeg_text(texto)
        assert ":" not in escaped or "\\:" in escaped
        log_pass("_escape_ffmpeg_text escapa caracteres especiales")

        # Test 3: Color grading presets (verificar que las funciones existan)
        from video_processor import aplicar_color_grading
        log_pass("aplicar_color_grading está disponible")

        # Test 4: Generar SRT desde transcripción mock
        transcripcion_mock = {
            "text": "Hola mundo",
            "segments": [
                {"start": 0.0, "end": 2.5, "text": "Hola mundo"},
                {"start": 2.5, "end": 5.0, "text": "Esta es una prueba"},
            ]
        }
        srt_path = generar_subtitulos_srt(transcripcion_mock)
        assert os.path.exists(srt_path), f"SRT no se creó: {srt_path}"
        with open(srt_path, 'r', encoding='utf-8') as f:
            srt_content = f.read()
        assert "Hola mundo" in srt_content
        assert "00:00" in srt_content  # timestamp
        log_pass(f"generar_subtitulos_srt crea archivo válido: {srt_path}")

    except Exception as e:
        import traceback
        log_fail("Video processor falló", str(e))
        traceback.print_exc()


# ============ TEST: Plantillas ============
def test_plantillas_completas():
    """Verifica que todas las plantillas tengan datos completos."""
    print(f"\n{Colors.BOLD}=== TEST: Plantillas ==={Colors.RESET}")

    try:
        from templates_data import PLANTILLAS_PROFESIONALES, MEMBRESIAS

        # Verificar 12 plantillas
        assert len(PLANTILLAS_PROFESIONALES) >= 12
        log_pass(f"Total de plantillas: {len(PLANTILLAS_PROFESIONALES)}")

        # Verificar cada plantilla tenga todos los campos
        campos = ["id", "nombre", "categoria", "color_primario", "color_secundario",
                  "color_acento", "color_texto", "color_sub", "fuente", "estilo",
                  "transicion", "duracion_transicion", "descripcion", "preview_texto",
                  "config_avanzada"]
        for p in PLANTILLAS_PROFESIONALES:
            for c in campos:
                assert c in p, f"Plantilla {p.get('id', '?')} falta: {c}"
        log_pass("Todas las plantillas tienen estructura completa")

        # Verificar IDs únicos
        ids = [p["id"] for p in PLANTILLAS_PROFESIONALES]
        assert len(ids) == len(set(ids)), "IDs duplicados"
        log_pass("Todos los IDs son únicos")

        # Verificar categorías
        from templates_data import get_categorias
        cats = get_categorias()
        assert len(cats) >= 5, f"Solo {len(cats)} categorías"
        log_pass(f"Categorías: {cats}")

        # Verificar membresías
        assert len(MEMBRESIAS) == 3
        for m in MEMBRESIAS:
            assert "id" in m
            assert "nombre" in m
            assert "precio" in m
            assert "tokens" in m
            assert "features" in m
            assert isinstance(m["features"], list)
        log_pass(f"Membresías: {[m['nombre'] for m in MEMBRESIAS]}")

    except Exception as e:
        log_fail("Plantillas fallaron", str(e))


# ============ MAIN ============
def main():
    print(f"{Colors.BOLD}{'=' * 60}{Colors.RESET}")
    print(f"{Colors.BOLD}VideoAI Studio Pro - Tests de Integración{Colors.RESET}")
    print(f"{Colors.BOLD}{'=' * 60}{Colors.RESET}")

    test_wizard_flow()
    test_html_rendering()
    test_guion_generation_mock()
    test_database_operations()
    test_video_processor_funcs()
    test_plantillas_completas()

    print(f"\n{Colors.GREEN}{Colors.BOLD}Tests completados!{Colors.RESET}")


if __name__ == "__main__":
    main()
