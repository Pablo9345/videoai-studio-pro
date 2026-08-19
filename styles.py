"""
Sistema de diseño premium para VideoAI Studio Pro.
Incluye: paleta de colores, tipografía, componentes glassmorphism,
animaciones y patrones visuales modernos.
"""

PREMIUM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Montserrat:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg-primary: #0a0e1a;
    --bg-secondary: #0f172a;
    --bg-tertiary: #1a2238;
    --bg-glass: rgba(26, 34, 56, 0.6);
    --bg-glass-hover: rgba(35, 47, 78, 0.7);
    --border-glass: rgba(99, 102, 241, 0.2);
    --border-active: rgba(99, 102, 241, 0.6);
    --text-primary: #f8fafc;
    --text-secondary: #cbd5e1;
    --text-muted: #64748b;
    --accent-primary: #6366f1;
    --accent-secondary: #8b5cf6;
    --accent-tertiary: #ec4899;
    --accent-success: #10b981;
    --accent-warning: #f59e0b;
    --accent-error: #ef4444;
    --gradient-primary: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%);
    --gradient-secondary: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%);
    --gradient-dark: linear-gradient(135deg, #0f172a 0%, #1a2238 100%);
    --gradient-mesh: radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.15) 0px, transparent 50%),
                     radial-gradient(at 100% 0%, rgba(236, 72, 153, 0.10) 0px, transparent 50%),
                     radial-gradient(at 50% 100%, rgba(139, 92, 246, 0.10) 0px, transparent 50%);
    --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.3);
    --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.4);
    --shadow-lg: 0 12px 32px rgba(0, 0, 0, 0.5);
    --shadow-glow: 0 0 32px rgba(99, 102, 241, 0.3);
    --radius-sm: 8px;
    --radius-md: 12px;
    --radius-lg: 18px;
    --radius-xl: 24px;
}

/* ==================== RESET & BASE ==================== */
.stApp {
    background: var(--bg-primary);
    background-image: var(--gradient-mesh);
    background-attachment: fixed;
    color: var(--text-primary);
    font-family: 'Inter', -apple-system, sans-serif;
}

.stApp::before {
    content: "";
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: var(--gradient-mesh);
    z-index: -1;
    pointer-events: none;
}

#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { background: transparent; }

h1, h2, h3, h4, h5, h6 {
    font-family: 'Montserrat', sans-serif !important;
    color: var(--text-primary) !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em;
}

h1 { font-size: 2.4rem !important; font-weight: 800 !important; }
h2 { font-size: 1.8rem !important; }
h3 { font-size: 1.3rem !important; }

p, li, span, div, label {
    color: var(--text-secondary) !important;
}

a {
    color: var(--accent-primary) !important;
    text-decoration: none;
    transition: color 0.2s;
}
a:hover { color: var(--accent-secondary) !important; }

/* ==================== HERO SECTION ==================== */
.hero-section {
    background: var(--gradient-dark);
    border: 1px solid var(--border-glass);
    border-radius: var(--radius-xl);
    padding: 3rem 2rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    box-shadow: var(--shadow-lg);
}

.hero-section::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: var(--gradient-primary);
}

.hero-title {
    font-family: 'Montserrat', sans-serif;
    font-size: 3rem !important;
    font-weight: 900;
    background: var(--gradient-primary);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.5rem !important;
    letter-spacing: -0.03em;
    line-height: 1.1;
}

.hero-subtitle {
    font-size: 1.1rem !important;
    color: var(--text-secondary) !important;
    margin-bottom: 1.5rem !important;
    font-weight: 400;
}

.hero-badges {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    margin-top: 1rem;
}

.hero-badge {
    background: var(--bg-glass);
    border: 1px solid var(--border-glass);
    color: var(--text-primary) !important;
    padding: 0.4rem 1rem;
    border-radius: 100px;
    font-size: 0.85rem;
    font-weight: 500;
    backdrop-filter: blur(10px);
}

.hero-badge-accent {
    background: var(--gradient-primary);
    border: none;
    color: white !important;
}

/* ==================== GLASS CARDS ==================== */
.glass-card {
    background: var(--bg-glass);
    border: 1px solid var(--border-glass);
    border-radius: var(--radius-lg);
    padding: 1.5rem;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    box-shadow: var(--shadow-md);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    margin-bottom: 1rem;
}

.glass-card:hover {
    transform: translateY(-2px);
    border-color: var(--border-active);
    box-shadow: var(--shadow-lg);
}

