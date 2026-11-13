
import streamlit as st
import pandas as pd
from pathlib import Path
import base64
import numpy as np

# --------------------------------------------------
# 1. Configuração
# --------------------------------------------------

st.set_page_config(
    page_title="Terra Signal",
    page_icon="assets/terra_signal.png",
    layout="wide"
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "processed"

# --------------------------------------------------
# 2. Estilo visual
# --------------------------------------------------

st.markdown("""
<style>
    /* ============================================================
       FUNDO GERAL
       ============================================================ */
    .stApp,
    [data-testid="stApp"],
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"] {
        background-color: #0E1E28 !important;
    }

    /* Header do topo */
    [data-testid="stHeader"] {
        background-color: #1B3139 !important;
    }

    /* Conteúdo principal */
    .block-container {
        max-width: 1500px;
        padding-top: 2rem !important;        /* era 4rem */
        padding-bottom: 1.5rem !important;   /* era 2rem */
    }

    /* Reduz espaço do divider após o header */
    [data-testid="stDivider"] {
        margin-top: 0.5rem !important;
        margin-bottom: 0.5rem !important;
        padding: 0 !important;
    }

    /* Reduz margem entre radio e selectbox */
    [data-testid="stRadio"] {
        margin-bottom: -0.5rem !important;
    }

    /* ============================================================
       REMOVER BARRA SUPERIOR DO STREAMLIT (HEADER + TOOLBAR)
       ============================================================ */

    /* Esconde a barra de ferramentas (três pontinhos) */
    [data-testid="stToolbar"] {
        display: none !important;
        visibility: hidden !important;
    }

    /* Esconde o cabeçalho (a barra física que ocupa espaço) */
    header[data-testid="stHeader"] {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
    }

    /* Garante que o conteúdo principal ocupe o topo */
    .stApp > header {
        display: none !important;
    }

    /* Remove o espaço extra que a barra deixava no topo */
    .block-container {
        padding-top: 1rem !important; /* Ajuste este valor conforme necessário */
    }

    /* ============================================================
       LOGOS (usar com <div class="logo-databricks"> / <div class="logo-terra">
       no Python, envolvendo o st.image)
       ============================================================ */
    .logo-databricks {
        display: flex;
        justify-content: flex-end;   /* colado à esquerda da coluna */
        width: 100%;
    }

    .logo-terra {
        display: flex;
        justify-content: flex-end;     /* colado à direita da coluna */
        width: 100%;
    }

    /* ============================================================
       TÍTULOS
       ============================================================ */
    h1, h2, h3 {
        color: #EEEDE9 !important;
    }

    /* ============================================================
       SEÇÕES — caixa da moldura externa (só o wrapper mais externo)
       ============================================================ */
    [data-testid="stVerticalBlockBorderWrapper"]:not(
        [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stVerticalBlockBorderWrapper"]
    ) {
        background: #1B3139 !important;
        border: 1px solid #2A4655 !important;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 2px 7px rgba(0, 0, 0, 0.35);
    }

    /* ============================================================
       MÉTRICAS — caixa individual (só o wrapper mais externo)
       ============================================================ */
    [data-testid="stMetric"]:not(
        [data-testid="stMetric"] [data-testid="stMetric"]
    ) {
        background: #1B3139 !important;
        border: 1px solid #2A4655 !important;
        border-radius: 12px;
        padding: 16px !important;
        box-shadow: 0 2px 7px rgba(0, 0, 0, 0.35);
    }

    [data-testid="stMetricLabel"] {
        color: #A0B4BC !important;
        white-space: normal !important;
        overflow: visible !important;
        text-overflow: unset !important;
    }

    [data-testid="stMetricLabel"] p {
        white-space: normal !important;
        overflow: visible !important;
        text-overflow: unset !important;
        font-size: 0.85rem !important;
    }

    /* ============================================================
    CARDS DE MÉTRICA CUSTOMIZADOS
    ============================================================ */
    .terra-metric-card {
        border: 1px solid #2A4655;
        border-radius: 12px;
        padding: 18px 16px;
        height: 130px;
        box-shadow: 0 2px 7px rgba(0, 0, 0, 0.35);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        gap: 6px;
        box-sizing: border-box;
        width: 100%;
    }

    .terra-metric-label {
        font-size: 0.85rem;
        font-weight: 500;
        text-align: center;
        width: 100%;
    }

    .terra-metric-value {
        font-size: 1.6rem;
        font-weight: 600;
        text-align: center;
        width: 100%;
        line-height: 1.2;
    }

    /* ============================================================
    GAUGE CARD — Probabilidade de Churn
    ============================================================ */
    .terra-gauge-card {
        border: 1px solid #2A4655;
        border-radius: 12px;
        padding: 12px 14px;
        background: #1B3139;
        box-shadow: 0 2px 7px rgba(0, 0, 0, 0.35);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 2px;
        height: 130px;
        box-sizing: border-box;
        width: 100%;
    }

    .terra-gauge-scale {
        display: flex;
        justify-content: space-between;
        width: 100%;
        max-width: 140px;
        font-size: 0.65rem;
        color: #6B7B82;
        line-height: 1;
    }

    /* ============================================================
       TABELA CUSTOMIZADA — Aspectos da experiência
       (wrapper + tabela; SEM duplicação)
       ============================================================ */
    .terra-table-wrapper {
        width: 100%;
        overflow-x: auto;
        border-radius: 10px;
    }

    .terra-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        background: #1B3139;
        border: 1px solid #2A4655;
        border-radius: 10px;
        color: #EEEDE9;
        font-size: 0.9rem;
        table-layout: fixed;
    }

    .terra-table thead th {
        background: #0E1E28;
        color: #EEEDE9;
        padding: 10px 14px;
        text-align: left;
        font-weight: 600;
        border-bottom: 1px solid #2A4655;
    }

    .terra-table tbody td {
        padding: 10px 14px;
        border-bottom: 1px solid #2A4655;
        color: #EEEDE9;
        word-wrap: break-word;
        overflow-wrap: break-word;
        white-space: normal;
    }

    .terra-table tbody tr:last-child td {
        border-bottom: none;
    }

    .terra-table tbody tr:hover {
        background: #243D48;
    }

    /* ============================================================
       DATAFRAMES (fallback, caso ainda haja algum st.dataframe)
       ============================================================ */
    [data-testid="stDataFrame"] {
        border: 1px solid #2A4655 !important;
        border-radius: 10px;
    }

    /* ============================================================
    SELECTBOX — campo + lista suspensa
    ============================================================ */
    [data-testid="stSelectbox"] [data-baseweb="select"] > div {
        background-color: #2A4655 !important;
        border-color: #2A4655 !important;
        color: #EEEDE9 !important;
        font-size: 1.05rem !important;      
        display: flex !important;           
        align-items: center !important;     
        min-height: 42px !important;        
    }

    [data-testid="stSelectbox"] [data-baseweb="select"] input,
    [data-testid="stSelectbox"] [data-baseweb="select"] div[role="button"],
    [data-testid="stSelectbox"] [data-baseweb="select"] span {
        background-color: transparent !important;
        color: #EEEDE9 !important;
    }

    [data-baseweb="popover"] ul,
    [data-baseweb="popover"] [role="listbox"] {
        background-color: #2A4655 !important;
    }

    [data-baseweb="popover"] li,
    [data-baseweb="popover"] [role="option"] {
        background-color: #2A4655 !important;
        color: #EEEDE9 !important;
    }

    [data-baseweb="popover"] li:hover,
    [data-baseweb="popover"] [role="option"]:hover {
        background-color: #34515F !important;
    }

    /* Item SELECIONADO no dropdown — mesma cor do cabeçalho da tabela */
    [data-baseweb="popover"] [role="option"][aria-selected="true"],
    [data-baseweb="popover"] li[aria-selected="true"] {
        background-color: #0E1E28 !important;
        color: #EEEDE9 !important;
        font-weight: 600 !important;
    }

    [data-baseweb="popover"] [role="option"][aria-selected="true"]:hover,
    [data-baseweb="popover"] li[aria-selected="true"]:hover {
        background-color: #1B3139 !important;   /* hover = Oasis, um pouco mais claro */
        color: #EEEDE9 !important;
    }

    /* Selectbox — campo fechado */
    [data-testid="stSelectbox"] [data-baseweb="select"] > div {
        background-color: #2A4655 !important;
        border-color: #2A4655 !important;
        color: #EEEDE9 !important;
        font-size: 1.05rem !important;
    }

    /* ============================================================
       CAIXA DE AVISO (st.info / st.warning / st.success / st.error)
       ============================================================ */
    [data-testid="stAlert"] {
        background-color: #2A4655 !important;
        border: 1px solid #2A4655 !important;
        border-radius: 10px !important;
    }

    [data-testid="stAlert"] * {
        color: #EEEDE9 !important;
    }

    [data-testid="stAlert"] svg {
        fill: #EEEDE9 !important;
        stroke: #EEEDE9 !important;
    }

    /* ============================================================
       MARCA (opcional — usado se você tiver <div class="brand">)
       ============================================================ */
    .brand {
        color: #EEEDE9;
        font-size: 23px;
        font-weight: 750;
        letter-spacing: -0.5px;
    }

    .subtitle {
        color: #A0B4BC;
        font-size: 13px;
    }

    /* ============================================================
       GUIDANCE BOX — Orientação de atendimento
       ============================================================ */
    .guidance {
        background: #1B3139;
        border-left: 4px solid #F85149;
        border-right: 4px solid #F85149;
        border-radius: 10px;
        padding: 22px 26px;
        color: #EEEDE9;
        line-height: 1.7;
        font-size: 0.95rem;
        width: 100%;
        box-sizing: border-box;
    }

    .guidance-title {
        font-size: 16px;
        font-weight: 700;
        color: #F85149;
        margin-bottom: 14px;
        letter-spacing: 0.3px;
    }

    .guidance-row {
        display: flex;
        gap: 16px;
        margin-bottom: 10px;
        align-items: flex-start;
    }

    .guidance-row:last-child {
        margin-bottom: 0;
    }

    .guidance-label {
        color: #F85149;
        font-weight: 600;
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        min-width: 120px;
        padding-top: 3px;
        flex-shrink: 0;
    }

    .guidance-body {
        color: #EEEDE9;
        flex: 1;
        padding: 10px 14px;
        border-radius: 8px;
        line-height: 1.6;
        background: rgba(255, 255, 255, 0.04);   /* fallback neutro */
    }

    .guidance.guidance-alert .guidance-body {
        background: rgba(239, 68, 68, 0.08);
    }

    .guidance.guidance-warning .guidance-body {
        background: rgba(245, 158, 11, 0.08);
    }

    .guidance.guidance-info .guidance-body {
        background: rgba(19, 169, 186, 0.08);
    }

    .guidance.guidance-neutral .guidance-body {
        background: rgba(160, 180, 188, 0.06);
    }

    /* Variante NEUTRA — churn = No (cinza-azulado) */
    .guidance.guidance-neutral {
        border-left-color: #A0B4BC;
        border-right-color: #A0B4BC;
    }

    .guidance.guidance-neutral .guidance-title,
    .guidance.guidance-neutral .guidance-label {
        color: #A0B4BC;
    }

    /* ============================================================
       DIVERSOS
       ============================================================ */
    hr {
        border-color: #2A4655;
    }
    .action-btn {
    display: inline-flex;
    align-items: center;
    padding: 0.45rem 1rem;
    background: #1B3139;
    border: 1px solid #2A4655;
    border-radius: 8px;
    color: #EEEDE9 !important;
    text-decoration: none !important;
    font-size: 0.9rem;
    font-family: inherit;
    margin: 0.25rem 0;
    transition: background 0.15s ease;
    width: fit-content;
    }

    .action-btn:hover {
        background: #2A4655;
        color: #EEEDE9 !important;
        text-decoration: none !important;
    }

    .action-btn-disabled {
        opacity: 0.9;
        cursor: not-allowed;
    }

    /* Botões Streamlit (Email/Aplicar) — mesma cor do WhatsApp */
    button[kind="secondary"],
    button[kind="primary"],
    button[kind="tertiary"],
    [data-testid="stBaseButton-secondary"],
    [data-testid="stBaseButton-primary"],
    [data-testid="stLinkButton"] a,
    [data-testid="stButton"] button {
        background-color: #1B3139 !important;
        border: 1px solid #2A4655 !important;
        color: #EEEDE9 !important;
        border-radius: 8px !important;
        opacity: 0.9 !important;
        transition: opacity 0.15s ease, background-color 0.15s ease !important;
    }

    button[kind="secondary"]:hover,
    button[kind="primary"]:hover,
    [data-testid="stBaseButton-secondary"]:hover,
    [data-testid="stBaseButton-primary"]:hover,
    [data-testid="stLinkButton"] a:hover,
    [data-testid="stButton"] button:hover {
        background-color: #2A4655 !important;
        border-color: #2A4655 !important;
        color: #EEEDE9 !important;
        opacity: 1 !important;
    }
    /* Hover do botão WhatsApp (custom <a>) */
    .wa-btn {
        transition: opacity 0.15s ease, background-color 0.15s ease !important;
    }

    .wa-btn:hover {
        background: #2A4655 !important;
        opacity: 1 !important;
    }
    .guidance.guidance-warning {
    border-left-color: #F59E0B;
    border-right-color: #F59E0B;
    }
    .guidance.guidance-warning .guidance-title,
    .guidance.guidance-warning .guidance-label {
        color: #F59E0B;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# 3. Carregamento dos dados
# --------------------------------------------------
@st.cache_data
def load_data():

    scores = pd.read_csv(
        DATA_DIR / "terra_signal_churn_scores.csv",
        sep=";",
        encoding="utf-8-sig",     # ← SEM decimal=","
    )
    intelligence = pd.read_csv(
        DATA_DIR / "terra_signal_customer_intelligence.csv",
        sep=";",
        decimal=",",
        encoding="latin-1",
    )
    aspects = pd.read_csv(
        DATA_DIR / "terra_signal_feedback_aspects.csv",
        sep=";",
        encoding="latin-1",
    )
    feedback = pd.read_csv(
        DATA_DIR / "terra_signal_feedback_text.csv",
        sep=";",
        decimal=",",
        encoding="latin-1",
    )

    def _limpar_bom(df, nome_arquivo):
        novos = {col: str(col).replace("\ufeff","").replace("ï»¿","").strip()
                 for col in df.columns}
        df = df.rename(columns=novos)
        if "customerID" not in df.columns:
            for c in df.columns:
                if c.strip().lower() == "customerid":
                    df = df.rename(columns={c: "customerID"})
                    break
        if "customerID" not in df.columns:
            raise ValueError(
                f"Coluna 'customerID' não encontrada em {nome_arquivo}. "
                f"Colunas: {list(df.columns)}"
            )
        return df

    scores       = _limpar_bom(scores,       "terra_signal_churn_scores.csv")
    intelligence = _limpar_bom(intelligence, "terra_signal_customer_intelligence.csv")
    aspects      = _limpar_bom(aspects,      "terra_signal_feedback_aspects.csv")
    feedback     = _limpar_bom(feedback,     "terra_signal_feedback_text.csv")

    def _to_float_br(series):
        s = series.astype(str).str.strip()
        sample = s.dropna().head(100).tolist()
        has_comma = sum("," in x for x in sample) > (len(sample) / 2)
        if has_comma:
            s = s.str.replace(".", "", regex=False).str.replace(",", ".", regex=False)
        else:
            s = s.str.replace(",", "", regex=False)
        return pd.to_numeric(s, errors="coerce").astype(float)

    scores["ChurnScore_"] = _to_float_br(scores["ChurnScore_"])
    scores["Threshold"]   = _to_float_br(scores["Threshold"])

    scores["ChurnPredicted__"] = np.where(
        scores["ChurnScore_"] > scores["Threshold"], "Yes", "No"
    )

    # --- aliases DEPOIS do fix (pra ficarem consistentes) ---
    scores["ChurnScore"]     = scores["ChurnScore_"]
    scores["ChurnPredicted"] = scores["ChurnPredicted__"]

    # --- FIX 2: SentimentScore correto vindo do feedback.csv ---
    feedback["SentimentScore"] = pd.to_numeric(
        feedback["SentimentScore"].astype(str).str.strip().str.replace(",", ".", regex=False),
        errors="coerce",
    )
    feedback["customerID"] = feedback["customerID"].astype(str).str.strip()
    scores["customerID"]   = scores["customerID"].astype(str).str.strip()

    feedback_score = (
        feedback
        .dropna(subset=["customerID"])
        .query("customerID != ''")
        .groupby("customerID", as_index=False)["SentimentScore"]
        .mean()
    )

    scores = (
        scores
        .drop(columns=["SentimentScore"], errors="ignore")
        .merge(feedback_score, on="customerID", how="left", validate="one_to_one")
    )
    # --- fim do FIX 2 ---

        # --- fim do FIX 2 ---

    # --- FIX 2b: SentimentScore também no intelligence ---
    intelligence = (
        intelligence
        .drop(columns=["SentimentScore"], errors="ignore")
        .merge(feedback_score, on="customerID", how="left", validate="one_to_one")
    )
    # --- fim do FIX 2b ---

    for df in [scores, intelligence, aspects, feedback]:
        df["customerID"] = df["customerID"].astype(str).str.strip()

    for df in [scores, intelligence, aspects, feedback]:
        df["customerID"] = df["customerID"].astype(str).str.strip()

    return scores, intelligence, aspects, feedback

scores, intelligence, aspects, feedback = load_data()


# --------------------------------------------------
# 4. Funções auxiliares
# --------------------------------------------------

def get_value(row, column, default="Não disponível"):

    if row is None or column not in row.index:
        return default

    value = row[column]

    if pd.isna(value) or str(value).strip() == "":
        return default

    return value

def classify_sentiment(score):
    """Converte score numérico em rótulo consistente (VADER padrão)."""
    try:
        s = float(score)
    except (ValueError, TypeError):
        return "Não disponível"

    if s >= 0.05:
        return "Positivo"
    elif s <= -0.05:
        return "Negativo"
    else:
        return "Neutro"


def format_sentiment(value):
    translations = {
        "positive": "Positivo",
        "negative": "Negativo",
        "mixed": "Misto",
        "neutral": "Neutro",
        "positivo": "Positivo",
        "negativo": "Negativo",
        "misto": "Misto",
        "neutro": "Misto",
    }

    return translations.get(
        str(value).strip().lower(), value
    )


def safe_number(value):

    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0

def render_metric_card(label, value, bg_color="#1B3139", text_color="#EEEDE9", label_color="#A0B4BC", accent_color=None):
    accent = f"border-left: 4px solid {accent_color};" if accent_color else ""
    st.html(
        f"""
        <div class="terra-metric-card" style="background: {bg_color}; {accent}">
            <div class="terra-metric-label" style="color: {label_color};">{label}</div>
            <div class="terra-metric-value" style="color: {text_color};">{value}</div>
        </div>
        """
    )

def render_gauge_card(probability):
    """Gauge com gradiente verde→amarelo→laranja→vermelho."""
    pct = max(0.0, min(1.0, float(probability)))
    pct_display = pct * 100

    # Cor do texto por faixa
    if pct >= 0.7:
        text_color = "#EF4444"
    elif pct >= 0.4:
        text_color = "#F97316"
    else:
        text_color = "#22C55E"

    arc_length = 251.33
    filled_length = arc_length * pct

    # Gradiente fixo no espaço do viewBox (x1=20 a x2=180)
    # Verde na ponta esquerda → vermelho na ponta direita
    stops = (
        f'<stop offset="0%" stop-color="#22C55E"/>'
        f'<stop offset="40%" stop-color="#EAB308"/>'
        f'<stop offset="70%" stop-color="#F97316"/>'
        f'<stop offset="100%" stop-color="#EF4444"/>'
    )

    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 100" width="200" height="100">'
        f'<defs>'
        f'<linearGradient id="churnGradient" gradientUnits="userSpaceOnUse" x1="20" y1="0" x2="180" y2="0">'
        f'{stops}'
        f'</linearGradient>'
        f'</defs>'
        f'<path d="M 20 85 A 80 80 0 0 1 180 85" fill="none" stroke="#2A4655" '
        f'stroke-width="14" stroke-linecap="round"/>'
        f'<path d="M 20 85 A 80 80 0 0 1 180 85" fill="none" stroke="url(#churnGradient)" '
        f'stroke-width="14" stroke-linecap="round" stroke-dasharray="{filled_length:.2f} {arc_length}"/>'
        f'<text x="100" y="78" text-anchor="middle" font-size="28" font-weight="700" '
        f'fill="{text_color}" font-family="Arial, sans-serif">{pct_display:.0f}%</text>'
        f'</svg>'
    )

    b64 = base64.b64encode(svg.encode("utf-8")).decode("utf-8")

    st.html(f"""
    <div class="terra-gauge-card">
        <img src="data:image/svg+xml;base64,{b64}"
             style="width: 100%; max-width: 160px; height: auto; display: block;" />
        <div class="terra-gauge-scale">
            <span>0%</span>
            <span>100%</span>
        </div>
    </div>
    """)

def get_whatsapp_icon_base64():
    """Lê o PNG do WhatsApp do assets e retorna como base64."""
    icon_path = Path(__file__).parent.parent / "assets" / "whatsapp.png"
    if not icon_path.exists():
        return ""
    with open(icon_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# --------------------------------------------------
# 5. Orientação condicional de atendimento
# --------------------------------------------------
def detect_churn_language(feedback_text):
    """Detecta linguagem explícita de saída no feedback, com tratamento de negação."""
    if not feedback_text or not isinstance(feedback_text, str):
        return False
    text_lower = feedback_text.lower()

    # 1. PRIMEIRO: checar negações explícitas
    negations = [
        "no plans to churn",
        "no plans to cancel",
        "no plans to switch",
        "no plans to leave",
        "not planning to churn",
        "not planning to cancel",
        "not planning to leave",
        "decided not to cancel",
        "decided not to churn",
        "decided not to leave",
        "will not churn",
        "won't churn",
        "will not cancel",
        "won't cancel",
    ]
    if any(p in text_lower for p in negations):
        return False

    # 2. DEPOIS: frases afirmativas de saída
    churn_phrases = [
        # Saída consumada (1ª pessoa / explícita)
        "had to churn",
        "i churned",
        "i cancelled",
        "i canceled",
        "i have cancelled",
        "i have canceled",
        "cancelled the service",
        "canceled the service",
        "cancelled my service",
        "canceled my service",
        "terminated my contract",
        "terminate my contract",
        # Decisão/declaração
        "decided to cancel",
        "decided to churn",
        "decided to leave",
        "decided to switch provider",
        "decided to switch to another",
        "had to cancel",
        "had to leave",
        # Estado atual
        "no longer a customer",
        "not a customer anymore",
        "switched provider",
        "switched to another",
        "moved to another provider",
    ]
    return any(phrase in text_lower for phrase in churn_phrases)

def detect_satisfaction(feedback_text):
    """Detecta satisfação explícita que o VADER pode interpretar errado."""
    if not feedback_text or not isinstance(feedback_text, str):
        return False
    t = feedback_text.lower()
    satisfaction_phrases = [
        "no plans to churn",
        "no plans to cancel",
        "no plans to leave",
        "no plans to switch",
        "no issues with the service",
        "no issues with my service",
        "no problems with",
        "very satisfied",
        "extremely satisfied",
        "highly satisfied",
        "i am satisfied",
        "have been satisfied",
        "would recommend",
        "highly recommend",
        "very happy with",
        "extremely happy with",
        "no complaints",
        "great service",
        "excellent service",
    ]
    return any(p in t for p in satisfaction_phrases)

def generate_guidance(prediction, customer_aspects, sentiment, feedback_text=""):
    """Gera guidance considerando aspectos, sentimento, previsão E sinal de saída no texto."""

    # Sinal 1 — menções negativas nos aspectos
    if "Qtd_Negativas" in customer_aspects.columns:
        negative_mentions = pd.to_numeric(
            customer_aspects["Qtd_Negativas"], errors="coerce"
        ).fillna(0).sum()
    else:
        negative_mentions = 0

    # Sinal 2 — sentimento
    sentiment_lower = str(sentiment).strip().lower()
    sentiment_negative = sentiment_lower in ("negativo", "negative")

    has_negativity = (negative_mentions > 0) or sentiment_negative

    # Sinal 3 — feedback menciona que o cliente já saiu
    already_churned = detect_churn_language(feedback_text)

    # Aspectos relevantes
    attention_aspects = []
    if not customer_aspects.empty and negative_mentions > 0:
        negative_aspects = customer_aspects.copy()
        negative_aspects["Qtd_Negativas"] = pd.to_numeric(
            negative_aspects["Qtd_Negativas"], errors="coerce"
        ).fillna(0)
        negative_aspects = negative_aspects[
            negative_aspects["Qtd_Negativas"] > 0
        ].sort_values("Qtd_Negativas", ascending=False)
        if "Aspecto" in negative_aspects.columns:
            attention_aspects = negative_aspects["Aspecto"].head(2).tolist()

    if attention_aspects:
        _aspects = ", ".join(attention_aspects)
        _prep_em = "em "
        _prep_a = "a "
        _prep_plain = ""
    else:
        _aspects = "aspectos da experiência"
        _prep_em = "nos "
        _prep_a = "aos "
        _prep_plain = "os "

    # ---- CASO ESPECIAL: feedback indica que o cliente já saiu ----
    if already_churned:
        if has_negativity:
            return (
                "⚠️ VERIFICAR STATUS — POSSÍVEL EX-CLIENTE",
                f"O feedback indica que o cliente saiu em algum momento, "
                f"mas o dado pode estar desatualizado (o cliente pode ter retornado). "
                f"Há sinais negativos, especialmente {_prep_em}{_aspects}.",
                f"1️⃣ ANTES DE AGIR: consulte o CRM para confirmar o status atual.\n"
                f"2️⃣ SE ATIVO: contato de retenção — investigue {_prep_plain}{_aspects} "
                f"e apresente alternativas de solução.\n"
                f"3️⃣ SE INATIVO: campanha de win-back — analise {_prep_plain}{_aspects} "
                f"e ofereça proposta direcionada de reativação.",
                "warning"
            )
        else:
            return (
                "⚠️ VERIFICAR STATUS — POSSÍVEL EX-CLIENTE",
                "O feedback indica que o cliente saiu em algum momento, "
                "mas o dado pode estar desatualizado. Sem sinais negativos claros no texto.",
                "1️⃣ ANTES DE AGIR: consulte o CRM para confirmar o status atual.\n"
                "2️⃣ SE ATIVO: mantenha o relacionamento e confirme a satisfação.\n"
                "3️⃣ SE INATIVO: considere oferta de win-back — a saída pode ter sido "
                "por motivo externo (preço, mudança).",
                "warning"
            )

    # ---- CLIENTE ATIVO (fluxo normal) ----
    if prediction == "Yes" and has_negativity:
        return (
            "PRIORIDADE ALTA",
            f"Existe previsão de churn e há sinais negativos no feedback, "
            f"especialmente {_prep_em}{_aspects}.",
            f"Priorize um contato proativo: investigue os problemas relacionados "
            f"{_prep_a}{_aspects}, apresente alternativas de solução e combine um "
            f"acompanhamento.",
            "alert"
        )

    elif prediction == "Yes":
        return (
            "CONTATO PREVENTIVO",
            "Existe previsão de churn, mas não foram identificados sinais negativos claros.",
            "Entre em contato para confirmar a satisfação, compreender possíveis "
            "riscos e reforçar os benefícios do serviço.",
            "warning"
        )

    elif has_negativity:
        return (
            "ACOMPANHAMENTO",
            f"Não há previsão de churn, mas há sinais negativos no feedback, "
            f"especialmente {_prep_em}{_aspects}.",
            f"Investigue os pontos de insatisfação, especialmente {_prep_plain}{_aspects}, "
            f"e acompanhe sua resolução.",
            "warning"
        )

    else:
        return (
            "MANUTENÇÃO DO RELACIONAMENTO",
            "Não há previsão de churn e não foram identificados sinais negativos.",
            "Mantenha o acompanhamento regular e reforce os aspectos positivos da experiência.",
            "neutral"
        )

# --------------------------------------------------
# 6. Cabeçalho
# --------------------------------------------------

header_left, header_center, header_right = st.columns(
    [0.9, 2.4, 0.9],
    vertical_alignment="center"
)

with header_left:
    st.markdown('<div class="logo-databricks">', unsafe_allow_html=True)
    st.image("assets/databricks.png", width=180)
    st.markdown('</div>', unsafe_allow_html=True)

with header_center:
    order_by = st.radio(
        "Ordenar por",
        ["Prioridade de churn", "Ordem alfabética"],
        horizontal=True,
        label_visibility="collapsed"
    )

    scores_sorted = (
        scores[["customerID", "ChurnScore"]]
        .dropna(subset=["customerID"])
    )

    if order_by == "Prioridade de churn":
        scores_sorted = scores_sorted.sort_values(
            "ChurnScore", ascending=False
        )
    else:
        scores_sorted = scores_sorted.sort_values(
            "customerID", ascending=True
        )

    customer_ids = scores_sorted["customerID"].tolist()

    customer_id = st.selectbox(
        "Pesquisar Cliente por ID",
        ["Selecione um cliente"] + customer_ids,
        label_visibility="visible"
    )

with header_right:
    st.markdown('<div class="logo-terra">', unsafe_allow_html=True)
    st.image("assets/terra_signal.png", width=200)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown(
    '<div style="border-bottom: 1px solid #2A4655; margin: 0.5rem 0;"></div>',
    unsafe_allow_html=True
)

# --------------------------------------------------
# 7. Informações do cliente
# --------------------------------------------------

if customer_id == "Selecione um cliente":

    st.info("Selecione um cliente para visualizar suas informações.")

else:

    customer_scores = scores[
        scores["customerID"] == customer_id
    ]

    customer_info = intelligence[
        intelligence["customerID"] == customer_id
    ]

    customer_aspects = aspects[
        aspects["customerID"] == customer_id
    ]

    customer_feedback = feedback[
        feedback["customerID"] == customer_id
    ]

    score_row = (
        customer_scores.iloc[0]
        if not customer_scores.empty else None
    )

    info_row = (
        customer_info.iloc[0]
        if not customer_info.empty else None
    )

    feedback_row = (
        customer_feedback.iloc[0]
        if not customer_feedback.empty else None
    )

    prediction = get_value(
        score_row, "ChurnPredicted"
    )

    # --------------------------------------------------
    # 8. Layout principal
    # --------------------------------------------------

    left, right = st.columns([1.05, 1.15], gap="large")

    # ================================================
    # COLUNA ESQUERDA
    # ================================================

    with left:

        # Score de churn
        with st.container(border=True):

            st.subheader("Score de Churn Histórico")

            col1, col2, col3 = st.columns(3)

            prediction_label = {
                "Yes": "Sim",
                "No": "Não"
            }.get(prediction, prediction)

            churn_probability = safe_number(
                get_value(score_row, "ChurnScore", 0)
            )

            rank = get_value(score_row, "Rank")

            try:
                rank = f"#{int(float(rank))}"
            except (ValueError, TypeError):
                rank = "Não disponível"

            with col1:
                if prediction == "Yes":
                    render_metric_card(
                        "Previsão de Churn",
                        prediction_label,
                        bg_color="rgba(239, 68, 68, 0.15)",
                        text_color="#EF4444",
                        label_color="rgba(239, 68, 68, 0.7)"
                    )
                else:
                    render_metric_card("Previsão de Churn", prediction_label)

            with col2:
                render_gauge_card(churn_probability)

            with col3:
                render_metric_card("Ranking do Cliente", rank)

        # Aspectos da experiência 
        with st.container(border=True):

            st.subheader("Aspectos da experiência")

            if not customer_aspects.empty:

                display_aspects = customer_aspects.copy()

                columns = [
                    "Aspecto",
                    "Sentimento_Consolidado",
                    "Qtd_Mistas",
                    "Qtd_Negativas",
                    "Qtd_Positivas"
                ]

                for column in columns:
                    if column not in display_aspects.columns:
                        display_aspects[column] = 0

                display_aspects = display_aspects[
                    columns
                ].rename(columns={
                    "Sentimento_Consolidado": "Sentimento",
                    "Qtd_Mencoes": "Menções",
                    "Qtd_Mistas": "Mistas",
                    "Qtd_Negativas": "Negativas",
                    "Qtd_Positivas": "Positivas"
                })

                display_aspects["Sentimento"] = (
                    display_aspects["Sentimento"]
                    .apply(format_sentiment)
                )

                # ---- FILTRO 1: remove linhas com todas as quantidades = 0 ----
                qty_cols = ["Menções", "Mistas", "Negativas", "Positivas"]
                qty_cols = [c for c in qty_cols if c in display_aspects.columns]
                if qty_cols:
                    total_mencoes = display_aspects[qty_cols].sum(axis=1)
                    display_aspects = display_aspects[total_mencoes > 0]

                # ---- FILTRO 2: remove placeholders ("sem avaliação", etc.) ----
                placeholders = [
                    "sem avaliação", "sem avaliacao",
                    "não avaliado", "nao avaliado",
                    "sem menção", "sem mencao",
                    "n/a", "na", "-", "",
                ]
                if "Aspecto" in display_aspects.columns:
                    display_aspects = display_aspects[
                        ~display_aspects["Aspecto"]
                        .astype(str).str.strip().str.lower()
                        .isin(placeholders)
                    ]

                # ---- Renderiza (ou avisa se ficou vazio) ----
                if display_aspects.empty:
                    st.info("Nenhum aspecto com menções relevantes para este cliente.")
                else:
                    st.html(
                        f'<div class="terra-table-wrapper">'
                        f'{display_aspects.to_html(index=False, classes="terra-table")}'
                        f'</div>'
                    )

    # ================================================
    # COLUNA DIREITA
    # ================================================

    with right:

        # Sentimento do cliente
        with st.container(border=True):

            # Workaround: SentimentScore + classify_sentiment (funciona com CSV atual)
            sentiment_score_raw = get_value(info_row, "SentimentScore")
            if sentiment_score_raw == "Não disponível" and feedback_row is not None:
                sentiment_score_raw = get_value(feedback_row, "SentimentScore")

            sentiment = classify_sentiment(sentiment_score_raw)

            # Redes de segurança (churn + satisfação)
            _fb_check = get_value(info_row, "Feedback_Limpo")
            if _fb_check == "Não disponível" and feedback_row is not None:
                _fb_check = get_value(feedback_row, "Feedback_Limpo")

            # 1. Rebaixar Positivo → Misto se há churn no texto
            if (detect_churn_language(_fb_check)
                and str(sentiment).strip().lower() in ("positivo", "positive")):
                sentiment = "Misto"

            # 2. Elevar Negativo/Neutro → Positivo se há satisfação explícita
            if (detect_satisfaction(_fb_check)
                and str(sentiment).strip().lower() in ("negativo", "negative", "neutro", "neutral")):
                sentiment = "Positivo"

            # Score para o card de referência
            sentiment_score = get_value(info_row, "SentimentScore")
            if sentiment_score == "Não disponível" and feedback_row is not None:
                sentiment_score = get_value(feedback_row, "SentimentScore")

            # Emoji condicional
            sentiment_raw = str(sentiment).strip().lower()

            if sentiment_raw in ("negative", "negativo"):
                sentiment_emoji = "💔"
            elif sentiment_raw in ("positive", "positivo"):
                sentiment_emoji = "❤️"
            else:
                sentiment_emoji = "🤍"

            st.subheader(f"{sentiment_emoji} Sentimento do cliente")

            # Cor por sentimento
            if sentiment_raw in ("positive", "positivo"):
                sentiment_bg = "rgba(34, 197, 94, 0.15)"
                sentiment_text = "#22C55E"
                sentiment_label_color = "rgba(34, 197, 94, 0.7)"
            elif sentiment_raw in ("negative", "negativo"):
                sentiment_bg = "rgba(249, 115, 22, 0.15)"
                sentiment_text = "#F97316"
                sentiment_label_color = "rgba(249, 115, 22, 0.7)"
            else:
                sentiment_bg = "#1B3139"
                sentiment_text = "#EEEDE9"
                sentiment_label_color = "#A0B4BC"

            sentiment_col1, sentiment_col2 = st.columns(2)

            with sentiment_col1:
                render_metric_card(
                    "Sentimento consolidado",
                    format_sentiment(sentiment),
                    bg_color=sentiment_bg,
                    text_color=sentiment_text,
                    label_color=sentiment_label_color
                )

            with sentiment_col2:
                score_value = (
                    f"{safe_number(sentiment_score):+.2f}"
                    if sentiment_score != "Não disponível"
                    else "Não disponível"
                )
                render_metric_card(
                    "Sentiment Score",
                    score_value,
                    text_color=sentiment_text,
                    label_color=sentiment_label_color
                )

        # Feedback completo
        with st.container(border=True):

            st.subheader("🗨️ Feedback completo")

            full_feedback = get_value(info_row, "Feedback_Limpo")

            if full_feedback == "Não disponível" and feedback_row is not None:
                full_feedback = get_value(feedback_row, "Feedback_Limpo")

            st.write(full_feedback)

    # --------------------------------------------------
    # 9. Orientação de atendimento
    # --------------------------------------------------

    st.markdown(" ")

    with st.container(border=True):

        _fb = get_value(info_row, "Feedback_Limpo")
        if _fb == "Não disponível" and feedback_row is not None:
            _fb = get_value(feedback_row, "Feedback_Limpo")

        guidance_title, guidance_condition, guidance_action, guidance_level = generate_guidance(
            prediction,
            customer_aspects,
            sentiment,
            feedback_text=_fb if _fb != "Não disponível" else ""
        )

        guidance_col, actions_col = st.columns([4, 1], gap="medium")

        # ---- Coluna esquerda: guidance ----
        with guidance_col:

            st.subheader("💡 Orientação de atendimento")

            st.html(
                f"""
                <div class="guidance guidance-{guidance_level}">
                    <div class="guidance-title">{guidance_title}</div>

                    <div class="guidance-row">
                        <span class="guidance-label">Condição</span>
                        <span class="guidance-body">{guidance_condition}</span>
                    </div>

                    <div class="guidance-row">
                        <span class="guidance-label">Ação sugerida</span>
                        <span class="guidance-body">{guidance_action}</span>
                    </div>
                </div>
                """
            )

        # ---- Coluna direita: ações ----
        with actions_col:

            st.subheader("Ações")

            # WhatsApp
            phone = get_value(info_row, "Phone")
            if phone == "Não disponível":
                phone = get_value(info_row, "Telefone")

            phone_str = str(phone).strip().lower() if phone != "Não disponível" else ""
            is_real_phone = (
                phone != "Não disponível"
                and phone_str not in ("yes", "no", "sim", "não", "true", "false", "")
            )

            wa_icon = get_whatsapp_icon_base64()

            # Carrega PNG do WhatsApp; se falhar, usa emoji como fallback
            wa_icon = get_whatsapp_icon_base64()
            use_logo = bool(wa_icon)

            if use_logo:
                wa_html = (
                    f'<img src="data:image/png;base64,{wa_icon}" '
                    f'style="width:18px;height:18px;vertical-align:middle;'
                    f'margin-right:6px;border:0;" />'
                )
            else:
                wa_html = "📱 "

            if is_real_phone:
                phone_clean = (
                    str(phone).replace(" ", "").replace("-", "")
                    .replace("(", "").replace(")", "").replace("+", "")
                )
                st.markdown(
                    f'<a href="https://wa.me/{phone_clean}" target="_blank" class="wa-btn" '
                    f'style="display:inline-flex;align-items:center;'
                    f'padding:0.45rem 1rem;background:#1B3139;'
                    f'border:1px solid #2A4655;border-radius:8px;'
                    f'color:#EEEDE9;text-decoration:none;font-size:0.9rem;'
                    f'font-family:inherit;margin:0.25rem 0;width:fit-content;">'
                    f'{wa_html}WhatsApp</a>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f'<a href="#" class="wa-btn" '
                    f'style="display:inline-flex;align-items:center;'
                    f'padding:0.45rem 1rem;background:#1B3139;'
                    f'border:1px solid #2A4655;border-radius:8px;'
                    f'color:#EEEDE9;text-decoration:none;font-size:0.9rem;'
                    f'font-family:inherit;margin:0.25rem 0;width:fit-content;">'
                    f'{wa_html}WhatsApp</a>',
                    unsafe_allow_html=True
                )

            # Email
            email = get_value(info_row, "Email")
            if email == "Não disponível":
                email = get_value(info_row, "CustomerEmail")

            is_real_email = email != "Não disponível" and "@" in str(email)

            if is_real_email:
                st.link_button("✉️ Email", f"mailto:{email}")
            else:
                if st.button("✉️ Email", key="btn_email"):
                    st.toast("Email não disponível nos dados", icon="ℹ️")

            # Aplicar plano (visual por enquanto)
            if st.button("🎯 Aplicar plano", key="btn_plan"):
                st.toast("Plano de retenção aplicado (simulado)", icon="✅")

        st.caption(
            "Orientação baseada em previsão de churn, sentimento, aspectos e sinais no feedback. "
            "⚠️ Quando o feedback indica possível saída, a orientação pede verificação no CRM "
            "antes de qualquer ação — o cliente pode ter retornado."
        )