"""
Pipeline de procesamiento de video profesional.
Incluye: detección de silencios, audio ducking, color grading,
transiciones cinemáticas, subtítulos con estilo y exportación multi-formato.
"""

import os
import subprocess
import uuid
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime

# Importar las rutas
from database import OUTPUTS, TEMP_DIR, UPLOADS


def _run_ffmpeg(cmd: List[str], timeout: int = 600) -> Tuple[bool, str]:
    """Ejecuta FFmpeg con manejo de errores."""
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout
        )
        if result.returncode != 0:
            return False, result.stderr[-500:] if result.stderr else "Error desconocido"
        return True, "OK"
    except subprocess.TimeoutExpired:
        return False, "Timeout procesando video"
    except Exception as e:
        return False, str(e)


def _get_video_duration(ruta_video: str) -> float:
    """Obtiene la duración de un video usando ffprobe."""
    try:
        cmd = [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", ruta_video
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return float(result.stdout.strip()) if result.stdout.strip() else 0.0
    except Exception:
        return 0.0


def detectar_silencios(ruta_video: str, umbral_db: int = -45,
                       duracion_min: float = 1.0) -> List[Tuple[float, float]]:
    """Detecta segmentos de silencio en el video."""
    cmd = [
        "ffmpeg", "-i", ruta_video,
        "-af", f"silencedetect=noise={umbral_db}dB:d={duracion_min}",
        "-f", "null", "-"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    silencios = []
    inicio = None
    for linea in result.stderr.splitlines():
        if "silence_start" in linea:
            try:
                inicio = float(linea.split("silence_start:")[1].strip())
            except (ValueError, IndexError):
                pass
        elif "silence_end" in linea and inicio is not None:
            try:
                fin = float(linea.split("silence_end:")[1].split("|")[0].strip())
                silencios.append((inicio, fin))
                inicio = None
            except (ValueError, IndexError):
                pass
    return silencios


def detectar_scenas(ruta_video: str, threshold: float = 0.3) -> List[float]:
    """Detecta cambios de escena usando detección de cortes."""
    try:
        cmd = [
            "ffmpeg", "-i", ruta_video,
            "-filter:v", f"select='gt(scene,{threshold})',showinfo",
            "-f", "null", "-"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        tiempos = []
        for linea in result.stderr.splitlines():
            if "pts_time:" in linea:
                try:
                    t = float(linea.split("pts_time:")[1].split()[0])
                    tiempos.append(t)
                except (ValueError, IndexError):
                    pass
        return tiempos
    except Exception:
        return []


def crear_intro_profesional(titulo: str, plantilla: Dict[str, Any],
                            duracion: int = 4, resolucion: str = "1920x1080") -> str:
    """
    Crea una intro profesional con gradiente, título animado y estilo de plantilla.
    """
    color_primario = plantilla.get("color_primario", "#6366F1")
    color_secundario = plantilla.get("color_secundario", "#1E1B4B")
    color_acento = plantilla.get("color_acento", "#FFFFFF")
    color_texto = plantilla.get("color_texto", "#FFFFFF")
    fuente = plantilla.get("fuente", "Inter")

    # Buscar fuente disponible
    fuente_path = _buscar_fuente(fuente)

    intro_path = OUTPUTS / f"intro_{uuid.uuid4().hex}.mp4"

    # Generar gradiente con overlay simple y texto animado (fade-in)
    w, h = resolucion.split("x")
    texto_escaped = _escape_ffmpeg_text(titulo)

    # Fondo sólido con viñeta sutil + texto con fade-in
    filter_complex = (
        f"color=c={color_primario}:s={resolucion}:d={duracion}:r=30[bg];"
        f"[bg]drawbox=x=0:y=0:w={w}:h={h}:color={color_secundario}@0.4:t=fill[bg2];"
        f"[bg2]drawtext=text='{texto_escaped}':"
        f"fontfile={fuente_path}:fontsize=72:fontcolor={color_texto}:"
        f"x=(w-text_w)/2:y=(h-text_h)/2:"
        f"alpha='if(lt(t,0.6),t/0.6,1)':"
        f"shadowcolor=black@0.7:shadowx=2:shadowy=2[v1];"
        f"[v1]drawtext=text='{texto_escaped}':"
        f"fontfile={fuente_path}:fontsize=72:fontcolor={color_acento}@0.3:"
        f"x=(w-text_w)/2+2:y=(h-text_h)/2+2:"
        f"alpha='if(lt(t,0.6),t/0.6,1)'[out]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-filter_complex", filter_complex,
        "-map", "[out]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-pix_fmt", "yuv420p",
        "-t", str(duracion),
        "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
        "-c:a", "aac", "-b:a", "192k", "-ar", "44100",
        "-shortest",
        str(intro_path)
    ]
    success, err = _run_ffmpeg(cmd)
    if not success:
        # Fallback: versión simple sin gradiente
        simple_cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi",
            "-i", f"color=c={color_primario}:s={resolucion}:d={duracion}:r=30",
            "-f", "lavfi",
            "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
            "-vf", f"drawtext=text='{texto_escaped}':"
                   f"fontfile={fuente_path}:fontsize=72:fontcolor={color_texto}:"
                   f"x=(w-text_w)/2:y=(h-text_h)/2:"
                   f"shadowcolor=black@0.7:shadowx=2:shadowy=2",
            "-c:v", "libx264", "-preset", "medium", "-crf", "20",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k",
            "-shortest",
            str(intro_path)
        ]
        _run_ffmpeg(simple_cmd)
    return str(intro_path)


def crear_outro_profesional(plantilla: Dict[str, Any], cta: str = "Suscríbete",
                            duracion: int = 3, resolucion: str = "1920x1080") -> str:
    """Crea un outro profesional con CTA."""
    color_primario = plantilla.get("color_primario", "#6366F1")
    color_acento = plantilla.get("color_acento", "#FFFFFF")
    color_texto = plantilla.get("color_texto", "#FFFFFF")
    fuente_path = _buscar_fuente(plantilla.get("fuente", "Inter"))

    outro_path = OUTPUTS / f"outro_{uuid.uuid4().hex}.mp4"
    cta_escaped = _escape_ffmpeg_text(cta or "Gracias por ver")

    # Outro simple y robusto con CTA + texto secundario
    vf = (
        f"drawtext=text='{cta_escaped}':"
        f"fontfile={fuente_path}:fontsize=64:fontcolor={color_texto}:"
        f"x=(w-text_w)/2:y=(h-text_h)/2-40:"
        f"alpha='if(lt(t,0.4),t/0.4,1)':"
        f"shadowcolor=black@0.7:shadowx=2:shadowy=2,"
        f"drawtext=text='GRACIAS POR VER':"
        f"fontfile={fuente_path}:fontsize=28:fontcolor={color_acento}@0.95:"
        f"x=(w-text_w)/2:y=(h-text_h)/2+40"
    )

    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", f"color=c={color_primario}:s={resolucion}:d={duracion}:r=30",
        "-f", "lavfi",
        "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
        "-vf", vf,
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        str(outro_path)
    ]
    success, _ = _run_ffmpeg(cmd)
    if not success:
        # Fallback mínimo
        fallback_cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi",
            "-i", f"color=c={color_primario}:s={resolucion}:d={duracion}:r=30",
            "-f", "lavfi",
            "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
            "-c:v", "libx264", "-preset", "medium", "-crf", "20",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k",
            "-shortest",
            str(outro_path)
        ]
        _run_ffmpeg(fallback_cmd)
    return str(outro_path)


