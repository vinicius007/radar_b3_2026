"""
Estilos e Temas CSS customizados para reproduzir o visual executivo do Power BI.
Suporta alternância dinâmica entre Modo Escuro (Dark Slate) e Modo Claro (Clean Executive).
Inclui estilização aprimorada de botões no Modo Escuro para garantir contraste elevado e destaque.
"""

def get_powerbi_css(dark_mode: bool = True) -> str:
    """Gera o CSS corporativo adaptado para Modo Escuro ou Modo Claro."""
    
    if dark_mode:
        # Paleta Modo Escuro (Dark Slate / Deep Navy)
        bg_app = "#0B1120"
        card_bg = "#1E293B"
        card_bg_alt = "#0F172A"
        header_bg = "linear-gradient(135deg, #0F172A 0%, #1E293B 100%)"
        border_color = "#334155"
        border_color_light = "#475569"
        text_primary = "#F8FAFC"
        text_secondary = "#94A3B8"
        text_muted = "#64748B"
        table_header_bg = "#0F172A"
        input_bg = "#0F172A"
        hover_shadow = "0 8px 25px rgba(0, 0, 0, 0.45)"
        
        # Botões destacados no modo escuro (fundo escuro e marcante, sem ficar claro)
        btn_sec_bg = "#0F172A"
        btn_sec_color = "#F8FAFC"
        btn_sec_border = "#38BDF8"
        btn_sec_hover_bg = "#1E293B"
        btn_sec_hover_color = "#38BDF8"
        btn_sec_hover_border = "#00D084"
        btn_sec_shadow = "0 4px 14px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.05)"
        
        btn_pri_bg = "linear-gradient(135deg, #0284C7 0%, #0369A1 100%)"
        btn_pri_hover_bg = "linear-gradient(135deg, #0369A1 0%, #075985 100%)"
        btn_pri_color = "#FFFFFF"
        btn_pri_border = "#38BDF8"
        btn_pri_shadow = "0 4px 16px rgba(2, 132, 199, 0.45)"
    else:
        # Paleta Modo Claro (Clean Executive / Crisp White)
        bg_app = "#F8FAFC"
        card_bg = "#FFFFFF"
        card_bg_alt = "#F1F5F9"
        header_bg = "linear-gradient(135deg, #FFFFFF 0%, #F1F5F9 100%)"
        border_color = "#CBD5E1"
        border_color_light = "#94A3B8"
        text_primary = "#0F172A"
        text_secondary = "#475569"
        text_muted = "#64748B"
        table_header_bg = "#E2E8F0"
        input_bg = "#FFFFFF"
        hover_shadow = "0 8px 25px rgba(0, 0, 0, 0.08)"
        
        btn_sec_bg = "#FFFFFF"
        btn_sec_color = "#0F172A"
        btn_sec_border = "#CBD5E1"
        btn_sec_hover_bg = "#F1F5F9"
        btn_sec_hover_color = "#0284C7"
        btn_sec_hover_border = "#0284C7"
        btn_sec_shadow = "0 2px 6px rgba(0, 0, 0, 0.06)"
        
        btn_pri_bg = "linear-gradient(135deg, #0284C7 0%, #0369A1 100%)"
        btn_pri_hover_bg = "linear-gradient(135deg, #0369A1 0%, #075985 100%)"
        btn_pri_color = "#FFFFFF"
        btn_pri_border = "#0284C7"
        btn_pri_shadow = "0 4px 12px rgba(2, 132, 199, 0.25)"

    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@300;400;600;700;800&family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"], [data-testid="stAppViewContainer"] {{
    font-family: 'Segoe UI', 'Inter', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
}}

.stApp {{
    background-color: {bg_app} !important;
    color: {text_primary} !important;
}}

/* ============================================================ */
/* ESTILIZAÇÃO DE BOTÕES EXECUTIVOS (DESTAQUE NO MODO ESCURO)    */
/* ============================================================ */
.stApp button,
[data-testid="stBaseButton-secondary"],
.stButton > button,
button[kind="secondary"] {{
    background: {btn_sec_bg} !important;
    color: {btn_sec_color} !important;
    border: 1.5px solid {btn_sec_border} !important;
    border-radius: 8px !important;
    padding: 8px 18px !important;
    font-weight: 700 !important;
    font-size: 13px !important;
    box-shadow: {btn_sec_shadow} !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    letter-spacing: 0.2px !important;
}}

