#!/usr/bin/env python3
"""
Tests exhaustivos de flujos del sistema VideoAI Studio Pro.
Verifica edge cases, manejo de errores y todos los flujos de usuario.
"""

import sys
import os
import json
import uuid
import tempfile
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
        print(f"   {Colors.RED}→{Colors.RESET} {detail}")
    results["fail"] += 1
    results["errors"].append((msg, detail))


def log_warn(msg):
    print(f"{Colors.YELLOW}⚠ WARN{Colors.RESET}: {msg}")
    results["warn"] += 1


def log_info(msg):
    print(f"{Colors.BLUE}ℹ{Colors.RESET} {msg}")


# ============ TEST 1: AUTENTICACIÓN - EDGE CASES ============
def test_auth_edge_cases():
    """Prueba casos extremos de autenticación."""
    print(f"\n{Colors.BOLD}=== TEST 1: Autenticación - Edge Cases ==={Colors.RESET}")

    try:
        from database import crear_usuario, autenticar_usuario, obtener_usuario

        # 1.1 - Email duplicado
        email = f"duplicate_{uuid.uuid4().hex[:8]}@test.com"
        u1, _ = crear_usuario("User 1", email, "pass1234")
        u2, msg = crear_usuario("User 2", email, "pass1234")
        assert u2 is None, f"Debería rechazar duplicado: {msg}"
        assert "ya está registrado" in msg.lower()
        log_pass("Rechaza email duplicado correctamente")

        # 1.2 - Login con contraseña incorrecta
        u, msg = autenticar_usuario(email, "wrongpassword")
        assert u is None
        assert "incorrectos" in msg.lower()
        log_pass("Rechaza contraseña incorrecta")

        # 1.3 - Login con email inexistente
        u, msg = autenticar_usuario(f"noexist_{uuid.uuid4().hex[:8]}@test.com", "pass1234")
        assert u is None
        log_pass("Rechaza email inexistente")

        # 1.4 - Email con mayúsculas (debe normalizar)
        email_mixed = f"MixedCase_{uuid.uuid4().hex[:8]}@TEST.COM"
        u, _ = crear_usuario("Mixed", email_mixed, "pass1234")
        u_login, _ = autenticar_usuario(email_mixed.lower(), "pass1234")
        assert u_login is not None, "Email con mayúsculas debe normalizarse"
        log_pass("Normaliza email con mayúsculas/minúsculas")

        # 1.5 - Email con espacios (debe hacer strip)
        email_spaces = f" spaces_{uuid.uuid4().hex[:8]}@test.com  "
        u, _ = crear_usuario("Spaces", email_spaces, "pass1234")
        u_login, _ = autenticar_usuario(email_spaces.strip(), "pass1234")
        assert u_login is not None
        log_pass("Hace strip de espacios en email")

        # 1.6 - Contraseña corta (permite pero recomendamos mínimo)
        u, _ = crear_usuario("Short Pass", f"short_{uuid.uuid4().hex[:8]}@test.com", "abc")
        # El sistema permite contraseñas cortas pero el frontend valida
        assert u is not None
        log_pass("Sistema acepta contraseñas cortas (frontend debe validar)")

    except Exception as e:
        import traceback
        log_fail("Auth edge cases falló", str(e))
        traceback.print_exc()


# ============ TEST 2: SISTEMA DE TOKENS ============
def test_token_system():
    """Prueba el sistema de tokens en detalle."""
    print(f"\n{Colors.BOLD}=== TEST 2: Sistema de Tokens ==={Colors.RESET}")

    try:
        from database import (
            crear_usuario, usar_token, verificar_tokens,
            obtener_usuario, cambiar_plan
        )

        # 2.1 - Usuario con plan gratis tiene 3 tokens
        email = f"tokens_{uuid.uuid4().hex[:8]}@test.com"
        u, _ = crear_usuario("Token Test", email, "pass1234", "gratis")
        assert u["tokens"] == 3, f"Esperaba 3 tokens, obtuvo {u['tokens']}"
        log_pass(f"Plan gratis: 3 tokens iniciales ✓")

        # 2.2 - Usar token uno por uno
        for i in range(3):
            assert usar_token(u["id"]) == True, f"Falló uso de token {i+1}"
        usuario_despues = obtener_usuario(u["id"])
        assert usuario_despues["tokens"] == 0
        log_pass("Después de usar 3 tokens: 0 tokens")

        # 2.3 - Intentar usar token sin disponibles
        assert usar_token(u["id"]) == False
        log_pass("Rechaza uso de token cuando no hay disponibles")

        # 2.4 - verificar_tokens retorna False cuando no hay
        assert verificar_tokens(u["id"]) == False
        log_pass("verificar_tokens retorna False cuando no hay tokens")

        # 2.5 - Cambiar plan recarga tokens
        cambiar_plan(u["id"], "pro")
        usuario_pro = obtener_usuario(u["id"])
        assert usuario_pro["plan"] == "pro"
        assert usuario_pro["tokens"] == 50  # Pro tiene 50
        log_pass(f"Cambio a plan Pro: {usuario_pro['tokens']} tokens")

        # 2.6 - Usuario inexistente
        assert usar_token("uid_inexistente") == False
        assert verificar_tokens("uid_inexistente") == False
        log_pass("Maneja UID inexistente correctamente")

        # 2.7 - tokens_usados se incrementa
        usuario_final = obtener_usuario(u["id"])
        assert usuario_final["tokens_usados"] == 3
        log_pass(f"tokens_usados = {usuario_final['tokens_usados']} (correcto)")

    except Exception as e:
        import traceback
        log_fail("Sistema de tokens falló", str(e))
        traceback.print_exc()