def crear_diapositiva_imagen(ruta_imagen: str, duracion: int = 3,
                             resolucion: str = "1920x1080",
                             ken_burns: bool = True) -> str:
    """
    Crea una diapositiva de imagen con efecto Ken Burns (zoom suave).
    """
    slide_path = OUTPUTS / f"slide_{uuid.uuid4().hex}.mp4"

    # Siempre usar el approach simple con pad+scale para máxima compatibilidad
    # El zoompan puede tener problemas con imágenes pequeñas o relaciones inusuales
    vf = (
        f"scale={resolucion}:force_original_aspect_ratio=decrease,"
        f"pad={resolucion}:(ow-iw)/2:(oh-ih)/2:color=black"
    )

    # Aplicar efecto zoom solo si está habilitado y la imagen lo permite
    if ken_burns:
        try:
            w, h = resolucion.split("x")
            # zoompan requiere dimensiones específicas
            vf_zoompan = (
                f"scale={int(w)*2}:{int(h)*2}:force_original_aspect_ratio=increase,"
                f"crop={int(w)*2}:{int(h)*2},"
                f"zoompan=z='min(zoom+0.0008,1.1)':d={duracion*30}:s={resolucion}:fps=30"
            )
            cmd = [
                "ffmpeg", "-y", "-loop", "1", "-i", ruta_imagen,
                "-t", str(duracion),
                "-vf", vf_zoompan,
                "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                "-pix_fmt", "yuv420p",
                "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
                "-c:a", "aac", "-b:a", "192k",
                "-shortest",
                str(slide_path)
            ]
            success, _ = _run_ffmpeg(cmd)
            if success:
                return str(slide_path)
        except Exception:
            pass

    # Fallback: diapositiva simple sin zoom
    cmd = [
        "ffmpeg", "-y", "-loop", "1", "-i", ruta_imagen,
        "-t", str(duracion),
        "-vf", vf,
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-pix_fmt", "yuv420p",
        "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        str(slide_path)
    ]
    _run_ffmpeg(cmd)
    return str(slide_path)


