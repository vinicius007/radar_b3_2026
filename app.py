"""
DIVIDEND RADAR B3 | RELATÓRIO EXECUTIVO DE PROVENTOS
Plataforma Executiva de Recomendação, Valuation (Bazin & Graham), Notícias e Frequência de Distribuição.
"""

import os
import textwrap
from datetime import datetime, date
import streamlit as st
import pandas as pd
import numpy as np

# Configuração da página Streamlit (Layout Wide executivo)
st.set_page_config(
    page_title="DIVIDEND RADAR B3 | RELATÓRIO EXECUTIVO DE PROVENTOS",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

import importlib

# Importações de módulos internos com reload garantido (na ordem de dependência)
import src.ui.powerbi_theme as _theme_mod
importlib.reload(_theme_mod)
from src.ui.powerbi_theme import get_powerbi_css, get_plotly_theme

import src.ui.auth_views as _auth_mod
importlib.reload(_auth_mod)
from src.ui.auth_views import (
    render_login_view,
    render_register_view,
    render_profile_view,
    render_change_password_view,
    render_reset_password_view,
    render_help_view,
    render_disclaimer_view,
    clear_login_fields,
    clear_register_fields,
    render_kmsi_cookie_setter,
    render_kmsi_cookie_clearer,
    get_kmsi_cookie_token
)

import src.ui.header as _header_mod
importlib.reload(_header_mod)
from src.ui.header import render_top_header
from src.auth.user_manager import (
    get_user_profile,
    ensure_master_user_exists,
    validate_kmsi_token,
    revoke_kmsi_token
)
from src.data.b3_universe import B3_DIVIDEND_UNIVERSE
from src.engine.recommender import get_ranked_recommendations, get_categorized_portfolios
from src.news.news_collector import fetch_ticker_news
from src.news.sentiment_analyzer import evaluate_company_news_sentiment
from src.data.portfolio_manager import (
    get_portfolio_summary,
    add_transaction,
    delete_transaction,
    load_transactions,
    get_portfolio_monthly_dividend_alerts,
    get_portfolio_dip_alerts,
    MONTH_NAMES
)
import src.ui.portfolio_components as _portfolio_ui_mod
importlib.reload(_portfolio_ui_mod)
from src.ui.portfolio_components import (
    render_portfolio_performance_overview,
    render_portfolio_kpis,
    render_pie_invested_chart,
    render_pie_current_value_chart,
    render_bar_profit_loss_chart,
    render_portfolio_summary_table,
    render_dividend_alerts_section,
    render_portfolio_dip_alerts,
    render_portfolio_dividend_history_card
)

import src.ui.components as _components_mod
importlib.reload(_components_mod)
from src.ui.components import (
    render_kpi_header,
    render_matrix_table,
    render_quadrant_scatter_chart,
    render_radar_comparison_chart,
    render_dividend_history_bars,
    render_monthly_calendar_grid,
    render_stock_dividend_agenda,
    render_news_feed,
    render_passive_income_calculator,
    render_top_dividend_yields_section,
    render_sub_10_bargain_detector,
    render_market_four_rankings_dashboard
)
from src.ui.donation_view import render_donation_view
import src.ui.radarzinha_view as _radarzinha_ui_mod
importlib.reload(_radarzinha_ui_mod)
from src.ui.radarzinha_view import render_radarzinha_tab, render_radarzinha_view, render_stop_speech_script

# Garantir existência do usuário master
ensure_master_user_exists()

# -------------------------------------------------------------
# GERENCIAMENTO DE ESTADO DA SESSÃO (SESSION STATE) & KMSI
# -------------------------------------------------------------
# Verificar cookie de sessão prolongada (KMSI) se ainda não autenticado
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
    
    cookie_token = get_kmsi_cookie_token()
    if cookie_token:
        kmsi_user = validate_kmsi_token(cookie_token)
        if kmsi_user:
            st.session_state["authenticated"] = True
            st.session_state["user"] = kmsi_user
            st.session_state["view"] = "dashboard"

if "user" not in st.session_state:
    st.session_state["user"] = None

if "view" not in st.session_state:
    st.session_state["view"] = "login" if not st.session_state.get("authenticated", False) else "dashboard"

if "dark_mode" not in st.session_state:
    st.session_state["dark_mode"] = True

if "refresh_key" not in st.session_state:
    st.session_state["refresh_key"] = 0

# Executar atualizações pendentes de cookies KMSI
if st.session_state.get("kmsi_set_token"):
    render_kmsi_cookie_setter(st.session_state.pop("kmsi_set_token"), max_age_days=30)

if st.session_state.get("kmsi_clear_cookie"):
    render_kmsi_cookie_clearer()
    del st.session_state["kmsi_clear_cookie"]

# Injeção dinâmica do Tema Power BI (Modo Escuro / Claro)
st.markdown(get_powerbi_css(dark_mode=st.session_state["dark_mode"]), unsafe_allow_html=True)

# Obter perfil atualizado do usuário autenticado
current_username = st.session_state.get("user")
if current_username and st.session_state.get("authenticated", False):
    current_profile = get_user_profile(current_username) or {
        "nome_completo": "Vinicius Augusto Marques",
        "usuario": "masterradar",
        "email": "viniciusamarques2026@gmail.com",
        "avatar_letter": "V"
    }
else:
    current_profile = {
        "nome_completo": "Visitante",
        "usuario": "",
        "email": "",
        "avatar_letter": "V"
    }

# -------------------------------------------------------------
# LAYOUT TOPO OFICIAL (LOGO OPÇÃO 4, TÍTULO, SUBTÍTULO, PERFIL)
# -------------------------------------------------------------
render_top_header(
    authenticated=st.session_state["authenticated"],
    user_profile=current_profile,
    dark_mode=st.session_state["dark_mode"]
)

# -------------------------------------------------------------
# ROTEAMENTO DE TELAS DEDICADAS
# -------------------------------------------------------------
# Rastreamento de transição de telas para limpeza de formulários
if "last_view_rendered" not in st.session_state:
    st.session_state["last_view_rendered"] = None

# Se não estiver autenticado, força a tela de login (ou cadastro/redefinição/doação/disclaimer)
if not st.session_state.get("authenticated", False):
    if st.session_state.get("view") not in ["register", "reset_password", "donation", "disclaimer"]:
        st.session_state["view"] = "login"

current_view = st.session_state.get("view", "login" if not st.session_state.get("authenticated", False) else "dashboard")

# Limpeza automática ao transitar de tela
if st.session_state["last_view_rendered"] != current_view:
    if current_view == "login":
        clear_login_fields()
    elif current_view == "register":
        if st.session_state.get("last_view_rendered") != "disclaimer":
            clear_register_fields()
    st.session_state["last_view_rendered"] = current_view

if current_view == "login":
    render_login_view()
    st.stop()
elif current_view == "register":
    render_register_view()
    st.stop()
elif current_view == "disclaimer":
    render_disclaimer_view()
    st.stop()
elif current_view == "profile":
    render_profile_view(current_username)
    st.stop()
elif current_view == "change_password":
    render_change_password_view(current_username)
    st.stop()
elif current_view == "reset_password":
    render_reset_password_view()
    st.stop()
elif current_view == "help":
    render_help_view()
    st.stop()
elif current_view == "donation":
    render_donation_view()
    st.stop()

# -------------------------------------------------------------
# CARREGAMENTO DE DADOS COM CACHE
# -------------------------------------------------------------
@st.cache_data(ttl=300, show_spinner=False)
def load_market_data(force_refresh: bool = False):
    return get_ranked_recommendations(force_refresh=force_refresh)

ranked_df = load_market_data(force_refresh=False)

if current_view == "radarzinha":
    render_radarzinha_view(ranked_df=ranked_df, current_profile=current_profile, is_tab=False)
    st.stop()

# Interromper qualquer áudio residual da Radarzinha ao sair da tela ou sob solicitação
if current_view != "radarzinha" or st.session_state.get("stop_speech_trigger", False):
    render_stop_speech_script()
    st.session_state["stop_speech_trigger"] = False

# -------------------------------------------------------------
# TOPO LADO ESQUERDO: MENU RETRÁTIL COM OPÇÕES DE MENU
# -------------------------------------------------------------
with st.sidebar:
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:10px; margin-bottom:12px;">
        <div class="pbi-avatar-circle" style="width:38px; height:38px; font-size:16px;">
            {current_profile.get('avatar_letter', 'V')}
        </div>
        <div>
            <div style="font-size:13px; font-weight:800; color:#38BDF8;">
                {current_profile.get('usuario', 'masterradar')}
            </div>
            <div style="font-size:11px; color:#94A3B8;">
                {current_profile.get('email', 'viniciusamarques2026@gmail.com')}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🏠 Home (Página Principal)", key="sb_btn_home", type="primary", use_container_width=True):
        st.session_state["view"] = "dashboard"
        st.rerun()

    c_sb1, c_sb2 = st.columns(2)
    with c_sb1:
        if st.button("👤 Perfil", key="sb_btn_profile", use_container_width=True):
            st.session_state["view"] = "profile"
            st.rerun()
    with c_sb2:
        if st.button("🚪 Logout", key="sb_btn_logout", use_container_width=True):
            tok = get_kmsi_cookie_token()
            if tok:
                revoke_kmsi_token(tok)
            st.session_state["kmsi_clear_cookie"] = True
            st.session_state["authenticated"] = False
            st.session_state["user"] = None
            clear_login_fields()
            clear_register_fields()
            st.session_state["view"] = "login"
            st.rerun()

    st.markdown("---")
    st.markdown("### 🎛️ Filtros do Relatório B3")
    st.caption("Parametrize a triagem fundamentalista em tempo real:")

    if st.button("🔄 Atualizar Dados da B3", use_container_width=True):
        st.cache_data.clear()
        st.session_state["refresh_key"] += 1
        st.rerun()

    # 1. Filtro de Setor
    all_sectors = ["Todos"] + sorted(list(ranked_df["sector"].unique()))
    selected_sector = st.selectbox("Setor de Atuação:", all_sectors, index=0)

    # 2. Filtro de Dividend Yield Mínimo
    min_dy = st.slider("Dividend Yield Mínimo (12M):", min_value=0.0, max_value=15.0, value=5.0, step=0.5, format="%.1f%%")

    # 3. Filtro de Preço Teto Bazin
    only_safe_bazin = st.checkbox("Apenas Margem Bazin Positiva (Preço < Teto)", value=False)

    # 4. Filtro de Score Mínimo
    min_score = st.slider("Score de Qualidade Mínimo:", min_value=0, max_value=100, value=50, step=5)

    st.markdown("---")
    # Opção: Conversar com a Radarzinha
    if st.button("💃 Conversar com a Radarzinha", key="sb_btn_radarzinha", use_container_width=True, help="Converse com a Radarzinha, sua mentora inteligente com voz sexy"):
        st.session_state["view"] = "radarzinha"
        st.rerun()

    # Opção: Apoie o Radar B3 (Doação)
    if st.button("❤️ Apoie o Radar B3", key="sb_btn_donation", use_container_width=True, help="Ajude a manter a plataforma gratuita e no ar!"):
        st.session_state["view"] = "donation"
        st.rerun()

    st.markdown("---")
    st.markdown("### 📌 Resumo Metodológico")
    st.markdown("""
    - **Décio Bazin**: Preço Teto = DPA Médio / 6% a.a.
    - **Benjamin Graham**: $V = \\sqrt{22.5 \\times LPA \\times VPA}$
    - **Score Multicritério**: Yield (35%), ROE (25%), Solvência (20%) e Notícias B3 (20%).
    """)

# -------------------------------------------------------------
# APLICAÇÃO DOS FILTROS NO DATASET
# -------------------------------------------------------------
filtered_df = ranked_df.copy()

if selected_sector != "Todos":
    filtered_df = filtered_df[filtered_df["sector"] == selected_sector]

filtered_df = filtered_df[filtered_df["dy_12m"] >= min_dy]
filtered_df = filtered_df[filtered_df["score"] >= min_score]

if only_safe_bazin:
    filtered_df = filtered_df[filtered_df["bazin_margin_safety"] > 0]

portfolios = get_categorized_portfolios(filtered_df)

# Linha de Cartões KPI Gerais do Mercado B3
render_kpi_header(filtered_df)
st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

# -------------------------------------------------------------
# LAYOUT CENTRAL OU DETALHES: NAVEGAÇÃO PRINCIPAL POR ABAS
# -------------------------------------------------------------
tab_portfolio, tab_alerts, tab_rankings4, tab_overview, tab_simulator, tab_radarzinha = st.tabs([
    "💼 Minha Carteira",
    "🚨 Alertas B3",
    "🏆 Grandes Rankings da B3",
    "📌 Visão Geral do Mercado",
    "💰 Simulador de Renda Passiva",
    "💃 Radarzinha AI"
])

# =============================================================
# 1. ABA MINHA CARTEIRA (POR USUÁRIO)
# =============================================================
with tab_portfolio:
    st.markdown(f"### 💼 Minha Carteira &bull; Posição de @{current_username}")
    st.caption("Gestão de patrimônio real, recálculo de preço médio, histórico de lançamentos e alertas preditivos de proventos")

    # Obter dados consolidados da carteira do usuário logado
    portfolio_summary = get_portfolio_summary(ranked_df, username=current_username)

    # 1. 📈 Minha Carteira: Desempenho (RETRÁTIL)
    with st.expander("📈 Minha Carteira: Desempenho", expanded=True):
        render_portfolio_performance_overview(portfolio_summary, username=current_username)
        st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)
        render_portfolio_kpis(portfolio_summary)

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

    # 2. 🚨 Alertas de Proventos do Mês da Carteira (RETRÁTIL)
    with st.expander("🚨 Alertas de Proventos do Mês da Carteira", expanded=True):
        col_alert_hdr, col_month_sel = st.columns([2.4, 1.2])
        with col_alert_hdr:
            st.caption("Cruzamento em tempo real da custódia com o calendário de distribuições da B3")
        with col_month_sel:
            curr_m = datetime.now().month
            month_options = list(range(1, 13))
            selected_alert_month = st.selectbox(
                "📅 Simular Mês de Pagamento:",
                options=month_options,
                index=curr_m - 1,
                format_func=lambda m: f"{MONTH_NAMES.get(m, '')} (Mês {m:02d})",
                key="portfolio_user_month_selector"
            )

        alerts_data = get_portfolio_monthly_dividend_alerts(portfolio_summary, target_month=selected_alert_month)
        render_dividend_alerts_section(alerts_data)

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

    # 3. 📊 Histórico: Dividendos (RETRÁTIL)
    with st.expander("📊 Histórico: Dividendos", expanded=True):
        render_portfolio_dividend_history_card(portfolio_summary)

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

    # 📊 Graficos (RETRÁTIL)
    with st.expander("📊 Graficos", expanded=True):
        col_pie1, col_pie2 = st.columns(2)
        with col_pie1:
            with st.expander("🥧 Gráfico 1: Investimento dos Ativos Cadastrados", expanded=True):
                st.markdown('<div class="pbi-chart-container">', unsafe_allow_html=True)
                render_pie_invested_chart(portfolio_summary)
                st.markdown('</div>', unsafe_allow_html=True)

        with col_pie2:
            with st.expander("🥧 Gráfico 2: Valor Real dos Ativos Cadastrados", expanded=True):
                st.markdown('<div class="pbi-chart-container">', unsafe_allow_html=True)
                render_pie_current_value_chart(portfolio_summary)
                st.markdown('</div>', unsafe_allow_html=True)

        with st.expander("📊 Gráfico 3: Lucro / Perda dos Ativos Cadastrados", expanded=True):
            st.markdown('<div class="pbi-chart-container">', unsafe_allow_html=True)
            render_bar_profit_loss_chart(portfolio_summary)
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

    # 4. 📋 Posição Detalhada da Carteira por Ativo (RETRÁTIL)
    with st.expander("📋 Posição Detalhada da Carteira por Ativo", expanded=True):
        render_portfolio_summary_table(portfolio_summary)

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

    # 📝 Cadastro Ativos (RETRÁTIL)
    with st.expander("📝 Cadastro Ativos", expanded=True):
        col_cad, col_hist = st.columns([1, 1.4])

        with col_cad:
            with st.expander("📝 Cadastrar / Atualizar Ativo na Carteira", expanded=True):
                all_ticker_choices = sorted([r["ticker_clean"] for r in B3_DIVIDEND_UNIVERSE])
                
                with st.form("form_cadastro_ativo_user", clear_on_submit=False):
                    cad_ticker = st.selectbox("Ação (Ticker B3)", all_ticker_choices, index=0)
                    cad_data = st.date_input("Data da Operação", value=date.today())
                    cad_qtd = st.number_input("Quantidade de Ações", min_value=1, max_value=1000000, value=100, step=10)

                    # Sugerir cotação a mercado
                    sugg_price = 25.00
                    for r in ranked_df.to_dict("records"):
                        if r.get("ticker_clean") == cad_ticker:
                            sugg_price = r.get("price", 25.00)
                            break

                    cad_preco = st.number_input("Preço Unitário Pago (R$)", min_value=0.01, max_value=10000.0, value=float(sugg_price), step=0.10, format="%.2f")
                    cad_notas = st.text_input("Observações", value="Aporte focado em proventos")

                    v_tot = cad_qtd * cad_preco
                    st.info(f"💵 **Total da Operação**: R$ {v_tot:,.2f}")

                    submit_btn = st.form_submit_button("💾 Salvar / Atualizar no Portfólio", type="primary", use_container_width=True)
                    if submit_btn:
                        add_transaction(
                            ticker=cad_ticker,
                            date_str=cad_data.strftime("%Y-%m-%d"),
                            quantity=int(cad_qtd),
                            price_per_share=float(cad_preco),
                            notes=cad_notas,
                            username=current_username
                        )
                        st.success(f"✅ Operação registrada: {cad_qtd} ações de {cad_ticker} a R$ {cad_preco:.2f}!")
                        st.rerun()

        with col_hist:
            with st.expander("📜 Histórico Completo das Atualizações & Lançamentos", expanded=True):
                transactions_list = load_transactions(current_username)
                
                if not transactions_list:
                    st.info(f"Nenhuma transação registrada para o usuário @{current_username}.")
                else:
                    hist_df = pd.DataFrame(transactions_list)
                    if "date" in hist_df.columns:
                        hist_df = hist_df.sort_values(by="date", ascending=False).reset_index(drop=True)

                    hist_display = hist_df[["id", "date", "ticker_clean", "quantity", "price_per_share", "total_invested", "notes"]].copy().rename(columns={
                        "id": "ID",
                        "date": "Data",
                        "ticker_clean": "Ação",
                        "quantity": "Quantidade",
                        "price_per_share": "Preço Pago (R$)",
                        "total_invested": "Total Investido (R$)",
                        "notes": "Notas"
                    })

                    st.dataframe(
                        hist_display.style.format({
                            "Quantidade": "{:d}",
                            "Preço Pago (R$)": "R$ {:.2f}",
                            "Total Investido (R$)": "R$ {:,.2f}"
                        }),
                        use_container_width=True,
                        height=260
                    )

                    st.markdown("##### 🗑️ Gerenciamento de Lançamentos Individuais")
                    c_del1, c_del2 = st.columns([2, 1])
                    with c_del1:
                        tx_ids = [f"{t.get('id')} - {t.get('ticker_clean')} ({t.get('date')})" for t in transactions_list]
                        selected_del = st.selectbox("Selecione o lançamento:", tx_ids, key="del_user_tx")
                    with c_del2:
                        st.write("")
                        st.write("")
                        if st.button("Excluir Lançamento", type="secondary", use_container_width=True):
                            raw_id = selected_del.split(" - ")[0]
                            if delete_transaction(raw_id, username=current_username):
                                st.success(f"Lançamento {raw_id} excluído com sucesso!")
                                st.rerun()

