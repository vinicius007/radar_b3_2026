"""
Componentes Visuais de Gestão de Carteira e Gráficos Executivos Estilo Power BI.
Inclui os 7 KPIs da Carteira, Gráfico Pizza 1 (Investimento), Gráfico Pizza 2 (Valor Real),
Gráfico Barra 3 (Lucro/Perda #059669/#DC2626), Gráfico Histórico: Dividendos (#00D084) e Cadastro Multi-usuário.
"""

import textwrap
from typing import Dict, List, Any, Optional
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

from src.ui.powerbi_theme import get_plotly_theme
from src.auth.user_manager import get_user_monthly_goal, set_user_monthly_goal
from src.data.portfolio_manager import (
    load_transactions,
    add_transaction,
    delete_transaction,
    get_portfolio_summary,
    get_portfolio_dividend_history,
    MONTH_NAMES
)

def _render_perf_card(value_str: str, title_str: str, footer_str: str = "", footer_negative: bool = False) -> str:
    footer_cls = "pbi-perf-footer negative" if footer_negative else "pbi-perf-footer"
    footer_html = f'<div class="{footer_cls}">{footer_str}</div>' if footer_str else '<div style="height: 18px;"></div>'
    
    icon_svg = (
        '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" '
        'stroke="#10B981" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
        '<polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline>'
        '<polyline points="17 6 23 6 23 12"></polyline>'
        '</svg>'
    )
    
    return f"""
    <div class="pbi-perf-card">
        <div class="pbi-perf-top">
            <div class="pbi-perf-val">{value_str}</div>
            <div class="pbi-perf-icon">{icon_svg}</div>
        </div>
        <div class="pbi-perf-title">{title_str}</div>
        {footer_html}
    </div>
    """.strip()

def render_portfolio_performance_overview(summary: Dict[str, Any], username: str = "masterradar"):
    """
    Renderiza os 6 indicadores executivos da seção 'Minha Carteira: Desempenho'
    em grade 3x2:
    1. Rentabilidade Mensal
    2. Meta Mensal
    3. Meta Mensal Atingida
    4. Rentabilidade atual
    5. Patrimônio atual
    6. Proventos atual
    """
    is_empty = summary.get("is_empty", True)
    total_invested = summary.get("total_invested", 0.0)
    current_val = summary.get("total_current_value", 0.0)
    total_profit_loss_pct = summary.get("total_profit_loss_pct", 0.0)
    monthly_return_pct = summary.get("monthly_return_pct", 0.0)
    month_divs = summary.get("current_month_dividends", 0.0)
    
    # Meta Mensal do usuário
    monthly_goal = get_user_monthly_goal(username)
    
    # Header da Seção com ícone informativo e ajuste de meta
    col_hdr, col_actions = st.columns([3.8, 1.2])
    with col_hdr:
        st.markdown("""
        <div style="display:flex; align-items:center; gap:8px; margin-bottom: 6px;">
            <span style="font-size: 15px; font-weight: 600; color: #94A3B8;">Metas de Proventos & Rentabilidade do Investidor</span>
            <span title="Visão geral de rentabilidade, metas mensais e proventos atingidos na carteira" style="cursor:help; font-size:15px; color:#94A3B8;">ⓘ</span>
        </div>
        """, unsafe_allow_html=True)
    with col_actions:
        with st.popover("🎯 Meta Mensal", help="Definir ou alterar sua meta mensal de proventos (em R$)"):
            st.markdown("**Definir Meta Mensal de Proventos:**")
            new_goal = st.number_input(
                "Valor da Meta (R$):",
                min_value=0.0,
                value=float(monthly_goal),
                step=50.0,
                format="%.2f",
                key="perf_overview_monthly_goal_input"
            )
            if st.button("Salvar Meta", key="btn_save_perf_goal", type="primary", use_container_width=True):
                set_user_monthly_goal(username, new_goal)
                st.success("Meta atualizada!")
                st.rerun()

    # Formatação dos 3 indicadores restantes
    # Card 1: Meta Mensal
    val_meta = f"R$ {monthly_goal:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    # Card 2: Meta Mensal Atingida
    if is_empty or month_divs == 0.0:
        val_meta_atingida = "R$ 0,00"
    else:
        val_meta_atingida = f"R$ {month_divs:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    # Card 3: Rentabilidade atual
    if is_empty or total_profit_loss_pct == 0.0:
        val_rent_atual = "-%"
    else:
        val_rent_atual = f"{total_profit_loss_pct:+.2f}%".replace(".", ",")

    # Grade dos 3 cards executivos em linha única (3 colunas)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(_render_perf_card(
            value_str=val_meta,
            title_str="Meta Mensal",
            footer_str=""
        ), unsafe_allow_html=True)
    with c2:
        st.markdown(_render_perf_card(
            value_str=val_meta_atingida,
            title_str="Meta Mensal Atingida",
            footer_str="+ 0,00% em relação ao mês anterior"
        ), unsafe_allow_html=True)
    with c3:
        st.markdown(_render_perf_card(
            value_str=val_rent_atual,
            title_str="Rentabilidade atual",
            footer_str="+ 0,00% em relação ao mês anterior"
        ), unsafe_allow_html=True)