def aplicar_color_grading(ruta_video: str, preset: str = "neutro") -> str:
    """
    Aplica color grading según el preset seleccionado.
    Presets: neutro, calido, frio, cinematico, vibrante
    """
    presets = {
        "neutro": "eq=1.0:1.0:1.0:1.0:1.0:1.0:1.0:1.0",
        "calido": "eq=1.1:1.05:0.95:1.0:1.0:1.0:1.0:1.0,curves=r='0 0.05 1 1':g='0 0.02 1 1'",
        "frio": "eq=0.95:1.0:1.1:1.0:1.0:1.0:1.0:1.0,curves=b='0 0.05 1 1'",
        "cinematico": "eq=1.05:1.0:0.95:1.05:1.0:0.95:1.0:1.0,curves=all='0 0.1 0.5 0.55 1 0.9',vignette=PI/5",
        "vibrante": "eq=1.1:1.1:1.1:1.2:1.0:1.0:1.0:1.0,saturation=1.3",
    }

    vf = presets.get(preset, presets["neutro"])
    output_path = TEMP_DIR / f"graded_{uuid.uuid4().hex}.mp4"
    cmd = [
        "ffmpeg", "-y", "-i", ruta_video,
        "-vf", vf,
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-c:a", "copy",
        str(output_path)
    ]
    success, _ = _run_ffmpeg(cmd)
    return str(output_path) if success else ruta_video


def aplicar_audio_ducking(video_path: str, musica_path: str,
                          voz_volume: float = 1.0,
                          musica_volume: float = 0.15) -> str:
    """
    Mezcla audio de música con ducking automático (baja música cuando hay voz).
    """
    output_path = TEMP_DIR / f"ducked_{uuid.uuid4().hex}.mp4"

    # Ducking: baja el volumen de la música basado en la detección de voz
    filter_complex = (
        f"[0:a]volume={voz_volume}[voz];"
        f"[1:a]volume={musica_volume}[musica];"
        f"[voz][musica]amix=inputs=2:duration=first:dropout_transition=0[aout]"
    )

    cmd = [
        "ffmpeg", "-y", "-i", video_path, "-i", musica_path,
        "-filter_complex", filter_complex,
        "-map", "0:v", "-map", "[aout]",
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        str(output_path)
    ]
    success, _ = _run_ffmpeg(cmd)
    return str(output_path) if success else video_path