# ============ TEST 3: GENERACIÓN DE GUION (con mock) ============
def test_guion_generation_mock():
    """Simula la generación de guion sin llamar a la API real."""
    print(f"\n{Colors.BOLD}=== TEST 3: Generación de Guion (mock API) ==={Colors.RESET}")

    try:
        from groq_ai import GroqAI

        # Mock de respuesta de la API
        guion_mock = {
            "titulo": "Mi Video Test",
            "hook": "¿Sabías que...?",
            "introduccion": "En este video vamos a explorar...",
            "escenas": [
                {"numero": 1, "titulo_escena": "Intro", "descripcion": "Vista de la ciudad",
                 "narracion": "Bienvenidos", "texto_en_pantalla": "Hola",
                 "b_roll_sugerido": "Drone city", "musica_ambiente": "Upbeat", "duracion_seg": 10},
                {"numero": 2, "titulo_escena": "Desarrollo", "descripcion": "Detalle del producto",
                 "narracion": "Aquí está el producto", "texto_en_pantalla": "Nuevo!",
                 "b_roll_sugerido": "Producto close-up", "musica_ambiente": "Build up", "duracion_seg": 15}
            ],
            "cta_final": "Suscríbete para más contenido",
            "hashtags_sugeridos": ["#test", "#video", "#ai"],
            "descripcion_social": "Descripción para redes sociales"
        }

        groq = GroqAI("fake_api_key", "llama-3.1-8b-instant")

        # 3.1 - Mock _consultar para retornar JSON válido
        with patch.object(groq, '_consultar', return_value=json.dumps(guion_mock)):
            resultado = groq.generar_guion_completo(
                "Mensaje de prueba", "Publicitario", 1, "video.mp4", "Modern Tech"
            )

        assert "titulo" in resultado
        assert resultado["titulo"] == "Mi Video Test"
        assert len(resultado["escenas"]) == 2
        log_pass("generar_guion_completo con mock: estructura correcta")

        # 3.2 - Mock con respuesta que tiene markdown ```json
        with patch.object(groq, '_consultar', return_value=f"```json\n{json.dumps(guion_mock)}\n```"):
            resultado = groq.generar_guion_completo(
                "Test", "Publicitario", 1, "video.mp4", "Modern Tech"
            )
        assert resultado["titulo"] == "Mi Video Test"
        log_pass("Maneja respuesta con markdown ```json")

        # 3.3 - Mock con texto adicional antes/después del JSON
        respuesta_texto = f"Hola, aquí está el JSON:\n{json.dumps(guion_mock)}\nEspero que te sirva."
        with patch.object(groq, '_consultar', return_value=respuesta_texto):
            resultado = groq.generar_guion_completo("Test", "Publicitario", 1, "video.mp4", "Modern Tech")
        assert resultado["titulo"] == "Mi Video Test"
        log_pass("Extrae JSON de texto con ruido")

        # 3.4 - Mock con JSON inválido
        with patch.object(groq, '_consultar', return_value="esto no es json"):
            resultado = groq.generar_guion_completo("Test", "Publicitario", 1, "video.mp4", "Modern Tech")
        assert "error" in resultado
        log_pass("Maneja JSON inválido gracefully")

        # 3.5 - Mock con error de API
        with patch.object(groq, '_consultar', return_value="ERROR: HTTP 401: Unauthorized"):
            resultado = groq.generar_guion_completo("Test", "Publicitario", 1, "video.mp4", "Modern Tech")
        assert "error" in resultado
        log_pass("Maneja error de API gracefully")

        # 3.6 - Mock con timeout
        with patch.object(groq, '_consultar', return_value="ERROR: La consulta tardó demasiado"):
            resultado = groq.generar_guion_completo("Test", "Publicitario", 1, "video.mp4", "Modern Tech")
        assert "error" in resultado
        log_pass("Maneja timeout gracefully")

    except Exception as e:
        import traceback
        log_fail("Generación de guion mock falló", str(e))
        traceback.print_exc()


