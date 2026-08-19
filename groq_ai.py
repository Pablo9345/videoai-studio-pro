"""
Integración con la API de Groq AI.
Manejo robusto de max_tokens según el modelo, con auto-detección del límite.
"""

import json
import re
import requests
from typing import Any, Dict, List, Optional


# ============ LÍMITES POR MODELO (max_tokens de output) ============
# Groq tiene diferentes límites por modelo. Estos son los máximos conocidos.
MODEL_MAX_TOKENS = {
    # Modelos 70b (alta capacidad)
    "llama-3.1-70b-versatile": 8000,
    "llama-3.3-70b-versatile": 8000,
    "llama3-70b-8192": 8192,
    "llama-3.1-70b-instruct": 4096,
    # Modelos 8b (capacidad limitada)
    "llama-3.1-8b-instant": 8000,  # antes 512, ahora ampliado
    "llama3-8b-8192": 8192,
    "llama-3.1-8b-instruct": 4096,
    # Mixtral
    "mixtral-8x7b-32768": 32768,
    "mixtral-8x7b-instruct": 32768,
    # Gemma
    "gemma2-9b-it": 8192,
    "gemma-7b-it": 8192,
    # DeepSeek
    "deepseek-r1-distill-llama-70b": 8000,
    "deepseek-r1-distill-qwen-32b": 8000,
    # Whisper
    "whisper-large-v3": 8000,
    "whisper-large-v3-turbo": 8000,
}

# Límite seguro por defecto (compatible con TODOS los modelos)
SAFE_MAX_TOKENS = 4000

# Modelos recomendados (orden de preferencia)
MODELOS_RECOMENDADOS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-70b-versatile",
    "llama-3.1-8b-instant",
    "mixtral-8x7b-32768",
]