# =============================================================
# 2. ABA ALERTAS B3
# =============================================================
with tab_alerts:
    st.markdown("### 🚨 Central de Alertas B3 &bull; Proventos & Oportunidades de Preço Médio")
    st.caption("Diagnóstico preditivo em tempo real cruzando a custódia com preços teto de Décio Bazin e Graham")

    # 1. Alertas de Proventos do Mês da B3 (RETRÁTIL)
    with st.expander("🚨 1. Alertas de Proventos do Mês da B3", expanded=True):
        col_a_m1, col_a_m2 = st.columns([2.5, 1.2])
        with col_a_m1:
            st.caption("Monitor de fluxo de dividendos com cruzamento da quantidade em custódia e calendário da B3")
        with col_a_m2:
            curr_m = datetime.now().month
            sel_month_alerts_tab = st.selectbox(
                "Mês de Referência:",
                options=list(range(1, 13)),
                index=curr_m - 1,
                format_func=lambda m: f"{MONTH_NAMES.get(m, '')} (Mês {m:02d})",
                key="alerts_tab_month_selector"
            )

        b3_alerts = get_portfolio_monthly_dividend_alerts(portfolio_summary, target_month=sel_month_alerts_tab)
        render_dividend_alerts_section(b3_alerts)

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

    # 2. Alertas de Ações Abaixo do Valor de Compra (Preço < PM) da B3 (RETRÁTIL)
    with st.expander("🔻 2. Alertas de Ações Abaixo do Valor de Compra (Preço < PM) da B3", expanded=True):
        st.caption("Compara a cotação a mercado da B3 com o Preço Médio (PM) de compra e avalia margem de segurança de Bazin e Graham")
        dip_data = get_portfolio_dip_alerts(portfolio_summary, ranked_df)
        render_portfolio_dip_alerts(dip_data)

