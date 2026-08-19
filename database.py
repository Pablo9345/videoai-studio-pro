"""
Sistema de base de datos JSON con operaciones avanzadas,
thread-safe, con backup automático y migraciones.
"""

import json
import os
import shutil
import threading
from pathlib import Path
from datetime import datetime
import hashlib
import uuid
from typing import Any, Dict, List, Optional

# Configuración de paths (compatible con Streamlit Cloud)
BASE_PATH = Path(os.environ.get("VIDEOAI_BASE_PATH", "/tmp/videoai-studio"))
UPLOADS = BASE_PATH / "uploads"
OUTPUTS = BASE_PATH / "outputs"
DATABASE = BASE_PATH / "database"
PLANTILLAS_DIR = BASE_PATH / "plantillas"
IMAGENES_GENERADAS = BASE_PATH / "imagenes"
TEMP_DIR = BASE_PATH / "temp"

# Crear directorios
for carpeta in [BASE_PATH, UPLOADS, OUTPUTS, DATABASE, PLANTILLAS_DIR, IMAGENES_GENERADAS, TEMP_DIR]:
    carpeta.mkdir(parents=True, exist_ok=True)

DB_FILE = DATABASE / "sistema.json"
DB_BACKUP_DIR = DATABASE / "backups"

# Lock para thread-safety
_db_lock = threading.Lock()


def _default_db() -> Dict[str, Any]:
    """Estructura inicial de la base de datos."""
    from templates_data import MEMBRESIAS
    return {
        "version": "2.0",
        "usuarios": [],
        "plantillas_personalizadas": [],
        "membresias": MEMBRESIAS,
        "config": {
            "groq_api_key": os.environ.get("GROQ_API_KEY", ""),
            "groq_model": "llama-3.1-70b-versatile",
            "whisper_model": "base",
            "admin_password_hash": _hash_password("admin123"),
            "brand_name": "VideoAI Studio Pro",
            "primary_color": "#6366F1",
        },
        "stats": {
            "total_videos_procesados": 0,
            "total_minutos_procesados": 0,
            "fecha_inicio": datetime.now().isoformat(),
        }
    }


def _hash_password(password: str) -> str:
    """Hash seguro de contraseña con salt."""
    salt = "videoai_salt_2024"  # En producción usar bcrypt
    return hashlib.sha256(f"{salt}:{password}".encode()).hexdigest()


def _verify_password(password: str, hash_stored: str) -> bool:
    """Verifica una contraseña."""
    return _hash_password(password) == hash_stored


