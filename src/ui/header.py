"""
Componente de Layout TOPO Oficial do DIVIDEND RADAR B3.
Exibe a Logotipo Opção 4, Título e Subtítulo institucionais,
e no topo direito substitui os botões soltos por um Menu Retrátil acionado
ao clicar no ícone do usuário com:
- Minhas informações
- Alterar senha
- Ajuda
- Modo Escuro (alternância liga/desliga)
- Sair da conta
"""

import os
import base64
import textwrap
from datetime import datetime
import streamlit as st

try:
    from src.ui.auth_views import clear_login_fields, clear_register_fields, get_kmsi_cookie_token
except ImportError:
    from src.ui.auth_views import clear_login_fields, clear_register_fields
    def get_kmsi_cookie_token():
        try:
            return st.context.cookies.get("b3_kmsi_token")
        except Exception:
            return None

from src.auth.user_manager import revoke_kmsi_token

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOGO_PATH = os.path.join(BASE_DIR, "assets", "logo_opcao4_clean.png")

@st.cache_data
def get_logo_base64() -> str:
    """Carrega o logotipo opção 4 como base64."""
    if os.path.exists(LOGO_PATH):
        with open(LOGO_PATH, "rb") as f:
            return base64.b64encode(f.read()).decode("ascii")
    return ""

