"""
Telas e Vistas de Gestão de Usuários, Perfil e Autenticação do DIVIDEND RADAR B3.
Implementa Login, Cadastro, Minhas Informações (com Avatar V e Zona de Perigo),
Alterar Senha (com regras e toggles), Redefinir Senha e Ajuda.
"""

import re
import textwrap
from typing import Optional
import streamlit as st
import streamlit.components.v1 as components

from src.auth.user_manager import (
    get_user_profile,
    save_user_profile,
    create_user,
    update_user_profile,
    delete_user_account,
    change_user_password,
    request_password_reset,
    authenticate_user,
    validate_password_strength,
    validate_email,
    create_kmsi_token,
    validate_kmsi_token,
    revoke_kmsi_token,
    revoke_all_user_kmsi_tokens
)

def render_kmsi_cookie_setter(token: str, max_age_days: int = 30):
    """Injeta JavaScript para gravar o cookie persistente e espelhar no localStorage."""
    max_age_seconds = max_age_days * 24 * 60 * 60
    js = f"""
    <script>
        try {{
            const cookieStr = "b3_kmsi_token={token}; path=/; max-age={max_age_seconds}; SameSite=Lax";
            document.cookie = cookieStr;
            if (window.parent && window.parent.document) {{
                window.parent.document.cookie = cookieStr;
                try {{
                    window.parent.localStorage.setItem("b3_kmsi_token", "{token}");
                }} catch(e) {{}}
            }}
        }} catch(err) {{
            console.warn("Erro ao definir cookie KMSI:", err);
        }}
    </script>
    """
    components.html(js, height=0, width=0)

def render_kmsi_cookie_clearer():
    """Injeta JavaScript para apagar o cookie persistente e o localStorage no logout."""
    js = """
    <script>
        try {
            const cookieStr = "b3_kmsi_token=; path=/; max-age=0; expires=Thu, 01 Jan 1970 00:00:00 GMT; SameSite=Lax";
            document.cookie = cookieStr;
            if (window.parent && window.parent.document) {
                window.parent.document.cookie = cookieStr;
                try {
                    window.parent.localStorage.removeItem("b3_kmsi_token");
                } catch(e) {}
            }
        } catch(err) {
            console.warn("Erro ao limpar cookie KMSI:", err);
        }
    </script>
    """
    components.html(js, height=0, width=0)

def get_kmsi_cookie_token() -> Optional[str]:
    """Recupera o token KMSI dos cookies enviados pelo navegador."""
    try:
        return st.context.cookies.get("b3_kmsi_token")
    except Exception:
        return None

def clear_login_fields():
    """Limpa os campos e o estado de visualização de senha da tela de login."""
    st.session_state["login_usuario"] = ""
    st.session_state["login_senha"] = ""
    st.session_state["login_show_pwd"] = False

def clear_register_fields():
    """Limpa todos os campos da tela de cadastro de novos usuários."""
    for k in ["reg_nome", "reg_usuario", "reg_email", "reg_nasc", "reg_tel", "reg_senha", "reg_conf_senha"]:
        st.session_state[k] = ""
    st.session_state["reg_show_pwd"] = False
    st.session_state["reg_nao_resido"] = False
    st.session_state["reg_termos"] = False