.glass-card-feature {
    background: var(--bg-glass);
    border: 1px solid var(--border-glass);
    border-radius: var(--radius-md);
    padding: 1.2rem;
    backdrop-filter: blur(20px);
    text-align: center;
    transition: all 0.3s;
}

.glass-card-feature:hover {
    transform: translateY(-4px);
    border-color: var(--accent-primary);
    box-shadow: var(--shadow-glow);
}

.feature-icon {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
    display: block;
}

.feature-title {
    font-size: 1.1rem !important;
    font-weight: 700;
    color: var(--text-primary) !important;
    margin-bottom: 0.3rem;
}

.feature-desc {
    font-size: 0.9rem !important;
    color: var(--text-muted) !important;
}

/* ==================== BUTTONS ==================== */
.stButton > button, .stButton > button[kind="primary"] {
    background: var(--gradient-primary) !important;
    color: white !important;
    border: none !important;
    border-radius: var(--radius-md) !important;
    padding: 0.7rem 1.5rem !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 4px 16px rgba(99, 102, 241, 0.3) !important;
    position: relative;
    overflow: hidden;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(99, 102, 241, 0.4) !important;
    filter: brightness(1.1);
}

.stButton > button:active {
    transform: translateY(0) !important;
}

.stButton > button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none !important;
}

/* ==================== SIDEBAR ==================== */
section[data-testid="stSidebar"] {
    background: var(--bg-secondary) !important;
    border-right: 1px solid var(--border-glass) !important;
}

section[data-testid="stSidebar"] .stMarkdown h1,
section[data-testid="stSidebar"] .stMarkdown h2 {
    background: var(--gradient-primary);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.sidebar-user-card {
    background: var(--bg-glass);
    border: 1px solid var(--border-glass);
    border-radius: var(--radius-md);
    padding: 1rem;
    margin-bottom: 1rem;
    backdrop-filter: blur(10px);
}

.sidebar-token-display {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    background: linear-gradient(135deg, rgba(245, 158, 11, 0.15), rgba(245, 158, 11, 0.05));
    border: 1px solid rgba(245, 158, 11, 0.3);
    padding: 0.5rem 1rem;
    border-radius: var(--radius-md);
    margin: 0.5rem 0;
}

.sidebar-token-icon { font-size: 1.2rem; }
.sidebar-token-count {
    font-weight: 700;
    color: var(--accent-warning) !important;
    font-size: 1.1rem;
}

/* ==================== TABS ==================== */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.5rem;
    background: transparent;
}

.stTabs [data-baseweb="tab"] {
    background: var(--bg-glass);
    border-radius: var(--radius-md) var(--radius-md) 0 0;
    padding: 0.6rem 1.2rem;
    color: var(--text-secondary) !important;
    border: 1px solid var(--border-glass);
    border-bottom: none;
    font-weight: 500;
    transition: all 0.2s;
}

.stTabs [data-baseweb="tab"]:hover {
    background: var(--bg-glass-hover);
    color: var(--text-primary) !important;
}

.stTabs [aria-selected="true"] {
    background: var(--gradient-primary) !important;
    color: white !important;
    border: none !important;
}

/* ==================== INPUTS ==================== */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stNumberInput > div > div > input,
.stSelectbox > div > div > div {
    background: var(--bg-tertiary) !important;
    border: 1px solid var(--border-glass) !important;
    border-radius: var(--radius-md) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
    padding: 0.6rem 0.9rem !important;
    transition: all 0.2s;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--accent-primary) !important;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15) !important;
}

.stTextInput label, .stTextArea label, .stSelectbox label {
    color: var(--text-secondary) !important;
    font-weight: 500;
    margin-bottom: 0.3rem;
}

/* ==================== FILE UPLOADER ==================== */
.stFileUploader > div > div > div {
    background: var(--bg-glass) !important;
    border: 2px dashed var(--border-glass) !important;
    border-radius: var(--radius-lg) !important;
    padding: 1.5rem !important;
    transition: all 0.3s;
    backdrop-filter: blur(10px);
}

.stFileUploader > div > div > div:hover {
    border-color: var(--accent-primary) !important;
    background: var(--bg-glass-hover) !important;
}

/* ==================== TEMPLATE GALLERY ==================== */
.template-gallery {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 1.2rem;
    margin: 1.5rem 0;
}

.template-card {
    background: var(--bg-glass);
    border: 2px solid var(--border-glass);
    border-radius: var(--radius-lg);
    overflow: hidden;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    backdrop-filter: blur(20px);
    position: relative;
}