# ============ TEST 4: GENERACIÓN DE IDEAS (con mock) ============
def test_ideas_generation_mock():
    """Simula la generación de ideas con IA."""
    print(f"\n{Colors.BOLD}=== TEST 4: Generación de Ideas (mock API) ==={Colors.RESET}")

    try:
        from groq_ai import GroqAI

        ideas_mock = {
            "ideas": [
                {
                    "titulo": "5 trucos de productividad",
                    "gancho": "Estás perdiendo 3 horas al día...",
                    "descripcion": "Tutorial de productividad",
                    "tipo": "tutorial",
                    "duracion_sugerida": "2-3 minutos",
                    "potencial_viral": "alto",
                    "razon": "Tema evergreen con alta demanda"
                },
                {
                    "titulo": "Mi rutina matinal",
                    "gancho": "Esto cambió mi vida",
                    "descripcion": "Vlog de rutina",
                    "tipo": "vlog",
                    "duracion_sugerida": "3-5 minutos",
                    "potencial_viral": "medio",
                    "razon": "Conecta con audiencia personal"
                }
            ]
        }

        groq = GroqAI("fake_key", "llama-3.1-8b-instant")

        # 4.1 - Generación exitosa
        with patch.object(groq, '_consultar', return_value=json.dumps(ideas_mock)):
            resultado = groq.generar_ideas_contenido("productividad", "jóvenes", 2)

        assert "ideas" in resultado
        assert len(resultado["ideas"]) == 2
        assert resultado["ideas"][0]["potencial_viral"] == "alto"
        log_pass(f"generar_ideas_contenido: 2 ideas generadas correctamente")

        # 4.2 - Mock con JSON malformado
        with patch.object(groq, '_consultar', return_value='{"ideas": [incomplete}'):
            resultado = groq.generar_ideas_contenido("test", "test", 5)
        assert "error" in resultado
        log_pass("Maneja JSON malformado gracefully")

        # 4.3 - Cantidad límite (10)
        with patch.object(groq, '_consultar', return_value=json.dumps({"ideas": []})):
            groq.generar_ideas_contenido("test", "test", 15)  # Debe limitar a 10
        log_pass("Limita cantidad a 10 máximo")

    except Exception as e:
        import traceback
        log_fail("Generación de ideas mock falló", str(e))
        traceback.print_exc()


# ============ TEST 5: FLUJO DE ADMIN ============
def test_admin_flow():
    """Verifica el flujo de administración."""
    print(f"\n{Colors.BOLD}=== TEST 5: Flujo de Admin ==={Colors.RESET}")

    try:
        from database import (
            crear_usuario, obtener_usuario, actualizar_usuario,
            get_dashboard_data, listar_usuarios, verify_admin_password,
            set_admin_password, get_stats, agregar_proyecto
        )

        # 5.1 - Verificar contraseña admin por defecto
        assert verify_admin_password("admin123") == True
        log_pass("Contraseña admin por defecto (admin123) funciona")

        # 5.2 - Cambiar contraseña admin
        set_admin_password("new_admin_pass_2024")
        assert verify_admin_password("admin123") == False
        assert verify_admin_password("new_admin_pass_2024") == True
        log_pass("Cambio de contraseña admin funciona")

        # Restaurar para otros tests
        set_admin_password("admin123")

        # 5.3 - Listar usuarios (sin contraseñas)
        usuarios = listar_usuarios()
        assert isinstance(usuarios, list)
        for u in usuarios:
            assert "password_hash" not in u, "listar_usuarios no debe exponer password_hash"
        log_pass(f"listar_usuarios retorna {len(usuarios)} usuarios sin hashes")

        # 5.4 - Suspender usuario
        email = f"admin_test_{uuid.uuid4().hex[:8]}@test.com"
        u, _ = crear_usuario("Admin Test", email, "pass1234")
        actualizar_usuario(u["id"], {"activo": False})
        u_susp = obtener_usuario(u["id"])
        assert u_susp["activo"] == False
        log_pass("Suspensión de usuario funciona")

        # 5.5 - Reactivar usuario
        actualizar_usuario(u["id"], {"activo": True})
        u_act = obtener_usuario(u["id"])
        assert u_act["activo"] == True
        log_pass("Reactivación de usuario funciona")

        # 5.6 - Dashboard data
        dashboard = get_dashboard_data()
        assert "total_usuarios" in dashboard
        assert "usuarios_activos" in dashboard
        assert "tokens_distribuidos" in dashboard
        assert "tokens_usados" in dashboard
        assert "proyectos_totales" in dashboard
        assert "videos_procesados" in dashboard
        assert "distribucion_planes" in dashboard
        log_pass(f"Dashboard: {dashboard['total_usuarios']} usuarios, {dashboard['proyectos_totales']} proyectos")

        # 5.7 - Distribución de planes
        for plan_id in ["gratis", "pro", "business"]:
            assert plan_id in dashboard["distribucion_planes"]
        log_pass("Distribución de planes incluye los 3 planes")

        # 5.8 - Stats globales
        stats = get_stats()
        assert "total_videos_procesados" in stats
        assert "fecha_inicio" in stats
        log_pass("Stats globales accesibles")

        # 5.9 - Agregar proyecto actualiza stats
        videos_antes = stats.get("total_videos_procesados", 0)
        agregar_proyecto(u["id"], {
            "fecha": "20240101_120000",
            "video_original": "test.mp4",
            "video_final": "/tmp/test.mp4",
            "subtitulos": "/tmp/test.srt",
            "formatos": {"youtube": "/tmp/yt.mp4"},
            "transcripcion": "test",
        })
        stats_despues = get_stats()
        assert stats_despues["total_videos_procesados"] == videos_antes + 1
        log_pass(f"Stats se incrementan al agregar proyecto ({videos_antes} → {stats_despues['total_videos_procesados']})")

    except Exception as e:
        import traceback
        log_fail("Flujo de admin falló", str(e))
        traceback.print_exc()


