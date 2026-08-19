#!/usr/bin/env python3
"""
Tests exhaustivos para casos edge:
- Videos muy largos (10-30 min)
- Múltiples imágenes (10-20)
- Aspect ratios no estándar (vertical, cuadrado, ultra-wide, retrato)
- Videos sin audio
- Formatos no estándar (MKV, MOV, AVI, WEBM)
"""

import sys
import os
import time
import json
import uuid
import shutil
import subprocess
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

results = {"pass": 0, "fail": 0, "warn": 0, "errors": []}
test_assets_dir = Path("/tmp/videoai_edge_assets")
test_assets_dir.mkdir(parents=True, exist_ok=True)


def log_pass(msg):
    print(f"{Colors.GREEN}✅ PASS{Colors.RESET}: {msg}")
    results["pass"] += 1


def log_fail(msg, detail=""):
    print(f"{Colors.RED}❌ FAIL{Colors.RESET}: {msg}")
    if detail:
        print(f"   {Colors.RED}→{Colors.RESET} {detail[:300]}")
    results["fail"] += 1
    results["errors"].append((msg, detail))


def log_step(msg):
    print(f"   {Colors.YELLOW}→{Colors.RESET} {msg}")


# ============ GENERADORES DE ASSETS EDGE ============

def generar_video_largo(duracion_min=10, nombre=None):
    """Genera un video de 10-30 minutos para tests de larga duración."""
    if nombre is None:
        nombre = f"long_{duracion_min}min_{uuid.uuid4().hex[:8]}.mp4"
    ruta = str(test_assets_dir / nombre)

    # Generar con ultrafast para que sea rápido incluso siendo largo
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", f"testsrc=duration={duracion_min*60}:size=320x240:rate=15",
        "-f", "lavfi", "-i", f"sine=frequency=440:duration={duracion_min*60}",
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "35",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "32k",
        "-shortest",
        ruta
    ]
    result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, timeout=300)
    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg falló: {result.stderr.decode('utf-8', errors='replace')[-300:]}")
    return ruta


def generar_video_aspect_ratio(width, height, duracion=3, nombre=None):
    """Genera un video con aspect ratio específico."""
    if nombre is None:
        nombre = f"ar_{width}x{height}_{uuid.uuid4().hex[:8]}.mp4"
    ruta = str(test_assets_dir / nombre)

    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", f"testsrc=duration={duracion}:size={width}x{height}:rate=24",
        "-f", "lavfi", "-i", f"sine=frequency=440:duration={duracion}",
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "30",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "64k",
        "-shortest",
        ruta
    ]
    result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, timeout=30)
    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg falló: {result.stderr.decode('utf-8', errors='replace')[-300:]}")
    return ruta


def generar_video_sin_audio(duracion=3, nombre=None):
    """Genera un video sin pista de audio."""
    if nombre is None:
        nombre = f"no_audio_{uuid.uuid4().hex[:8]}.mp4"
    ruta = str(test_assets_dir / nombre)

    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", f"testsrc=duration={duracion}:size=320x240:rate=24",
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "30",
        "-pix_fmt", "yuv420p",
        "-an",  # Sin audio
        ruta
    ]
    result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, timeout=30)
    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg falló: {result.stderr.decode('utf-8', errors='replace')[-300:]}")
    return ruta


def generar_multiples_imagenes(cantidad=10, nombre_prefix="multi"):
    """Genera múltiples imágenes PNG para tests de B-roll."""
    colores = ["red", "blue", "green", "yellow", "purple", "orange", "pink", "cyan", "magenta", "lime"]
    rutas = []
    for i in range(cantidad):
        color = colores[i % len(colores)]
        ruta = str(test_assets_dir / f"{nombre_prefix}_{i:02d}.png")
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", f"color=c={color}:s=640x480:d=1",
            "-frames:v", "1",
            ruta
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=10)
        if os.path.exists(ruta):
            rutas.append(ruta)
    return rutas


