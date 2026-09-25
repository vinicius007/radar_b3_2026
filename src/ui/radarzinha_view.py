"""
Interface Interativa da Radarzinha AI no B3 Dividend Radar.
Inclui Chat Executivo, Avatar Animado, Botões de Atalho, Controle Total de Áudio e Síntese de Voz Web Speech API.
"""

import json
import textwrap
from datetime import datetime
from typing import Optional
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

from src.agent.radarzinha_engine import RadarzinhaEngine, get_radarzinha_response

def render_stop_speech_script():
    """
    Injeta JavaScript para parar imediatamente qualquer reprodução de voz ativa da Radarzinha
    em todos os contextos (janela atual, pai e topo).
    """
    stop_js = """
    <script>
    (function() {
        try {
            if ('speechSynthesis' in window) {
                window.speechSynthesis.cancel();
            }
        } catch(e) {}
        try {
            if (window.parent && 'speechSynthesis' in window.parent) {
                window.parent.speechSynthesis.cancel();
            }
        } catch(e) {}
        try {
            if (window.top && 'speechSynthesis' in window.top) {
                window.top.speechSynthesis.cancel();
            }
        } catch(e) {}
    })();
    </script>
    """
    components.html(stop_js, height=0, width=0)

def render_voice_speech_script(text_to_speak: str, auto_play: bool = True, element_id: str = "radarzinha_tts"):
    """
    Injeta componente interativo com Web Speech API para reproduzir a voz feminina
    da Radarzinha com total compatibilidade de navegadores (Chrome, Edge, Firefox, Safari).
    Inclui botão nativo '⏹️ Parar' para cancelamento instantâneo no cliente e
    limpeza automática ao descarregar a página (beforeunload/unload).
    """
    clean_text = text_to_speak.replace('"', '\\"').replace("'", "\\'").replace('\n', ' ').replace('\r', ' ')
    preview = (text_to_speak[:90] + "...") if len(text_to_speak) > 90 else text_to_speak
    preview_clean = preview.replace('"', '&quot;').replace("'", "&#39;")

    js_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
        body {{
            margin: 0;
            padding: 0;
            background: transparent;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }}
        .player-card {{
            background: linear-gradient(135deg, rgba(244, 63, 94, 0.22) 0%, rgba(30, 41, 59, 0.95) 100%);
            border: 1px solid #F43F5E;
            border-radius: 10px;
            padding: 10px 16px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            box-shadow: 0 4px 14px rgba(244, 63, 94, 0.25);
            color: #F8FAFC;
        }}
        .left-info {{
            display: flex;
            align-items: center;
            gap: 12px;
            overflow: hidden;
        }}
        .avatar {{
            font-size: 26px;
            filter: drop-shadow(0 0 8px rgba(244, 63, 94, 0.6));
        }}
        .title {{
            font-size: 13px;
            font-weight: 800;
            color: #FFF1F2;
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        .preview {{
            font-size: 11.5px;
            color: #FDA4AF;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            max-width: 500px;
            margin-top: 2px;
        }}
        .btn-group {{
            display: flex;
            gap: 8px;
            flex-shrink: 0;
        }}
        .btn-play {{
            background: linear-gradient(135deg, #F43F5E, #E11D48);
            color: #FFFFFF;
            border: none;
            padding: 8px 18px;
            border-radius: 7px;
            font-size: 13px;
            font-weight: 800;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 6px;
            transition: all 0.2s ease;
            box-shadow: 0 2px 10px rgba(244, 63, 94, 0.45);
        }}
        .btn-play:hover {{
            background: linear-gradient(135deg, #FB7185, #F43F5E);
            transform: translateY(-1px);
            box-shadow: 0 4px 14px rgba(244, 63, 94, 0.6);
        }}
        .btn-stop {{
            background: #E11D48;
            color: #FFFFFF;
            border: 1px solid #FDA4AF;
            padding: 8px 16px;
            border-radius: 7px;
            font-size: 13px;
            font-weight: 800;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 6px;
            transition: all 0.2s ease;
            box-shadow: 0 2px 8px rgba(225, 29, 72, 0.4);
        }}
        .btn-stop:hover {{
            background: #BE123C;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(225, 29, 72, 0.6);
        }}
        .pulse {{
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #10B981;
            box-shadow: 0 0 8px #10B981;
            animation: pulse-dot 1.4s infinite;
        }}
        @keyframes pulse-dot {{
            0% {{ opacity: 0.3; transform: scale(0.85); }}
            50% {{ opacity: 1; transform: scale(1.25); }}
            100% {{ opacity: 0.3; transform: scale(0.85); }}
        }}
    </style>
    </head>
    <body>
    <div class="player-card">
        <div class="left-info">
            <div class="avatar">💃</div>
            <div>
                <div class="title"><span class="pulse"></span>Áudio da Radarzinha Pronto!</div>
                <div class="preview">"{preview_clean}"</div>
            </div>
        </div>
        <div class="btn-group">
            <button class="btn-play" onclick="playVoice()">
                🔊 Tocar Voz
            </button>
            <button class="btn-stop" onclick="stopVoice()">
                ⏹️ Parar
            </button>
        </div>
    </div>

    <script>
    const textData = "{clean_text}";
    
    function stopVoice() {{
        try {{ if ('speechSynthesis' in window) window.speechSynthesis.cancel(); }} catch(e){{}}
        try {{ if (window.top && 'speechSynthesis' in window.top) window.top.speechSynthesis.cancel(); }} catch(e){{}}
        try {{ if (window.parent && 'speechSynthesis' in window.parent) window.parent.speechSynthesis.cancel(); }} catch(e){{}}
    }}

    function playVoice() {{
        if (!('speechSynthesis' in window)) {{
            alert("Seu navegador não suporta a síntese de voz nativa.");
            return;
        }}
        stopVoice();
        
        const utter = new SpeechSynthesisUtterance(textData);
        utter.lang = 'pt-BR';
        utter.pitch = 1.08;
        utter.rate = 0.96;
        utter.volume = 1.0;
        
        function applyVoice() {{
            const voices = window.speechSynthesis.getVoices();
            const femaleBR = voices.find(v => 
                v.lang.replace('_', '-').toLowerCase().startsWith('pt') && 
                (v.name.includes('Maria') || v.name.includes('Francisca') || v.name.includes('Luciana') || 
                 v.name.includes('Helena') || v.name.includes('Google') || v.name.toLowerCase().includes('female') ||
                 v.name.includes('Letícia') || v.name.includes('Yara'))
            ) || voices.find(v => v.lang.replace('_', '-').toLowerCase().startsWith('pt'));
            
            if (femaleBR) utter.voice = femaleBR;
            window.speechSynthesis.speak(utter);
        }}

        if (window.speechSynthesis.getVoices().length > 0) {{
            applyVoice();
        }} else {{
            window.speechSynthesis.onvoiceschanged = applyVoice;
            setTimeout(() => {{
                if (!window.speechSynthesis.speaking) {{
                    applyVoice();
                }}
            }}, 250);
        }}
    }}

    // Cancela a fala automaticamente caso o usuário feche, recarregue ou navegue para outra tela
    window.addEventListener('beforeunload', stopVoice);
    window.addEventListener('unload', stopVoice);

    // Tenta reprodução automática se o navegador permitir
    {'setTimeout(playVoice, 100);' if auto_play else ''}
    </script>
    </body>
    </html>
    """
    components.html(js_code, height=68)

def render_radarzinha_view(ranked_df: Optional[pd.DataFrame] = None, current_profile: Optional[dict] = None, is_tab: bool = False):
    """
    Renderiza a interface completa da Radarzinha AI.
    Pode ser exibida como página dedicada (com botão de voltar) ou como aba no dashboard.
    """
    # -------------------------------------------------------------
    # GESTÃO DE ESTADOS DE VOZ E NAVEGAÇÃO
    # -------------------------------------------------------------
    if "radarzinha_chat_history" not in st.session_state:
        st.session_state["radarzinha_chat_history"] = [
            {
                "role": "radarzinha",
                "content": RadarzinhaEngine.GREETING,
                "tts": RadarzinhaEngine.VOICE_INTRO,
                "time": datetime.now().strftime("%H:%M")
            }
        ]
        
    if "radarzinha_voice_enabled" not in st.session_state:
        st.session_state["radarzinha_voice_enabled"] = True

    if "radarzinha_last_spoken_tts" not in st.session_state:
        st.session_state["radarzinha_last_spoken_tts"] = None

    if "radarzinha_current_speaking_id" not in st.session_state:
        st.session_state["radarzinha_current_speaking_id"] = None

    # Se houver gatilho de parada pendente, cancela áudio no navegador
    if st.session_state.get("stop_speech_trigger", False):
        render_stop_speech_script()
        st.session_state["stop_speech_trigger"] = False

    username = current_profile.get("usuario") if current_profile else st.session_state.get("user")
    user_name_display = current_profile.get("nome_completo", "Investidor") if current_profile else "Investidor"

    # Se for página dedicada, exibe botão superior de retorno ao Dashboard
    if not is_tab:
        col_back, col_stop_quick = st.columns([1.4, 3.6])
        with col_back:
            if st.button("← 🏠 Voltar ao Dashboard", key="radarzinha_btn_back_top", use_container_width=True):
                # 1º: Para a fala imediatamente ao clicar em voltar
                render_stop_speech_script()
                st.session_state["radarzinha_last_spoken_tts"] = None
                st.session_state["radarzinha_current_speaking_id"] = None
                st.session_state["stop_speech_trigger"] = True
                st.session_state["view"] = "dashboard"
                st.rerun()
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # CABEÇALHO EXECUTIVO E APRESENTAÇÃO DA RADARZINHA
    # -------------------------------------------------------------
    st.markdown(textwrap.dedent(f"""
    <div class="pbi-auth-card" style="padding: 24px 26px; border-top: 4px solid #F43F5E; margin-bottom: 18px; background: linear-gradient(135deg, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 0.98) 100%);">
        <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 16px;">
            <div style="display: flex; align-items: center; gap: 18px;">
                <div style="width: 64px; height: 64px; border-radius: 50%; background: linear-gradient(135deg, #F43F5E 0%, #E11D48 100%); display: flex; align-items: center; justify-content: center; font-size: 32px; box-shadow: 0 0 20px rgba(244, 63, 94, 0.45); border: 2px solid #FDA4AF;">
                    💃
                </div>
                <div>
                    <div style="font-size: 26px; font-weight: 900; color: #FFF1F2; letter-spacing: -0.5px;">
                        Radarzinha AI
                    </div>
                    <div style="font-size: 14px; font-weight: 600; color: #38BDF8; margin-top: 2px;">
                        Sua Mentora & Conselheira Executiva de Dividendos B3 ✨
                    </div>
                    <div style="font-size: 12px; color: #94A3B8; margin-top: 3px;">
                        Atendendo agora: <b style="color: #F8FAFC;">{user_name_display}</b> &bull; Voz feminina suave, inteligente e envolvente
                    </div>
                </div>
            </div>
            <div style="background: rgba(244, 63, 94, 0.1); border: 1px solid rgba(244, 63, 94, 0.3); border-radius: 8px; padding: 10px 16px; text-align: right;">
                <div style="font-size: 11px; text-transform: uppercase; font-weight: 800; color: #F43F5E; letter-spacing: 1px;">Status da Mentora</div>
                <div style="font-size: 13.5px; font-weight: 700; color: #10B981; margin-top: 2px;">● Pronta para te orientar</div>
            </div>
        </div>
    </div>
    """).strip(), unsafe_allow_html=True)

    # -------------------------------------------------------------
    # BARRA DE CONTROLE DE VOZ, DESATIVAÇÃO DE SOM E BOTÃO PARAR
    # -------------------------------------------------------------
    c_v1, c_v2, c_v3, c_v4 = st.columns([1.5, 1.2, 1.2, 1.1])
    with c_v1:
        # 2º: Ícone / Alternador de Som (Desativação completa e parada imediata)
        voice_on = st.toggle(
            "🔊 Voz da Radarzinha",
            value=st.session_state["radarzinha_voice_enabled"],
            key="toggle_radarzinha_voice",
            help="Ativar ou desativar o som da Radarzinha"
        )
        if voice_on != st.session_state["radarzinha_voice_enabled"]:
            st.session_state["radarzinha_voice_enabled"] = voice_on
            if not voice_on:
                # Se desativou o som, para imediatamente qualquer fala ativa
                render_stop_speech_script()
                st.session_state["radarzinha_last_spoken_tts"] = None
                st.session_state["radarzinha_current_speaking_id"] = None
                st.session_state["stop_speech_trigger"] = True
                st.toast("🔇 Som da Radarzinha desativado e voz interrompida!", icon="🔇")
            else:
                st.toast("🔊 Som da Radarzinha ativado!", icon="🔊")
            st.rerun()

    with c_v2:
        if st.button("💋 Ouvir Saudação", key="btn_test_voice", use_container_width=True, help="Clique para escutar a saudação charmosa da Radarzinha"):
            if st.session_state.get("radarzinha_voice_enabled", True):
                st.session_state["radarzinha_current_speaking_id"] = "intro"
                st.session_state["radarzinha_last_spoken_tts"] = RadarzinhaEngine.VOICE_INTRO
                st.rerun()
            else:
                st.toast("⚠️ Ative '🔊 Voz da Radarzinha' no botão ao lado para ouvir!", icon="🔇")

    with c_v3:
        # 3º: Botão Parar dedicado em destaque para interromper a voz
        if st.button("⏹️ Parar Voz", key="btn_stop_voice", use_container_width=True, help="Interromper imediatamente a voz da Radarzinha"):
            render_stop_speech_script()
            st.session_state["radarzinha_last_spoken_tts"] = None
            st.session_state["radarzinha_current_speaking_id"] = None
            st.session_state["stop_speech_trigger"] = True
            st.toast("⏹️ Fala da Radarzinha interrompida!", icon="⏹️")
            st.rerun()

    with c_v4:
        if st.button("🔄 Limpar Chat", key="btn_clear_chat", use_container_width=True, help="Reiniciar conversa com a Radarzinha"):
            render_stop_speech_script()
            st.session_state["radarzinha_chat_history"] = [
                {
                    "role": "radarzinha",
                    "content": RadarzinhaEngine.GREETING,
                    "tts": RadarzinhaEngine.VOICE_INTRO,
                    "time": datetime.now().strftime("%H:%M")
                }
            ]
            st.session_state["radarzinha_last_spoken_tts"] = None
            st.session_state["radarzinha_current_speaking_id"] = None
            st.session_state["stop_speech_trigger"] = True
            st.rerun()

    # Injeção de áudio interativo se houver fala pendente e som habilitado
    if st.session_state.get("radarzinha_voice_enabled", True) and st.session_state.get("radarzinha_last_spoken_tts"):
        render_voice_speech_script(st.session_state["radarzinha_last_spoken_tts"], auto_play=True)

    # -------------------------------------------------------------
    # ATALHOS RÁPIDOS (CHIPS DE 1 CLIQUE)
    # -------------------------------------------------------------
    st.markdown("##### 💡 Perguntas Frequentes & Atalhos Rápidos")
    chip_col1, chip_col2, chip_col3 = st.columns(3)
    chip_col4, chip_col5, chip_col6 = st.columns(3)

    user_prompt_submitted = None

    with chip_col1:
        if st.button("🎯 Melhores ações abaixo do Teto", key="chip_1", use_container_width=True):
            user_prompt_submitted = "Quais as melhores ações abaixo do Preço Teto hoje?"
    with chip_col2:
        if st.button("⏰ Quando comprar e vender?", key="chip_2", use_container_width=True):
            user_prompt_submitted = "Em qual momento devo comprar e vender determinada ação da minha carteira?"
    with chip_col3:
        if st.button("💰 Montar carteira de R$ 2.000/mês", key="chip_3", use_container_width=True):
            user_prompt_submitted = "Como montar uma carteira de dividendos para ter retorno de 2000 reais mensais?"

    with chip_col4:
        if st.button("🔍 Analisar minha carteira e PM", key="chip_4", use_container_width=True):
            user_prompt_submitted = "Como está a minha carteira e quais ações estão abaixo do meu preço médio?"
    with chip_col5:
        if st.button("📖 Dicionário de Siglas (P/L, ROE, Bazin)", key="chip_5", use_container_width=True):
            user_prompt_submitted = "Me explique as principais siglas da B3 como DY, P/L, ROE e Preço Teto de Bazin."
    with chip_col6:
        if st.button("🧭 Onde acho cada função no site?", key="chip_6", use_container_width=True):
            user_prompt_submitted = "Como funciona o site e onde acho as ferramentas de alertas e rankings?"

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # HISTÓRICO DE MENSAGENS DO CHAT
    # -------------------------------------------------------------
    st.markdown("##### 💬 Conversa com a Radarzinha")
    chat_container = st.container()

    with chat_container:
        for idx, msg in enumerate(st.session_state["radarzinha_chat_history"]):
            if msg["role"] == "user":
                st.markdown(textwrap.dedent(f"""
                <div style="display: flex; justify-content: flex-end; margin-bottom: 14px;">
                    <div style="background: linear-gradient(135deg, rgba(56, 189, 248, 0.15) 0%, rgba(14, 165, 233, 0.25) 100%); border: 1px solid #38BDF8; border-radius: 14px 14px 2px 14px; padding: 14px 18px; max-width: 80%; box-shadow: 0 4px 12px rgba(0,0,0,0.2);">
                        <div style="font-size: 11px; font-weight: 700; color: #38BDF8; margin-bottom: 4px; display: flex; justify-content: space-between;">
                            <span>👤 Você ({user_name_display})</span>
                            <span style="color: #64748B;">{msg.get('time', '')}</span>
                        </div>
                        <div style="font-size: 14.5px; color: #F8FAFC; line-height: 1.5;">
                            {msg['content']}
                        </div>
                    </div>
                </div>
                """).strip(), unsafe_allow_html=True)
            else:
                col_radar_msg, col_radar_audio = st.columns([5.5, 0.9])
                with col_radar_msg:
                    st.markdown(textwrap.dedent(f"""
                    <div style="display: flex; justify-content: flex-start; margin-bottom: 8px;">
                        <div style="background: linear-gradient(135deg, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 0.95) 100%); border: 1px solid rgba(244, 63, 94, 0.35); border-left: 4px solid #F43F5E; border-radius: 14px 14px 14px 2px; padding: 18px 22px; max-width: 95%; box-shadow: 0 4px 16px rgba(244, 63, 94, 0.12);">
                            <div style="font-size: 12px; font-weight: 800; color: #F43F5E; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center;">
                                <span>💃 Radarzinha AI &bull; Mentora de Dividendos</span>
                                <span style="color: #64748B; font-weight: 500;">{msg.get('time', '')}</span>
                            </div>
                            <div style="font-size: 14.5px; color: #F1F5F9; line-height: 1.7;">
                                {msg['content']}
                            </div>
                        </div>
                    </div>
                    """).strip(), unsafe_allow_html=True)

                msg_id = f"msg_{idx}"
                is_this_msg_playing = (
                    st.session_state.get("radarzinha_current_speaking_id") == msg_id and
                    st.session_state.get("radarzinha_voice_enabled", True)
                )

                with col_radar_audio:
                    # Se esta mensagem estiver tocando, exibe o botão vermelho Parar
                    if is_this_msg_playing:
                        if st.button("⏹️ Parar", key=f"btn_listen_msg_{idx}", help="Parar esta fala agora", type="primary"):
                            render_stop_speech_script()
                            st.session_state["radarzinha_last_spoken_tts"] = None
                            st.session_state["radarzinha_current_speaking_id"] = None
                            st.session_state["stop_speech_trigger"] = True
                            st.toast("⏹️ Fala interrompida!", icon="⏹️")
                            st.rerun()
                    else:
                        if st.button("🔊 Ouvir", key=f"btn_listen_msg_{idx}", help="Ouvir esta resposta com a voz da Radarzinha"):
                            if st.session_state.get("radarzinha_voice_enabled", True):
                                st.session_state["radarzinha_current_speaking_id"] = msg_id
                                st.session_state["radarzinha_last_spoken_tts"] = msg.get("tts", msg["content"])
                                st.rerun()
                            else:
                                st.toast("⚠️ Ative '🔊 Voz da Radarzinha' no botão acima para escutar!", icon="🔇")

    # -------------------------------------------------------------
    # CAIXA DE ENTRADA LIVRE (PERGUNTE QUALQUER COISA)
    # -------------------------------------------------------------
    typed_prompt = st.chat_input("Pergunte qualquer coisa sobre dividendos, ações, ou sua carteira para a Radarzinha...")
    
    active_prompt = user_prompt_submitted or typed_prompt

    if active_prompt:
        current_time_str = datetime.now().strftime("%H:%M")
        
        # 1. Adiciona a pergunta do investidor ao histórico
        st.session_state["radarzinha_chat_history"].append({
            "role": "user",
            "content": active_prompt,
            "time": current_time_str
        })

        # 2. Gera a resposta executiva e o script de voz
        response_text, response_tts = get_radarzinha_response(
            query=active_prompt,
            username=username,
            ranked_df=ranked_df
        )

        # 3. Adiciona a resposta da Radarzinha
        st.session_state["radarzinha_chat_history"].append({
            "role": "radarzinha",
            "content": response_text,
            "tts": response_tts,
            "time": current_time_str
        })

        # 4. Se a voz estiver habilitada, prepara para falar
        if st.session_state.get("radarzinha_voice_enabled", True):
            st.session_state["radarzinha_current_speaking_id"] = f"msg_{len(st.session_state['radarzinha_chat_history']) - 1}"
            st.session_state["radarzinha_last_spoken_tts"] = response_tts

        st.rerun()

    # Botão inferior de retorno ao Dashboard se estiver na página dedicada
    if not is_tab:
        st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)
        col_back_b, _ = st.columns([1.4, 3.6])
        with col_back_b:
            if st.button("← 🏠 Voltar ao Dashboard", key="radarzinha_btn_back_bottom", use_container_width=True):
                # 1º: Para a fala imediatamente ao clicar em voltar
                render_stop_speech_script()
                st.session_state["radarzinha_last_spoken_tts"] = None
                st.session_state["radarzinha_current_speaking_id"] = None
                st.session_state["stop_speech_trigger"] = True
                st.session_state["view"] = "dashboard"
                st.rerun()

def render_radarzinha_tab(ranked_df: Optional[pd.DataFrame] = None, current_profile: Optional[dict] = None):
    """Alias para renderizar a Radarzinha como aba dentro do dashboard principal."""
    render_radarzinha_view(ranked_df=ranked_df, current_profile=current_profile, is_tab=True)