def render_portfolio_kpis(summary: Dict[str, Any]):
    """
    Renderiza os 7 cartões de KPI consolidados da carteira do investidor
    dentro de um expander retrátil para consulta detalhada de custos e posição:
    1. Total Investido de Compra
    2. Patrimônio Real Atual
    3. Lucro / Prejuízo Consolidado (R$ e %)
    4. Proventos Estimados Anuais & Mensais da sua Carteira
    5. Rentabilidade atual em relação ao mês anterior
    6. Total de Dividendos ganhos no mês
    7. Total de Dividendos ganhos desde a compra até hoje
    """
    with st.expander("📊 Ver Métricas Detalhadas de Custos e Posição (Custo de Aquisição, Lucro/Prejuízo em R$, etc.)", expanded=False):
        total_invested = summary.get("total_invested", 0.0)
        current_val = summary.get("total_current_value", 0.0)
        profit_loss = summary.get("total_profit_loss", 0.0)
        profit_loss_pct = summary.get("total_profit_loss_pct", 0.0)
        annual_divs = summary.get("total_annual_dividends", 0.0)
        monthly_divs = summary.get("total_monthly_dividends", 0.0)
        monthly_return_pct = summary.get("monthly_return_pct", 0.0)
        month_divs = summary.get("current_month_dividends", 0.0)
        since_purchase_divs = summary.get("total_dividends_since_purchase", 0.0)

        pl_arrow = "▲" if profit_loss >= 0 else "▼"
        pl_color = "#059669" if profit_loss >= 0 else "#DC2626"
        ret_color = "#059669" if monthly_return_pct >= 0 else "#DC2626"
        ret_arrow = "▲" if monthly_return_pct >= 0 else "▼"

        # Primeira linha: 4 KPIs principais
        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.markdown(textwrap.dedent(f"""
            <div class="pbi-kpi-card">
                <div class="pbi-kpi-label">💵 Total Investido de Compra</div>
                <div class="pbi-kpi-value">R$ {total_invested:,.2f}</div>
                <div class="pbi-kpi-sub"><span class="pbi-tag-neutral">Custo de Aquisição</span> Acumulado</div>
            </div>
            """).strip(), unsafe_allow_html=True)

        with c2:
            st.markdown(textwrap.dedent(f"""
            <div class="pbi-kpi-card">
                <div class="pbi-kpi-label">💎 Patrimônio Real Atual</div>
                <div class="pbi-kpi-value" style="color:#38BDF8;">R$ {current_val:,.2f}</div>
                <div class="pbi-kpi-sub"><span class="pbi-tag-positive">● Cotação B3 Ao Vivo</span> a Mercado</div>
            </div>
            """).strip(), unsafe_allow_html=True)

        with c3:
            st.markdown(textwrap.dedent(f"""
            <div class="pbi-kpi-card">
                <div class="pbi-kpi-label">📈 Lucro / Prejuízo Consolidado</div>
                <div class="pbi-kpi-value" style="color:{pl_color};">
                    {pl_arrow} R$ {abs(profit_loss):,.2f}
                </div>
                <div class="pbi-kpi-sub">
                    <span style="color:{pl_color}; font-weight:700;">{profit_loss_pct:+.2f}%</span> Variação de Capital
                </div>
            </div>
            """).strip(), unsafe_allow_html=True)

        with c4:
            st.markdown(textwrap.dedent(f"""
            <div class="pbi-kpi-card">
                <div class="pbi-kpi-label">💰 Proventos Estimados (Ano & Mês)</div>
                <div class="pbi-kpi-value" style="color:#10B981;">R$ {annual_divs:,.2f}</div>
                <div class="pbi-kpi-sub"><span class="pbi-tag-positive">~ R$ {monthly_divs:,.2f}/mês</span> em Proventos</div>
            </div>
            """).strip(), unsafe_allow_html=True)

        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

        # Segunda linha: 3 KPIs complementares de proventos e rentabilidade
        c5, c6, c7 = st.columns(3)

        with c5:
            st.markdown(textwrap.dedent(f"""
            <div class="pbi-kpi-card">
                <div class="pbi-kpi-label">📊 Rentabilidade vs Mês Anterior</div>
                <div class="pbi-kpi-value" style="color:{ret_color};">
                    {ret_arrow} {monthly_return_pct:+.2f}%
                </div>
                <div class="pbi-kpi-sub"><span class="pbi-tag-neutral">Desempenho Relativo</span> Últimos 30 Dias</div>
            </div>
            """).strip(), unsafe_allow_html=True)

        with c6:
            st.markdown(textwrap.dedent(f"""
            <div class="pbi-kpi-card">
                <div class="pbi-kpi-label">🗓️ Total Dividendos Ganhos no Mês</div>
                <div class="pbi-kpi-value" style="color:#00D084;">R$ {month_divs:,.2f}</div>
                <div class="pbi-kpi-sub"><span class="pbi-tag-positive">Crédito Previsto em Conta</span> Mês Corrente</div>
            </div>
            """).strip(), unsafe_allow_html=True)

        with c7:
            st.markdown(textwrap.dedent(f"""
            <div class="pbi-kpi-card">
                <div class="pbi-kpi-label">🏆 Proventos Acumulados Desde Compra</div>
                <div class="pbi-kpi-value" style="color:#F59E0B;">R$ {since_purchase_divs:,.2f}</div>
                <div class="pbi-kpi-sub"><span class="pbi-tag-neutral">Efeito Bola de Neve</span> Total Recebido</div>
            </div>
            """).strip(), unsafe_allow_html=True)


