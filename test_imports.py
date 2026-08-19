#!/usr/bin/env python3
"""Test de imports - verifica que todos los módulos carguen correctamente."""
import sys
import os

# Añadir el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=== Test de imports de VideoAI Studio Pro ===\n")

# Probar imports de cada módulo
tests = [
    ("styles", "PREMIUM_CSS, get_premium_css, render_template_preview_card, render_stat_card, render_wizard"),
    ("templates_data", "PLANTILLAS_PROFESIONALES, MEMBRESIAS, get_plantilla_by_id"),
    ("database", "cargar_db, guardar_db, crear_usuario, autenticar_usuario"),
    ("groq_ai", "GroqAI"),
    ("video_processor", "procesar_video_completo, detectar_silencios"),
]

errors = []
for module, names in tests:
    try:
        exec(f"from {module} import {names}")
        print(f"✅ {module}: OK ({names.split(',')[0].strip()}...)")
    except Exception as e:
        print(f"❌ {module}: ERROR - {e}")
        errors.append((module, str(e)))

print(f"\n=== Resumen: {len(tests) - len(errors)}/{len(tests)} módulos OK ===")

if errors:
    print("\nErrores detallados:")
    for mod, err in errors:
        print(f"  - {mod}: {err}")
    sys.exit(1)
else:
    print("\n✅ Todos los módulos cargan correctamente!")
    sys.exit(0)
