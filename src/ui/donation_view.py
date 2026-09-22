"""
Página de Doação e Apoio ao Projeto - Radar B3.
Apresenta as informações para contribuição comunitária via PIX (Chave, QR Code e Copia e Cola),
com visual executivo Power BI Dark Slate e navegação de retorno.
"""

import os
import textwrap
import streamlit as st
from PIL import Image

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
QR_CODE_PATH = os.path.join(BASE_DIR, "assets", "pix_qrcode.png")

PIX_KEY = "(62) 99930-8633"
PIX_RECEIVER = "VINICIUS AUGUSTO MARQUES"
PIX_COPY_PASTE = "00020126710014BR.GOV.BCB.PIX0114+55629993086330231Ajudando a continuidade do site5204000053039865802BR5924VINICIUS AUGUSTO MARQUES6009SAO PAULO6226052279ZshPqrzBFOYSWAL1iZmY630451FA"

def render_donation_view():
    """Renderiza a página completa de Apoio e Doação ao Radar B3."""
    # Botão de retorno superior
    col_back, _ = st.columns([1.2, 3.8])
    with col_back:
        if st.button("← 🏠 Voltar à Plataforma", key="donation_btn_back_top", use_container_width=True):
            st.session_state["view"] = "dashboard"
            st.rerun()

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    # Cabeçalho Principal com letras maiores conforme solicitado
    st.markdown(textwrap.dedent("""
    <div class="pbi-auth-card" style="text-align: center; padding: 32px 24px 28px 24px; border-top: 4px solid #F43F5E; margin-bottom: 24px;">
        <div style="font-size: 38px; font-weight: 900; color: #F43F5E; letter-spacing: -0.5px; line-height: 1.2;">
            ❤️ Apoie o Radar B3
        </div>
        <div style="font-size: 19px; font-weight: 600; color: #38BDF8; margin-top: 8px;">
            Seu apoio mantém este projeto vivo
        </div>
    </div>
    """).strip(), unsafe_allow_html=True)

    # Mensagem de Apresentação
    st.markdown(textwrap.dedent("""
    <div class="pbi-auth-card" style="padding: 24px; margin-bottom: 24px; border-left: 4px solid #38BDF8;">
        <div style="font-size: 18px; font-weight: 700; color: #F8FAFC; margin-bottom: 12px;">
            Olá!
        </div>
        <p style="font-size: 15px; line-height: 1.7; color: #E2E8F0; margin-bottom: 14px;">
            O <strong>Radar B3</strong> nasceu com um objetivo simples: 
            ajudar investidores a encontrar informações relevantes de forma prática, rápida e gratuita.
        </p>
        <p style="font-size: 15px; line-height: 1.7; color: #CBD5E1; margin-bottom: 0;">
            Se a plataforma já ajudou você a encontrar oportunidades, acompanhar seus investimentos ou aprender mais sobre o mercado financeiro, considere fazer uma contribuição.
        </p>
    </div>
    """).strip(), unsafe_allow_html=True)

    # Seção: Por que doar?
    st.markdown("### 🚀 Por que doar?")
    st.markdown(textwrap.dedent("""
    <p style="font-size: 14.5px; color: #94A3B8; margin-bottom: 16px;">
        Manter um projeto independente no ar exige investimento constante.<br>
        Sua contribuição ajuda a custear:
    </p>
    """).strip(), unsafe_allow_html=True)

    c_mot1, c_mot2 = st.columns(2)
    with c_mot1:
        st.markdown(textwrap.dedent("""
        <div class="pbi-kpi-card" style="border-left: 3px solid #38BDF8; min-height: 105px; margin-bottom: 14px; padding: 14px 16px;">
            <div style="font-size: 15px; font-weight: 800; color: #F8FAFC;">🌐 Infraestrutura e Hospedagem</div>
            <div style="font-size: 13px; color: #CBD5E1; margin-top: 6px; line-height: 1.4;">
                Servidores, banco de dados e recursos necessários para manter o sistema rápido, estável e disponível.
            </div>
        </div>

        <div class="pbi-kpi-card" style="border-left: 3px solid #10B981; min-height: 105px; margin-bottom: 14px; padding: 14px 16px;">
            <div style="font-size: 15px; font-weight: 800; color: #F8FAFC;">🛠️ Novas Funcionalidades</div>
            <div style="font-size: 13px; color: #CBD5E1; margin-top: 6px; line-height: 1.4;">
                Desenvolvimento de novos radares, indicadores, análises e melhorias para a plataforma.
            </div>
        </div>

        <div class="pbi-kpi-card" style="border-left: 3px solid #F59E0B; min-height: 105px; margin-bottom: 14px; padding: 14px 16px;">
            <div style="font-size: 15px; font-weight: 800; color: #F8FAFC;">🔒 Segurança e Confiabilidade</div>
            <div style="font-size: 13px; color: #CBD5E1; margin-top: 6px; line-height: 1.4;">
                Monitoramento, atualizações e mecanismos para garantir uma experiência segura para todos.
            </div>
        </div>
        """).strip(), unsafe_allow_html=True)

    with c_mot2:
        st.markdown(textwrap.dedent("""
        <div class="pbi-kpi-card" style="border-left: 3px solid #818CF8; min-height: 105px; margin-bottom: 14px; padding: 14px 16px;">
            <div style="font-size: 15px; font-weight: 800; color: #F8FAFC;">📈 Evolução Contínua</div>
            <div style="font-size: 13px; color: #CBD5E1; margin-top: 6px; line-height: 1.4;">
                Correções, otimizações, melhorias visuais e novas ideias sugeridas pela própria comunidade.
            </div>
        </div>

        <div class="pbi-kpi-card" style="border-left: 3px solid #EC4899; min-height: 105px; margin-bottom: 14px; padding: 14px 16px;">
            <div style="font-size: 15px; font-weight: 800; color: #F8FAFC;">☕ Café para o Desenvolvedor</div>
            <div style="font-size: 13px; color: #CBD5E1; margin-top: 6px; line-height: 1.4;">
                Porque algumas das melhores funcionalidades nascem durante longas madrugadas de código.
            </div>
        </div>
        """).strip(), unsafe_allow_html=True)

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    # Seção Principal: Contribuição via PIX
    st.markdown("### 💚 Faça sua contribuição via PIX")

    col_pix_dados, col_pix_qr = st.columns([1.2, 1.0])

    with col_pix_dados:
        st.markdown(textwrap.dedent(f"""
        <div class="pbi-auth-card" style="padding: 20px; border-left: 4px solid #10B981; margin-bottom: 18px;">
            <div style="font-size: 12px; text-transform: uppercase; font-weight: 800; color: #10B981; letter-spacing: 1px;">
                Chave PIX
            </div>
            <div style="font-size: 22px; font-weight: 800; color: #F8FAFC; margin-top: 6px; letter-spacing: 0.5px;">
                📱 {PIX_KEY}
            </div>
            <div style="margin-top: 14px; border-top: 1px solid #334155; padding-top: 12px;">
                <div style="font-size: 11.5px; text-transform: uppercase; font-weight: 700; color: #94A3B8; letter-spacing: 0.5px;">
                    Favorecido
                </div>
                <div style="font-size: 16px; font-weight: 700; color: #38BDF8; margin-top: 3px;">
                    {PIX_RECEIVER}
                </div>
            </div>
        </div>
        """).strip(), unsafe_allow_html=True)

        st.markdown("##### 📋 Código PIX Copia e Cola")
        st.caption("Clique no ícone de cópia no canto direito da caixa abaixo para copiar o código:")
        st.code(PIX_COPY_PASTE, language=None)

    with col_pix_qr:
        st.markdown(textwrap.dedent("""
        <div class="pbi-auth-card" style="text-align: center; padding: 18px; border-top: 3px solid #10B981;">
            <div style="font-size: 16px; font-weight: 800; color: #F8FAFC; margin-bottom: 4px;">
                QR Code PIX
            </div>
            <div style="font-size: 12px; color: #94A3B8; margin-bottom: 14px;">
                Escaneie o QR Code abaixo utilizando o aplicativo do seu banco:
            </div>
        </div>
        """).strip(), unsafe_allow_html=True)

        if os.path.exists(QR_CODE_PATH):
            try:
                qr_img = Image.open(QR_CODE_PATH)
                st.image(qr_img, caption="QR Code PIX - Itaú (Vinicius Augusto Marques)", use_container_width=True)
            except Exception as e:
                st.error(f"Erro ao carregar a imagem do QR Code: {e}")
        else:
            st.warning("Imagem do QR Code não localizada em assets/pix_qrcode.png")

    # Agradecimento
    st.markdown(textwrap.dedent("""
    <div class="pbi-auth-card" style="padding: 24px; border-left: 4px solid #10B981; margin-top: 24px; margin-bottom: 24px;">
        <div style="font-size: 20px; font-weight: 900; color: #10B981; margin-bottom: 10px;">
            🙏 Muito Obrigado!
        </div>
        <p style="font-size: 14.5px; line-height: 1.6; color: #E2E8F0; margin-bottom: 10px;">
            Cada contribuição, independentemente do valor, faz diferença.
        </p>
        <p style="font-size: 14.5px; line-height: 1.6; color: #E2E8F0; margin-bottom: 10px;">
            Além de ajudar a manter o Radar B3 funcionando, você contribui diretamente para a criação de novas funcionalidades e para a melhoria contínua da plataforma.
        </p>
        <p style="font-size: 14.5px; line-height: 1.6; color: #CBD5E1; margin-bottom: 16px;">
            Obrigado pela confiança, pelo incentivo e por fazer parte desta jornada.
        </p>
        <div style="font-size: 16px; font-weight: 800; color: #F43F5E; text-align: center; border-top: 1px solid #334155; padding-top: 14px;">
            Juntos podemos construir a melhor plataforma gratuita de análise e acompanhamento de investimentos da comunidade. ❤️
        </div>
    </div>
    """).strip(), unsafe_allow_html=True)

    # Botão de retorno no final conforme explicitamente solicitado
    st.markdown("---")
    col_f1, col_f2, col_f3 = st.columns([1, 2, 1])
    with col_f2:
        if st.button("← 🏠 Voltar à Plataforma", key="donation_btn_back_bottom", type="primary", use_container_width=True):
            st.session_state["view"] = "dashboard"
            st.rerun()