def render_pie_invested_chart(summary: Dict[str, Any]):
    """
    🥧 Gráfico 1: Investimento dos Ativos Cadastrados (Formato Pizza / Donut):
    Distribuição percentual e em R$ por ação com base no Custo de Aquisição (Preço de Compra).
    Exibição destacada do Total do Valor Investido.
    """
    assets_df = summary.get("assets_df", pd.DataFrame())
    total_invested = summary.get("total_invested", 0.0)

    if assets_df.empty:
        st.info("Nenhum ativo cadastrado para gerar o gráfico de investimento.")
        return

    fig = go.Figure(data=[go.Pie(
        labels=assets_df["ticker_clean"],
        values=assets_df["total_invested"],
        hole=0.60,
        textinfo="label+percent",
        hovertemplate="<b>%{label}</b><br>Valor Investido: R$ %{value:,.2f}<br>Participação: %{percent}<extra></extra>",
        marker=dict(
            colors=["#F59E0B", "#38BDF8", "#10B981", "#818CF8", "#F43F5E", "#EC4899", "#A855F7", "#06B6D4", "#EAB308"],
            line=dict(color="#1E293B", width=2)
        )
    )])

    fig.update_layout(
        title={
            "text": "🥧 1. Investimento por Ativo (Custo de Compra)",
            "font": {"size": 15, "color": "#F8FAFC", "family": "Inter, Segoe UI, sans-serif"}
        },
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94A3B8", size=11),
        margin=dict(l=20, r=20, t=50, b=20),
        height=320,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        annotations=[{
            "text": f"<b>Total Investido</b><br><span style='color:#F59E0B; font-size:16px;'>R$ {total_invested:,.2f}</span>",
            "x": 0.5, "y": 0.5,
            "font": {"size": 12, "color": "#F8FAFC"},
            "showarrow": False
        }]
    )

    st.plotly_chart(fig, use_container_width=True)

