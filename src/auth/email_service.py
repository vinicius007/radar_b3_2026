"""
Serviço de E-mail para Redefinição de Senha e Notificações - Radar B3.
Implementa envio seguro via SMTP (Gmail / TLS / SSL) com suporte a templates
em texto puro e HTML executivo.
"""

import os
import json
import smtplib
import ssl
import re
import secrets
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any, Tuple, Optional

# Diretório base para persistência de dados
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")
SMTP_CONFIG_FILE = os.path.join(DATA_DIR, "smtp_config.json")

# Configurações padrão para envio de e-mails via Gmail
DEFAULT_SMTP_CONFIG = {
    "server": "smtp.gmail.com",
    "port": 587,
    "user": "constecinf@gmail.com",
    "password": "",  # Senha de aplicativo do Google (16 caracteres)
    "sender_name": "Radar B3",
    "use_tls": True,
    "use_ssl": False,
    "support_email": "constecinf@gmail.com",
    "platform_url": "https://relatorio-executivo-de-proventos.onrender.com"
}

def load_smtp_config() -> Dict[str, Any]:
    """
    Carrega as configurações SMTP com ordem de prioridade:
    1. Arquivo data/smtp_config.json
    2. Streamlit secrets (se disponíveis via st.secrets)
    3. Variáveis de ambiente do sistema
    4. Valores padrão pré-definidos
    """
    config = dict(DEFAULT_SMTP_CONFIG)

    # 1. Carregar de arquivo local se existir
    if os.path.exists(SMTP_CONFIG_FILE):
        try:
            with open(SMTP_CONFIG_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f)
                config.update(saved)
        except Exception as e:
            print(f"[EmailService] Erro ao ler {SMTP_CONFIG_FILE}: {e}")

    # 2. Tentar carregar do Streamlit secrets
    try:
        import streamlit as st
        if hasattr(st, "secrets"):
            if "smtp" in st.secrets:
                s_dict = dict(st.secrets["smtp"])
                config.update({k.lower(): v for k, v in s_dict.items()})
            if "SMTP_PASSWORD" in st.secrets and not config.get("password"):
                config["password"] = str(st.secrets["SMTP_PASSWORD"])
            if "SMTP_USER" in st.secrets:
                config["user"] = str(st.secrets["SMTP_USER"])
            if "SMTP_SERVER" in st.secrets:
                config["server"] = str(st.secrets["SMTP_SERVER"])
            if "SMTP_PORT" in st.secrets:
                config["port"] = int(st.secrets["SMTP_PORT"])
    except Exception:
        pass

    # 3. Variáveis de ambiente
    if os.getenv("SMTP_SERVER"):
        config["server"] = os.getenv("SMTP_SERVER")
    if os.getenv("SMTP_PORT"):
        try:
            config["port"] = int(os.getenv("SMTP_PORT"))
        except ValueError:
            pass
    if os.getenv("SMTP_USER") or os.getenv("EMAIL_USER"):
        config["user"] = os.getenv("SMTP_USER") or os.getenv("EMAIL_USER")
    if os.getenv("SMTP_PASSWORD") or os.getenv("EMAIL_PASSWORD") or os.getenv("GMAIL_APP_PASSWORD"):
        config["password"] = (
            os.getenv("SMTP_PASSWORD") or 
            os.getenv("EMAIL_PASSWORD") or 
            os.getenv("GMAIL_APP_PASSWORD")
        )
    if os.getenv("SMTP_SENDER_NAME"):
        config["sender_name"] = os.getenv("SMTP_SENDER_NAME")

    # Limpar possíveis espaços na senha de app
    if config.get("password"):
        config["password"] = str(config["password"]).replace(" ", "").strip()

    return config

def save_smtp_config(config_updates: Dict[str, Any]) -> bool:
    """Salva configurações SMTP atualizadas no arquivo data/smtp_config.json."""
    os.makedirs(DATA_DIR, exist_ok=True)
    current = load_smtp_config()
    current.update(config_updates)
    try:
        with open(SMTP_CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(current, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"[EmailService] Erro ao salvar {SMTP_CONFIG_FILE}: {e}")
        return False

def generate_temporary_password() -> str:
    """
    Gera uma senha provisória aleatória de 10 caracteres que atende estritamente
    a todos os critérios de segurança (maiúscula, minúscula, número e caractere especial),
    garantindo nota máxima no validador.
    """
    specials = "@#$%&*"
    chars = [
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.digits),
        secrets.choice(specials),
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.digits),
        secrets.choice(specials),
    ]
    secrets.SystemRandom().shuffle(chars)
    return "B3" + "".join(chars)