class GroqAI:
    """Cliente para la API de Groq con métodos especializados."""

    def __init__(self, api_key: str, model: str = "llama-3.1-8b-instant"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.groq.com/openai/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        self._max_tokens_cache: Optional[int] = None

    def esta_configurado(self) -> bool:
        return bool(self.api_key)

    def listar_modelos(self) -> List[str]:
        """Lista los modelos disponibles en Groq."""
        try:
            r = requests.get(f"{self.base_url}/models", headers=self.headers, timeout=15)
            if r.status_code == 200:
                data = r.json()
                if "data" in data:
                    return [m["id"] for m in data["data"]]
                return list(data.keys())
            return []
        except Exception:
            return []

    def _get_max_tokens(self, requested: int) -> int:
        """
        Obtiene el límite de max_tokens según el modelo.
        Si no conocemos el modelo, usa un valor seguro (4000).
        Nunca excede el límite del modelo.
        """
        # Si ya tenemos cache, usarlo
        if self._max_tokens_cache is not None:
            return min(requested, self._max_tokens_cache)

        # Buscar el límite del modelo actual
        limite = MODEL_MAX_TOKENS.get(self.model, SAFE_MAX_TOKENS)

        # Si el modelo está en nuestro diccionario, confiamos en ese límite
        # Solo aplicar el límite conservador si NO conocemos el modelo
        if self.model not in MODEL_MAX_TOKENS:
            # Para modelos 8b desconocidos, ser conservador
            if "8b" in self.model.lower() and "instant" not in self.model.lower():
                limite = min(limite, 4000)

        self._max_tokens_cache = limite
        return min(requested, limite)

    def _limpiar_json(self, texto: str) -> str:
        """Extrae JSON limpio de una respuesta de LLM."""
        if isinstance(texto, dict):
            return json.dumps(texto)
        if not isinstance(texto, str):
            return str(texto)

        texto = re.sub(r'```json\s*|\s*```', '', texto)
        texto = re.sub(r'```\s*\n?', '', texto)
        # Buscar el primer { o [
        starts = [i for i in (texto.find('{'), texto.find('[')) if i != -1]
        if not starts:
            return texto.strip()
        start = min(starts)
        # Encontrar el cierre correspondiente
        stack = []
        for i, ch in enumerate(texto[start:], start):
            if ch in '{[':
                stack.append(ch)
            elif ch in '}]':
                if stack and ((ch == '}' and stack[-1] == '{') or (ch == ']' and stack[-1] == '[')):
                    stack.pop()
                    if not stack:
                        return texto[start:i+1]
        return texto[start:].strip()

    def _consultar(self, prompt: str, temperature: float = 0.7,
                   max_tokens: int = 3000, system: Optional[str] = None,
                   reintentar: bool = True) -> str:
        """
        Hace una consulta al modelo con manejo robusto de errores.
        Si max_tokens excede el límite del modelo, se ajusta automáticamente.
        """
        if not self.api_key:
            return "ERROR: API key no configurada"

        # Ajustar max_tokens según el modelo
        max_tokens_ajustado = self._get_max_tokens(max_tokens)

        try:
            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})

            data = {
                "model": self.model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens_ajustado,
            }
            r = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=data,
                timeout=90,
            )
            if r.status_code == 200:
                return r.json()["choices"][0]["message"]["content"]

            # Manejo de error de max_tokens
            error_text = r.text
            if "max_tokens" in error_text and reintentar:
                # Reintentar con menos tokens (mitad)
                nuevo_max = min(max_tokens_ajustado // 2, 2000)
                if nuevo_max >= 500:  # mínimo razonable
                    # Actualizar cache para futuras llamadas
                    self._max_tokens_cache = nuevo_max
                    return self._consultar(prompt, temperature, nuevo_max, system, reintentar=False)

            # Otro error de API
            try:
                error_json = r.json()
                error_msg = error_json.get("error", {}).get("message", error_text)
            except (json.JSONDecodeError, AttributeError):
                error_msg = error_text[:300]

            return f"ERROR: HTTP {r.status_code}: {error_msg}"

        except requests.exceptions.Timeout:
            return "ERROR: La consulta tardó demasiado. Intenta de nuevo."
        except requests.exceptions.ConnectionError:
            return "ERROR: No se pudo conectar con Groq. Verifica tu conexión a internet."
        except Exception as e:
            return f"ERROR: {str(e)}"

    def _safe_json(self, texto: str) -> Dict[str, Any]:
        """Intenta parsear JSON de forma segura."""
        limpio = self._limpiar_json(texto)
        try:
            return json.loads(limpio)
        except json.JSONDecodeError as e:
            return {"error": f"No se pudo parsear JSON: {str(e)}", "raw": texto[:500]}

    # ============ GENERACIÓN DE GUIONES ============

    def generar_guion_completo(self, texto_objetivo: str, tipo_contenido: str,
                              duracion_minutos: int, material_descripcion: str,
                              plantilla_nombre: str = "") -> Dict[str, Any]:
        """
        Genera un guion técnico completo con estructura profesional.
        """
        system = """Eres un director de producción audiovisual y guionista profesional.
Especializado en contenido viral y producción corporativa premium.
Optimizas storytelling y retención de audiencia.
Respondes SIEMPRE con JSON válido, sin texto adicional."""

        # Calcular número de escenas basado en duración (1 escena por ~15 seg)
        num_escenas = max(3, min(8, duracion_minutos * 4))

        prompt = f"""Crea un guion profesional para un video de {duracion_minutos} minuto(s).

Tipo: {tipo_contenido}
Objetivo: {texto_objetivo}
Material: {material_descripcion}
Plantilla: {plantilla_nombre}

Genera exactamente {num_escenas} escenas.

Devuelve SOLO JSON válido con esta estructura:
{{
    "titulo": "título atractivo (máx 60 caracteres)",
    "hook": "frase gancho primeros 3 segundos",
    "introduccion": "texto narrado 2 frases",
    "escenas": [
        {{
            "numero": 1,
            "titulo_escena": "nombre corto",
            "descripcion": "qué se ve en pantalla",
            "narracion": "texto a narrar",
            "texto_en_pantalla": "texto breve a mostrar",
            "b_roll_sugerido": "qué material usar",
            "musica_ambiente": "ambiente sonoro",
            "duracion_seg": 10
        }}
    ],
    "cta_final": "call to action claro y directo",
    "hashtags_sugeridos": ["#hashtag1", "#hashtag2", "#hashtag3"],
    "descripcion_social": "descripción corta para redes sociales"
}}

La duración total debe sumar ~{duracion_minutos * 60} segundos.
Responde SOLO con el JSON, sin markdown ni comentarios."""

        resultado = self._consultar(prompt, temperature=0.7, max_tokens=3000, system=system)
        return self._safe_json(resultado)

    # ============ GENERACIÓN DE CONTENIDO SOCIAL ============

    def generar_metadata_social(self, titulo: str, descripcion: str,
                                tipo_contenido: str) -> Dict[str, Any]:
        """Genera metadata optimizada para redes sociales."""
        prompt = f"""Genera metadata para publicar un video.

Título: {titulo}
Descripción: {descripcion}
Tipo: {tipo_contenido}

Devuelve SOLO JSON:
{{
    "titulo_youtube": "título SEO (máx 70 chars)",
    "titulo_tiktok": "título corto viral (máx 100 chars)",
    "titulo_instagram": "título con emojis",
    "descripcion_youtube": "descripción con keywords (máx 1000 chars)",
    "descripcion_instagram": "caption con emojis y hashtags",
    "hashtags": ["lista de 10 hashtags"],
    "tags_youtube": ["lista de 8 tags"]
}}
Responde SOLO con JSON válido."""

        resultado = self._consultar(prompt, temperature=0.6, max_tokens=2000)
        return self._safe_json(resultado)

    def generar_ideas_contenido(self, nicho: str, publico_objetivo: str,
                               cantidad: int = 8) -> Dict[str, Any]:
        """Genera ideas de contenido para un nicho específico."""
        # Limitar cantidad para no exceder max_tokens
        cantidad = min(cantidad, 10)

        prompt = f"""Genera {cantidad} ideas de contenido viral para video.

Nicho: {nicho}
Público: {publico_objetivo}

Devuelve SOLO JSON con esta estructura exacta:
{{
    "ideas": [
        {{
            "titulo": "título atractivo",
            "gancho": "frase de gancho primeros 3 segundos",
            "descripcion": "de qué trata en 1 frase",
            "tipo": "tutorial/review/educativo/entretenimiento",
            "duracion_sugerida": "1-2 minutos",
            "potencial_viral": "alto/medio/bajo",
            "razon": "por qué tiene potencial"
        }}
    ]
}}

Genera EXACTAMENTE {cantidad} ideas.
Responde SOLO con JSON, sin markdown."""

        resultado = self._consultar(prompt, temperature=0.8, max_tokens=2500)
        return self._safe_json(resultado)

    def mejorar_guion(self, guion_actual: str, instrucciones: str = "") -> str:
        """Mejora un guion existente según instrucciones."""
        prompt = f"""Mejora este guion:

{guion_actual[:2000]}

Instrucciones: {instrucciones or "Mejora narrativa, flujo y retención"}

Devuelve el guion mejorado en texto plano."""

        return self._consultar(prompt, temperature=0.7, max_tokens=2000)

    def generar_concepto_miniatura(self, titulo: str, tipo_contenido: str) -> Dict[str, Any]:
        """Genera conceptos para la miniatura del video."""
        prompt = f"""Genera concepto de miniatura para video.

Título: {titulo}
Tipo: {tipo_contenido}

Devuelve SOLO JSON:
{{
    "concepto_principal": "idea de la miniatura",
    "colores_recomendados": ["#hex1", "#hex2", "#hex3"],
    "texto_superpuesto": "texto breve (máx 4 palabras)",
    "elementos_visuales": ["elemento1", "elemento2"],
    "composicion": "descripción composición",
    "emocion_a_transmitir": "emoción objetivo",
    "estilo": "minimalista/realista/ilustrativo/dramático"
}}
Responde SOLO con JSON."""

        resultado = self._consultar(prompt, temperature=0.7, max_tokens=1200)
        return self._safe_json(resultado)

    def generar_subtitulos_mejorados(self, transcripcion: str) -> Dict[str, Any]:
        """Mejora una transcripción generando subtítulos con puntuación."""
        prompt = f"""Mejora esta transcripción:

{transcripcion[:2000]}

Devuelve SOLO JSON:
{{
    "subtitulos_limpios": "texto limpio con puntuación",
    "idioma_detectado": "español/inglés/...",
    "palabras_clave": ["palabra1", "palabra2"],
    "resumen": "resumen en 2 líneas"
}}
Responde SOLO con JSON."""

        resultado = self._consultar(prompt, temperature=0.3, max_tokens=1500)
        return self._safe_json(resultado)

    def test_conexion(self) -> Dict[str, Any]:
        """
        Hace una consulta simple para verificar que la API funcione.
        Retorna info sobre el modelo y límites detectados.
        """
        if not self.api_key:
            return {"ok": False, "error": "API key no configurada"}

        try:
            # Primero listar modelos para verificar conexión
            modelos = self.listar_modelos()
            if not modelos:
                return {"ok": False, "error": "No se pudo conectar. Verifica tu API key."}

            # Verificar que el modelo seleccionado esté disponible
            modelo_activo = self.model
            if modelo_activo not in modelos:
                # Buscar un modelo recomendado disponible
                for m in MODELOS_RECOMENDADOS:
                    if m in modelos:
                        modelo_activo = m
                        self.model = m
                        self._max_tokens_cache = None  # reset cache
                        break
                else:
                    # Usar el primer modelo disponible
                    modelo_activo = modelos[0]
                    self.model = modelo_activo
                    self._max_tokens_cache = None

            # Hacer una consulta simple para verificar max_tokens
            resultado = self._consultar(
                "Responde con la palabra: OK",
                temperature=0,
                max_tokens=50,
                reintentar=False
            )

            if resultado.startswith("ERROR"):
                return {
                    "ok": False,
                    "error": resultado,
                    "modelos_disponibles": modelos,
                    "modelo_seleccionado": modelo_activo
                }

            max_tokens_detectado = self._get_max_tokens(99999)

            return {
                "ok": True,
                "modelo_activo": modelo_activo,
                "modelos_disponibles": modelos,
                "max_tokens_detectado": max_tokens_detectado,
                "respuesta_test": resultado[:100]
            }

        except Exception as e:
            return {"ok": False, "error": str(e)}