.stApp button:hover,
[data-testid="stBaseButton-secondary"]:hover,
.stButton > button:hover,
button[kind="secondary"]:hover {{
    background: {btn_sec_hover_bg} !important;
    color: {btn_sec_hover_color} !important;
    border-color: {btn_sec_hover_border} !important;
    box-shadow: 0 0 16px rgba(56, 189, 248, 0.4) !important;
    transform: translateY(-2px) !important;
}}

.stApp button:active,
.stButton > button:active {{
    transform: translateY(0) !important;
}}

[data-testid="stBaseButton-primary"],
.stButton > button[kind="primary"],
button[kind="primary"],
[data-testid="stFormSubmitButton"] > button {{
    background: {btn_pri_bg} !important;
    color: {btn_pri_color} !important;
    border: 1.5px solid {btn_pri_border} !important;
    border-radius: 8px !important;
    padding: 8px 20px !important;
    font-weight: 800 !important;
    font-size: 13.5px !important;
    box-shadow: {btn_pri_shadow} !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
}}

[data-testid="stBaseButton-primary"]:hover,
.stButton > button[kind="primary"]:hover,
button[kind="primary"]:hover,
[data-testid="stFormSubmitButton"] > button:hover {{
    background: {btn_pri_hover_bg} !important;
    border-color: #00D084 !important;
    box-shadow: 0 0 20px rgba(56, 189, 248, 0.6) !important;
    transform: translateY(-2px) !important;
}}

/* TOPO EXECUTIVO POWER BI */
.pbi-header-container {{
    background: {header_bg};
    border: 1px solid {border_color};
    border-radius: 12px;
    padding: 16px 22px;
    margin-bottom: 20px;
    box-shadow: {hover_shadow};
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 16px;
    flex-wrap: wrap;
}}

.pbi-logo-img {{
    height: 62px;
    width: auto;
    object-fit: contain;
    border-radius: 8px;
    filter: drop-shadow(0 2px 8px rgba(0, 128, 255, 0.25));
}}

.pbi-header-title {{
    font-size: 20px;
    font-weight: 800;
    color: {text_primary};
    letter-spacing: -0.3px;
    margin: 0;
    line-height: 1.2;
}}

.pbi-header-subtitle {{
    font-size: 12.5px;
    color: {text_secondary};
    margin-top: 4px;
    font-weight: 400;
    line-height: 1.3;
}}

.pbi-avatar-circle {{
    width: 34px;
    height: 34px;
    border-radius: 50%;
    background: linear-gradient(135deg, #0284C7 0%, #0369A1 100%);
    color: #FFFFFF;
    font-weight: 800;
    font-size: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 2px 6px rgba(2, 132, 199, 0.4);
}}

/* CARTÕES DE KPI EXECUTIVOS */
.pbi-kpi-card {{
    background: {card_bg};
    border: 1px solid {border_color};
    border-radius: 10px;
    padding: 14px 16px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    transition: transform 0.2s ease, border-color 0.2s ease;
    height: 100%;
}}

.pbi-kpi-card:hover {{
    border-color: #38BDF8;
    transform: translateY(-2px);
}}

.pbi-kpi-label {{
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    color: {text_secondary};
    margin-bottom: 4px;
}}

.pbi-kpi-value {{
    font-size: 22px;
    font-weight: 800;
    color: {text_primary};
    letter-spacing: -0.5px;
    line-height: 1.15;
    margin-bottom: 4px;
}}

.pbi-kpi-sub {{
    font-size: 11.5px;
    color: {text_secondary};
    display: flex;
    align-items: center;
    gap: 4px;
}}

.pbi-tag-positive {{
    color: #10B981;
    font-weight: 700;
}}

.pbi-tag-negative {{
    color: #EF4444;
    font-weight: 700;
}}

.pbi-tag-neutral {{
    color: {text_secondary};
    font-weight: 600;
}}

/* CONTAINERS DE GRÁFICOS E TABELAS */
.pbi-chart-container {{
    background: {card_bg};
    border: 1px solid {border_color};
    border-radius: 10px;
    padding: 18px 20px;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.12);
    margin-bottom: 16px;
}}