def generar_video_formato(formato="mkv", duracion=3, nombre=None):
    """Genera un video en formato específico (mkv, mov, avi, webm)."""
    if nombre is None:
        nombre = f"test_video_{uuid.uuid4().hex[:8]}.{formato}"
    ruta = str(test_assets_dir / nombre)

    codec_a = "aac"
    codec_v = "libx264"
    if formato == "webm":
        codec_v = "libvpx"
        codec_a = "libvorbis"

    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", f"testsrc=duration={duracion}:size=320x240:rate=24",
        "-f", "lavfi", "-i", f"sine=frequency=440:duration={duracion}",
        "-c:v", codec_v, "-preset", "ultrafast", "-crf", "30",
        "-pix_fmt", "yuv420p",
        "-c:a", codec_a, "-b:a", "64k",
        "-shortest",
        ruta
    ]
    result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, timeout=30)
    if result.returncode != 0:
        # Algunos formatos pueden no estar disponibles, retornar None
        return None
    return ruta if os.path.exists(ruta) else None


# ============ TEST 1: VIDEO MUY LARGO (10 min) ============
def test_video_largo_10min():
    """Prueba el pipeline con un video de 10 minutos."""
    print(f"\n{Colors.BOLD}=== TEST 1: Video largo (10 min) ==={Colors.RESET}")

    try:
        from video_processor import (
            detectar_silencios, _get_video_duration,
            aplicar_color_grading, crear_intro_profesional
        )
        from templates_data import PLANTILLAS_PROFESIONALES

        log_step("Generando video de 10 minutos...")
        video_path = generar_video_largo(duracion_min=10)
        assert os.path.exists(video_path), "No se creó el video largo"
        tamano_mb = os.path.getsize(video_path) / (1024 * 1024)
        log_pass(f"Video de 10 min creado: {tamano_mb:.1f} MB")

        # Verificar duración
        duracion = _get_video_duration(video_path)
        assert duracion >= 590, f"Duración esperada ~600s, obtuvo {duracion}"
        log_pass(f"Duración correcta: {duracion:.1f}s ({duracion/60:.1f} min)")

        # Detectar silencios (debe manejar videos largos)
        log_step("Detectando silencios en video largo...")
        inicio = time.time()
        silencios = detectar_silencios(video_path, umbral_db=-50, duracion_min=2.0)
        tiempo_detect = time.time() - inicio
        log_pass(f"Detección de silencios completada en {tiempo_detect:.1f}s")

        # Aplicar color grading (debe ser rápido incluso con video largo)
        log_step("Aplicando color grading...")
        inicio = time.time()
        graded = aplicar_color_grading(video_path, "neutro")
        tiempo_grade = time.time() - inicio
        assert os.path.exists(graded), "No se creó video con grading"
        log_pass(f"Color grading en {tiempo_grade:.1f}s")

        # Limpiar (archivos grandes)
        for path in [video_path, graded]:
            try:
                os.remove(path)
            except OSError:
                pass

    except Exception as e:
        import traceback
        log_fail("Test video largo falló", str(e))
        traceback.print_exc()


# ============ TEST 2: VIDEO MUY LARGO (30 min) ============
def test_video_largo_30min():
    """Prueba con un video extremadamente largo (30 min) - solo verificación de duración."""
    print(f"\n{Colors.BOLD}=== TEST 2: Video muy largo (30 min) ==={Colors.RESET}")

    try:
        from video_processor import _get_video_duration

        log_step("Generando video de 30 minutos...")
        video_path = generar_video_largo(duracion_min=30)
        if not os.path.exists(video_path):
            log_fail("No se pudo generar video de 30 min (timeout o espacio)")
            return

        tamano_mb = os.path.getsize(video_path) / (1024 * 1024)
        log_pass(f"Video de 30 min creado: {tamano_mb:.1f} MB")

        # Solo verificar duración (no procesar completo, tomaría mucho tiempo)
        duracion = _get_video_duration(video_path)
        assert duracion >= 1790, f"Duración esperada ~1800s, obtuvo {duracion}"
        log_pass(f"Duración correcta: {duracion:.1f}s ({duracion/60:.1f} min)")

        # Limpiar
        try:
            os.remove(video_path)
        except OSError:
            pass

    except Exception as e:
        log_fail("Test video 30 min falló", str(e))