# =============================================================
# 3. ABA GRANDES RANKINGS DA B3 (COM DETECTOR DE AÇÕES)
# =============================================================
with tab_rankings4:
    # 🏆 Painel dos 4 Grandes Rankings da B3
    render_market_four_rankings_dashboard(filtered_df)
    st.markdown("---")

    # 🎯 DETECTOR DE AÇÕES (com valor digitado, slider de teto e periodicidade)
    render_sub_10_bargain_detector(ranked_df)

# =============================================================
# 4. ABA VISÃO GERAL DO MERCADO (COM NOTÍCIAS E RAIO-X)
# =============================================================
with tab_overview:
    sub_overview, sub_news, sub_deepdive = st.tabs([
        "📊 Panorama Geral & Agenda B3",
        "📰 Notícias Reais & Dados B3",
        "🔍 Raio-X Individual (Bazin & Graham)"
    ])

    with sub_overview:
        # Matriz de Oportunidades (DY x ROE)
        st.markdown('<div class="pbi-chart-title">🎯 Matriz de Oportunidades (DY x ROE)</div>', unsafe_allow_html=True)
        render_quadrant_scatter_chart(filtered_df)
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

        # 1. Ranking Geral de Ações de Dividendos da B3 (RETRÁTIL)
        with st.expander("📊 Ranking Geral de Ações de Dividendos da B3", expanded=True):
            render_matrix_table(filtered_df, "📊 Ranking Geral de Ações de Dividendos da B3")

        # 2. Calendário Anual de Proventos da B3 (RETRÁTIL com Agenda de dividendos inclusa)
        with st.expander("🗓️ Calendário Anual de Proventos da B3", expanded=True):
            render_monthly_calendar_grid(filtered_df.to_dict("records")[:12])
            st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

            # Agenda de dividendos de AÇÕES (RETRÁTIL com filtros DE e ATÉ e paginação)
            with st.expander("📅 Agenda de dividendos de AÇÕES", expanded=True):
                render_stock_dividend_agenda(ranked_df)

    with sub_news:
        # 4. Notícias Reais & Análise de Sentimento das Empresas da B3 (RETRÁTIL)
        with st.expander("📰 Notícias Reais & Análise de Sentimento das Empresas da B3", expanded=True):
            st.caption("Monitoramento contínuo de notícias, fatos relevantes e impacto fundamentalista sobre dividendos")

            ticker_options = [r["ticker_clean"] for r in ranked_df.to_dict("records")]
            c_n1, c_n2 = st.columns([1, 1.8])

            with c_n1:
                sel_news_ticker = st.selectbox("Selecione a empresa para análise de notícias:", ticker_options, index=0, key="news_tab_ticker")
                stk_news = ranked_df[ranked_df["ticker_clean"] == sel_news_ticker].iloc[0].to_dict()

                # Coletar notícias reais
                live_news = fetch_ticker_news(stk_news["ticker"], company_name=stk_news["name"], max_results=5)
                sentiment_res = evaluate_company_news_sentiment(live_news)

                st.markdown(textwrap.dedent(f"""
                <div class="pbi-action-card">
                    <div style="font-size:12px; color:#94A3B8; font-weight:700;">DIAGNÓSTICO DE SENTIMENTO B3</div>
                    <div style="font-size:24px; font-weight:800; color:{sentiment_res['color']}; margin: 8px 0;">
                        {sentiment_res['badge']}
                    </div>
                    <div style="font-size:13px; color:#CBD5E1; line-height:1.4;">
                        {sentiment_res['impact_on_dividends']}
                    </div>
                    <div style="margin-top:10px; font-size:12px; color:#64748B;">
                        Score de Notícias: <b>{sentiment_res['score']:+.2f}</b> (Escala -1.0 a +1.0)
                    </div>
                </div>
                """).strip(), unsafe_allow_html=True)

                st.markdown(textwrap.dedent(f"""
                <div class="pbi-action-card" style="margin-top:12px;">
                    <div style="font-size:12px; color:#94A3B8; font-weight:700;">DADOS AO VIVO &bull; {stk_news['name']}</div>
                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-top:8px;">
                        <div><span style="color:#94A3B8; font-size:11px;">Cotação:</span> <b style="color:#F8FAFC;">R$ {stk_news['price']:.2f}</b></div>
                        <div><span style="color:#94A3B8; font-size:11px;">DY 12M:</span> <b style="color:#10B981;">{stk_news['dy_12m']:.2f}%</b></div>
                        <div><span style="color:#94A3B8; font-size:11px;">Teto Bazin:</span> <b style="color:#38BDF8;">R$ {stk_news['bazin_target_price']:.2f}</b></div>
                        <div><span style="color:#94A3B8; font-size:11px;">Justo Graham:</span> <b style="color:#F59E0B;">R$ {stk_news['graham_fair_value']:.2f}</b></div>
                    </div>
                </div>
                """).strip(), unsafe_allow_html=True)

            with c_n2:
                st.markdown(f"#### 🌐 Feed de Notícias em Tempo Real - {stk_news['name']} ({sel_news_ticker})")
                render_news_feed(live_news, stock_ticker=sel_news_ticker)

    with sub_deepdive:
        st.markdown("### 🔍 Análise Fundamentalista Detalhada por Ação")
        ticker_options = [r["ticker_clean"] for r in ranked_df.to_dict("records")]
        selected_clean_ticker = st.selectbox("Selecione a ação para análise individual aprofundada:", ticker_options, index=0, key="deepdive_selector")
        stock_row = ranked_df[ranked_df["ticker_clean"] == selected_clean_ticker].iloc[0].to_dict()

        c_d1, c_d2, c_d3, c_d4 = st.columns(4)
        c_d1.metric("Cotação Atual", f"R$ {stock_row['price']:.2f}")
        c_d2.metric("Preço Teto Bazin (6%)", f"R$ {stock_row['bazin_target_price']:.2f}", delta=f"{stock_row['bazin_margin_safety']:+.1f}% de Margem")
        c_d3.metric("Valor Justo Graham", f"R$ {stock_row['graham_fair_value']:.2f}", delta=f"{stock_row['graham_margin_safety']:+.1f}% de Margem")
        c_d4.metric("Dividend Yield (12M)", f"{stock_row['dy_12m']:.2f}%", f"DPA R$ {stock_row['dpa_12m']:.2f}")

        st.markdown("---")
        col_radar, col_hist = st.columns([1, 1.2])
        with col_radar:
            st.markdown('<div class="pbi-chart-title">🎯 Radar Multicritério vs Média B3</div>', unsafe_allow_html=True)
            sector_bench = {
                "dy_12m": ranked_df["dy_12m"].mean(),
                "roe": ranked_df["roe"].mean(),
                "net_margin": ranked_df["net_margin"].mean(),
                "bazin_margin_safety": ranked_df["bazin_margin_safety"].mean(),
                "debt_ebitda": ranked_df["debt_ebitda"].mean()
            }
            render_radar_comparison_chart(stock_row, sector_bench)

        with col_hist:
            st.markdown('<div class="pbi-chart-title">📊 Histórico de Proventos Anuais</div>', unsafe_allow_html=True)
            render_dividend_history_bars(stock_row)

# =============================================================
# 5. ABA SIMULADOR DE RENDA PASSIVA
# =============================================================
with tab_simulator:
    st.markdown("### 💰 Simulador de Independência Financeira e Efeito Bola de Neve")
    sim_ticker = st.selectbox("Selecione o ativo base para a simulação:", ticker_options, index=0, key="sim_base_ticker")
    sim_stock = ranked_df[ranked_df["ticker_clean"] == sim_ticker].iloc[0].to_dict()
    render_passive_income_calculator(sim_stock)

# =============================================================
# 6. ABA RADARZINHA AI (MENTORA & CONSELHEIRA DE DIVIDENDOS)
# =============================================================
with tab_radarzinha:
    render_radarzinha_tab(ranked_df=ranked_df, current_profile=current_profile)

# -------------------------------------------------------------
# RODAPÉ INSTITUCIONAL
# -------------------------------------------------------------
st.markdown("---")
st.markdown("""
<div style="text-align: center; font-size: 12px; color: #64748B; padding: 12px 0;">
    <b>DIVIDEND RADAR B3</b> &bull; Relatório Executivo de Proventos &bull; Desenvolvido em Python &bull; Dados Públicos B3 e Feeds em Tempo Real
</div>
""", unsafe_allow_html=True)