.pbi-chart-title {{
    font-size: 15px;
    font-weight: 700;
    color: {text_primary};
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
}}

/* CARTÃO DE AÇÃO / ALERTAS */
.pbi-action-card {{
    background: {card_bg};
    border: 1px solid {border_color};
    border-radius: 10px;
    padding: 16px 18px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    margin-bottom: 12px;
}}

.pbi-action-ticker {{
    font-size: 16px;
    font-weight: 800;
    color: #38BDF8;
}}

.pbi-action-name {{
    font-size: 13px;
    color: {text_secondary};
    margin-left: 6px;
}}

/* ZONA DE PERIGO */
.pbi-danger-zone {{
    background: rgba(239, 68, 68, 0.08);
    border: 2px solid #EF4444;
    border-radius: 10px;
    padding: 20px;
    margin-top: 24px;
}}

.pbi-danger-title {{
    color: #EF4444;
    font-weight: 800;
    font-size: 16px;
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 6px;
}}

.pbi-danger-text {{
    color: {text_secondary};
    font-size: 13px;
    margin-bottom: 14px;
}}

/* CARD CENTRALIZADO DE LOGIN / CADASTRO */
.pbi-auth-card {{
    background: {card_bg};
    border: 1px solid {border_color};
    border-radius: 14px;
    padding: 32px 36px;
    box-shadow: {hover_shadow};
    max-width: 520px;
    margin: 20px auto;
}}

/* BARRA DE FORÇA DE SENHA */
.pbi-strength-bar {{
    height: 6px;
    border-radius: 4px;
    background: #334155;
    margin-top: 6px;
    overflow: hidden;
}}

.pbi-strength-fill {{
    height: 100%;
    transition: width 0.3s ease, background-color 0.3s ease;
}}

/* AJUSTES NO STREAMLIT */
[data-testid="stSidebar"] {{
    background-color: {card_bg_alt} !important;
    border-right: 1px solid {border_color} !important;
}}

.stTabs [data-baseweb="tab-list"] {{
    gap: 8px;
    border-bottom: 1px solid {border_color};
}}

.stTabs [data-baseweb="tab"] {{
    border-radius: 6px 6px 0 0;
    padding: 8px 16px;
    font-weight: 600;
    font-size: 13px;
    color: {text_secondary};
}}

.stTabs [aria-selected="true"] {{
    color: #38BDF8 !important;
    border-bottom: 2px solid #38BDF8 !important;
}}

/* ESTILIZAÇÃO DO MENU RETRÁTIL DO TOPO DIREITO */
[data-testid="stPopover"] {{
    width: 100%;
}}

[data-testid="stPopover"] > button {{
    border-radius: 20px !important;
    padding: 8px 18px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-size: 13.5px !important;
    font-weight: 800 !important;
    letter-spacing: 0.3px !important;
}}

[data-testid="stPopoverBody"] {{
    border-radius: 12px !important;
    padding: 14px 16px !important;
    box-shadow: 0 12px 36px rgba(0, 0, 0, 0.6) !important;
    min-width: 260px !important;
}}

/* BOTÕES DO TOPO (DESLOGADO) CONFORME IMAGEM DO USUÁRIO */
.st-key-top_btn_cadastre_se button,
div[data-testid="stButton"].st-key-top_btn_cadastre_se button,
div.st-key-top_btn_cadastre_se > button {{
    background: #D83A14 !important;
    background-color: #D83A14 !important;
    color: #FFFFFF !important;
    font-weight: 800 !important;
    font-size: 13px !important;
    letter-spacing: 0.5px !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 8px 16px !important;
    box-shadow: 0 2px 6px rgba(216, 58, 20, 0.4) !important;
    transition: all 0.2s ease !important;
}}