.template-card:hover {
    transform: translateY(-6px);
    border-color: var(--accent-primary);
    box-shadow: var(--shadow-lg), var(--shadow-glow);
}

.template-card.selected {
    border-color: var(--accent-primary);
    box-shadow: var(--shadow-glow);
    background: rgba(99, 102, 241, 0.1);
}

.template-card.selected::after {
    content: "✓ SELECCIONADO";
    position: absolute;
    top: 0.5rem;
    right: 0.5rem;
    background: var(--gradient-primary);
    color: white !important;
    padding: 0.3rem 0.8rem;
    border-radius: 100px;
    font-size: 0.7rem;
    font-weight: 700;
    z-index: 10;
}

.template-preview {
    height: 160px;
    position: relative;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
}

.template-preview-content {
    text-align: center;
    padding: 1rem;
    z-index: 2;
}

.template-preview-title {
    font-size: 1.3rem;
    font-weight: 800;
    margin-bottom: 0.3rem;
    text-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
}

.template-preview-subtitle {
    font-size: 0.85rem;
    opacity: 0.9;
    margin-bottom: 0.5rem;
}

.template-preview-cta {
    display: inline-block;
    padding: 0.3rem 0.8rem;
    border-radius: 100px;
    font-size: 0.75rem;
    font-weight: 600;
}

.template-card-body {
    padding: 1rem;
}

.template-card-title {
    font-size: 1.1rem !important;
    font-weight: 700;
    color: var(--text-primary) !important;
    margin-bottom: 0.3rem;
}

.template-card-desc {
    font-size: 0.85rem !important;
    color: var(--text-muted) !important;
    margin-bottom: 0.5rem;
    line-height: 1.4;
}

.template-card-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
    margin-top: 0.6rem;
}

.template-tag {
    background: var(--bg-tertiary);
    color: var(--text-secondary) !important;
    padding: 0.2rem 0.6rem;
    border-radius: 100px;
    font-size: 0.7rem;
    font-weight: 500;
}

.template-color-strip {
    display: flex;
    height: 6px;
    margin-top: 0.8rem;
    border-radius: 3px;
    overflow: hidden;
}

.template-color-strip > div { flex: 1; }

/* ==================== STATS / METRICS ==================== */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 1rem;
    margin: 1.5rem 0;
}

.stat-card {
    background: var(--bg-glass);
    border: 1px solid var(--border-glass);
    border-radius: var(--radius-md);
    padding: 1.2rem;
    backdrop-filter: blur(10px);
    transition: all 0.3s;
    position: relative;
    overflow: hidden;
}

.stat-card::before {
    content: "";
    position: absolute;
    top: 0; left: 0;
    width: 4px;
    height: 100%;
    background: var(--gradient-primary);
}

.stat-card:hover {
    transform: translateY(-3px);
    border-color: var(--accent-primary);
}

.stat-icon { font-size: 1.8rem; margin-bottom: 0.5rem; }
.stat-value {
    font-size: 1.8rem;
    font-weight: 800;
    color: var(--text-primary) !important;
    font-family: 'Montserrat', sans-serif;
    line-height: 1;
}
.stat-label {
    font-size: 0.85rem;
    color: var(--text-muted) !important;
    margin-top: 0.3rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* ==================== WIZARD STEPS ==================== */
.wizard-steps {
    display: flex;
    justify-content: space-between;
    margin-bottom: 2rem;
    position: relative;
}

.wizard-steps::before {
    content: "";
    position: absolute;
    top: 20px;
    left: 0; right: 0;
    height: 2px;
    background: var(--border-glass);
    z-index: 1;
}

.wizard-step {
    display: flex;
    flex-direction: column;
    align-items: center;
    z-index: 2;
    flex: 1;
    position: relative;
}

.wizard-step-circle {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: var(--bg-tertiary);
    border: 2px solid var(--border-glass);
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    color: var(--text-muted) !important;
    transition: all 0.3s;
    margin-bottom: 0.5rem;
}

.wizard-step.active .wizard-step-circle {
    background: var(--gradient-primary);
    border-color: var(--accent-primary);
    color: white !important;
    box-shadow: var(--shadow-glow);
}

.wizard-step.completed .wizard-step-circle {
    background: var(--accent-success);
    border-color: var(--accent-success);
    color: white !important;
}

.wizard-step-label {
    font-size: 0.85rem;
    color: var(--text-secondary) !important;
    font-weight: 500;
    text-align: center;
}

.wizard-step.active .wizard-step-label {
    color: var(--accent-primary) !important;
    font-weight: 600;
}

/* ==================== PROGRESS / LOADING ==================== */
.processing-container {
    background: var(--bg-glass);
    border: 1px solid var(--border-glass);
    border-radius: var(--radius-lg);
    padding: 2rem;
    text-align: center;
    backdrop-filter: blur(20px);
    margin: 1.5rem 0;
}

.processing-icon {
    font-size: 4rem;
    margin-bottom: 1rem;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.05); opacity: 0.8; }
}

@keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

.spinner-glow {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    border: 3px solid transparent;
    border-top-color: var(--accent-primary);
    border-right-color: var(--accent-secondary);
    margin: 0 auto 1rem;
    animation: spin 1s linear infinite;
}

/* ==================== ALERTS / NOTIFICATIONS ==================== */
.custom-alert {
    padding: 1rem 1.2rem;
    border-radius: var(--radius-md);
    margin: 0.8rem 0;
    display: flex;
    align-items: flex-start;
    gap: 0.8rem;
    border-left: 4px solid;
    backdrop-filter: blur(10px);
}

.custom-alert-success {
    background: rgba(16, 185, 129, 0.1);
    border-color: var(--accent-success);
    color: var(--accent-success) !important;
}

.custom-alert-warning {
    background: rgba(245, 158, 11, 0.1);
    border-color: var(--accent-warning);
    color: var(--accent-warning) !important;
}

.custom-alert-error {
    background: rgba(239, 68, 68, 0.1);
    border-color: var(--accent-error);
    color: var(--accent-error) !important;
}

.custom-alert-info {
    background: rgba(99, 102, 241, 0.1);
    border-color: var(--accent-primary);
    color: var(--accent-primary) !important;
}

/* ==================== PRICING / PLANS ==================== */
.pricing-card {
    background: var(--bg-glass);
    border: 1px solid var(--border-glass);
    border-radius: var(--radius-lg);
    padding: 1.8rem;
    text-align: center;
    backdrop-filter: blur(20px);
    transition: all 0.3s;
    position: relative;
    height: 100%;
}

.pricing-card:hover {
    transform: translateY(-6px);
    border-color: var(--accent-primary);
    box-shadow: var(--shadow-lg);
}

.pricing-card.featured {
    border: 2px solid var(--accent-primary);
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.08), rgba(139, 92, 246, 0.05));
}

.pricing-card.featured::before {
    content: "MÁS POPULAR";
    position: absolute;
    top: -12px;
    left: 50%;
    transform: translateX(-50%);
    background: var(--gradient-primary);
    color: white !important;
    padding: 0.3rem 1rem;
    border-radius: 100px;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.05em;
}

.pricing-name {
    font-size: 1.3rem !important;
    font-weight: 700;
    color: var(--text-primary) !important;
    margin-bottom: 0.3rem;
}

.pricing-price {
    font-size: 2.8rem;
    font-weight: 900;
    color: var(--text-primary) !important;
    font-family: 'Montserrat', sans-serif;
    margin: 0.5rem 0;
}

.pricing-price-currency {
    font-size: 1.4rem;
    vertical-align: top;
    color: var(--text-muted) !important;
}

.pricing-price-period {
    font-size: 0.9rem;
    color: var(--text-muted) !important;
    font-weight: 400;
}

.pricing-features {
    list-style: none;
    padding: 0;
    margin: 1.5rem 0;
    text-align: left;
}

.pricing-features li {
    padding: 0.4rem 0;
    color: var(--text-secondary) !important;
    font-size: 0.92rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.pricing-features li::before {
    content: "✓";
    color: var(--accent-success);
    font-weight: 700;
}

/* ==================== SCENE CARD ==================== */
.scene-card {
    background: var(--bg-glass);
    border: 1px solid var(--border-glass);
    border-radius: var(--radius-md);
    padding: 1rem;
    margin-bottom: 0.8rem;
    backdrop-filter: blur(10px);
    transition: all 0.2s;
    border-left: 3px solid var(--accent-primary);
}

.scene-card:hover {
    border-color: var(--accent-primary);
    transform: translateX(4px);
}

.scene-number {
    display: inline-block;
    background: var(--gradient-primary);
    color: white !important;
    width: 28px;
    height: 28px;
    border-radius: 50%;
    text-align: center;
    line-height: 28px;
    font-weight: 700;
    font-size: 0.85rem;
    margin-right: 0.5rem;
}

.scene-text {
    color: var(--text-secondary) !important;
    font-size: 0.92rem;
    margin-top: 0.5rem;
}

.scene-meta {
    display: flex;
    gap: 1rem;
    margin-top: 0.5rem;
    font-size: 0.8rem;
    color: var(--text-muted) !important;
}

/* ==================== CODE / JSON ==================== */
pre, code, .stCode {
    background: var(--bg-tertiary) !important;
    border: 1px solid var(--border-glass) !important;
    border-radius: var(--radius-md) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.85rem !important;
}

/* ==================== MISC ==================== */
.divider-gradient {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--accent-primary), transparent);
    margin: 2rem 0;
    border: none;
}