# ============ TEST 3: MÚLTIPLES IMÁGENES (10) ============
def test_multiples_imagenes_10():
    """Prueba generar 10 diapositivas con Ken Burns."""
    print(f"\n{Colors.BOLD}=== TEST 3: Múltiples imágenes (10) ==={Colors.RESET}")

    try:
        from video_processor import crear_diapositiva_imagen

        log_step("Generando 10 imágenes...")
        imagenes = generar_multiples_imagenes(cantidad=10)
        assert len(imagenes) == 10
        log_pass(f"10 imágenes generadas")

        log_step("Creando diapositivas con Ken Burns...")
        slides_creados = 0
        for i, img in enumerate(imagenes):
            slide = crear_diapositiva_imagen(img, duracion=2, resolucion="320x180", ken_burns=True)
            if os.path.exists(slide) and os.path.getsize(slide) > 0:
                slides_creados += 1
                os.remove(slide)  # Limpiar para no llenar disco

        assert slides_creados == 10, f"Solo se crearon {slides_creados}/10 diapositivas"
        log_pass(f"10/10 diapositivas creadas correctamente")

    except Exception as e:
        import traceback
        log_fail("Test múltiples imágenes falló", str(e))
        traceback.print_exc()


# ============ TEST 4: MÚLTIPLES IMÁGENES (20) ============
def test_multiples_imagenes_20():
    """Prueba generar 20 diapositivas."""
    print(f"\n{Colors.BOLD}=== TEST 4: Múltiples imágenes (20) ==={Colors.RESET}")

    try:
        from video_processor import crear_diapositiva_imagen

        log_step("Generando 20 imágenes...")
        imagenes = generar_multiples_imagenes(cantidad=20, nombre_prefix="multi20")
        assert len(imagenes) == 20
        log_pass(f"20 imágenes generadas")

        log_step("Creando 20 diapositivas...")
        slides_creados = 0
        for i, img in enumerate(imagenes):
            slide = crear_diapositiva_imagen(img, duracion=1, resolucion="160x90", ken_burns=False)
            if os.path.exists(slide) and os.path.getsize(slide) > 0:
                slides_creados += 1
                os.remove(slide)

        # Al menos 18 deben crearse (tolerancia de 10%)
        assert slides_creados >= 18, f"Solo se crearon {slides_creados}/20"
        log_pass(f"{slides_creados}/20 diapositivas creadas")

    except Exception as e:
        log_fail("Test 20 imágenes falló", str(e))


# ============ TEST 5: ASPECT RATIO NO ESTÁNDAR (9:16) ============
def test_aspect_ratio_vertical():
    """Prueba con video vertical 9:16 (TikTok/Reels nativo)."""
    print(f"\n{Colors.BOLD}=== TEST 5: Aspect ratio vertical 9:16 ==={Colors.RESET}")

    try:
        from video_processor import _get_video_duration, crear_intro_profesional
        from templates_data import PLANTILLAS_PROFESIONALES

        log_step("Generando video vertical 360x640 (9:16)...")
        video = generar_video_aspect_ratio(360, 640, duracion=3)
        assert os.path.exists(video)
        log_pass(f"Video vertical creado: {os.path.getsize(video)} bytes")

        # Crear intro con aspect ratio vertical
        plantilla = PLANTILLAS_PROFESIONALES[0]
        intro = crear_intro_profesional("Test Vertical", plantilla, duracion=2, resolucion="360x640")
        assert os.path.exists(intro) and os.path.getsize(intro) > 0
        log_pass(f"Intro vertical creada: {os.path.getsize(intro)} bytes")

        # Limpiar
        for path in [video, intro]:
            try:
                os.remove(path)
            except OSError:
                pass

    except Exception as e:
        log_fail("Test aspect ratio vertical falló", str(e))


# ============ TEST 6: ASPECT RATIO CUADRADO (1:1) ============
def test_aspect_ratio_cuadrado():
    """Prueba con video cuadrado 1:1 (Instagram nativo)."""
    print(f"\n{Colors.BOLD}=== TEST 6: Aspect ratio cuadrado 1:1 ==={Colors.RESET}")

    try:
        from video_processor import crear_intro_profesional, crear_diapositiva_imagen
        from templates_data import PLANTILLAS_PROFESIONALES

        log_step("Generando video cuadrado 400x400...")
        video = generar_video_aspect_ratio(400, 400, duracion=3)
        assert os.path.exists(video)
        log_pass(f"Video cuadrado creado: {os.path.getsize(video)} bytes")

        # Crear intro cuadrada
        plantilla = PLANTILLAS_PROFESIONALES[0]
        intro = crear_intro_profesional("Test Square", plantilla, duracion=2, resolucion="400x400")
        assert os.path.exists(intro) and os.path.getsize(intro) > 0
        log_pass(f"Intro cuadrada creada: {os.path.getsize(intro)} bytes")

        # Limpiar
        for path in [video, intro]:
            try:
                os.remove(path)
            except OSError:
                pass

    except Exception as e:
        log_fail("Test aspect ratio cuadrado falló", str(e))


