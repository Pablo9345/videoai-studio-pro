"""
Integración con la API de Groq AI.
Incluye: generación de guiones, hashtags, descripciones, miniaturas,
títulos optimizados y mejora de prompts.
"""

import json
import re
import requests
from typing import Any, Dict, List, Optional


class GroqAI:
    """Cliente para la API de Groq con métodos especializados."""

    def __init__(self, api_key: str, model: str = "llama-3.1-70b-versatile"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.groq.com/openai/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

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

    def _limpiar_json(self, texto: str) -> str:
        """Extrae JSON limpio de una respuesta de LLM."""
        if isinstance(texto, dict):
            return json.dumps(texto)
        texto = re.sub(r'```json\s*|\s*```', '', texto)
        texto = re.sub(r'```.*?```', '', texto, flags=re.DOTALL)
        # Buscar el primer { o [
        starts = [i for i in (texto.find('{'), texto.find('[')) if i != -1]
        if not starts:
            return texto
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
        return texto

    def _consultar(self, prompt: str, temperature: float = 0.7,
                   max_tokens: int = 4000, system: Optional[str] = None) -> str:
        """Hace una consulta al modelo."""
        if not self.api_key:
            return "ERROR: API key no configurada"
        try:
            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})

            data = {
                "model": self.model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
            }
            r = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=data,
                timeout=60,
            )
            if r.status_code == 200:
                return r.json()["choices"][0]["message"]["content"]
            return f"ERROR: HTTP {r.status_code}: {r.text}"
        except Exception as e:
            return f"ERROR: {str(e)}"

    def _safe_json(self, texto: str) -> Dict[str, Any]:
        """Intenta parsear JSON de forma segura."""
        limpio = self._limpiar_json(texto)
        try:
            return json.loads(limpio)
        except json.JSONDecodeError:
            return {"error": "No se pudo parsear JSON", "raw": texto[:500]}

    # ============ GENERACIÓN DE GUIONES ============

    def generar_guion_completo(self, texto_objetivo: str, tipo_contenido: str,
                              duracion_minutos: int, material_descripcion: str,
                              plantilla_nombre: str = "") -> Dict[str, Any]:
        """
        Genera un guion técnico completo con estructura profesional.
        Incluye: título, hook, escenas con B-roll sugerido, CTA y elementos de marca.
        """
        system = """Eres un director de producción audiovisual y guionista profesional con 15 años de experiencia.
Especializado en contenido viral para redes sociales y producción corporativa premium.
Conoces perfectamente técnicas de storytelling, retención de audiencia y narrativa visual.
Tus guiones son estructurados, profesionales y están optimizados para retener la atención del espectador."""

        prompt = f"""
Crea un guion técnico COMPLETO y PROFESIONAL para un video de {duracion_minutos} minutos.

INFORMACIÓN:
- Tipo de contenido: {tipo_contenido}
- Objetivo/mensaje: {texto_objetivo}
- Material disponible: {material_descripcion}
- Estilo de plantilla: {plantilla_nombre}

REQUISITOS:
1. Hook potente en los primeros 3 segundos
2. Estructura narrativa con inicio, desarrollo y cierre
3. Cada escena debe tener: descripción visual, texto en pantalla, sugerencia de B-roll y duración precisa
4. Música/ambiente sugerido para cada escena
5. CTA (Call to Action) claro al final
6. Optimizado para retención de audiencia

Devuelve ÚNICAMENTE un JSON válido con esta estructura exacta:
{{
    "titulo": "título atractivo del video",
    "hook": "frase de gancho para los primeros 3 segundos",
    "introduccion": "texto narrado de introducción (2-3 frases)",
    "escenas": [
        {{
            "numero": 1,
            "titulo_escena": "nombre corto de la escena",
            "descripcion": "descripción visual detallada de lo que se ve",
            "narracion": "texto que se narra en esta escena",
            "texto_en_pantalla": "texto breve a mostrar en pantalla",
            "b_roll_sugerido": "qué material mostrar",
            "musica_ambiente": "descripción del ambiente sonoro",
            "duracion_seg": 8
        }}
    ],
    "cta_final": "call to action final claro y directo",
    "hashtags_sugeridos": ["#hashtag1", "#hashtag2"],
    "descripcion_social": "descripción optimizada para redes sociales"
}}

REGLAS:
- La duración total de las escenas debe sumar aproximadamente {duracion_minutos * 60} segundos
- El hook debe ser impactante y crear curiosidad inmediata
- Usa lenguaje natural, conversacional y cercano
- Adapta el tono al tipo de contenido: {tipo_contenido}
"""

        resultado = self._consultar(prompt, temperature=0.7, max_tokens=4000, system=system)
        return self._safe_json(resultado)

    # ============ GENERACIÓN DE CONTENIDO SOCIAL ============

    def generar_metadata_social(self, titulo: str, descripcion: str,
                                tipo_contenido: str) -> Dict[str, Any]:
        """Genera metadata optimizada para redes sociales."""
        prompt = f"""
Genera metadata optimizada para publicar un video en múltiples plataformas.

INFORMACIÓN:
- Título del video: {titulo}
- Descripción: {descripcion}
- Tipo: {tipo_contenido}

Devuelve JSON con:
{{
    "titulo_youtube": "título SEO optimizado (máx 70 chars)",
    "titulo_tiktok": "título corto viral (máx 100 chars)",
    "titulo_instagram": "título con emojis y atractivo",
    "descripcion_youtube": "descripción con keywords, max 5000 chars",
    "descripcion_instagram": "caption con emojis y hashtags integrados",
    "hashtags": ["lista de 15 hashtags relevantes"],
    "tags_youtube": ["lista de 10 tags para YouTube"],
    "mejor_hora_publicacion": "hora recomendada",
    "categoria_youtube": "categoría sugerida"
}}
"""
        resultado = self._consultar(prompt, temperature=0.6, max_tokens=2000)
        return self._safe_json(resultado)

    def generar_ideas_contenido(self, nicho: str, publico_objetivo: str,
                               cantidad: int = 10) -> Dict[str, Any]:
        """Genera ideas de contenido para un nicho específico."""
        prompt = f"""
Genera {cantidad} ideas de contenido viral para video.

Nicho: {nicho}
Público objetivo: {publico_objetivo}

Devuelve JSON con:
{{
    "ideas": [
        {{
            "titulo": "título atractivo",
            "gancho": "frase de gancho para primeros 3 segundos",
            "descripcion": "de qué trata",
            "tipo": "tutorial/review/storylist/educativo/entretenimiento",
            "duracion_sugerida": "1-2 minutos",
            "potencial_viral": "alto/medio/bajo",
            "razon": "por qué tiene potencial"
        }}
    ]
}}
"""
        resultado = self._consultar(prompt, temperature=0.8, max_tokens=3000)
        return self._safe_json(resultado)

    def mejorar_guion(self, guion_actual: str, instrucciones: str = "") -> str:
        """Mejora un guion existente según instrucciones."""
        prompt = f"""
Mejora el siguiente guion de video:

GUION ACTUAL:
{guion_actual}

INSTRUCCIONES: {instrucciones or "Mejora la narrativa, flujo, retención y claridad"}

Devuelve el guion mejorado en texto plano, sin comentarios adicionales.
"""
        return self._consultar(prompt, temperature=0.7, max_tokens=3000)

    def generar_concepto_miniatura(self, titulo: str, tipo_contenido: str) -> Dict[str, Any]:
        """Genera conceptos para la miniatura del video."""
        prompt = f"""
Genera un concepto detallado para la miniatura de un video.

Título: {titulo}
Tipo: {tipo_contenido}

Devuelve JSON con:
{{
    "concepto_principal": "idea general de la miniatura",
    "colores_recomendados": ["#hex1", "#hex2", "#hex3"],
    "texto_superpuesto": "texto breve a mostrar (máx 4 palabras)",
    "elementos_visuales": ["lista de elementos a incluir"],
    "composicion": "descripción de la composición visual",
    "emocion_a_transmitir": "emoción objetivo",
    "estilo": "minimalista/realista/ilustrativo/dramático"
}}
"""
        resultado = self._consultar(prompt, temperature=0.7, max_tokens=1500)
        return self._safe_json(resultado)

    def generar_subtitulos_mejorados(self, transcripcion: str) -> Dict[str, Any]:
        """Mejora una transcripción generando subtítulos con puntuación."""
        prompt = f"""
A partir de esta transcripción, genera subtítulos limpios y profesionales.

TRANSCRIPCIÓN:
{transcripcion[:3000]}

Devuelve JSON con:
{{
    "subtitulos_limpios": "texto limpio con puntuación correcta",
    "idioma_detectado": "español/inglés/...",
    "palabras_clave": ["palabra1", "palabra2"],
    "resumen": "resumen en 2-3 líneas"
}}
"""
        resultado = self._consultar(prompt, temperature=0.3, max_tokens=2000)
        return self._safe_json(resultado)