def render_pie_current_value_chart(summary: Dict[str, Any]):
    """
    🥧 Gráfico 2: Valor Real dos Ativos Cadastrados (Formato Pizza / Donut):
    Distribuição por ação com base na Cotação Real Atualizada da B3.
    Exibição destacada do Patrimônio Total Real Atualizado.
    """
    assets_df = summary.get("assets_df", pd.DataFrame())
    total_current = summary.get("total_current_value", 0.0)

    if assets_df.empty:
        st.info("Nenhum ativo cadastrado para gerar o gráfico de valor a mercado.")
        return

    fig = go.Figure(data=[go.Pie(
        labels=assets_df["ticker_clean"],
        values=assets_df["current_value"],
        hole=0.60,
        textinfo="label+percent",
        hovertemplate="<b>%{label}</b><br>Valor a Mercado: R$ %{value:,.2f}<br>Participação: %{percent}<extra></extra>",
        marker=dict(
            colors=["#38BDF8", "#10B981", "#F59E0B", "#818CF8", "#06B6D4", "#F43F5E", "#A855F7", "#EAB308", "#14B8A6"],
            line=dict(color="#1E293B", width=2)
        )
    )])

    fig.update_layout(
        title={
            "text": "🥧 2. Valor Real dos Ativos (Cotação B3)",
            "font": {"size": 15, "color": "#F8FAFC", "family": "Inter, Segoe UI, sans-serif"}
        },
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94A3B8", size=11),
        margin=dict(l=20, r=20, t=50, b=20),
        height=320,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        annotations=[{
            "text": f"<b>Patrimônio Real</b><br><span style='color:#38BDF8; font-size:16px;'>R$ {total_current:,.2f}</span>",
            "x": 0.5, "y": 0.5,
            "font": {"size": 12, "color": "#F8FAFC"},
            "showarrow": False
        }]
    )

    st.plotly_chart(fig, use_container_width=True)

def render_bar_profit_loss_chart(summary: Dict[str, Any]):
    """
    📊 Gráfico 3: Lucro / Perda dos Ativos Cadastrados (Formato Barra Vertical):
    Variação em R$ e Rentabilidade (%) por ação.
    Cores condicionais automáticas: Verde (#059669) para Lucro e Vermelho (#DC2626) para Prejuízo.
    Exibição do resultado total consolidado da carteira no cabeçalho do gráfico.
    """
    assets_df = summary.get("assets_df", pd.DataFrame())
    total_pl = summary.get("total_profit_loss", 0.0)
    total_pl_pct = summary.get("total_profit_loss_pct", 0.0)

    if assets_df.empty:
        st.info("Nenhum ativo cadastrado para gerar o gráfico de lucro e prejuízo.")
        return

    df_sorted = assets_df.sort_values(by="profit_loss", ascending=False).reset_index(drop=True)

    # Cores condicionais: Verde (#059669) e Vermelho (#DC2626)
    colors = ["#059669" if pl >= 0 else "#DC2626" for pl in df_sorted["profit_loss"]]

    # Texto das barras: R$ e %
    texts = [
        f"{'+' if pl >= 0 else ''}R$ {pl:,.2f}<br>({pct:+.1f}%)"
        for pl, pct in zip(df_sorted["profit_loss"], df_sorted["profit_loss_pct"])
    ]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df_sorted["ticker_clean"],
        y=df_sorted["profit_loss"],
        marker=dict(
            color=colors,
            line=dict(color=colors, width=1),
            cornerradius=6
        ),
        text=texts,
        textposition="outside",
        textfont=dict(size=11, color="#F8FAFC", family="Inter, Segoe UI, sans-serif"),
        hovertemplate="<b>%{x}</b><br>Resultado: R$ %{y:,.2f}<extra></extra>"
    ))

    # Linha zero
    fig.add_hline(y=0, line_color="#64748B", line_width=1.5)

    header_status = f"Resultado Consolidado: {'+' if total_pl >= 0 else ''}R$ {total_pl:,.2f} ({total_pl_pct:+.2f}%)"
    header_color = "#059669" if total_pl >= 0 else "#DC2626"

    max_y = max(abs(df_sorted["profit_loss"].max()), abs(df_sorted["profit_loss"].min()), 100.0)

    fig.update_layout(
        title={
            "text": f"📊 3. Lucro / Perda por Ativo &bull; <span style='color:{header_color};'>{header_status}</span>",
            "font": {"size": 15, "color": "#F8FAFC", "family": "Inter, Segoe UI, sans-serif"}
        },
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94A3B8", size=11),
        margin=dict(l=30, r=20, t=50, b=30),
        height=340,
        showlegend=False,
        xaxis=dict(
            showgrid=False,
            tickfont=dict(size=12, color="#CBD5E1", weight="bold"),
            linecolor="#334155"
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#334155",
            tickfont=dict(size=11, color="#94A3B8"),
            range=[-max_y * 1.35, max_y * 1.35]
        )
    )

    st.plotly_chart(fig, use_container_width=True)