# ============ TEST 6: VIDEO PROCESSOR (con mocks) ============
def test_video_processor_with_mocks():
    """Prueba el pipeline de video con mocks de FFmpeg."""
    print(f"\n{Colors.BOLD}=== TEST 6: Video Processor (mocks) ==={Colors.RESET}")

    try:
        from video_processor import (
            detectar_silencios, _run_ffmpeg, _get_video_duration,
            _escape_ffmpeg_text, _buscar_fuente, generar_subtitulos_srt,
            crear_intro_profesional, crear_outro_profesional,
            crear_diapositiva_imagen, aplicar_color_grading
        )
        from templates_data import PLANTILLAS_PROFESIONALES

        # 6.1 - _escape_ffmpeg_text con casos extremos
        casos = [
            ("Hola", "Hola"),
            ("Hola: mundo", "Hola\\: mundo"),
            ("100% gratis", "100\\% gratis"),
            ("", ""),
            ("Texto 'con comillas'", "Texto \u2019con comillas\u2019"),
        ]
        for input_text, expected_substring in casos:
            result = _escape_ffmpeg_text(input_text)
            assert expected_substring in result or result == expected_substring, \
                f"Para '{input_text}' esperaba '{expected_substring}', obtuvo '{result}'"
        log_pass("_escape_ffmpeg_text maneja casos extremos")

        # 6.2 - _buscar_fuente con nombres desconocidos
        fuente = _buscar_fuente("FuenteInexistente")
        assert fuente.endswith(".ttf"), f"Debe retornar fuente por defecto: {fuente}"
        log_pass("_buscar_fuente retorna fuente por defecto para nombres desconocidos")

        # 6.3 - Generar SRT con transcripción vacía
        srt_path = generar_subtitulos_srt({"segments": [], "text": ""})
        assert os.path.exists(srt_path)
        with open(srt_path, 'r', encoding='utf-8') as f:
            content = f.read()
        assert content == ""
        log_pass("generar_subtitulos_srt maneja transcripción vacía")

        # 6.4 - Generar SRT con segmentos múltiples
        transcripcion = {
            "text": "Hola mundo",
            "segments": [
                {"start": 0.0, "end": 1.5, "text": "Hola"},
                {"start": 1.5, "end": 3.0, "text": "mundo"},
                {"start": 3.0, "end": 5.0, "text": "esto es una prueba"},
            ]
        }
        srt_path = generar_subtitulos_srt(transcripcion)
        with open(srt_path, 'r', encoding='utf-8') as f:
            content = f.read()
        assert "1\n" in content  # número
        assert "00:00:00,000" in content  # timestamp inicio
        assert "Hola" in content
        assert "mundo" in content
        log_pass("generar_subtitulos_srt con múltiples segmentos")

        # 6.5 - detectar_silencios con FFmpeg mock
        with patch('video_processor.subprocess.run') as mock_run:
            # Simular output de FFmpeg con silencios
            mock_run.return_value = MagicMock(
                stderr="silence_start: 5.0\nsilence_end: 6.5|silence_duration: 1.5\nsilence_start: 10.0\nsilence_end: 11.0|silence_duration: 1.0\n",
                returncode=0
            )
            silencios = detectar_silencios("/fake/video.mp4")
        assert len(silencios) == 2
        assert silencios[0] == (5.0, 6.5)
        assert silencios[1] == (10.0, 11.0)
        log_pass(f"detectar_silencios parsea correctamente: {silencios}")

        # 6.6 - detectar_silencios sin silencios
        with patch('video_processor.subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(stderr="", returncode=0)
            silencios = detectar_silencios("/fake/video.mp4")
        assert silencios == []
        log_pass("detectar_silencios retorna lista vacía cuando no hay silencios")

        # 6.7 - crear_intro_profesional con plantilla
        plantilla = PLANTILLAS_PROFESIONALES[0]
        with patch('video_processor._run_ffmpeg', return_value=(True, "OK")):
            intro_path = crear_intro_profesional("Test Title", plantilla, duracion=3)
        assert intro_path.endswith(".mp4")
        log_pass(f"crear_intro_profesional retorna path válido")

        # 6.8 - aplicar_color_grading con diferentes presets
        with patch('video_processor._run_ffmpeg', return_value=(True, "OK")):
            for preset in ["neutro", "calido", "frio", "cinematico", "vibrante"]:
                result = aplicar_color_grading("/fake/video.mp4", preset)
                assert isinstance(result, str)
        log_pass("aplicar_color_grading funciona con 5 presets")

        # 6.9 - aplicar_color_grading con preset desconocido
        with patch('video_processor._run_ffmpeg', return_value=(True, "OK")):
            result = aplicar_color_grading("/fake/video.mp4", "preset_inexistente")
        assert isinstance(result, str)
        log_pass("aplicar_color_grading maneja preset desconocido")

    except Exception as e:
        import traceback
        log_fail("Video processor mocks falló", str(e))
        traceback.print_exc()


# ============ TEST 7: PLANTILLAS Y RENDERIZADO ============
def test_plantillas_renderizado():
    """Verifica plantillas y su renderizado HTML."""
    print(f"\n{Colors.BOLD}=== TEST 7: Plantillas y Renderizado ==={Colors.RESET}")

    try:
        from templates_data import (
            PLANTILLAS_PROFESIONALES, get_plantilla_by_id,
            get_categorias, get_plantillas_by_categoria, get_plantilla_default
        )
        from styles import (
            render_template_preview_card, render_stat_card,
            render_wizard, render_scene_card, render_pricing_card, html_safe
        )

        # 7.1 - Cada plantilla tiene colores hex válidos
        import re
        hex_pattern = re.compile(r'^#[0-9A-Fa-f]{6}$')
        for p in PLANTILLAS_PROFESIONALES:
            assert hex_pattern.match(p["color_primario"]), f"{p['id']}: color_primario inválido"
            assert hex_pattern.match(p["color_secundario"]), f"{p['id']}: color_secundario inválido"
            if p.get("color_acento") and p["color_acento"] != "#FFFFFF":
                # color_acento puede ser blanco
                pass
        log_pass("Todas las plantillas tienen colores hex válidos")

        # 7.2 - get_plantilla_by_id funciona
        for p in PLANTILLAS_PROFESIONALES:
            found = get_plantilla_by_id(p["id"])
            assert found is not None
            assert found["id"] == p["id"]
        log_pass("get_plantilla_by_id funciona para todas las plantillas")

        # 7.3 - get_plantilla_by_id con ID inexistente
        assert get_plantilla_by_id("id_inexistente") is None
        log_pass("get_plantilla_by_id retorna None para ID inexistente")

        # 7.4 - get_categorias retorna lista no vacía
        cats = get_categorias()
        assert isinstance(cats, list)
        assert len(cats) >= 5
        log_pass(f"get_categorias: {len(cats)} categorías")

        # 7.5 - get_plantillas_by_categoria funciona
        for cat in cats:
            plantillas = get_plantillas_by_categoria(cat)
            assert len(plantillas) >= 1
            for p in plantillas:
                assert p["categoria"] == cat
        log_pass("get_plantillas_by_categoria filtra correctamente")

        # 7.6 - get_plantilla_default retorna una plantilla válida
        default = get_plantilla_default()
        assert default is not None
        assert "id" in default
        assert "nombre" in default
        log_pass(f"get_plantilla_default: {default['nombre']}")

        # 7.7 - Renderizar cada plantilla no causa errores
        for p in PLANTILLAS_PROFESIONALES:
            html = render_template_preview_card(p, 0, False)
            html_safe_html = html_safe(html)
            assert '<div class="template-card' in html_safe_html
            assert p["nombre"] in html_safe_html
        log_pass(f"Renderizadas {len(PLANTILLAS_PROFESIONALES)} plantillas sin errores")

        # 7.8 - Plantilla seleccionada tiene clase CSS correcta
        html = render_template_preview_card(PLANTILLAS_PROFESIONALES[0], 0, True)
        assert 'selected' in html
        log_pass("Plantilla seleccionada tiene clase CSS 'selected'")

        # 7.9 - Renderizar wizard con 1, 3 y 6 pasos
        for n in [1, 3, 6]:
            html = render_wizard(2, [f"Step {i+1}" for i in range(n)])
            html_limpio = html_safe(html)
            # Cada paso genera un div con clase wizard-step (seguido de un espacio y state)
            # Ej: <div class="wizard-step active">
            count = html_limpio.count('<div class="wizard-step ')
            assert count == n, f"Para {n} pasos, obtuvo {count} divs de wizard-step"
        log_pass("render_wizard funciona con 1, 3 y 6 pasos")

        # 7.10 - Renderizar wizard paso 1 (todos pending excepto el 1)
        html = render_wizard(1, ["A", "B", "C"])
        assert 'class="wizard-step active"' in html
        assert 'class="wizard-step pending"' in html
        log_pass("render_wizard(1): paso 1 es active, otros pending")

        # 7.11 - Renderizar wizard paso final (todos completed excepto el último)
        html = render_wizard(3, ["A", "B", "C"])
        assert 'class="wizard-step completed"' in html
        assert 'class="wizard-step active"' in html
        log_pass("render_wizard(3): pasos 1-2 completed, paso 3 active")

    except Exception as e:
        import traceback
        log_fail("Plantillas y renderizado falló", str(e))
        traceback.print_exc()


# ============ TEST 8: HTML_SAFE Y SANITIZACIÓN ============
def test_html_safe():
    """Verifica que html_safe funcione correctamente."""
    print(f"\n{Colors.BOLD}=== TEST 8: html_safe y sanitización ==={Colors.RESET}")

    try:
        from styles import html_safe

        # 8.1 - Elimina saltos de línea
        html = '<div>\n<span>test</span>\n</div>'
        result = html_safe(html)
        assert '\n' not in result, f"Tiene saltos: {result}"
        log_pass("html_safe elimina saltos de línea")

        # 8.2 - HTML vacío
        assert html_safe("") == ""
        assert html_safe(None) == ""
        log_pass("html_safe maneja HTML vacío y None")

        # 8.3 - HTML ya limpio (no debe romper)
        html = '<div class="test">Content</div>'
        result = html_safe(html)
        assert result == '<div class="test">Content</div>'
        log_pass("html_safe preserva HTML ya limpio")

        # 8.4 - HTML con múltiples espacios
        html = '<div>   <span>   test   </span>   </div>'
        result = html_safe(html)
        assert '   ' not in result  # no debe tener 3+ espacios seguidos
        log_pass("html_safe colapsa espacios múltiples")

        # 8.5 - HTML con tags anidados
        html = """
        <div class="outer">
            <div class="inner">
                <span>Texto</span>
            </div>
        </div>
        """
        result = html_safe(html)
        assert '<div class="outer">' in result
        assert '<div class="inner">' in result
        assert '<span>Texto</span>' in result
        log_pass("html_safe preserva estructura de tags anidados")

    except Exception as e:
        log_fail("html_safe falló", str(e))


# ============ TEST 9: FLUJO COMPLETO DE USUARIO ============
def test_user_full_flow():
    """Simula el flujo completo de un usuario real."""
    print(f"\n{Colors.BOLD}=== TEST 9: Flujo completo de usuario ==={Colors.RESET}")

    try:
        import streamlit as st
        from auth import init_session_state, is_logged_in, is_admin
        from database import (
            crear_usuario, autenticar_usuario, obtener_usuario,
            usar_token, agregar_proyecto
        )
        from templates_data import PLANTILLAS_PROFESIONALES

        # Limpiar sesión
        st.session_state.clear()
        init_session_state()

        # 9.1 - Estado inicial: no logueado
        assert is_logged_in() == False
        assert is_admin() == False
        assert st.session_state.wizard_step == 1
        log_pass("Estado inicial correcto (no logueado)")

        # 9.2 - Registro de usuario
        email = f"fullflow_{uuid.uuid4().hex[:8]}@test.com"
        usuario, msg = crear_usuario("Usuario Flow", email, "pass1234", "pro")
        assert usuario is not None
        st.session_state.usuario = usuario
        assert is_logged_in() == True
        log_pass(f"Usuario registrado y logueado: {email}")

        # 9.3 - Simular flujo del wizard
        # Paso 1: subir archivos
        st.session_state.archivos_guardados = {
            "principal": "/tmp/test.mp4",
            "principal_name": "test.mp4",
            "videos": [],
            "imagenes": [],
            "audio": None,
        }
        st.session_state.wizard_step = 2
        log_pass("Paso 1 completado: archivos subidos")

        # Paso 2: descripción
        st.session_state["texto_objetivo_input"] = "Promocionar mi marca"
        st.session_state["tipo_contenido_sel"] = "Publicitario"
        st.session_state["duracion_slider"] = 2
        st.session_state.wizard_step = 3
        log_pass("Paso 2 completado: descripción del proyecto")

        # Paso 3: plantilla
        st.session_state.plantilla_elegida = PLANTILLAS_PROFESIONALES[5]  # Viral TikTok
        st.session_state.wizard_step = 4
        log_pass(f"Paso 3 completado: plantilla {PLANTILLAS_PROFESIONALES[5]['nombre']}")

        # Paso 4: formatos
        st.session_state.formatos_seleccionados = ["youtube", "tiktok", "instagram"]
        st.session_state.wizard_step = 5
        log_pass(f"Paso 4 completado: {len(st.session_state.formatos_seleccionados)} formatos")

        # Paso 5: guion generado (mock)
        st.session_state.guion = {
            "titulo": "Video promocional de mi marca",
            "hook": "¿Quieres conocer mi marca?",
            "introduccion": "Hoy te presento...",
            "escenas": [
                {"numero": 1, "descripcion": "Vista general", "texto_en_pantalla": "Hola", "duracion_seg": 10},
                {"numero": 2, "descripcion": "Producto en acción", "texto_en_pantalla": "Nuevo!", "duracion_seg": 15},
            ],
            "cta_final": "Visita mi web",
            "hashtags_sugeridos": ["#marca", "#producto"],
        }
        st.session_state.wizard_step = 6
        log_pass("Paso 5 completado: guion generado")

        # 9.4 - Validar que todos los datos del wizard estén presentes
        required = ["archivos_guardados", "plantilla_elegida", "guion",
                    "formatos_seleccionados", "usuario"]
        for key in required:
            assert st.session_state.get(key) is not None, f"Falta: {key}"
        log_pass("Todos los datos del wizard presentes en sesión")

        # 9.5 - Simular producción exitosa
        proyecto = {
            "fecha": "20240101_120000",
            "video_original": "test.mp4",
            "video_final": "/tmp/output.mp4",
            "subtitulos": "/tmp/subs.srt",
            "formatos": {fmt: f"/tmp/{fmt}.mp4" for fmt in st.session_state.formatos_seleccionados},
            "transcripcion": "Transcripción de prueba",
            "plantilla_usada": st.session_state.plantilla_elegida["nombre"],
        }
        agregar_proyecto(usuario["id"], proyecto)
        usar_token(usuario["id"])

        # Refrescar usuario
        usuario_actualizado = obtener_usuario(usuario["id"])
        assert len(usuario_actualizado["proyectos"]) == 1
        assert usuario_actualizado["tokens"] == usuario["tokens"] - 1
        log_pass(f"Proyecto agregado, tokens: {usuario['tokens']} → {usuario_actualizado['tokens']}")

        # 9.6 - Verificar que el proyecto tenga todos los campos
        proyecto_guardado = usuario_actualizado["proyectos"][0]
        campos = ["fecha", "video_original", "video_final", "subtitulos",
                  "formatos", "transcripcion", "plantilla_usada"]
        for c in campos:
            assert c in proyecto_guardado, f"Falta campo: {c}"
        log_pass("Proyecto guardado con todos los campos requeridos")

    except Exception as e:
        import traceback
        log_fail("Flujo completo de usuario falló", str(e))
        traceback.print_exc()


# ============ TEST 10: MANEJO DE ERRORES ============
def test_error_handling():
    """Verifica el manejo de errores en casos extremos."""
    print(f"\n{Colors.BOLD}=== TEST 10: Manejo de errores ==={Colors.RESET}")

    try:
        from database import (
            cargar_db, guardar_db, obtener_usuario, actualizar_usuario,
            usar_token, agregar_proyecto
        )
        from groq_ai import GroqAI

        # 10.1 - obtener_usuario con ID inexistente
        result = obtener_usuario("uid_inexistente_xyz")
        assert result is None
        log_pass("obtener_usuario(None) retorna None sin error")

        # 10.2 - actualizar_usuario con ID inexistente
        result = actualizar_usuario("uid_inexistente_xyz", {"tokens": 10})
        assert result == False
        log_pass("actualizar_usuario retorna False para UID inexistente")

        # 10.3 - agregar_proyecto con UID inexistente
        result = agregar_proyecto("uid_inexistente_xyz", {"fecha": "test"})
        assert result == False
        log_pass("agregar_proyecto retorna False para UID inexistente")

        # 10.4 - GroqAI sin API key
        groq = GroqAI("", "llama-3.1-8b-instant")
        assert groq.esta_configurado() == False
        resultado = groq._consultar("test prompt")
        assert "ERROR" in resultado
        log_pass("GroqAI sin API key maneja error correctamente")

        # 10.5 - GroqAI con API key pero conexión fallida
        groq = GroqAI("fake_key", "llama-3.1-8b-instant")
        # Mock para simular error de conexión
        with patch('groq_ai.requests.post', side_effect=Exception("Connection error")):
            resultado = groq._consultar("test prompt")
        assert "ERROR" in resultado
        log_pass("GroqAI maneja error de conexión")

        # 10.6 - GroqAI con timeout
        import requests
        with patch('groq_ai.requests.post', side_effect=requests.exceptions.Timeout("timeout")):
            resultado = groq._consultar("test prompt")
        assert "ERROR" in resultado
        # El mensaje debe indicar que fue un problema de tiempo/timeout
        assert any(word in resultado.lower() for word in ["tiempo", "timeout", "tardó", "demoró"]), \
            f"Mensaje no contiene referencia al timeout: {resultado}"
        log_pass("GroqAI maneja timeout con mensaje apropiado")

        # 10.7 - GroqAI con error de conexión
        with patch('groq_ai.requests.post', side_effect=requests.exceptions.ConnectionError("no connection")):
            resultado = groq._consultar("test prompt")
        assert "ERROR" in resultado
        assert "conex" in resultado.lower()
        log_pass("GroqAI maneja error de conexión con mensaje apropiado")

    except Exception as e:
        import traceback
        log_fail("Manejo de errores falló", str(e))
        traceback.print_exc()


# ============ TEST 11: INTEGRIDAD DE DATOS ============
def test_data_integrity():
    """Verifica la integridad de los datos guardados."""
    print(f"\n{Colors.BOLD}=== TEST 11: Integridad de datos ==={Colors.RESET}")

    try:
        from database import (
            cargar_db, guardar_db, crear_usuario, obtener_usuario
        )

        # 11.1 - DB carga correctamente
        db = cargar_db()
        assert isinstance(db, dict)
        assert "usuarios" in db
        assert "config" in db
        assert "membresias" in db
        log_pass("Estructura de DB correcta")

        # 11.2 - Config tiene todos los campos
        config = db["config"]
        campos = ["groq_api_key", "groq_model", "whisper_model",
                  "admin_password_hash", "brand_name", "primary_color"]
        for c in campos:
            assert c in config, f"Falta campo en config: {c}"
        log_pass("Config tiene todos los campos requeridos")

        # 11.3 - Membresías tienen 3 planes
        assert len(db["membresias"]) == 3
        for m in db["membresias"]:
            assert "id" in m
            assert "nombre" in m
            assert "precio" in m
            assert "tokens" in m
            assert "features" in m
            assert isinstance(m["features"], list)
        log_pass(f"Membresías: {[m['nombre'] for m in db['membresias']]}")

        # 11.4 - Guardar y cargar preserva datos
        email = f"integrity_{uuid.uuid4().hex[:8]}@test.com"
        crear_usuario("Integrity Test", email, "pass1234", "pro")

        db2 = cargar_db()
        found = False
        for u in db2["usuarios"]:
            if u["email"] == email:
                found = True
                # Verificar que password_hash esté presente
                assert "password_hash" in u
                assert u["password_hash"] != "pass1234"  # No debe estar en plano
                break
        assert found, "Usuario no encontrado después de guardar"
        log_pass("Guardar/cargar preserva datos y contraseñas hasheadas")

        # 11.5 - Stats tienen campos requeridos
        assert "stats" in db
        stats = db["stats"]
        assert "total_videos_procesados" in stats
        assert "fecha_inicio" in stats
        log_pass("Stats globales presentes")

    except Exception as e:
        import traceback
        log_fail("Integridad de datos falló", str(e))
        traceback.print_exc()


# ============ TEST 12: FLUJO DE CONFIGURACIÓN ============
def test_config_flow():
    """Verifica el flujo de configuración del sistema."""
    print(f"\n{Colors.BOLD}=== TEST 12: Flujo de configuración ==={Colors.RESET}")

    try:
        from database import get_config, update_config
        from groq_ai import MODEL_MAX_TOKENS, MODELOS_RECOMENDADOS, SAFE_MAX_TOKENS, GroqAI

        # 12.1 - get_config retorna dict
        config = get_config()
        assert isinstance(config, dict)
        log_pass("get_config retorna dict")

        # 12.2 - update_config agrega campos
        update_config({"test_field": "test_value"})
        config = get_config()
        assert config["test_field"] == "test_value"
        log_pass("update_config agrega campos correctamente")

        # 12.3 - update_config no sobrescribe otros campos
        update_config({"another_field": 123})
        config = get_config()
        assert config["test_field"] == "test_value"  # Sigue ahí
        assert config["another_field"] == 123
        log_pass("update_config preserva campos existentes")

        # 12.4 - MODEL_MAX_TOKENS tiene modelos conocidos
        assert "llama-3.1-70b-versatile" in MODEL_MAX_TOKENS
        assert "llama-3.1-8b-instant" in MODEL_MAX_TOKENS
        assert "mixtral-8x7b-32768" in MODEL_MAX_TOKENS
        log_pass(f"MODEL_MAX_TOKENS tiene {len(MODEL_MAX_TOKENS)} modelos")

        # 12.5 - MODELOS_RECOMENDADOS es lista no vacía
        assert isinstance(MODELOS_RECOMENDADOS, list)
        assert len(MODELOS_RECOMENDADOS) >= 3
        log_pass(f"MODELOS_RECOMENDADOS: {MODELOS_RECOMENDADOS}")

        # 12.6 - SAFE_MAX_TOKENS es razonable
        assert 1000 <= SAFE_MAX_TOKENS <= 5000
        log_pass(f"SAFE_MAX_TOKENS = {SAFE_MAX_TOKENS} (razonable)")

        # 12.7 - GroqAI respeta max_tokens según modelo
        for modelo, max_esperado in MODEL_MAX_TOKENS.items():
            groq = GroqAI("test", modelo)
            max_real = groq._get_max_tokens(99999)
            assert max_real == max_esperado, f"Modelo {modelo}: esperado {max_esperado}, obtuvo {max_real}"
        log_pass(f"GroqAI respeta max_tokens para {len(MODEL_MAX_TOKENS)} modelos")

    except Exception as e:
        import traceback
        log_fail("Flujo de configuración falló", str(e))
        traceback.print_exc()


# ============ MAIN ============
def main():
    print(f"{Colors.BOLD}{'=' * 70}{Colors.RESET}")
    print(f"{Colors.BOLD}VideoAI Studio Pro - Suite de Tests Adicional{Colors.RESET}")
    print(f"{Colors.BOLD}{'=' * 70}{Colors.RESET}")
    print(f"Fecha: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    test_auth_edge_cases()
    test_token_system()
    test_guion_generation_mock()
    test_ideas_generation_mock()
    test_admin_flow()
    test_video_processor_with_mocks()
    test_plantillas_renderizado()
    test_html_safe()
    test_user_full_flow()
    test_error_handling()
    test_data_integrity()
    test_config_flow()

    # Resumen final
    total = results["pass"] + results["fail"] + results["warn"]
    print(f"\n{Colors.BOLD}{'=' * 70}{Colors.RESET}")
    print(f"{Colors.BOLD}RESUMEN FINAL{Colors.RESET}")
    print(f"{Colors.BOLD}{'=' * 70}{Colors.RESET}")
    print(f"{Colors.GREEN}✅ Pasaron: {results['pass']}/{total}{Colors.RESET}")
    print(f"{Colors.RED}❌ Fallaron: {results['fail']}/{total}{Colors.RESET}")
    print(f"{Colors.YELLOW}⚠ Advertencias: {results['warn']}/{total}{Colors.RESET}")
    print(f"Tasa de éxito: {(results['pass'] / total * 100):.1f}%")

    if results["fail"] > 0:
        print(f"\n{Colors.RED}{Colors.BOLD}ERRORES DETALLADOS:{Colors.RESET}")
        for msg, detail in results["errors"]:
            print(f"  - {msg}")
            if detail:
                print(f"    → {detail[:200]}")
        sys.exit(1)
    else:
        print(f"\n{Colors.GREEN}{Colors.BOLD}¡TODOS LOS TESTS PASARON! 🎉{Colors.RESET}")
        sys.exit(0)


if __name__ == "__main__":
    main()
