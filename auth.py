"""
Módulo de autenticación y manejo de sesión con Streamlit.
"""

import streamlit as st
from datetime import datetime
from database import (
    autenticar_usuario, crear_usuario, obtener_usuario,
    usar_token, verificar_tokens, actualizar_usuario, cambiar_plan
)


def init_session_state():
    """Inicializa el estado de sesión."""
    if 'usuario' not in st.session_state:
        st.session_state.usuario = None
    if 'vista' not in st.session_state:
        st.session_state.vista = "home"
    if 'admin_mode' not in st.session_state:
        st.session_state.admin_mode = False
    if 'plantilla_elegida' not in st.session_state:
        st.session_state.plantilla_elegida = None
    if 'guion' not in st.session_state:
        st.session_state.guion = None
    if 'wizard_step' not in st.session_state:
        st.session_state.wizard_step = 1


def is_logged_in() -> bool:
    return st.session_state.get('usuario') is not None


def is_admin() -> bool:
    return st.session_state.get('admin_mode', False)


def logout():
    """Cierra la sesión del usuario."""
    st.session_state.usuario = None
    st.session_state.vista = "home"
    st.session_state.admin_mode = False
    st.session_state.plantilla_elegida = None
    st.session_state.guion = None
    st.session_state.wizard_step = 1
    st.rerun()


def render_login_form():
    """Renderiza el formulario de login/registro mejorado."""
    from styles import PREMIUM_CSS

    st.markdown("""
    <div class="hero-section" style="text-align: center; max-width: 700px; margin: 0 auto 2rem;">
        <div class="hero-title">VideoAI Studio Pro</div>
        <div class="hero-subtitle">Producción de video profesional con IA · Guiones inteligentes · Plantillas premium</div>
        <div class="hero-badges" style="justify-content: center;">
            <span class="hero-badge hero-badge-accent">✨ 12 Plantillas Pro</span>
            <span class="hero-badge">🎬 Multi-formato</span>
            <span class="hero-badge">🤖 IA Groq</span>
            <span class="hero-badge">📝 Subtítulos Auto</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🔐 Iniciar Sesión", "✨ Crear Cuenta Gratis"])

    with tab1:
        with st.container():
            email = st.text_input("📧 Email", key="login_email",
                                   placeholder="tu@email.com")
            password = st.text_input("🔒 Contraseña", type="password",
                                     key="login_password")

            col1, col2 = st.columns([3, 1])
            with col1:
                if st.button("🚀 Entrar", type="primary", use_container_width=True):
                    if not email or not password:
                        st.warning("Completa todos los campos")
                    else:
                        usuario, msg = autenticar_usuario(email, password)
                        if usuario:
                            st.session_state.usuario = usuario
                            st.session_state.vista = "process"
                            st.success(f"¡Bienvenido, {usuario['nombre']}!")
                            st.rerun()
                        else:
                            st.error(msg)
            with col2:
                if st.button("Demo"):
                    # Login demo rápido
                    usuario, _ = autenticar_usuario("demo@videoai.com", "demo1234")
                    if not usuario:
                        crear_usuario("Usuario Demo", "demo@videoai.com", "demo1234", "pro")
                        usuario, _ = autenticar_usuario("demo@videoai.com", "demo1234")
                    if usuario:
                        st.session_state.usuario = usuario
                        st.session_state.vista = "process"
                        st.rerun()

    with tab2:
        with st.container():
            nombre = st.text_input("👤 Nombre completo", key="reg_nombre",
                                   placeholder="Tu nombre")
            email = st.text_input("📧 Email", key="reg_email",
                                  placeholder="tu@email.com")
            password = st.text_input("🔒 Contraseña", type="password",
                                      key="reg_password")
            password2 = st.text_input("🔒 Confirmar contraseña", type="password",
                                       key="reg_password2")

            if st.button("✨ Crear Cuenta Gratis", type="primary", use_container_width=True):
                if not all([nombre, email, password, password2]):
                    st.warning("Completa todos los campos")
                elif password != password2:
                    st.error("Las contraseñas no coinciden")
                elif len(password) < 6:
                    st.error("La contraseña debe tener al menos 6 caracteres")
                else:
                    usuario, msg = crear_usuario(nombre, email, password, "gratis")
                    if usuario:
                        st.session_state.usuario = usuario
                        st.session_state.vista = "process"
                        st.success("¡Cuenta creada! Bienvenido a VideoAI Studio Pro")
                        st.rerun()
                    else:
                        st.error(msg)


def render_user_sidebar():
    """Renderiza el sidebar con info del usuario."""
    usuario = st.session_state.usuario

    st.markdown(f"""
    <div class="sidebar-user-card">
        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
            <div style="width: 36px; height: 36px; border-radius: 50%;
                        background: var(--gradient-primary); display: flex;
                        align-items: center; justify-content: center;
                        font-weight: 700; color: white;">
                {usuario['nombre'][0].upper()}
            </div>
            <div>
                <div style="font-weight: 700; color: var(--text-primary) !important;">
                    {usuario['nombre']}
                </div>
                <div style="font-size: 0.8rem; color: var(--text-muted) !important;">
                    {usuario['email']}
                </div>
            </div>
        </div>
        <div class="sidebar-token-display">
            <span class="sidebar-token-icon">🪙</span>
            <span class="sidebar-token-count">{usuario['tokens']}</span>
            <span style="color: var(--text-muted) !important; font-size: 0.85rem;">
                tokens disponibles
            </span>
        </div>
        <div style="display: flex; gap: 0.3rem; margin-top: 0.5rem;">
            <span class="template-tag" style="background: var(--bg-tertiary);">
                Plan {usuario['plan'].upper()}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    vista = st.radio(
        "📍 Navegación",
        ["🏠 Inicio", "📤 Producción", "🎨 Plantillas",
         "📊 Mis Proyectos", "💡 Ideas IA", "💎 Planes", "⚙️ Configuración"],
        key="nav_radio"
    )

    # Mapear selección a vista interna
    vista_map = {
        "🏠 Inicio": "home",
        "📤 Producción": "process",
        "🎨 Plantillas": "templates",
        "📊 Mis Proyectos": "projects",
        "💡 Ideas IA": "ideas",
        "💎 Planes": "plans",
        "⚙️ Configuración": "config"
    }
    st.session_state.vista = vista_map.get(vista, "home")

    st.markdown("---")

    if st.button("🚪 Cerrar Sesión", use_container_width=True):
        logout()