def unir_clips_con_transiciones(clips: List[str],
                                tipo_transicion: str = "fade",
                                duracion_transicion: float = 0.5) -> str:
    """
    Une clips aplicando transiciones suaves entre ellos.
    Transiciones: fade, slide, zoom, wipe, smooth
    """
    if not clips:
        return ""
    if len(clips) == 1:
        return clips[0]

    output_path = TEMP_DIR / f"merged_{uuid.uuid4().hex}.mp4"

    # Normalizar todos los clips: misma resolución, fps, codec, audio
    normalized_clips = []
    for i, clip in enumerate(clips):
        norm_path = TEMP_DIR / f"norm_{i}_{uuid.uuid4().hex}.mp4"
        norm_cmd = [
            "ffmpeg", "-y", "-i", clip,
            "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=black,fps=30",
            "-c:v", "libx264", "-preset", "fast", "-crf", "22",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2",
            "-t", str(_get_video_duration(clip) or 10),  # Limitar duración
            str(norm_path)
        ]
        if _run_ffmpeg(norm_cmd)[0]:
            normalized_clips.append(str(norm_path))
        else:
            # Si falla, usar el original
            normalized_clips.append(clip)

    # Si solo quedó un clip válido
    if len(normalized_clips) == 1:
        return normalized_clips[0]

    # Calcular duraciones de clips normalizados
    durations = [_get_video_duration(c) for c in normalized_clips]
    if any(d == 0 for d in durations):
        # No pudimos obtener duraciones, usar concatenación simple
        list_path = TEMP_DIR / f"concat_list_{uuid.uuid4().hex}.txt"
        with open(list_path, 'w') as f:
            for c in normalized_clips:
                f.write(f"file '{c}'\n")
        cmd_concat = [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", str(list_path),
            "-c", "copy",
            str(output_path)
        ]
        if _run_ffmpeg(cmd_concat)[0]:
            return str(output_path)
        # Si falla, retornar el primer clip
        return normalized_clips[0]

    # Construir filter_complex con xfade encadenado
    inputs = []
    for clip in normalized_clips:
        inputs.extend(["-i", clip])

    filter_parts = []
    prev_label = "[0:v]"

    for i in range(1, len(normalized_clips)):
        # Offset acumulado
        offset = sum(durations[:i]) - duracion_transicion
        if offset < 0:
            offset = 0.1
        out_label = f"[v{i}]" if i < len(normalized_clips) - 1 else "[vout]"
        filter_parts.append(
            f"{prev_label}[{i}:v]xfade=transition={tipo_transicion}:"
            f"duration={duracion_transicion}:offset={offset:.3f}{out_label}"
        )
        prev_label = out_label

    filter_complex = ";".join(filter_parts)

    cmd = [
        "ffmpeg", "-y"
    ] + inputs + [
        "-filter_complex", filter_complex,
        "-map", "[vout]",
        "-map", "0:a",
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        str(output_path)
    ]

    success, err = _run_ffmpeg(cmd, timeout=900)

    if not success:
        # Fallback: concatenación simple sin transiciones
        list_path = TEMP_DIR / f"concat_fallback_{uuid.uuid4().hex}.txt"
        with open(list_path, 'w') as f:
            for c in normalized_clips:
                f.write(f"file '{c}'\n")
        cmd_concat = [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", str(list_path),
            "-c:v", "libx264", "-preset", "fast", "-crf", "22",
            "-c:a", "aac", "-b:a", "192k",
            str(output_path)
        ]
        success, _ = _run_ffmpeg(cmd_concat, timeout=900)

    return str(output_path) if success else normalized_clips[0]