def build_password_reset_email_text(user_name: str, username: str, temp_password: str) -> str:
    """
    Gera o corpo do e-mail em texto puro conforme o modelo estipulado pelo usuário.
    """
    display_name = user_name.strip() if user_name else username
    return f"""Assunto: Radar B3 - Redefinição de senha solicitada
		
Olá, {display_name},

Recebemos uma solicitação para redefinir a senha da sua conta [{username}].

Segue abaixo a senha provisoria: 

{temp_password}

Lembre-se de alterar a senha após logar.

Se você não solicitou a redefinição, ignore este e-mail. Sua senha atual continuará funcionando normalmente.

Por segurança, nunca compartilhe sua senha com ninguém.

Se precisar de ajuda, entre em contato com nosso suporte: [constecinf@gmail.com].

Atenciosamente,

Equipe  Radar B3

https://relatorio-executivo-de-proventos.onrender.com
""".strip()

def build_password_reset_email_html(user_name: str, username: str, temp_password: str) -> str:
    """
    Gera a versão HTML formatada e executiva do e-mail, mantendo a identidade visual
    do Radar B3 e perfeita compatibilidade com Gmail, Outlook e dispositivos móveis.
    """
    display_name = user_name.strip() if user_name else username
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Radar B3 - Redefinição de Senha</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            background-color: #0F172A;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            color: #F8FAFC;
        }}
        .container {{
            max-width: 600px;
            margin: 24px auto;
            background-color: #1E293B;
            border-radius: 12px;
            border: 1px solid #334155;
            overflow: hidden;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
        }}
        .header {{
            background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
            padding: 28px 24px;
            text-align: center;
            border-bottom: 2px solid #F59E0B;
        }}
        .header h1 {{
            margin: 0;
            font-size: 22px;
            font-weight: 800;
            color: #F8FAFC;
            letter-spacing: -0.5px;
        }}
        .header span {{
            color: #F59E0B;
        }}
        .content {{
            padding: 32px 24px;
            font-size: 15px;
            line-height: 1.6;
            color: #E2E8F0;
        }}
        .content p {{
            margin: 0 0 16px 0;
        }}
        .badge-box {{
            background-color: #0B1120;
            border: 1px solid #38BDF8;
            border-left: 4px solid #38BDF8;
            border-radius: 8px;
            padding: 16px 20px;
            margin: 24px 0;
            text-align: center;
        }}
        .badge-box .label {{
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #94A3B8;
            margin-bottom: 8px;
            font-weight: 700;
        }}
        .badge-box .password {{
            font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, Courier, monospace;
            font-size: 22px;
            font-weight: 800;
            color: #38BDF8;
            letter-spacing: 3px;
        }}
        .button {{
            display: inline-block;
            background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
            color: #0F172A !important;
            font-weight: 800;
            font-size: 15px;
            text-decoration: none;
            padding: 14px 28px;
            border-radius: 8px;
            margin: 20px 0;
            text-align: center;
        }}
        .alert-box {{
            background: rgba(245, 158, 11, 0.1);
            border-left: 3px solid #F59E0B;
            padding: 12px 16px;
            border-radius: 4px;
            font-size: 13px;
            color: #FDE68A;
            margin: 20px 0;
        }}
        .footer {{
            background-color: #0F172A;
            padding: 20px 24px;
            text-align: center;
            font-size: 12px;
            color: #64748B;
            border-top: 1px solid #334155;
        }}
        .footer a {{
            color: #38BDF8;
            text-decoration: none;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>RADAR <span>B3</span> &bull; INTELIGÊNCIA EM DIVIDENDOS</h1>
        </div>
        <div class="content">
            <p>Olá, <strong>{display_name}</strong>,</p>
            <p>Recebemos uma solicitação para redefinir a senha da sua conta <strong>[{username}]</strong>.</p>
            <p>Segue abaixo a senha provisória:</p>
            
            <div class="badge-box">
                <div class="label">Sua Senha Provisória</div>
                <div class="password">{temp_password}</div>
            </div>

            <div class="alert-box">
                ⚠️ <strong>Atenção:</strong> Lembre-se de alterar a senha após efetuar o login.
            </div>

            <div style="text-align: center;">
                <a href="https://relatorio-executivo-de-proventos.onrender.com" class="button" target="_blank">
                    🚀 Acessar Plataforma Radar B3
                </a>
            </div>

            <p style="margin-top: 24px;">Se você não solicitou a redefinição, ignore este e-mail. Sua senha atual continuará funcionando normalmente.</p>
            <p>Por segurança, nunca compartilhe sua senha com ninguém.</p>
            <p>Se precisar de ajuda, entre em contato com nosso suporte: <a href="mailto:constecinf@gmail.com" style="color: #38BDF8;">constecinf@gmail.com</a>.</p>
            
            <p style="margin-top: 28px; line-height: 1.4;">
                Atenciosamente,<br>
                <strong>Equipe Radar B3</strong><br>
                <a href="https://relatorio-executivo-de-proventos.onrender.com" style="color: #F59E0B; font-size: 13px;">https://relatorio-executivo-de-proventos.onrender.com</a>
            </p>
        </div>
        <div class="footer">
            &copy; 2026 Radar B3 &bull; Inteligência Executiva de Dividendos.<br>
            Este é um e-mail de serviço transacional automático gerado pelo sistema.
        </div>
    </div>
</body>
</html>
"""

def send_password_reset_email(to_email: str, user_name: str, username: str, temp_password: str) -> Tuple[bool, str]:
    """
    Envia o e-mail de recuperação de senha com a nova senha provisória via SMTP.
    Retorna (True, "Mensagem de sucesso") ou (False, "Detalhes do erro").
    """
    config = load_smtp_config()
    server_host = config.get("server", "smtp.gmail.com")
    server_port = int(config.get("port", 587))
    sender_user = config.get("user", "constecinf@gmail.com")
    sender_pwd = config.get("password", "")
    sender_name = config.get("sender_name", "Radar B3")
    use_tls = config.get("use_tls", True)
    use_ssl = config.get("use_ssl", False) or server_port == 465

    # Validar se há senha configurada
    if not sender_pwd:
        return False, "Senha de aplicativo SMTP não configurada. Configure a senha de aplicativo do e-mail remetente."

    # Criar mensagem MIME Multipart (Texto Puro + HTML)
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Radar B3 - Redefinição de senha solicitada"
    msg["From"] = f"{sender_name} <{sender_user}>"
    msg["To"] = to_email

    # Gerar conteúdos
    text_content = build_password_reset_email_text(user_name, username, temp_password)
    html_content = build_password_reset_email_html(user_name, username, temp_password)

    part_text = MIMEText(text_content, "plain", "utf-8")
    part_html = MIMEText(html_content, "html", "utf-8")

    msg.attach(part_text)
    msg.attach(part_html)

    try:
        if use_ssl:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(server_host, server_port, context=context, timeout=15) as server:
                server.login(sender_user, sender_pwd)
                server.sendmail(sender_user, [to_email], msg.as_string())
        else:
            with smtplib.SMTP(server_host, server_port, timeout=15) as server:
                server.ehlo()
                if use_tls:
                    context = ssl.create_default_context()
                    server.starttls(context=context)
                    server.ehlo()
                server.login(sender_user, sender_pwd)
                server.sendmail(sender_user, [to_email], msg.as_string())

        return True, f"E-mail de redefinição enviado com sucesso para {to_email}!"

    except smtplib.SMTPAuthenticationError as e:
        return False, (
            "Falha de autenticação SMTP: Usuário ou senha de aplicativo do Gmail incorretos. "
            "Certifique-se de usar uma 'Senha de App' de 16 caracteres gerada na Conta Google."
        )
    except smtplib.SMTPConnectError as e:
        return False, f"Falha ao conectar ao servidor SMTP {server_host}:{server_port}: {e}"
    except smtplib.SMTPRecipientsRefused:
        return False, f"O endereço de destino '{to_email}' foi recusado pelo servidor de e-mail."
    except Exception as e:
        return False, f"Erro inesperado no envio de e-mail: {str(e)}"