.gradient-text {
    background: var(--gradient-primary);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 800;
}

.section-divider {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin: 2rem 0 1rem;
}

.section-divider-line {
    flex: 1;
    height: 1px;
    background: var(--border-glass);
}

.section-divider-text {
    color: var(--text-muted) !important;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-weight: 600;
}

/* Scrollbar */
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb {
    background: var(--bg-tertiary);
    border-radius: 5px;
    border: 2px solid var(--bg-primary);
}
::-webkit-scrollbar-thumb:hover { background: var(--accent-primary); }

/* Spinner fix */
.stSpinner > div {
    border-top-color: var(--accent-primary) !important;
}

/* Hide streamlit branding */
#stDecoration { visibility: hidden; }

/* Markdown fixes */
.stMarkdown table {
    background: var(--bg-glass);
    border-radius: var(--radius-md);
    overflow: hidden;
}

.stMarkdown th {
    background: var(--bg-tertiary);
    color: var(--text-primary) !important;
    font-weight: 700;
}

.stMarkdown td { color: var(--text-secondary) !important; }

/* Expander */
.stExpander {
    background: var(--bg-glass) !important;
    border: 1px solid var(--border-glass) !important;
    border-radius: var(--radius-md) !important;
    backdrop-filter: blur(10px);
    overflow: hidden;
}

.stExpander > details > summary {
    color: var(--text-primary) !important;
    font-weight: 600;
    padding: 0.8rem 1rem;
}

/* Radio buttons in sidebar */
section[data-testid="stSidebar"] .stRadio > div {
    background: var(--bg-glass);
    border-radius: var(--radius-md);
    padding: 0.5rem;
    gap: 0.2rem !important;
}

section[data-testid="stSidebar"] .stRadio > div > label {
    padding: 0.5rem 0.8rem !important;
    border-radius: var(--radius-sm);
    transition: all 0.2s;
    color: var(--text-secondary) !important;
    font-weight: 500;
}

section[data-testid="stSidebar"] .stRadio > div > label:hover {
    background: var(--bg-glass-hover);
    color: var(--text-primary) !important;
}

section[data-testid="stSidebar"] .stRadio > div > label[data-checked="true"] {
    background: var(--gradient-primary);
    color: white !important;
}