def render_top_header(authenticated: bool, user_profile: dict, dark_mode: bool = True):
    """Renderiza o cabeçalho executivo institucional com menu retrátil no topo direito."""
    logo_b64 = get_logo_base64()
    logo_img_tag = f'<img class="pbi-logo-img" src="data:image/png;base64,{logo_b64}" alt="Radar B3 - Opção 4">' if logo_b64 else '<span style="font-size:36px;">📈</span>'

    # Seção Esquerda e Central: Logo Opção 4 + Título + Subtítulo
    col_left, col_right = st.columns([2.8, 1.2])

    with col_left:
        st.markdown(textwrap.dedent(f"""
        <div style="display: flex; align-items: center; gap: 18px;">
            <div>
                {logo_img_tag}
            </div>
            <div>
                <div class="pbi-header-title">
                    DIVIDEND RADAR B3 | RELATÓRIO EXECUTIVO DE PROVENTOS
                </div>
                <div class="pbi-header-subtitle">
                    Gestão de Carteira Real, Recomendação de Ações, Valuation (Bazin & Graham), Notícias e Frequência de Distribuição
                </div>
            </div>
        </div>
        """).strip(), unsafe_allow_html=True)

    with col_right:
        if not authenticated:
            # TOPO lado direito: (ao sair / deslogado)
            # Estilos embutidos com alta prioridade idênticos à imagem enviada
            st.markdown("""
            <style>
            .st-key-top_btn_cadastre_se button,
            div.st-key-top_btn_cadastre_se > button,
            div[data-testid="stButton"].st-key-top_btn_cadastre_se button {
                background: #D83A14 !important;
                background-color: #D83A14 !important;
                color: #FFFFFF !important;
                font-weight: 800 !important;
                font-size: 13.5px !important;
                letter-spacing: 0.5px !important;
                text-transform: uppercase !important;
                border: 1px solid #E64A19 !important;
                border-radius: 6px !important;
                padding: 7px 16px !important;
                box-shadow: 0 2px 8px rgba(216, 58, 20, 0.4) !important;
                transition: all 0.2s ease !important;
            }
            .st-key-top_btn_cadastre_se button p,
            div.st-key-top_btn_cadastre_se button * {
                color: #FFFFFF !important;
                font-weight: 800 !important;
                font-size: 13.5px !important;
            }
            .st-key-top_btn_cadastre_se button:hover {
                background: #BF2D0B !important;
                background-color: #BF2D0B !important;
                transform: translateY(-1px) !important;
                box-shadow: 0 4px 12px rgba(216, 58, 20, 0.6) !important;
            }

            .st-key-top_btn_entrar button,
            div.st-key-top_btn_entrar > button,
            div[data-testid="stButton"].st-key-top_btn_entrar button {
                background: #0D4E56 !important;
                background-color: #0D4E56 !important;
                color: #FFFFFF !important;
                font-weight: 800 !important;
                font-size: 13.5px !important;
                letter-spacing: 0.5px !important;
                text-transform: uppercase !important;
                border: 2px solid #00C49F !important;
                border-radius: 6px !important;
                padding: 6px 16px !important;
                box-shadow: 0 2px 8px rgba(0, 196, 159, 0.3) !important;
                transition: all 0.2s ease !important;
            }
            .st-key-top_btn_entrar button p,
            div.st-key-top_btn_entrar button * {
                color: #FFFFFF !important;
                font-weight: 800 !important;
                font-size: 13.5px !important;
            }
            .st-key-top_btn_entrar button:hover {
                background: #11606A !important;
                background-color: #11606A !important;
                border-color: #2DD4BF !important;
                transform: translateY(-1px) !important;
                box-shadow: 0 4px 12px rgba(45, 212, 191, 0.5) !important;
            }
            </style>
            """, unsafe_allow_html=True)

            c_auth1, c_auth2 = st.columns([1.2, 1.0])
            with c_auth1:
                if st.button("CADASTRE-SE", key="top_btn_cadastre_se", use_container_width=True):
                    clear_register_fields()
                    st.session_state["view"] = "register"
                    st.rerun()
            with c_auth2:
                if st.button("ENTRAR", key="top_btn_entrar", use_container_width=True):
                    clear_login_fields()
                    st.session_state["view"] = "login"
                    st.rerun()
        else:
            # TOPO lado direito: (apos logar)
            # Menu Retrátil acionado pelo ícone do usuário
            u_login = user_profile.get("usuario", "masterradar")
            u_email = user_profile.get("email", "viniciusamarques2026@gmail.com")
            u_letter = user_profile.get("avatar_letter", "V")

            st.write("")  # alinhamento vertical sutil
            
            with st.popover(f"👤 {u_login} ({u_letter}) ▾", help="Clique no ícone do usuário para abrir o menu retrátil", use_container_width=True):
                st.markdown(textwrap.dedent(f"""
                <div style="padding: 6px 0 12px 0; border-bottom: 1px solid #334155; margin-bottom: 10px;">
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <div class="pbi-avatar-circle" style="width: 38px; height: 38px; font-size: 16px;">{u_letter}</div>
                        <div style="line-height: 1.2;">
                            <div style="font-size: 13.5px; font-weight: 800; color: #38BDF8;">{u_login} <span style="font-size: 10.5px; color: #10B981; font-weight: 600;">(logado)</span></div>
                            <div style="font-size: 11px; color: #94A3B8;">{u_email}</div>
                        </div>
                    </div>
                </div>
                """).strip(), unsafe_allow_html=True)

                if st.button("🏠 Home", key="pop_btn_home", use_container_width=True, help="Voltar à Página Principal"):
                    st.session_state["view"] = "dashboard"
                    st.rerun()

                if st.button("👤 Perfil", key="pop_btn_perfil", use_container_width=True, help="Acessar Perfil do Usuário"):
                    st.session_state["view"] = "profile"
                    st.rerun()

                if st.button("📋 Minhas informações", key="pop_btn_info", use_container_width=True):
                    st.session_state["view"] = "profile"
                    st.rerun()

                if st.button("🔑 Alterar senha", key="pop_btn_pwd", use_container_width=True):
                    st.session_state["view"] = "change_password"
                    st.rerun()

                if st.button("❓ Ajuda", key="pop_btn_help", use_container_width=True):
                    st.session_state["view"] = "help"
                    st.rerun()

                st.markdown("<hr style='margin: 8px 0; border: 0; border-top: 1px solid #334155;'>", unsafe_allow_html=True)

                # Modo Escuro (alternância liga/desliga)
                is_dark = st.toggle(
                    "Modo Escuro (alternância liga/desliga)",
                    value=dark_mode,
                    key="pop_toggle_dark_mode",
                    help="Ativar ou desativar o Modo Escuro"
                )
                if is_dark != dark_mode:
                    st.session_state["dark_mode"] = is_dark
                    st.rerun()

                st.markdown("<hr style='margin: 8px 0; border: 0; border-top: 1px solid #334155;'>", unsafe_allow_html=True)

                if st.button("🚪 Sair da conta", key="pop_btn_logout", type="secondary", use_container_width=True):
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

    st.markdown("<hr style='margin: 12px 0 16px 0; border: 0; border-top: 1px solid #334155;'>", unsafe_allow_html=True)