def render_login_view():
    """Tela de Login centralizada conforme especificações completas (campos sempre limpos)."""
    col_l1, col_l2, col_l3 = st.columns([1, 1.4, 1])
    with col_l2:
        st.markdown(textwrap.dedent("""
        <div class="pbi-auth-card">
            <div style="text-align: center; margin-bottom: 20px;">
                <div style="font-size: 38px; margin-bottom: 6px;">🔐</div>
                <div style="font-size: 24px; font-weight: 800; color: #F8FAFC; letter-spacing: -0.5px;">Entrar</div>
                <div style="font-size: 13px; color: #94A3B8; margin-top: 4px;">Acesse seu painel executivo de proventos B3</div>
            </div>
        </div>
        """).strip(), unsafe_allow_html=True)

        if st.session_state.get("kmsi_clear_cookie"):
            render_kmsi_cookie_clearer()
            del st.session_state["kmsi_clear_cookie"]

        if "login_usuario" not in st.session_state:
            st.session_state["login_usuario"] = ""
        if "login_senha" not in st.session_state:
            st.session_state["login_senha"] = ""
        if "login_show_pwd" not in st.session_state:
            st.session_state["login_show_pwd"] = False

        show_pwd = st.session_state.get("login_show_pwd", False)

        usuario_input = st.text_input("Usuário", placeholder="Digite seu usuário...", key="login_usuario")
        senha_input = st.text_input(
            "Senha", 
            type="default" if show_pwd else "password",
            placeholder="••••••••",
            key="login_senha"
        )

        col_chk, col_reset = st.columns([1.2, 1.0])
        with col_chk:
            st.checkbox(
                "👁️ Mostrar senha" if not show_pwd else "🙈 Ocultar senha", 
                key="login_show_pwd"
            )
        with col_reset:
            st.markdown("<div style='text-align: right; padding-top: 8px;'>", unsafe_allow_html=True)
            st.caption("Esqueceu a sua senha?")
            st.markdown("</div>", unsafe_allow_html=True)

        kmsi_opt = st.checkbox(
            "🔒 Permanecer conectado neste dispositivo",
            value=True,
            key="login_kmsi",
            help="Salva um cookie persistente e seguro no navegador para manter sua sessão ativa por até 30 dias mesmo após fechar a janela ou reiniciar o dispositivo."
        )

        btn_entrar = st.button("🚀 Entrar", type="primary", use_container_width=True, key="btn_login_submit")

        if btn_entrar:
            u_clean = usuario_input.strip()
            s_clean = senha_input.strip()
            if not u_clean or not s_clean:
                st.error("❌ Preencha o usuário e a senha.")
            else:
                user_auth = authenticate_user(u_clean, s_clean)
                if user_auth:
                    logged_user = user_auth.get("usuario", "masterradar")
                    st.session_state["authenticated"] = True
                    st.session_state["user"] = logged_user
                    st.session_state["view"] = "dashboard"

                    if kmsi_opt:
                        token = create_kmsi_token(logged_user, days=30)
                        st.session_state["kmsi_set_token"] = token
                    else:
                        st.session_state["kmsi_clear_cookie"] = True
                        curr_tok = get_kmsi_cookie_token()
                        if curr_tok:
                            revoke_kmsi_token(curr_tok)

                    st.success(f"✅ Bem-vindo, {user_auth.get('nome_completo', u_clean)}!")
                    st.rerun()
                else:
                    st.error("❌ Usuário ou senha incorretos. Verifique suas credenciais.")

        col_r1, col_r2 = st.columns([1, 1])
        with col_r1:
            if st.button("🔑 Redefinir senha", key="link_to_reset", use_container_width=True):
                st.session_state["view"] = "reset_password"
                st.rerun()
        with col_r2:
            if st.button("📝 Cadastre-se", key="link_to_register", use_container_width=True):
                clear_register_fields()
                st.session_state["view"] = "register"
                st.rerun()

        st.markdown("<div style='margin: 16px 0; text-align: center; color: #64748B; font-size: 12px;'>─── Ou entre com o seu login social ───</div>", unsafe_allow_html=True)

        if st.button("🌐 Entrar com Google", key="btn_login_google", use_container_width=True):
            # Simulação do login social Google
            st.session_state["authenticated"] = True
            st.session_state["user"] = "masterradar"
            st.session_state["view"] = "dashboard"
            if kmsi_opt:
                token = create_kmsi_token("masterradar", days=30)
                st.session_state["kmsi_set_token"] = token
            st.success("✅ Conectado com sua Conta Google (viniciusamarques2026@gmail.com)!")
            st.rerun()

        st.markdown(textwrap.dedent("""
        <div style="margin-top: 20px; font-size: 11.5px; color: #94A3B8; text-align: center; line-height: 1.4;">
            Ao continuar você concorda com nossos <b>Termos de Uso</b> e <b>Política de Privacidade</b>.<br>
            Ainda não possui uma conta? Clique em <b>Cadastre-se</b> acima.
        </div>
        """).strip(), unsafe_allow_html=True)