def cargar_db() -> Dict[str, Any]:
    """Carga la base de datos desde el archivo JSON."""
    with _db_lock:
        if DB_FILE.exists():
            try:
                with open(DB_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                # Intentar cargar backup
                backup = _get_latest_backup()
                if backup:
                    with open(backup, 'r', encoding='utf-8') as f:
                        return json.load(f)
                return _default_db()
        return _default_db()


def guardar_db(data: Dict[str, Any]) -> None:
    """Guarda la base de datos con backup automático."""
    with _db_lock:
        # Crear backup si existe el archivo
        if DB_FILE.exists():
            DB_BACKUP_DIR.mkdir(parents=True, exist_ok=True)
            backup_name = f"sistema_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            shutil.copy2(DB_FILE, DB_BACKUP_DIR / backup_name)
            # Limpiar backups antiguos (mantener solo los últimos 10)
            backups = sorted(DB_BACKUP_DIR.glob("sistema_*.json"))
            for old in backups[:-10]:
                old.unlink()

        # Guardar archivo principal
        tmp_file = DB_FILE.with_suffix('.json.tmp')
        with open(tmp_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        tmp_file.replace(DB_FILE)


def _get_latest_backup() -> Optional[Path]:
    """Obtiene el backup más reciente."""
    if not DB_BACKUP_DIR.exists():
        return None
    backups = sorted(DB_BACKUP_DIR.glob("sistema_*.json"))
    return backups[-1] if backups else None


# ============ OPERACIONES DE USUARIO ============

def crear_usuario(nombre: str, email: str, password: str, plan: str = "gratis") -> tuple:
    """Crea un nuevo usuario. Retorna (usuario, mensaje)."""
    db = cargar_db()
    email = email.lower().strip()

    # Verificar duplicados
    for u in db["usuarios"]:
        if u["email"] == email:
            return None, "Este email ya está registrado"

    # Buscar plan
    plan_info = next((m for m in db["membresias"] if m["id"] == plan), db["membresias"][0])

    usuario = {
        "id": str(uuid.uuid4()),
        "nombre": nombre.strip(),
        "email": email,
        "password_hash": _hash_password(password),
        "plan": plan,
        "tokens": plan_info["tokens"],
        "tokens_usados": 0,
        "proyectos": [],
        "fecha_registro": datetime.now().isoformat(),
        "ultimo_acceso": datetime.now().isoformat(),
        "activo": True,
        "config_personal": {
            "plantilla_favorita": None,
            "formato_preferido": "youtube",
            "notificaciones": True,
        }
    }
    db["usuarios"].append(usuario)
    guardar_db(db)
    return usuario, "Usuario creado exitosamente"


def autenticar_usuario(email: str, password: str) -> tuple:
    """Autentica un usuario. Retorna (usuario, mensaje)."""
    db = cargar_db()
    email = email.lower().strip()

    for u in db["usuarios"]:
        if u["email"] == email and _verify_password(password, u["password_hash"]):
            if not u.get("activo", True):
                return None, "Cuenta suspendida. Contacta soporte."
            # Actualizar último acceso
            u["ultimo_acceso"] = datetime.now().isoformat()
            guardar_db(db)
            return u, "Login exitoso"
    return None, "Email o contraseña incorrectos"


def actualizar_usuario(uid: str, cambios: Dict[str, Any]) -> bool:
    """Actualiza campos de un usuario."""
    db = cargar_db()
    for u in db["usuarios"]:
        if u["id"] == uid:
            u.update(cambios)
            guardar_db(db)
            return True
    return False


def usar_token(uid: str) -> bool:
    """Descuenta un token del usuario."""
    db = cargar_db()
    for u in db["usuarios"]:
        if u["id"] == uid:
            if u["tokens"] > 0:
                u["tokens"] -= 1
                u["tokens_usados"] = u.get("tokens_usados", 0) + 1
                guardar_db(db)
                return True
            return False
    return False


def verificar_tokens(uid: str) -> bool:
    """Verifica si el usuario tiene tokens disponibles."""
    db = cargar_db()
    for u in db["usuarios"]:
        if u["id"] == uid:
            return u["tokens"] > 0
    return False


def obtener_usuario(uid: str) -> Optional[Dict[str, Any]]:
    """Obtiene un usuario por ID."""
    db = cargar_db()
    for u in db["usuarios"]:
        if u["id"] == uid:
            return u
    return None


def agregar_proyecto(uid: str, proyecto: Dict[str, Any]) -> bool:
    """Agrega un proyecto al historial del usuario."""
    db = cargar_db()
    for u in db["usuarios"]:
        if u["id"] == uid:
            if "proyectos" not in u:
                u["proyectos"] = []
            u["proyectos"].append(proyecto)
            # Actualizar stats globales
            db["stats"]["total_videos_procesados"] = db["stats"].get("total_videos_procesados", 0) + 1
            guardar_db(db)
            return True
    return False


def listar_usuarios() -> List[Dict[str, Any]]:
    """Lista todos los usuarios (sin contraseñas)."""
    db = cargar_db()
    return [{k: v for k, v in u.items() if k != "password_hash"} for u in db["usuarios"]]


def cambiar_plan(uid: str, nuevo_plan: str) -> bool:
    """Cambia el plan de un usuario."""
    db = cargar_db()
    plan_info = next((m for m in db["membresias"] if m["id"] == nuevo_plan), None)
    if not plan_info:
        return False
    for u in db["usuarios"]:
        if u["id"] == uid:
            u["plan"] = nuevo_plan
            u["tokens"] += plan_info["tokens"]
            guardar_db(db)
            return True
    return False


# ============ CONFIGURACIÓN ============

def get_config() -> Dict[str, Any]:
    """Obtiene la configuración del sistema."""
    db = cargar_db()
    return db.get("config", {})


def update_config(cambios: Dict[str, Any]) -> None:
    """Actualiza la configuración del sistema."""
    db = cargar_db()
    db["config"].update(cambios)
    guardar_db(db)


def verify_admin_password(password: str) -> bool:
    """Verifica la contraseña de admin."""
    db = cargar_db()
    stored_hash = db["config"].get("admin_password_hash", "")
    if not stored_hash:
        # Compatibilidad con versiones anteriores
        return password == db["config"].get("admin_password", "admin123")
    return _verify_password(password, stored_hash)


def set_admin_password(password: str) -> None:
    """Establece la contraseña de admin."""
    db = cargar_db()
    db["config"]["admin_password_hash"] = _hash_password(password)
    db["config"].pop("admin_password", None)
    guardar_db(db)


# ============ STATS ============

def get_stats() -> Dict[str, Any]:
    """Obtiene estadísticas del sistema."""
    db = cargar_db()
    return db.get("stats", {})


def get_dashboard_data() -> Dict[str, Any]:
    """Obtiene datos agregados para el dashboard."""
    db = cargar_db()
    usuarios = db["usuarios"]
    return {
        "total_usuarios": len(usuarios),
        "usuarios_activos": sum(1 for u in usuarios if u.get("activo", True)),
        "tokens_distribuidos": sum(u.get("tokens", 0) for u in usuarios),
        "tokens_usados": sum(u.get("tokens_usados", 0) for u in usuarios),
        "proyectos_totales": sum(len(u.get("proyectos", [])) for u in usuarios),
        "videos_procesados": db["stats"].get("total_videos_procesados", 0),
        "distribucion_planes": {
            plan["id"]: sum(1 for u in usuarios if u["plan"] == plan["id"])
            for plan in db["membresias"]
        }
    }


# ============ PLANTILLAS PERSONALIZADAS ============

def guardar_plantilla_personalizada(plantilla: Dict[str, Any]) -> bool:
    """Guarda una plantilla personalizada creada por admin."""
    db = cargar_db()
    if "plantillas_personalizadas" not in db:
        db["plantillas_personalizadas"] = []
    plantilla["fecha_creacion"] = datetime.now().isoformat()
    db["plantillas_personalizadas"].append(plantilla)
    guardar_db(db)
    return True


def eliminar_plantilla_personalizada(plantilla_id: str) -> bool:
    """Elimina una plantilla personalizada."""
    db = cargar_db()
    if "plantillas_personalizadas" not in db:
        return False
    antes = len(db["plantillas_personalizadas"])
    db["plantillas_personalizadas"] = [
        p for p in db["plantillas_personalizadas"] if p["id"] != plantilla_id
    ]
    if len(db["plantillas_personalizadas"]) < antes:
        guardar_db(db)
        return True
    return False