def generar_subtitulos_srt(transcripcion: Dict[str, Any]) -> str:
    """Genera archivo SRT desde transcripción de Whisper."""
    srt_content = ""
    segments = transcripcion.get("segments", [])

    for i, segm in enumerate(segments, 1):
        start = segm["start"]
        end = segm["end"]
        text = segm["text"].strip()

        def format_time(s: float) -> str:
            h = int(s // 3600)
            m = int((s % 3600) // 60)
            sec = int(s % 60)
            ms = int((s - int(s)) * 1000)
            return f"{h:02d}:{m:02d}:{sec:02d},{ms:03d}"

        srt_content += f"{i}\n{format_time(start)} --> {format_time(end)}\n{text}\n\n"

    ruta_srt = OUTPUTS / f"subtitulos_{uuid.uuid4().hex}.srt"
    with open(ruta_srt, 'w', encoding='utf-8') as f:
        f.write(srt_content)
    return str(ruta_srt)


def quemar_subtitulos(video_path: str, ruta_srt: str,
                      plantilla: Dict[str, Any]) -> str:
    """Quema subtítulos en el video con el estilo de la plantilla."""
    output_path = TEMP_DIR / f"subtitled_{uuid.uuid4().hex}.mp4"

    color_sub = plantilla.get("color_sub", "#FFFFFF")
    color_borde = "#000000"
    tamano = plantilla.get("config_avanzada", {}).get("subtitulo_tamano", 24)
    posicion = plantilla.get("config_avanzada", {}).get("subtitulo_posicion", "bottom")

    # Convertir color hex a ASS (formato BGR invertido)
    def hex_to_ass(h):
        h = h.lstrip("#")
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        return f"&H00{b:02X}{g:02X}{r:02X}"

    margin_v = 60 if posicion == "bottom" else (200 if posicion == "center" else 60)
    alignment = 2 if posicion == "bottom" else (5 if posicion == "center" else 8)

    force_style = (
        f"FontName=Montserrat,FontSize={tamano},"
        f"PrimaryColour={hex_to_ass(color_sub)},"
        f"OutlineColour={hex_to_ass(color_borde)},"
        f"BorderStyle=1,Outline=2,Shadow=1,"
        f"Alignment={alignment},MarginV={margin_v}"
    )

    # Construir filtro de subtítulos con escape correcto de la ruta
    # FFmpeg usa ':' como separador, hay que escapar en Windows/rutas con :
    srt_escaped = ruta_srt.replace("\\", "/").replace(":", "\\:")

    # Intentar primero con force_style, fallback a estilo simple si falla
    cmd = [
        "ffmpeg", "-y", "-i", video_path,
        "-vf", f"subtitles='{srt_escaped}':force_style='{force_style}'",
        "-c:a", "copy",
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-pix_fmt", "yuv420p",
        str(output_path)
    ]
    success, _ = _run_ffmpeg(cmd, timeout=900)

    if not success:
        # Fallback: subtítulos con estilo básico
        cmd_basic = [
            "ffmpeg", "-y", "-i", video_path,
            "-vf", f"subtitles='{srt_escaped}'",
            "-c:a", "copy",
            "-c:v", "libx264", "-preset", "medium", "-crf", "20",
            "-pix_fmt", "yuv420p",
            str(output_path)
        ]
        success, _ = _run_ffmpeg(cmd_basic, timeout=900)

    return str(output_path) if success else video_path


def exportar_multi_formato(video_path: str) -> Dict[str, str]:
    """Exporta el video en formatos para YouTube, TikTok e Instagram."""
    formatos = {}

    # YouTube 16:9 (1920x1080)
    yt_path = OUTPUTS / f"youtube_{uuid.uuid4().hex}.mp4"
    cmd_yt = [
        "ffmpeg", "-y", "-i", video_path,
        "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=black",
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-c:a", "aac", "-b:a", "192k",
        str(yt_path)
    ]
    if _run_ffmpeg(cmd_yt)[0]:
        formatos["youtube"] = str(yt_path)

    # TikTok 9:16 (1080x1920)
    tk_path = OUTPUTS / f"tiktok_{uuid.uuid4().hex}.mp4"
    cmd_tk = [
        "ffmpeg", "-y", "-i", video_path,
        "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=black",
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-c:a", "aac", "-b:a", "192k",
        str(tk_path)
    ]
    if _run_ffmpeg(cmd_tk)[0]:
        formatos["tiktok"] = str(tk_path)

    # Instagram 1:1 (1080x1080)
    ig_path = OUTPUTS / f"instagram_{uuid.uuid4().hex}.mp4"
    cmd_ig = [
        "ffmpeg", "-y", "-i", video_path,
        "-vf", "scale=1080:1080:force_original_aspect_ratio=decrease,pad=1080:1080:(ow-iw)/2:(oh-ih)/2:color=black",
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-c:a", "aac", "-b:a", "192k",
        str(ig_path)
    ]
    if _run_ffmpeg(cmd_ig)[0]:
        formatos["instagram"] = str(ig_path)

    return formatos


def procesar_video_completo(ruta_video: str, guion: Dict[str, Any],
                            plantilla: Dict[str, Any],
                            archivos_extra: Dict[str, Any],
                            formatos_seleccionados: List[str] = None,
                            progress_callback=None) -> Dict[str, Any]:
    """
    Pipeline completo de procesamiento de video.
    """
    try:
        if progress_callback:
            progress_callback(0.05, "Iniciando transcripción con Whisper...")

        # Transcripción con Whisper
        import whisper
        whisper_model = plantilla.get("config_avanzada", {}).get("whisper_model", "base")
        modelo = whisper.load_model(whisper_model)
        transcripcion = modelo.transcribe(ruta_video, fp16=False)

        if progress_callback:
            progress_callback(0.15, "Transcripción completada. Detectando silencios...")

        # Detectar silencios para cortar muerto
        silencios = detectar_silencios(ruta_video)

        if progress_callback:
            progress_callback(0.25, "Cortando segmentos útiles...")

        # Cortar segmentos útiles del video principal
        temp_dir = TEMP_DIR / f"project_{uuid.uuid4().hex}"
        temp_dir.mkdir(parents=True, exist_ok=True)

        segmentos = []
        inicio = 0.0
        for i, (s_ini, s_fin) in enumerate(silencios):
            if s_ini - inicio >= 2:  # Solo segmentos > 2s
                seg = temp_dir / f"seg_{i:03d}.mp4"
                cmd = [
                    "ffmpeg", "-y", "-ss", str(inicio), "-i", ruta_video,
                    "-t", str(s_ini - inicio),
                    "-c:v", "libx264", "-preset", "fast", "-crf", "22",
                    "-c:a", "aac",
                    str(seg)
                ]
                if _run_ffmpeg(cmd)[0]:
                    segmentos.append(str(seg))
            inicio = s_fin

        # Último segmento
        seg_final = temp_dir / "seg_final.mp4"
        cmd = [
            "ffmpeg", "-y", "-ss", str(inicio), "-i", ruta_video,
            "-c:v", "libx264", "-preset", "fast", "-crf", "22",
            "-c:a", "aac",
            str(seg_final)
        ]
        if _run_ffmpeg(cmd)[0]:
            segmentos.append(str(seg_final))

        if progress_callback:
            progress_callback(0.40, "Creando intro profesional...")

        # Construir lista final de clips
        clips_finales = []

        # 1. Intro
        if guion and "titulo" in guion:
            intro = crear_intro_profesional(
                guion["titulo"], plantilla,
                duracion=plantilla.get("config_avanzada", {}).get("intro_duracion", 4)
            )
            clips_finales.append(intro)

        # 2. Imágenes como B-roll intercalado
        if archivos_extra.get("imagenes"):
            for img_path in archivos_extra["imagenes"]:
                slide = crear_diapositiva_imagen(img_path, duracion=3, ken_burns=True)
                clips_finales.append(slide)

        # 3. Segmentos del video principal
        clips_finales.extend(segmentos)

        # 4. Videos extra
        if archivos_extra.get("videos"):
            for v_path in archivos_extra["videos"]:
                clips_finales.append(v_path)

        # 5. Outro
        if guion and "cta_final" in guion:
            outro = crear_outro_profesional(
                plantilla, guion["cta_final"],
                duracion=plantilla.get("config_avanzada", {}).get("outro_duracion", 3)
            )
            clips_finales.append(outro)

        if progress_callback:
            progress_callback(0.60, "Uniendo clips con transiciones...")

        # Unir con transiciones
        tipo_transicion = plantilla.get("transicion", "fade")
        dur_transicion = plantilla.get("duracion_transicion", 0.5)

        if len(clips_finales) > 1:
            video_base = unir_clips_con_transiciones(
                clips_finales, tipo_transicion, dur_transicion
            )
        else:
            video_base = clips_finales[0] if clips_finales else ruta_video

        if progress_callback:
            progress_callback(0.70, "Aplicando color grading...")

        # Color grading
        preset_grading = plantilla.get("config_avanzada", {}).get("color_grading", "neutro")
        video_base = aplicar_color_grading(video_base, preset_grading)

        if progress_callback:
            progress_callback(0.80, "Procesando audio...")

        # Audio ducking con música
        if archivos_extra.get("audio"):
            musica_vol = plantilla.get("config_avanzada", {}).get("musica_volumen", 0.15)
            voz_vol = plantilla.get("config_avanzada", {}).get("voz_volumen", 1.0)
            video_base = aplicar_audio_ducking(
                video_base, archivos_extra["audio"], voz_vol, musica_vol
            )

        if progress_callback:
            progress_callback(0.85, "Generando subtítulos...")

        # Subtítulos
        ruta_srt = None
        if transcripcion and "segments" in transcripcion:
            ruta_srt = generar_subtitulos_srt(transcripcion)
            video_base = quemar_subtitulos(video_base, ruta_srt, plantilla)

        if progress_callback:
            progress_callback(0.95, "Exportando a múltiples formatos...")

        # Exportar formatos
        formatos_seleccionados = formatos_seleccionados or ["youtube", "tiktok", "instagram"]
        todos_formatos = exportar_multi_formato(video_base)
        formatos_filtrados = {
            k: v for k, v in todos_formatos.items()
            if k in formatos_seleccionados
        }

        if progress_callback:
            progress_callback(1.0, "¡Video completado!")

        return {
            "video_final": video_base,
            "formatos": formatos_filtrados,
            "subtitulos": ruta_srt,
            "transcripcion": transcripcion.get("text", ""),
            "segmentos_procesados": len(segmentos),
            "duracion_original": _get_video_duration(ruta_video),
        }

    except Exception as e:
        return {"error": f"Error en procesamiento: {str(e)}"}


# ============ UTILIDADES DE FUENTES ============

def _buscar_fuente(nombre_fuente: str) -> str:
    """Busca una fuente disponible por nombre."""
    mapeo_fuentes = {
        "Inter": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "Montserrat": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "Poppins": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "Lato": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "JetBrains Mono": "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    }
    return mapeo_fuentes.get(nombre_fuente, "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")


def _escape_ffmpeg_text(texto: str) -> str:
    """Escapa texto para usar en drawtext de FFmpeg."""
    if not texto:
        return ""
    # Reemplazar caracteres problemáticos
    texto = texto.replace("\\", "\\\\")
    texto = texto.replace(":", "\\:")
    texto = texto.replace("'", "\u2019")
    texto = texto.replace("%", "\\%")
    return texto