def render_register_view():
    """Tela de Cadastro de Usuário completa com campos sempre limpos ao entrar."""
    col_l1, col_l2, col_l3 = st.columns([1, 1.5, 1])
    with col_l2:
        st.markdown(textwrap.dedent("""
        <div class="pbi-auth-card">
            <div style="text-align: center; margin-bottom: 18px;">
                <div style="font-size: 36px; margin-bottom: 6px;">📝</div>
                <div style="font-size: 24px; font-weight: 800; color: #F8FAFC; letter-spacing: -0.5px;">Cadastre-se</div>
                <div style="font-size: 13px; color: #94A3B8; margin-top: 4px;">Crie sua conta para gerenciar sua carteira na B3</div>
            </div>
        </div>
        """).strip(), unsafe_allow_html=True)

        for k in ["reg_nome", "reg_usuario", "reg_email", "reg_nasc", "reg_tel", "reg_senha", "reg_conf_senha"]:
            if k not in st.session_state:
                st.session_state[k] = ""
        if "reg_show_pwd" not in st.session_state:
            st.session_state["reg_show_pwd"] = False
        if "reg_nao_resido" not in st.session_state:
            st.session_state["reg_nao_resido"] = False
        if "reg_termos" not in st.session_state:
            st.session_state["reg_termos"] = False

        st.markdown("##### 👤 Informações Pessoais")
        nome = st.text_input("Nome completo *", placeholder="Ex: Seu Nome Completo", key="reg_nome", help="Mínimo de 5 caracteres.")
        usuario = st.text_input("Usuário *", placeholder="Ex: seu.usuario", key="reg_usuario", help="Chave primária / login (letras, números e ponto).")
        email = st.text_input("E-mail *", placeholder="nome@dominio.com", key="reg_email", help="Será utilizado para notificações e login.")
        
        c_d1, c_d2 = st.columns(2)
        with c_d1:
            nasc = st.text_input("Data de nascimento *", placeholder="DD/MM/AAAA", key="reg_nasc")
        with c_d2:
            tel = st.text_input("Telefone *", placeholder="+55 (XX) XXXXX-XXXX", key="reg_tel")

        st.markdown("##### 🔒 Credenciais de Acesso")
        
        reg_show_pwd = st.session_state.get("reg_show_pwd", False)

        senha = st.text_input(
            "Senha *", 
            type="default" if reg_show_pwd else "password", 
            placeholder="••••••••", 
            key="reg_senha", 
            help="Mínimo 8 caracteres, maiúscula, minúscula, número e caractere especial."
        )
        conf_senha = st.text_input(
            "Confirmar nova senha *", 
            type="default" if reg_show_pwd else "password", 
            placeholder="••••••••", 
            key="reg_conf_senha"
        )

        st.checkbox(
            "👁️ Mostrar senhas digitadas" if not reg_show_pwd else "🙈 Ocultar senhas digitadas", 
            key="reg_show_pwd"
        )

        # Indicador de força de senha
        if senha:
            is_valid_pwd, errors, score = validate_password_strength(senha)
            color = "#EF4444" if score < 50 else ("#F59E0B" if score < 100 else "#10B981")
            label = "Fraca" if score < 50 else ("Média" if score < 100 else "Forte e Segura")
            st.markdown(f"""
            <div style="margin-top: -6px; margin-bottom: 10px;">
                <div style="font-size: 11px; color: {color}; font-weight: 700;">Força da Senha: {label} ({score}%)</div>
                <div class="pbi-strength-bar">
                    <div class="pbi-strength-fill" style="width: {score}%; background-color: {color};"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if errors:
                st.caption("Pendências: " + ", ".join(errors))

        nao_resido = st.checkbox("Não resido no Brasil", key="reg_nao_resido")
        termos = st.checkbox("Li e concordo com os Termos de uso e Política de Privacidade (LGPD) *", key="reg_termos")

        btn_cadastrar = st.button("✅ Cadastrar Conta", type="primary", use_container_width=True, key="btn_reg_submit")

        if btn_cadastrar:
            success, msg = create_user(
                nome_completo=nome,
                usuario=usuario,
                email=email,
                data_nascimento=nasc,
                telefone=tel,
                senha=senha,
                confirmar_senha=conf_senha,
                termos_uso=termos,
                nao_resido_brasil=nao_resido
            )
            if success:
                st.session_state["authenticated"] = True
                st.session_state["user"] = usuario.strip().lower()
                st.session_state["view"] = "dashboard"
                st.success(f"🎉 Conta criada com sucesso! Seja bem-vindo(a), {nome}!")
                st.rerun()
            else:
                st.error(f"❌ {msg}")

        st.markdown("<div style='margin: 14px 0 6px 0; text-align: center;'>", unsafe_allow_html=True)
        if st.button("Já tem uma conta? Faça Login", key="reg_to_login", use_container_width=True):
            clear_login_fields()
            st.session_state["view"] = "login"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

def render_profile_view(username: str):
    """Tela Minhas Informações com dados editáveis, Avatar V e Zona de Perigo com confirmação."""
    col_back, _ = st.columns([1, 4])
    with col_back:
        if st.button("← 🏠 Home (Voltar à Página Principal)", key="prof_btn_back"):
            st.session_state["view"] = "dashboard"
            st.rerun()

    user_data = get_user_profile(username)
    if not user_data:
        st.error("Usuário não encontrado.")
        return

    avatar_char = user_data.get("avatar_letter", "V")
    email_val = user_data.get("email", "viniciusamarques2026@gmail.com")
    user_val = user_data.get("usuario", "masterradar")

    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 20px;">
        <div class="pbi-avatar-circle" style="width: 54px; height: 54px; font-size: 26px;">{avatar_char}</div>
        <div>
            <div style="font-size: 22px; font-weight: 800; color: #F8FAFC;">Minhas informações</div>
            <div style="font-size: 13px; color: #94A3B8;">{email_val} &bull; <b style="color:#38BDF8;">@{user_val}</b></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c_form, c_danger = st.columns([1.6, 1.1])

    with c_form:
        with st.form("form_edit_profile"):
            st.markdown("##### 📝 Dados Cadastrais (Editáveis)")

            # Campos bloqueados conforme regras
            st.text_input("Usuário (Chave de Login)", value=user_val, disabled=True, help="O identificador de login não pode ser alterado.")
            st.text_input("E-mail Cadastrado", value=email_val, disabled=True, help="O e-mail principal não pode ser alterado nesta tela.")

            nome = st.text_input("Nome completo *", value=user_data.get("nome_completo", "Vinicius Augusto Marques"))
            
            c1, c2 = st.columns(2)
            with c1:
                nasc = st.text_input("Data de nascimento *", value=user_data.get("data_nascimento", "19/10/1975"))
            with c2:
                tel = st.text_input("Telefone *", value=user_data.get("telefone", "+556256454544"))

            nao_reside = st.checkbox("☑ Não resido no Brasil", value=bool(user_data.get("nao_resido_brasil", True)))
            termos = st.checkbox("☑ Termos de uso/Privacidade", value=bool(user_data.get("termos_uso_privacidade", True)))

            st.markdown("<br>", unsafe_allow_html=True)
            col_b1, col_b2 = st.columns([1, 1])
            with col_b1:
                cancel_btn = st.form_submit_button("Cancelar", use_container_width=True)
            with col_b2:
                save_btn = st.form_submit_button("💾 Salvar Alterações", type="primary", use_container_width=True)

            if cancel_btn:
                st.session_state["view"] = "dashboard"
                st.rerun()

            if save_btn:
                ok, msg = update_user_profile(
                    username=username,
                    nome_completo=nome,
                    data_nascimento=nasc,
                    telefone=tel,
                    nao_resido_brasil=nao_reside,
                    termos_uso=termos
                )
                if ok:
                    st.success("✅ " + msg)
                    st.rerun()
                else:
                    st.error("❌ " + msg)

    with c_danger:
        st.markdown("""
        <div class="pbi-danger-zone">
            <div class="pbi-danger-title">⚠️ Zona de Perigo</div>
            <div class="pbi-danger-text">
                A exclusão da conta é permanente e não pode ser desfeita. Todos os seus dados, histórico de compras e carteira serão apagados.
            </div>
        </div>
        """, unsafe_allow_html=True)

        confirm_del = st.checkbox("Tenho certeza e desejo excluir minha conta definitivamente", key="chk_confirm_delete")

        if st.button("🗑️ Excluir conta permanentemente", type="secondary", use_container_width=True):
            if not confirm_del:
                st.warning("⚠️ Por segurança, marque a caixa de confirmação acima para prosseguir.")
            else:
                delete_user_account(username)
                st.session_state["authenticated"] = False
                st.session_state["user"] = None
                clear_login_fields()
                clear_register_fields()
                st.session_state["view"] = "login"
                st.success("Conta excluída com sucesso.")
                st.rerun()

def render_change_password_view(username: str):
    """Tela Alterar Senha com verificação de requisitos e toggle de visualização."""
    col_l1, col_l2, col_l3 = st.columns([1, 1.4, 1])
    with col_l2:
        st.markdown(textwrap.dedent("""
        <div class="pbi-auth-card">
            <div style="text-align: center; margin-bottom: 18px;">
                <div style="font-size: 36px; margin-bottom: 6px;">🔑</div>
                <div style="font-size: 24px; font-weight: 800; color: #F8FAFC; letter-spacing: -0.5px;">Alterar Senha</div>
                <div style="font-size: 13px; color: #94A3B8; margin-top: 4px;">Atualize suas credenciais de segurança com senha forte</div>
            </div>
        </div>
        """).strip(), unsafe_allow_html=True)

        for k in ["cpwd_atual", "cpwd_nova", "cpwd_conf"]:
            if k not in st.session_state:
                st.session_state[k] = ""
        if "change_show_pwd" not in st.session_state:
            st.session_state["change_show_pwd"] = False

        show_pwd = st.session_state.get("change_show_pwd", False)

        senha_atual = st.text_input("Senha atual *", type="default" if show_pwd else "password", placeholder="Digite sua senha atual...", key="cpwd_atual")
        nova_senha = st.text_input("Nova Senha *", type="default" if show_pwd else "password", placeholder="Digite a nova senha...", key="cpwd_nova")

        st.info("ℹ️ A nova senha deve conter pelo menos 8 caracteres, ser composta por maiúscula, minúscula, um número e um caractere especial.")

        confirmar_nova = st.text_input("Confirmar nova senha *", type="default" if show_pwd else "password", placeholder="Repita a nova senha...", key="cpwd_conf")

        st.checkbox(
            "👁️ Mostrar senhas digitadas" if not show_pwd else "🙈 Ocultar senhas digitadas", 
            key="change_show_pwd"
        )

        if nova_senha:
            _, _, score = validate_password_strength(nova_senha)
            color = "#EF4444" if score < 50 else ("#F59E0B" if score < 100 else "#10B981")
            st.markdown(f"""
            <div class="pbi-strength-bar">
                <div class="pbi-strength-fill" style="width: {score}%; background-color: {color};"></div>
            </div>
            """, unsafe_allow_html=True)

        c1, c2 = st.columns([1, 1])
        with c1:
            cancel = st.button("Cancelar", use_container_width=True, key="btn_cancel_cpwd")
        with c2:
            salvar = st.button("💾 Salvar Nova Senha", type="primary", use_container_width=True, key="btn_save_cpwd")

        if cancel:
            st.session_state["view"] = "dashboard"
            st.rerun()

        if salvar:
            ok, msg = change_user_password(username, senha_atual, nova_senha, confirmar_nova)
            if ok:
                st.success("✅ " + msg)
                st.session_state["view"] = "dashboard"
                st.rerun()
            else:
                st.error("❌ " + msg)

def render_reset_password_view():
    """Tela de Redefinir Senha com envio de senha provisória por e-mail."""
    col_l1, col_l2, col_l3 = st.columns([1, 1.4, 1])
    with col_l2:
        st.markdown(textwrap.dedent("""
        <div class="pbi-auth-card">
            <div style="text-align: center; margin-bottom: 20px;">
                <div style="font-size: 38px; margin-bottom: 6px;">📩</div>
                <div style="font-size: 24px; font-weight: 800; color: #F8FAFC; letter-spacing: -0.5px;">Redefinir Senha</div>
                <div style="font-size: 13px; color: #94A3B8; margin-top: 4px;">Informe seu e-mail cadastrado para receber sua nova senha provisória</div>
            </div>
        </div>
        """).strip(), unsafe_allow_html=True)

        if "reset_email" not in st.session_state:
            st.session_state["reset_email"] = ""

        email_recup = st.text_input("E-mail *", placeholder="Digite seu e-mail cadastrado...", key="reset_email")
        btn_enviar = st.button("✉️ Enviar Senha Provisória por E-mail", type="primary", use_container_width=True, key="btn_reset_submit")

        if btn_enviar:
            if not email_recup.strip():
                st.error("❌ Por favor, digite seu e-mail.")
            else:
                ok, msg, details = request_password_reset(email_recup)
                if not ok:
                    st.error("❌ " + msg)
                else:
                    if details.get("email_sent"):
                        st.success("✅ E-mail de redefinição enviado com sucesso!")
                        st.markdown(textwrap.dedent(f"""
                        <div class="pbi-auth-card" style="border-left: 4px solid #10B981; margin-top: 14px; padding: 16px;">
                            <div style="font-size: 15px; font-weight: 700; color: #10B981; margin-bottom: 6px;">
                                📩 Verifique sua Caixa de Entrada
                            </div>
                            <div style="font-size: 13px; color: #CBD5E1; line-height: 1.5;">
                                Enviamos a senha provisória para a conta <b>[{details.get('usuario')}]</b> no e-mail:<br>
                                <span style="color: #38BDF8; font-weight: 600;">{details.get('email')}</span>
                            </div>
                            <div style="font-size: 12px; color: #94A3B8; margin-top: 10px; border-top: 1px solid #334155; padding-top: 8px;">
                                💡 <b>Dica:</b> Caso não localize a mensagem de imediato, confira a sua pasta de <b>Spam</b> ou <b>Lixo Eletrônico</b>. Lembre-se de alterar a senha após logar.
                            </div>
                        </div>
                        """).strip(), unsafe_allow_html=True)
                    else:
                        st.warning("⚠️ Nova senha provisória gerada e ativada no sistema!")
                        st.markdown(textwrap.dedent(f"""
                        <div class="pbi-auth-card" style="border-left: 4px solid #F59E0B; margin-top: 14px; padding: 16px;">
                            <div style="font-size: 15px; font-weight: 700; color: #F59E0B; margin-bottom: 6px;">
                                🔑 Senha Provisória Ativada
                            </div>
                            <div style="font-size: 13px; color: #CBD5E1; line-height: 1.5;">
                                Sua conta <b>[{details.get('usuario')}]</b> foi atualizada com uma nova senha provisória válida.<br>
                                <span style="color: #94A3B8; font-size: 12px;">(O envio automático de e-mail requer configuração da Senha de App SMTP nas opções abaixo).</span>
                            </div>
                            <div style="margin: 14px 0; padding: 14px; background: #0B1120; border: 1px solid #38BDF8; border-radius: 8px; text-align: center;">
                                <div style="font-size: 11px; text-transform: uppercase; color: #94A3B8; letter-spacing: 1px;">Sua Senha Provisória</div>
                                <div style="font-family: monospace; font-size: 24px; font-weight: 800; color: #38BDF8; letter-spacing: 3px; margin-top: 4px;">
                                    {details.get('temp_pwd')}
                                </div>
                            </div>
                            <div style="font-size: 12px; color: #FDE68A; background: rgba(245, 158, 11, 0.1); padding: 8px 12px; border-radius: 6px;">
                                ⚠️ <b>Lembre-se de alterar a senha após logar.</b> Use a senha provisória acima na tela de Login.
                            </div>
                        </div>
                        """).strip(), unsafe_allow_html=True)

        st.markdown("<div style='margin-top: 12px;'>", unsafe_allow_html=True)
        # Expander de configuração SMTP para facilitar testes e configuração
        with st.expander("⚙️ Configuração do Envio de E-mail (SMTP / Gmail)", expanded=False):
            st.caption("Para disparo real de e-mails via Gmail, utilize uma Senha de App gerada na Conta Google (Segurança > Senhas de app).")
            from src.auth.email_service import load_smtp_config, save_smtp_config, send_password_reset_email
            smtp_cfg = load_smtp_config()

            c_smtp1, c_smtp2 = st.columns(2)
            with c_smtp1:
                smtp_srv = st.text_input("Servidor SMTP", value=smtp_cfg.get("server", "smtp.gmail.com"), key="cfg_smtp_server")
                smtp_usr = st.text_input("E-mail Remetente (Gmail)", value=smtp_cfg.get("user", "constecinf@gmail.com"), key="cfg_smtp_user")
            with c_smtp2:
                smtp_prt = st.number_input("Porta", value=int(smtp_cfg.get("port", 587)), min_value=1, max_value=65535, key="cfg_smtp_port")
                current_pwd = smtp_cfg.get("password", "")
                smtp_pwd_in = st.text_input(
                    "Senha de App Google (16 letras)",
                    value=current_pwd,
                    type="password",
                    placeholder="ex: abcd efgh ijkl mnop",
                    help="Gere em: https://myaccount.google.com/apppasswords",
                    key="cfg_smtp_password"
                )

            c_sbtn1, c_sbtn2 = st.columns(2)
            with c_sbtn1:
                if st.button("💾 Salvar Configurações", key="btn_save_smtp", use_container_width=True):
                    save_smtp_config({
                        "server": smtp_srv.strip(),
                        "port": int(smtp_prt),
                        "user": smtp_usr.strip(),
                        "password": smtp_pwd_in.strip()
                    })
                    st.success("✅ Configurações salvas em data/smtp_config.json!")
                    st.rerun()

            with c_sbtn2:
                if st.button("🧪 Enviar E-mail Teste", key="btn_test_smtp", use_container_width=True):
                    target = email_recup.strip() or smtp_usr.strip()
                    st.info(f"Disparando e-mail de teste para: {target}...")
                    t_ok, t_msg = send_password_reset_email(
                        to_email=target,
                        user_name="Usuário Teste",
                        username="teste.radar",
                        temp_password="B3@Teste2026"
                    )
                    if t_ok:
                        st.success(f"✅ {t_msg}")
                    else:
                        st.error(f"❌ {t_msg}")

        if st.button("← Voltar para o Login", key="btn_reset_to_login", use_container_width=True):
            clear_login_fields()
            st.session_state["view"] = "login"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

def render_help_view():
    """Tela de Ajuda e Glossário Executivo do Dividend Radar B3."""
    col_back, _ = st.columns([1, 4])
    with col_back:
        if st.button("← 🏠 Home (Voltar à Página Principal)", key="help_btn_back"):
            st.session_state["view"] = "dashboard"
            st.rerun()

    st.markdown("### ❓ Central de Ajuda & Metodologia Executiva")
    st.caption("Guia rápido para interpretação das métricas, valuation e uso da plataforma.")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(r"""
        #### 📐 Metodologia de Valuation
        - **Preço Teto de Décio Bazin (Yield 6%)**:
          $$	ext{Preço Teto} = rac{	ext{DPA Médio (12M)}}{0{,}06}$$
          *Indica o preço máximo a pagar para obter no mínimo 6% ao ano em proventos.*
        - **Valor Justo de Benjamin Graham**:
          $$V = \sqrt{22{,}5 	imes 	ext{LPA} 	imes 	ext{VPA}}$$
          *Métrica clássica de Value Investing considerando lucros e valor patrimonial.*
        - **Score Multicritério B3**:
          Combinação ponderada de Dividend Yield (35%), ROE (25%), Solvência/Dívida (20%) e Notícias B3 (20%).
        """)
    with c2:
        st.markdown("""
        #### 💼 Gestão da Carteira Real
        - **Preço Médio (PM)**: Recalculado automaticamente a cada aporte via média ponderada.
        - **Alertas de Queda (Preço < PM)**: Avisam quando ativos de qualidade caem abaixo do seu custo de compra, abrindo chance de baixar o PM.
        - **Alertas de Dividendos do Mês**: Cruzamento automático entre quantidade em custódia e calendário de pagamentos da B3.
        - **Detector de Ações**: Digite qualquer valor máximo (ex: R$ 10,00) para encontrar ativos com alto potencial de crescimento e fluxo regular.
        """)