def render_portfolio_dividend_history_card(portfolio_summary: Dict[str, Any]):
    """
    Renderiza o componente executivo 'Histórico: Dividendos' exatamente conforme especificação:
    - Título corporativo: 📊 Histórico: Dividendos com seletor (6 Meses, 12 Meses, Ano Atual) e ajuste de Meta.
    - Barras verticais verde esmeralda (#00D084) com cantos arredondados.
    - Valores monetários formatados no topo de cada barra no padrão brasileiro (56,33, 307,23, etc.).
    - Linha sutil de referência para a Meta Mensal configurada.
    - Rodapé: Legenda 🟩 Ações e ⬜ Meta 2.000, Métricas Média e Total, Nota de rodapé.
    - Expansor com breakdown dos ativos mês a mês.
    """
    col_hdr_title, col_hdr_ctrl = st.columns([2.0, 1.4])
    with col_hdr_title:
        st.markdown(textwrap.dedent("""
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 2px;">
            <span style="font-size: 20px; font-weight: 800; color: #F8FAFC; letter-spacing: -0.3px;">📊 Histórico: Dividendos</span>
            <span style="color: #00D084; font-size: 18px; font-weight: 800;">&rsaquo;</span>
        </div>
        <div style="font-size: 12px; color: #94A3B8; margin-bottom: 8px;">
            Evolução mensal dos proventos recebidos na carteira com comparativo de meta
        </div>
        """).strip(), unsafe_allow_html=True)
    with col_hdr_ctrl:
        c_period, c_goal = st.columns([1.1, 1.1])
        with c_period:
            period_choice = st.selectbox("Período:", ["6 Meses", "12 Meses", "Ano Atual (YTD)"], index=0, key="hist_div_period")
        with c_goal:
            meta_input = st.number_input("Meta (R$):", min_value=100.0, max_value=100000.0, value=2000.0, step=250.0, format="%.0f", key="hist_div_goal")

    p_type = "6m" if period_choice == "6 Meses" else ("12m" if period_choice == "12 Meses" else "ytd")
    history_data = get_portfolio_dividend_history(portfolio_summary, period_type=p_type, meta_goal=float(meta_input))

    month_codes = history_data.get("month_codes", [])
    values = history_data.get("values", [])
    total_val = history_data.get("total_period", 0.0)
    avg_val = history_data.get("avg_monthly", 0.0)
    meta_goal_str = history_data.get("meta_goal_str", "2.000")
    meta_val = history_data.get("meta_goal", 2000.0)

    total_formatted = f"{total_val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    avg_formatted = f"{avg_val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    max_val = max(values) if values and max(values) > 0 else 100.0
    bar_texts = [f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") if v > 0 else "0,00" for v in values]

    fig = go.Figure()

    # Barras verticais verde esmeralda (#00D084) com cantos arredondados
    fig.add_trace(go.Bar(
        x=month_codes,
        y=values,
        name="Ações",
        marker=dict(
            color="#00D084",
            line=dict(color="#00D084", width=1),
            cornerradius=5
        ),
        text=bar_texts,
        textposition="outside",
        textfont=dict(size=13, color="#F8FAFC", family="Inter, Segoe UI, sans-serif"),
        hovertemplate="<b>%{x}</b><br>Proventos: R$ %{y:,.2f}<extra></extra>"
    ))

    # Linha sutil de referência para a Meta Mensal
    if meta_val <= max_val * 1.6:
        fig.add_hline(
            y=meta_val,
            line_dash="dot",
            line_color="#64748B",
            line_width=1.5,
            annotation_text=f"Meta {meta_goal_str}",
            annotation_position="top right",
            annotation_font=dict(size=10, color="#94A3B8")
        )

    y_upper = max(max_val * 1.25, 100.0)

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94A3B8", size=12, family="Inter, Segoe UI, sans-serif"),
        margin=dict(l=35, r=20, t=35, b=15),
        height=320,
        showlegend=False,
        xaxis=dict(
            showgrid=False,
            tickfont=dict(size=12, color="#CBD5E1", weight="bold"),
            linecolor="#334155",
            showline=True
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#334155",
            gridwidth=1,
            tickfont=dict(size=11, color="#94A3B8"),
            zeroline=True,
            zerolinecolor="#475569",
            range=[0, y_upper]
        )
    )

    st.markdown('<div class="pbi-chart-container" style="padding: 16px 20px; border-radius: 12px; margin-bottom: 16px;">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)

    # Rodapé Informativo estruturado
    bottom_footer_html = f"""
    <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-top: 4px; padding-top: 12px; border-top: 1px solid #1E293B; flex-wrap: wrap; gap: 12px;">
        <div style="display: flex; align-items: center; gap: 16px;">
            <div style="display: flex; align-items: center; gap: 6px;">
                <span style="display: inline-block; width: 14px; height: 14px; background: #00D084; border-radius: 3px;"></span>
                <span style="font-size: 13px; color: #CBD5E1; font-weight: 600;">Ações</span>
            </div>
            <div style="display: flex; align-items: center; gap: 6px;">
                <span style="display: inline-block; width: 14px; height: 14px; background: #64748B; border-radius: 3px;"></span>
                <span style="font-size: 13px; color: #CBD5E1; font-weight: 600;">Meta {meta_goal_str}</span>
            </div>
        </div>
        <div style="display: flex; align-items: center; gap: 20px;">
            <div style="font-size: 13px; color: #94A3B8;">
                Média {period_choice}: <b style="color: #F8FAFC; font-size: 14px;">R$ {avg_formatted}</b>
            </div>
            <div style="font-size: 13px; color: #94A3B8;">
                Total no período: <b style="color: #00D084; font-size: 15px;">R$ {total_formatted}</b> ℹ️
            </div>
        </div>
    </div>
    <div style="font-size: 11px; color: #64748B; margin-top: 8px; font-style: italic;">
        * Histórico de pagamentos de proventos em R$.
    </div>
    """
    st.markdown(textwrap.dedent(bottom_footer_html).strip(), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Detalhamento Interativo mês a mês
    with st.expander("🔍 Detalhamento Interativo Mês a Mês"):
        months_data = history_data.get("months_data", [])
        if not months_data:
            st.info("Sem dados detalhados para exibir no momento.")
        else:
            rows = []
            for m in months_data:
                rows.append({
                    "Mês": m["month_full"],
                    "Código": m["month_code"],
                    "Total Recebido (R$)": m["value"],
                    "Ativos Pagadores": ", ".join([b["ticker"] for b in m["breakdown"]]) if m["breakdown"] else "Sem distribuições"
                })
            df_det = pd.DataFrame(rows)
            st.dataframe(
                df_det.style.format({"Total Recebido (R$)": "R$ {:.2f}"}),
                use_container_width=True
            )

def render_portfolio_summary_table(summary: Dict[str, Any]):
    """Renderiza a tabela analítica da posição consolidada em custódia."""
    assets_df = summary.get("assets_df", pd.DataFrame())
    if assets_df.empty:
        return

    st.markdown('<div class="pbi-chart-title">📋 Posição Detalhada da Carteira por Ativo</div>', unsafe_allow_html=True)

    display_df = assets_df[[
        "ticker_clean", "name", "sector", "quantity", 
        "avg_price", "current_price", "total_invested", "current_value", 
        "profit_loss", "profit_loss_pct", "dy_12m", "estimated_annual_dividends"
    ]].copy().rename(columns={
        "ticker_clean": "Ticker",
        "name": "Empresa",
        "sector": "Setor",
        "quantity": "Qtd",
        "avg_price": "Preço Médio (R$)",
        "current_price": "Cotação B3 (R$)",
        "total_invested": "Total Investido (R$)",
        "current_value": "Patrimônio Atual (R$)",
        "profit_loss": "Lucro/Prej. (R$)",
        "profit_loss_pct": "Rentab. (%)",
        "dy_12m": "DY (12M %)",
        "estimated_annual_dividends": "Proventos Estim. (Ano)"
    })

    st.dataframe(
        display_df.style.format({
            "Qtd": "{:d}",
            "Preço Médio (R$)": "R$ {:.2f}",
            "Cotação B3 (R$)": "R$ {:.2f}",
            "Total Investido (R$)": "R$ {:,.2f}",
            "Patrimônio Atual (R$)": "R$ {:,.2f}",
            "Lucro/Prej. (R$)": "R$ {:+,.2f}",
            "Rentab. (%)": "{:+.2f}%",
            "DY (12M %)": "{:.2f}%",
            "Proventos Estim. (Ano)": "R$ {:,.2f}"
        }),
        use_container_width=True,
        height=320
    )

def render_dividend_alerts_section(alerts_data: Dict[str, Any]):
    """Renderiza a seção de alertas preditivos de proventos do mês corrente ou simulado."""
    has_alerts = alerts_data.get("has_alerts", False)
    month_name = alerts_data.get("month_name", "")
    total_month = alerts_data.get("total_month_payout", 0.0)
    paying_stocks = alerts_data.get("paying_stocks", [])
    stocks_count = alerts_data.get("stocks_count", 0)
    next_month_name = alerts_data.get("next_month_name", "")
    next_stocks = alerts_data.get("next_paying_stocks", [])

    if has_alerts:
        banner_html = f"""
        <div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(30, 41, 59, 0.95) 100%); border: 2px solid #10B981; border-radius: 12px; padding: 18px 22px; margin-bottom: 18px; box-shadow: 0 4px 20px rgba(16, 185, 129, 0.25);">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                <div>
                    <span style="background: rgba(16, 185, 129, 0.25); color: #34D399; border: 1px solid #10B981; padding: 3px 10px; border-radius: 14px; font-size: 11px; font-weight: 700; letter-spacing: 0.5px;">
                        🚨 ALERTA ATIVO &bull; PAGAMENTOS PREVISTOS
                    </span>
                    <div style="font-size: 22px; font-weight: 800; color: #F8FAFC; margin-top: 8px;">
                        💰 R$ {total_month:,.2f} em Proventos Estimados para {month_name}!
                    </div>
                    <div style="font-size: 13px; color: #CBD5E1; margin-top: 3px;">
                        Cruzamento de <b>{stocks_count} {'ações pagadoras' if stocks_count > 1 else 'ação pagadora'}</b> em custódia com o calendário de distribuições da B3.
                    </div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 12px; color: #94A3B8; text-transform: uppercase; font-weight: 700;">Radar do Próximo Mês ({next_month_name})</div>
                    <div style="font-size: 18px; font-weight: 800; color: #38BDF8; margin-top: 4px;">
                        {len(next_stocks)} {'ações no radar' if len(next_stocks) != 1 else 'ação no radar'}
                    </div>
                </div>
            </div>
        </div>
        """
        st.markdown(textwrap.dedent(banner_html).strip(), unsafe_allow_html=True)

        cols = st.columns(min(3, max(1, len(paying_stocks))))
        for idx, stock in enumerate(paying_stocks):
            col_idx = idx % len(cols)
            with cols[col_idx]:
                stock_card_html = f"""
                <div class="pbi-action-card" style="border-left: 4px solid #10B981;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span class="pbi-action-ticker">{stock['ticker_clean']}</span>
                            <span class="pbi-action-name">{stock['name']}</span>
                        </div>
                        <span style="background:rgba(16, 185, 129, 0.15); color:#10B981; border:1px solid #10B981; padding:2px 8px; border-radius:4px; font-size:11px; font-weight:700;">
                            {stock['frequency_label']}
                        </span>
                    </div>
                    <div style="display:flex; justify-content:space-between; margin-top:10px; padding:8px; background:#0F172A; border-radius:6px;">
                        <div>
                            <div style="font-size:11px; color:#94A3B8;">Posição em Custódia</div>
                            <div style="font-size:14px; font-weight:700; color:#F8FAFC;">{stock['quantity']} ações</div>
                        </div>
                        <div>
                            <div style="font-size:11px; color:#94A3B8;">DPA Estimado/Ação</div>
                            <div style="font-size:14px; font-weight:700; color:#F8FAFC;">R$ {stock['dpa_distribution']:.2f}</div>
                        </div>
                    </div>
                    <div style="margin-top:10px; display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-size:12px; color:#94A3B8;">Total a Receber:</span>
                        <span style="font-size:18px; font-weight:800; color:#10B981;">R$ {stock['payout_val']:,.2f}</span>
                    </div>
                </div>
                """
                st.markdown(textwrap.dedent(stock_card_html).strip(), unsafe_allow_html=True)
    else:
        st.info(f"Nenhum ativo da sua carteira possui distribuição regular prevista para o mês de **{month_name}**.")

def render_portfolio_dip_alerts(dip_data: Dict[str, Any]):
    """Renderiza alertas de ativos abaixo do Preço Médio (Preço < PM)."""
    has_dips = dip_data.get("has_dip_alerts", False)
    dip_count = dip_data.get("dip_count", 0)
    dip_stocks = dip_data.get("dip_stocks", [])
    total_unrealized_loss = dip_data.get("total_unrealized_loss", 0.0)

    if not has_dips:
        st.markdown(textwrap.dedent("""
        <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid #10B981; border-radius: 10px; padding: 14px 18px; margin-bottom: 16px;">
            <span style="color: #10B981; font-weight: 700; font-size: 14px;">
                🎉 Excelente Postura de Carteira!
            </span>
            <div style="color: #CBD5E1; font-size: 13px; margin-top: 4px;">
                Todos os ativos em custódia estão sendo negociados <b>acima ou no mesmo nível</b> do seu Preço Médio de compra!
            </div>
        </div>
        """).strip(), unsafe_allow_html=True)
        return

    st.markdown(textwrap.dedent(f"""
    <div style="background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(30, 41, 59, 0.95) 100%); border: 2px solid #EF4444; border-radius: 12px; padding: 18px 22px; margin-bottom: 18px; box-shadow: 0 4px 16px rgba(239, 68, 68, 0.15);">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
            <div>
                <span style="background: rgba(239, 68, 68, 0.25); color: #FCA5A5; border: 1px solid #EF4444; padding: 3px 10px; border-radius: 14px; font-size: 11px; font-weight: 700; letter-spacing: 0.5px;">
                    🔻 ALERTA DE PREÇO MÉDIO &bull; OPORTUNIDADE / RISCO
                </span>
                <div style="font-size: 20px; font-weight: 800; color: #F8FAFC; margin-top: 8px;">
                    ⚠️ {dip_count} {f"Ações Abaixo" if dip_count > 1 else "Ação Abaixo"} do seu Preço Médio de Compra
                </div>
                <div style="font-size: 13px; color: #CBD5E1; margin-top: 3px;">
                    Ativos com desconto nominal. Analise Preço Teto Bazin e Preço Justo Graham para decidir novos aportes.
                </div>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 12px; color: #94A3B8; text-transform: uppercase; font-weight: 700;">Desconto Total Acumulado</div>
                <div style="font-size: 28px; font-weight: 800; color: #EF4444; letter-spacing: -0.5px;">
                    - R$ {total_unrealized_loss:,.2f}
                </div>
            </div>
        </div>
    </div>
    """).strip(), unsafe_allow_html=True)

    cols = st.columns(min(3, max(1, len(dip_stocks))))
    for idx, s in enumerate(dip_stocks):
        col_idx = idx % len(cols)
        with cols[col_idx]:
            card_html = f"""
            <div class="pbi-action-card" style="border-left: 4px solid #EF4444;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <div>
                        <span class="pbi-action-ticker">{s['ticker_clean']}</span>
                        <span class="pbi-action-name">{s['name']}</span>
                    </div>
                    <span style="background: rgba(239, 68, 68, 0.2); color: #EF4444; border: 1px solid #EF4444; padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: 800;">
                        {s['diff_pct']:+.2f}%
                    </span>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin: 10px 0; padding: 10px; background: #0F172A; border-radius: 6px;">
                    <div>
                        <div style="font-size: 11px; color: #94A3B8;">Preço Médio Pago</div>
                        <div style="font-size: 15px; font-weight: 700; color: #F8FAFC;">R$ {s['avg_price']:.2f}</div>
                    </div>
                    <div>
                        <div style="font-size: 11px; color: #94A3B8;">Cotação Atual B3</div>
                        <div style="font-size: 15px; font-weight: 700; color: #EF4444;">R$ {s['current_price']:.2f}</div>
                    </div>
                    <div>
                        <div style="font-size: 11px; color: #94A3B8;">Diferença / Ação</div>
                        <div style="font-size: 13px; font-weight: 600; color: #FCA5A5;">- R$ {s['diff_nominal']:.2f}</div>
                    </div>
                    <div>
                        <div style="font-size: 11px; color: #94A3B8;">Teto Bazin (6%)</div>
                        <div style="font-size: 13px; font-weight: 600; color: #10B981;">R$ {s['bazin_target_price']:.2f}</div>
                    </div>
                </div>
                <div style="background: rgba(56, 189, 248, 0.1); border: 1px dashed {s['badge_color']}; border-radius: 6px; padding: 8px 10px; margin-top: 8px;">
                    <div style="font-size: 12px; font-weight: 700; color: {s['badge_color']};">
                        {s['action_badge']}
                    </div>
                    <div style="font-size: 11px; color: #CBD5E1; margin-top: 3px; line-height: 1.3;">
                        {s['action_tip']}
                    </div>
                </div>
            </div>
            """
            st.markdown(textwrap.dedent(card_html).strip(), unsafe_allow_html=True)