section[data-testid="stSidebar"] .stRadio > div > label[data-checked="true"] span {
    color: white !important;
}
</style>
"""

def get_premium_css():
    """Retorna el CSS premium completo."""
    return PREMIUM_CSS


def html_safe(html: str) -> str:
    """
    Limpia HTML para usar con st.markdown(unsafe_allow_html=True).
    Elimina saltos de línea y espacios innecesarios que pueden causar
    que Streamlit interprete el HTML como markdown.
    """
    if not html:
        return ""
    # Colapsar whitespace entre tags
    import re
    # Eliminar saltos de línea y espacios entre tags
    html = re.sub(r'>\s+<', '><', html)
    # Eliminar saltos de línea sueltos dentro de tags
    html = re.sub(r'\s+', ' ', html)
    return html.strip()


def render_template_preview_card(plantilla, index, selected=False):
    """
    Genera el HTML para una tarjeta de plantilla con vista previa visual real.
    El HTML se devuelve en una sola línea para evitar problemas con Streamlit markdown.
    """
    selected_class = " selected" if selected else ""
    gradient_bg = f"linear-gradient(135deg, {plantilla['color_primario']} 0%, {plantilla['color_secundario']} 100%)"

    html = (
        f'<div class="template-card{selected_class}" id="tpl_{plantilla["id"]}">'
        f'<div class="template-preview" style="background: {gradient_bg};">'
        f'<div class="template-preview-content">'
        f'<div class="template-preview-title" style="color: {plantilla["color_texto"]}; font-family: {plantilla["fuente"]}, sans-serif;">{plantilla["nombre"]}</div>'
        f'<div class="template-preview-subtitle" style="color: {plantilla["color_texto"]}; opacity: 0.85; font-family: {plantilla["fuente"]}, sans-serif;">{plantilla.get("preview_texto", "Tu texto aparecerá aquí")}</div>'
        f'<div class="template-preview-cta" style="background: {plantilla.get("color_acento", "#FFFFFF")}33; color: {plantilla["color_texto"]}; border: 1px solid {plantilla.get("color_acento", "#FFFFFF")}80;">▶ VER MÁS</div>'
        f'</div></div>'
        f'<div class="template-card-body">'
        f'<div class="template-card-title">{plantilla["nombre"]}</div>'
        f'<div class="template-card-desc">{plantilla["descripcion"]}</div>'
        f'<div class="template-card-meta">'
        f'<span class="template-tag">{plantilla["estilo"]}</span>'
        f'<span class="template-tag">{plantilla["transicion"]}</span>'
        f'<span class="template-tag">{plantilla.get("categoria", "General")}</span>'
        f'</div>'
        f'<div class="template-color-strip">'
        f'<div style="background: {plantilla["color_primario"]};"></div>'
        f'<div style="background: {plantilla["color_secundario"]};"></div>'
        f'<div style="background: {plantilla.get("color_acento", "#FFFFFF")};"></div>'
        f'</div>'
        f'</div></div>'
    )
    return html


def render_stat_card(icon, value, label):
    """Genera una tarjeta de estadística (HTML en una línea)."""
    return (
        f'<div class="stat-card">'
        f'<div class="stat-icon">{icon}</div>'
        f'<div class="stat-value">{value}</div>'
        f'<div class="stat-label">{label}</div>'
        f'</div>'
    )


def render_wizard_step(step_num, label, state="pending"):
    """
    state: 'pending' | 'active' | 'completed'
    HTML en una sola línea para evitar problemas con Streamlit markdown.
    """
    icon = step_num if state != "completed" else "✓"
    return (
        f'<div class="wizard-step {state}">'
        f'<div class="wizard-step-circle">{icon}</div>'
        f'<div class="wizard-step-label">{label}</div>'
        f'</div>'
    )


def render_wizard(current_step, steps):
    """
    Renderiza el wizard completo.
    current_step: int (1-indexed)
    steps: list of step labels
    Devuelve HTML en una sola línea.
    """
    html = '<div class="wizard-steps">'
    for i, label in enumerate(steps, 1):
        if i < current_step:
            state = "completed"
        elif i == current_step:
            state = "active"
        else:
            state = "pending"
        html += render_wizard_step(i, label, state)
    html += '</div>'
    return html


def render_scene_card(scene_num, descripcion, texto_pantalla, duracion, imagen_sugerida=""):
    """Renderiza una tarjeta de escena del guion (HTML en una línea)."""
    img_html = f'<div class="scene-meta"><span>🎬 {imagen_sugerida}</span></div>' if imagen_sugerida else ''
    texto_html = f'<div class="scene-text" style="margin-top:0.4rem; font-style:italic;">💬 "{texto_pantalla}"</div>' if texto_pantalla else ''
    return (
        f'<div class="scene-card">'
        f'<span class="scene-number">{scene_num}</span>'
        f'<strong style="color: var(--text-primary) !important;">Escena {scene_num}</strong>'
        f'<div class="scene-text">{descripcion}</div>'
        f'{texto_html}'
        f'<div class="scene-meta"><span>⏱ {duracion}s</span></div>'
        f'{img_html}'
        f'</div>'
    )


def render_pricing_card(plan, featured=False):
    """Renderiza una tarjeta de plan de precios (HTML en una línea)."""
    featured_class = " featured" if featured else ""
    features_html = "".join(f"<li>{f}</li>" for f in plan["features"])
    return (
        f'<div class="pricing-card{featured_class}">'
        f'<div class="pricing-name">{plan["nombre"]}</div>'
        f'<div class="pricing-price">'
        f'<span class="pricing-price-currency">$</span>{plan["precio"]}'
        f'<span class="pricing-price-period">/mes</span>'
        f'</div>'
        f'<div style="color: var(--text-muted) !important; margin-bottom: 1rem; font-size: 0.9rem;">'
        f'{plan["tokens"]} tokens incluidos</div>'
        f'<ul class="pricing-features">{features_html}</ul>'
        f'</div>'
    )