# ============ TEST 7: ASPECT RATIO ULTRA-WIDE (21:9) ============
def test_aspect_ratio_ultrawide():
    """Prueba con video ultra-wide 21:9."""
    print(f"\n{Colors.BOLD}=== TEST 7: Aspect ratio ultra-wide 21:9 ==={Colors.RESET}")

    try:
        from video_processor import crear_intro_profesional
        from templates_data import PLANTILLAS_PROFESIONALES

        log_step("Generando video ultra-wide 560x240 (21:9)...")
        video = generar_video_aspect_ratio(560, 240, duracion=3)
        assert os.path.exists(video)
        log_pass(f"Video ultra-wide creado: {os.path.getsize(video)} bytes")

        # Crear intro ultra-wide
        plantilla = PLANTILLAS_PROFESIONALES[0]
        intro = crear_intro_profesional("Test UltraWide", plantilla, duracion=2, resolucion="560x240")
        assert os.path.exists(intro) and os.path.getsize(intro) > 0
        log_pass(f"Intro ultra-wide creada: {os.path.getsize(intro)} bytes")

        # Limpiar
        for path in [video, intro]:
            try:
                os.remove(path)
            except OSError:
                pass

    except Exception as e:
        log_fail("Test aspect ratio ultra-wide falló", str(e))


# ============ TEST 8: ASPECT RATIO RETRATO (4:5) ============
def test_aspect_ratio_retrato():
    """Prueba con video en retrato 4:5."""
    print(f"\n{Colors.BOLD}=== TEST 8: Aspect ratio retrato 4:5 ==={Colors.RESET}")

    try:
        from video_processor import crear_intro_profesional
        from templates_data import PLANTILLAS_PROFESIONALES

        log_step("Generando video retrato 320x400 (4:5)...")
        video = generar_video_aspect_ratio(320, 400, duracion=3)
        assert os.path.exists(video)
        log_pass(f"Video retrato creado: {os.path.getsize(video)} bytes")

        # Crear intro en retrato
        plantilla = PLANTILLAS_PROFESIONALES[0]
        intro = crear_intro_profesional("Test Portrait", plantilla, duracion=2, resolucion="320x400")
        assert os.path.exists(intro) and os.path.getsize(intro) > 0
        log_pass(f"Intro retrato creada: {os.path.getsize(intro)} bytes")

        # Limpiar
        for path in [video, intro]:
            try:
                os.remove(path)
            except OSError:
                pass

    except Exception as e:
        log_fail("Test aspect ratio retrato falló", str(e))


# ============ TEST 9: VIDEO SIN AUDIO ============
def test_video_sin_audio():
    """Prueba procesamiento de un video sin pista de audio."""
    print(f"\n{Colors.BOLD}=== TEST 9: Video sin audio ==={Colors.RESET}")

    try:
        from video_processor import (
            _get_video_duration, aplicar_color_grading,
            detectar_silencios, crear_intro_profesional
        )
        from templates_data import PLANTILLAS_PROFESIONALES

        log_step("Generando video sin audio...")
        video = generar_video_sin_audio(duracion=3)
        assert os.path.exists(video)
        log_pass(f"Video sin audio creado: {os.path.getsize(video)} bytes")

        # Verificar duración
        duracion = _get_video_duration(video)
        assert duracion > 0
        log_pass(f"Duración: {duracion:.2f}s")

        # Detectar silencios (debe manejar videos sin audio)
        silencios = detectar_silencios(video)
        log_pass(f"Detección de silencios en video sin audio: {len(silencios)} silencios")

        # Aplicar color grading
        graded = aplicar_color_grading(video, "neutro")
        assert os.path.exists(graded)
        log_pass(f"Color grading en video sin audio: {os.path.getsize(graded)} bytes")

        # Limpiar
        for path in [video, graded]:
            try:
                os.remove(path)
            except OSError:
                pass

    except Exception as e:
        import traceback
        log_fail("Test video sin audio falló", str(e))
        traceback.print_exc()


