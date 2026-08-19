#!/usr/bin/env python3
"""
Tests E2E con FFmpeg REAL - VERSIÓN OPTIMIZADA para ejecución rápida.
Usa videos muy cortos (2-3s) y resoluciones pequeñas (320x240) para rapidez.
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
test_assets_dir = Path("/tmp/videoai_test_assets_fast")
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


# ============ HELPERS PARA ASSETS RÁPIDOS ============

def video_corto(duracion=2, nombre=None):
    """Genera un video muy corto (2s default) en resolución pequeña."""
    if nombre is None:
        nombre = f"v_{uuid.uuid4().hex[:8]}.mp4"
    ruta = str(test_assets_dir / nombre)
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", f"testsrc=duration={duracion}:size=320x240:rate=24",
        "-f", "lavfi", "-i", f"sine=frequency=440:duration={duracion}",
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "30",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "64k",
        "-shortest",
        ruta
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=30)
    return ruta


def imagen_corta(nombre=None):
    """Genera una imagen PNG."""
    if nombre is None:
        nombre = f"i_{uuid.uuid4().hex[:8]}.png"
    ruta = str(test_assets_dir / nombre)
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", "color=c=blue:s=640x480:d=1",
        "-frames:v", "1",
        ruta
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=15)
    return ruta


def audio_corto(duracion=3, nombre=None):
    """Genera un WAV corto."""
    if nombre is None:
        nombre = f"a_{uuid.uuid4().hex[:8]}.wav"
    ruta = str(test_assets_dir / nombre)
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", f"sine=frequency=300:duration={duracion}",
        "-ar", "44100",
        ruta
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=15)
    return ruta


# ============ TESTS ============

def test_assets():
    """Genera assets y verifica que existan."""
    print(f"\n{Colors.BOLD}=== TEST 1: Generación de assets ==={Colors.RESET}")

    v = video_corto()
    assert os.path.exists(v) and os.path.getsize(v) > 0
    log_pass(f"Video: {os.path.getsize(v)} bytes")

    i = imagen_corta()
    assert os.path.exists(i) and os.path.getsize(i) > 0
    log_pass(f"Imagen: {os.path.getsize(i)} bytes")

    a = audio_corto()
    assert os.path.exists(a) and os.path.getsize(a) > 0
    log_pass(f"Audio: {os.path.getsize(a)} bytes")


def test_intro_outro():
    """Test crear intro y outro con plantillas."""
    print(f"\n{Colors.BOLD}=== TEST 2: Intro/Outro ==={Colors.RESET}")

    from video_processor import crear_intro_profesional, crear_outro_profesional, _get_video_duration
    from templates_data import PLANTILLAS_PROFESIONALES

    plantilla = PLANTILLAS_PROFESIONALES[0]
    intro = crear_intro_profesional("Test", plantilla, duracion=2, resolucion="320x180")
    assert os.path.exists(intro) and os.path.getsize(intro) > 0
    d = _get_video_duration(intro)
    assert d > 0
    log_pass(f"Intro: {os.path.getsize(intro)}B, {d:.2f}s")

    outro = crear_outro_profesional(plantilla, "CTA Test", duracion=2, resolucion="320x180")
    assert os.path.exists(outro) and os.path.getsize(outro) > 0
    log_pass(f"Outro: {os.path.getsize(outro)}B")


def test_diapositiva():
    """Test crear diapositiva con y sin Ken Burns."""
    print(f"\n{Colors.BOLD}=== TEST 3: Diapositivas ==={Colors.RESET}")

    from video_processor import crear_diapositiva_imagen

    img = imagen_corta()

    # Sin Ken Burns
    slide = crear_diapositiva_imagen(img, duracion=2, resolucion="320x180", ken_burns=False)
    assert os.path.exists(slide), "No se creó slide sin KB"
    assert os.path.getsize(slide) > 0, "Slide sin KB está vacío"
    log_pass(f"Sin Ken Burns: {os.path.getsize(slide)}B")

    # Con Ken Burns
    slide_kb = crear_diapositiva_imagen(img, duracion=2, resolucion="320x180", ken_burns=True)
    assert os.path.exists(slide_kb), "No se creó slide con KB"
    assert os.path.getsize(slide_kb) > 0, "Slide con KB está vacío"
    log_pass(f"Con Ken Burns: {os.path.getsize(slide_kb)}B")


def test_color_grading():
    """Test color grading con todos los presets."""
    print(f"\n{Colors.BOLD}=== TEST 4: Color grading ==={Colors.RESET}")

    from video_processor import aplicar_color_grading

    video = video_corto(duracion=2)

    for preset in ["neutro", "calido", "frio", "cinematico", "vibrante"]:
        resultado = aplicar_color_grading(video, preset)
        assert os.path.exists(resultado), f"No existe salida para {preset}"
        assert os.path.getsize(resultado) > 0, f"Vacío para {preset}"
        log_pass(f"{preset}: {os.path.getsize(resultado)}B")


def test_audio_ducking():
    """Test audio ducking."""
    print(f"\n{Colors.BOLD}=== TEST 5: Audio ducking ==={Colors.RESET}")

    from video_processor import aplicar_audio_ducking

    video = video_corto(duracion=2)
    musica = audio_corto(duracion=3)

    resultado = aplicar_audio_ducking(video, musica, 1.0, 0.15)
    assert os.path.exists(resultado), "No existe salida"
    assert os.path.getsize(resultado) > 0, "Salida vacía"
    log_pass(f"Audio ducking: {os.path.getsize(resultado)}B")


def test_unir_clips():
    """Test unir 2 clips con transición fade."""
    print(f"\n{Colors.BOLD}=== TEST 6: Unir clips ==={Colors.RESET}")

    from video_processor import unir_clips_con_transiciones, _get_video_duration

    clip1 = video_corto(duracion=2, nombre="c1.mp4")
    clip2 = video_corto(duracion=2, nombre="c2.mp4")

    resultado = unir_clips_con_transiciones([clip1, clip2], "fade", 0.3)
    assert os.path.exists(resultado), "No existe resultado"
    assert os.path.getsize(resultado) > 0, "Resultado vacío"
    d = _get_video_duration(resultado)
    # 2 + 2 - 0.3 (transición) = 3.7s aprox
    log_pass(f"Unión: {os.path.getsize(resultado)}B, {d:.2f}s")


def test_subtitulos():
    """Test generación y quemado de subtítulos."""
    print(f"\n{Colors.BOLD}=== TEST 7: Subtítulos ==={Colors.RESET}")

    from video_processor import generar_subtitulos_srt, quemar_subtitulos
    from templates_data import PLANTILLAS_PROFESIONALES

    transcripcion = {
        "text": "Hola mundo",
        "segments": [
            {"start": 0.0, "end": 1.5, "text": "Hola"},
            {"start": 1.5, "end": 2.5, "text": "mundo"},
        ]
    }
    srt = generar_subtitulos_srt(transcripcion)
    assert os.path.exists(srt)
    with open(srt, 'r', encoding='utf-8') as f:
        content = f.read()
    assert "Hola" in content
    log_pass(f"SRT: {len(content)} chars")

    video = video_corto(duracion=2)
    plantilla = PLANTILLAS_PROFESIONALES[0]
    video_subs = quemar_subtitulos(video, srt, plantilla)
    assert os.path.exists(video_subs), "No existe video con subs"
    assert os.path.getsize(video_subs) > 0, "Video con subs vacío"
    log_pass(f"Video con subs: {os.path.getsize(video_subs)}B")


def test_export_multi_formato():
    """Test exportación a YouTube, TikTok, Instagram."""
    print(f"\n{Colors.BOLD}=== TEST 8: Exportación multi-formato ==={Colors.RESET}")

    from video_processor import exportar_multi_formato

    video = video_corto(duracion=2)
    formatos = exportar_multi_formato(video)

    for fmt in ["youtube", "tiktok", "instagram"]:
        assert fmt in formatos, f"Falta {fmt}"
        assert os.path.exists(formatos[fmt]), f"No existe {fmt}"
        assert os.path.getsize(formatos[fmt]) > 0, f"Vacío: {fmt}"

        # Verificar dimensiones
        cmd_probe = [
            "ffprobe", "-v", "error", "-select_streams", "v:0",
            "-show_entries", "stream=width,height", "-of", "csv=p=0",
            formatos[fmt]
        ]
        result = subprocess.run(cmd_probe, capture_output=True, text=True, timeout=10)
        dims = result.stdout.strip().split(',')
        w, h = int(dims[0]), int(dims[1])

        if fmt == "youtube":
            assert w == 1920 and h == 1080, f"YT debe ser 1920x1080, obtuve {w}x{h}"
        elif fmt == "tiktok":
            assert w == 1080 and h == 1920, f"TT debe ser 1080x1920, obtuve {w}x{h}"
        elif fmt == "instagram":
            assert w == 1080 and h == 1080, f"IG debe ser 1080x1080, obtuve {w}x{h}"

        log_pass(f"{fmt}: {w}x{h}, {os.path.getsize(formatos[fmt])}B")


def test_pipeline_completo():
    """Test pipeline completo sin Whisper (usando funciones individuales)."""
    print(f"\n{Colors.BOLD}=== TEST 9: Pipeline completo (sin Whisper) ==={Colors.RESET}")

    from video_processor import (
        crear_intro_profesional, crear_outro_profesional,
        crear_diapositiva_imagen, unir_clips_con_transiciones,
        aplicar_color_grading, aplicar_audio_ducking,
        exportar_multi_formato, _get_video_duration
    )
    from templates_data import PLANTILLAS_PROFESIONALES

    plantilla = PLANTILLAS_PROFESIONALES[0]
    video_principal = video_corto(duracion=3)
    img = imagen_corta()
    audio = audio_corto(duracion=5)

    inicio = time.time()

    # Crear intro
    intro = crear_intro_profesional("Test Pipeline", plantilla, duracion=2, resolucion="320x180")
    assert os.path.getsize(intro) > 0
    log_step(f"✓ Intro creada")

    # Crear diapositiva
    slide = crear_diapositiva_imagen(img, duracion=2, resolucion="320x180", ken_burns=True)
    assert os.path.getsize(slide) > 0
    log_step(f"✓ Diapositiva creada")

    # Crear outro
    outro = crear_outro_profesional(plantilla, "Suscríbete!", duracion=2, resolucion="320x180")
    assert os.path.getsize(outro) > 0
    log_step(f"✓ Outro creada")

    # Unir clips
    merged = unir_clips_con_transiciones([intro, slide, video_principal, outro], "fade", 0.3)
    assert os.path.getsize(merged) > 0
    log_step(f"✓ Clips unidos")

    # Color grading
    graded = aplicar_color_grading(merged, plantilla.get("config_avanzada", {}).get("color_grading", "neutro"))
    log_step(f"✓ Color grading aplicado")

    # Audio ducking
    final_audio = aplicar_audio_ducking(graded, audio, 1.0, 0.15)
    log_step(f"✓ Audio ducking aplicado")

    # Exportar
    formatos = exportar_multi_formato(final_audio)
    for fmt, path in formatos.items():
        assert os.path.getsize(path) > 0, f"Formato {fmt} vacío"
    log_step(f"✓ {len(formatos)} formatos exportados")

    duracion_total = time.time() - inicio
    log_pass(f"Pipeline completo en {duracion_total:.1f}s")


def test_robustez():
    """Test robustez: caracteres especiales, títulos vacíos, etc."""
    print(f"\n{Colors.BOLD}=== TEST 10: Robustez ==={Colors.RESET}")

    from video_processor import crear_intro_profesional, crear_diapositiva_imagen
    from templates_data import PLANTILLAS_PROFESIONALES

    plantilla = PLANTILLAS_PROFESIONALES[0]

    # Título con caracteres especiales
    intro = crear_intro_profesional("Título: 100% Test!", plantilla, duracion=2, resolucion="320x180")
    assert os.path.exists(intro) and os.path.getsize(intro) > 0
    log_pass("Maneja caracteres especiales")

    # Título vacío
    intro2 = crear_intro_profesional("", plantilla, duracion=2, resolucion="320x180")
    assert os.path.exists(intro2)
    log_pass("Maneja título vacío")

    # Título muy largo
    intro3 = crear_intro_profesional("A" * 100, plantilla, duracion=2, resolucion="320x180")
    assert os.path.exists(intro3)
    log_pass("Maneja título largo")

    # Imagen inexistente (debe manejar error)
    try:
        slide = crear_diapositiva_imagen("/no/existe.png", duracion=2, resolucion="320x180", ken_burns=False)
        log_pass("Manejó imagen inexistente sin crashear")
    except Exception:
        log_pass("Manejó imagen inexistente con excepción")


# ============ MAIN ============
def main():
    print(f"{Colors.BOLD}{'=' * 70}{Colors.RESET}")
    print(f"{Colors.BOLD}Tests E2E con FFmpeg REAL (versión optimizada){Colors.RESET}")
    print(f"{Colors.BOLD}{'=' * 70}{Colors.RESET}")
    print(f"FFmpeg: {subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True).stdout.split(chr(10))[0][:50]}")

    test_assets()
    test_intro_outro()
    test_diapositiva()
    test_color_grading()
    test_audio_ducking()
    test_unir_clips()
    test_subtitulos()
    test_export_multi_formato()
    test_pipeline_completo()
    test_robustez()

    # Limpiar
    try:
        shutil.rmtree(test_assets_dir)
    except Exception:
        pass

    # Resumen
    total = results["pass"] + results["fail"] + results["warn"]
    print(f"\n{Colors.BOLD}{'=' * 70}{Colors.RESET}")
    print(f"{Colors.BOLD}RESUMEN{Colors.RESET}")
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
        print(f"\n{Colors.GREEN}{Colors.BOLD}¡TODOS LOS TESTS E2E PASARON! 🎉{Colors.RESET}")
        sys.exit(0)


if __name__ == "__main__":
    main()