.st-key-top_btn_cadastre_se button:hover,
div[data-testid="stButton"].st-key-top_btn_cadastre_se button:hover,
div.st-key-top_btn_cadastre_se > button:hover {{
    background: #BF2D0B !important;
    background-color: #BF2D0B !important;
    color: #FFFFFF !important;
    border: none !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 10px rgba(216, 58, 20, 0.6) !important;
}}

.st-key-top_btn_entrar button,
div[data-testid="stButton"].st-key-top_btn_entrar button,
div.st-key-top_btn_entrar > button {{
    background: rgba(13, 148, 136, 0.2) !important;
    background-color: rgba(13, 148, 136, 0.2) !important;
    color: #FFFFFF !important;
    font-weight: 800 !important;
    font-size: 13px !important;
    letter-spacing: 0.5px !important;
    text-transform: uppercase !important;
    border: 2px solid #14B8A6 !important;
    border-radius: 6px !important;
    padding: 6px 16px !important;
    box-shadow: 0 2px 6px rgba(20, 184, 166, 0.25) !important;
    transition: all 0.2s ease !important;
}}

.st-key-top_btn_entrar button:hover,
div[data-testid="stButton"].st-key-top_btn_entrar button:hover,
div.st-key-top_btn_entrar > button:hover {{
    background: rgba(13, 148, 136, 0.45) !important;
    background-color: rgba(13, 148, 136, 0.45) !important;
    color: #FFFFFF !important;
    border: 2px solid #2DD4BF !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 10px rgba(45, 212, 191, 0.45) !important;
}}

/* ============================================================ */
/* MINHA CARTEIRA: DESEMPENHO (GRADE 3x2)                       */
/* ============================================================ */
.pbi-perf-container {{
    margin-bottom: 18px;
}}

.pbi-perf-header-bar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
}}

.pbi-perf-main-title {{
    font-size: 17px;
    font-weight: 700;
    color: {text_primary};
    display: flex;
    align-items: center;
    gap: 8px;
}}

.pbi-perf-card {{
    background: {card_bg};
    border: 1px solid {border_color};
    border-radius: 8px;
    padding: 18px 20px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-height: 125px;
    height: 100%;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    box-sizing: border-box;
    margin-bottom: 14px;
}}

.pbi-perf-card:hover {{
    border-color: #10B981;
    box-shadow: 0 4px 14px rgba(16, 185, 129, 0.15);
    transform: translateY(-2px);
}}

.pbi-perf-top {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 6px;
}}

.pbi-perf-val {{
    font-size: 24px;
    font-weight: 800;
    color: {text_primary};
    letter-spacing: -0.5px;
    line-height: 1.1;
}}

.pbi-perf-icon {{
    display: flex;
    align-items: center;
    justify-content: center;
}}

.pbi-perf-title {{
    font-size: 13.5px;
    font-weight: 500;
    color: {text_muted};
    margin-bottom: 8px;
    line-height: 1.25;
}}

.pbi-perf-footer {{
    font-size: 12px;
    font-weight: 600;
    color: #10B981;
    display: flex;
    align-items: center;
    gap: 4px;
    min-height: 18px;
}}

.pbi-perf-footer.negative {{
    color: #EF4444;
}}

</style>
"""

POWERBI_CSS = get_powerbi_css(dark_mode=True)

def get_plotly_theme(dark_mode: bool = True) -> dict:
    """Retorna configuração do tema Plotly dinâmico para os gráficos."""
    if dark_mode:
        return {
            "layout": {
                "paper_bgcolor": "#1E293B",
                "plot_bgcolor": "#1E293B",
                "font": {"color": "#CBD5E1", "family": "Inter, Segoe UI, sans-serif"},
                "gridcolor": "#334155"
            }
        }
    else:
        return {
            "layout": {
                "paper_bgcolor": "#FFFFFF",
                "plot_bgcolor": "#FFFFFF",
                "font": {"color": "#1E293B", "family": "Inter, Segoe UI, sans-serif"},
                "gridcolor": "#E2E8F0"
            }
        }

PLOTLY_POWERBI_THEME = get_plotly_theme(dark_mode=True)