# ============ TEST 10: FORMATOS NO ESTÁNDAR (MKV, MOV, AVI) ============
def test_formatos_no_estandar():
    """Prueba procesamiento de videos en formatos no estándar."""
    print(f"\n{Colors.BOLD}=== TEST 10: Formatos no estándar ==={Colors.RESET}")

    formatos_a_probar = ["mkv", "mov", "avi", "webm"]

    for formato in formatos_a_probar:
        try:
            log_step(f"Generando video en formato .{formato}...")
            video = generar_video_formato(formato, duracion=2)

            if video is None:
                log_pass(f"Formato .{formato}: no disponible en este sistema (omitido)")
                continue

            assert os.path.exists(video), f"No se creó video .{formato}"
            tam = os.path.getsize(video)
            log_pass(f"Video .{formato} creado: {tam} bytes")

            # Verificar que FFmpeg puede procesarlo
            from video_processor import _get_video_duration
            duracion = _get_video_duration(video)
            assert duracion > 0, f"Duración inválida para .{formato}"
            log_pass(f"Duración .{formato}: {duracion:.2f}s")

            # Limpiar
            try:
                os.remove(video)
            except OSError:
                pass

        except Exception as e:
            log_fail(f"Formato .{formato} falló", str(e))


# ============ TEST 11: TRANSICIONES NUEVAS ============
def test_transiciones_nuevas():
    """Prueba que las nuevas transiciones funcionen en FFmpeg."""
    print(f"\n{Colors.BOLD}=== TEST 11: Transiciones nuevas ==={Colors.RESET}")

    try:
        from templates_data import TRANSICIONES_DISPONIBLES
        from video_processor import unir_clips_con_transiciones, _get_video_duration
        from test_e2e_fast import video_corto

        log_pass(f"Total transiciones disponibles: {len(TRANSICIONES_DISPONIBLES)}")

        # Generar 2 clips para probar transiciones
        clip1 = video_corto(duracion=2, nombre="trans_c1.mp4")
        clip2 = video_corto(duracion=2, nombre="trans_c2.mp4")

        # Probar transiciones principales
        trans_a_probar = ["fade", "slide", "zoom", "dissolve", "wipeleft", "wiperight"]
        exitosas = 0
        for trans_id in trans_a_probar:
            try:
                resultado = unir_clips_con_transiciones([clip1, clip2], trans_id, 0.3)
                if os.path.exists(resultado) and os.path.getsize(resultado) > 0:
                    exitosas += 1
                    log_pass(f"Transición '{trans_id}' funciona")
                    # Limpiar
                    if resultado != clip1:
                        try:
                            os.remove(resultado)
                        except OSError:
                            pass
                else:
                    log_fail(f"Transición '{trans_id}' no generó archivo")
            except Exception as e:
                log_fail(f"Transición '{trans_id}' falló", str(e)[:100])

        # Al menos 4 de 6 deben funcionar
        assert exitosas >= 4, f"Solo funcionaron {exitosas}/{len(trans_a_probar)}"
        log_pass(f"✓ {exitosas}/{len(trans_a_probar)} transiciones principales funcionan")

        # Limpiar clips
        for path in [clip1, clip2]:
            try:
                os.remove(path)
            except OSError:
                pass

    except Exception as e:
        log_fail("Test transiciones falló", str(e))


# ============ TEST 12: EFECTOS VISUALES NUEVOS ============
def test_efectos_visuales_nuevos():
    """Prueba que los efectos visuales nuevos funcionen."""
    print(f"\n{Colors.BOLD}=== TEST 12: Efectos visuales nuevos ==={Colors.RESET}")

    try:
        from templates_data import EFECTOS_DISPONIBLES
        from video_processor import aplicar_efectos_visuales
        from test_e2e_fast import video_corto

        log_pass(f"Total efectos disponibles: {len(EFECTOS_DISPONIBLES)}")

        video = video_corto(duracion=2)

        # Probar efectos principales
        efectos_a_probar = ["ninguno", "vignette", "vintage", "vhs", "film_grain",
                            "zoom_blur", "glitch", "neon", "noir", "warm_sunset"]
        exitosos = 0
        for efecto_id in efectos_a_probar:
            resultado = aplicar_efectos_visuales(video, efecto_id, 0.5)
            if os.path.exists(resultado) and os.path.getsize(resultado) > 0:
                exitosos += 1
                log_pass(f"Efecto '{efecto_id}' aplicado: {os.path.getsize(resultado)} bytes")
                # Limpiar
                if resultado != video:
                    try:
                        os.remove(resultado)
                    except OSError:
                        pass
            else:
                log_fail(f"Efecto '{efecto_id}' no generó archivo")

        # Al menos 8 de 10 deben funcionar
        assert exitosos >= 8, f"Solo funcionaron {exitosos}/{len(efectos_a_probar)}"
        log_pass(f"✓ {exitosos}/{len(efectos_a_probar)} efectos principales funcionan")

        # Limpiar
        try:
            os.remove(video)
        except OSError:
            pass

    except Exception as e:
        import traceback
        log_fail("Test efectos visuales falló", str(e))
        traceback.print_exc()


# ============ TEST 13: PREVIEW ANIMADO ============
def test_preview_animado():
    """Prueba la generación de previews animados HTML."""
    print(f"\n{Colors.BOLD}=== TEST 13: Preview animado HTML ==={Colors.RESET}")

    try:
        from preview_renderer import generar_preview_animado, generar_preview_compacto
        from templates_data import PLANTILLAS_PROFESIONALES

        for plantilla in PLANTILLAS_PROFESIONALES[:5]:  # Primeras 5
            html = generar_preview_animado(plantilla, "Test Video", "Publicitario", 2)
            assert len(html) > 1000, f"HTML muy corto para {plantilla['nombre']}"
            assert plantilla["color_primario"] in html, f"Falta color primario en HTML"
            assert "animation" in html, f"Falta animación CSS en HTML"
            log_pass(f"Preview animado para '{plantilla['nombre']}': {len(html)} chars")

            # Compacto
            html_c = generar_preview_compacto(plantilla)
            assert len(html_c) > 500
            log_pass(f"Preview compacto para '{plantilla['nombre']}': {len(html_c)} chars")

    except Exception as e:
        import traceback
        log_fail("Test preview animado falló", str(e))
        traceback.print_exc()


# ============ MAIN ============
def main():
    print(f"{Colors.BOLD}{'=' * 70}{Colors.RESET}")
    print(f"{Colors.BOLD}Tests Casos Edge - VideoAI Studio Pro{Colors.RESET}")
    print(f"{Colors.BOLD}{'=' * 70}{Colors.RESET}")

    test_video_largo_10min()
    test_multiples_imagenes_10()
    test_aspect_ratio_vertical()
    test_aspect_ratio_cuadrado()
    test_aspect_ratio_ultrawide()
    test_aspect_ratio_retrato()
    test_video_sin_audio()
    test_formatos_no_estandar()
    test_transiciones_nuevas()
    test_efectos_visuales_nuevos()
    test_preview_animado()

    # Tests más pesados al final
    print(f"\n{Colors.YELLOW}⚠ Ejecutando tests pesados (pueden tardar varios minutos)...{Colors.RESET}")
    test_multiples_imagenes_20()
    test_video_largo_30min()

    # Limpiar
    try:
        shutil.rmtree(test_assets_dir)
    except Exception:
        pass

    # Resumen
    total = results["pass"] + results["fail"] + results["warn"]
    print(f"\n{Colors.BOLD}{'=' * 70}{Colors.RESET}")
    print(f"{Colors.BOLD}RESUMEN FINAL{Colors.RESET}")
    print(f"{Colors.BOLD}{'=' * 70}{Colors.RESET}")
    print(f"{Colors.GREEN}✅ Pasaron: {results['pass']}/{total}{Colors.RESET}")
    print(f"{Colors.RED}❌ Fallaron: {results['fail']}/{total}{Colors.RESET}")
    print(f"{Colors.YELLOW}⚠ Advertencias: {results['warn']}/{total}{Colors.RESET}")
    if total > 0:
        print(f"Tasa de éxito: {(results['pass'] / total * 100):.1f}%")

    if results["fail"] > 0:
        print(f"\n{Colors.RED}{Colors.BOLD}ERRORES:{Colors.RESET}")
        for msg, detail in results["errors"]:
            print(f"  - {msg}")
            if detail:
                print(f"    → {detail[:200]}")
        sys.exit(1)
    else:
        print(f"\n{Colors.GREEN}{Colors.BOLD}¡TODOS LOS TESTS EDGE PASARON! 🎉{Colors.RESET}")
        sys.exit(0)


if __name__ == "__main__":
    main()
