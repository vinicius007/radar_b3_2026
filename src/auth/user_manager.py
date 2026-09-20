"""
Módulo de Gestão de Usuários e Autenticação do DIVIDEND RADAR B3.
Gerencia persistência em Usuario/<usuario>/ e data/<usuario>/,
regras de senha, cadastros, alterações de perfil, exclusão de conta e autenticação.
"""

import os
import json
import re
import shutil
import secrets
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Tuple, List

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
USUARIOS_DIR = os.path.join(BASE_DIR, "Usuario")
DATA_DIR = os.path.join(BASE_DIR, "data")

def ensure_base_directories():
    os.makedirs(USUARIOS_DIR, exist_ok=True)
    os.makedirs(DATA_DIR, exist_ok=True)

def ensure_master_user_exists() -> Dict[str, Any]:
    """Garante que o usuário masterradar existe com os dados corretos conforme especificação."""
    ensure_base_directories()
    
    master_data = {
        "nome_completo": "Vinicius Augusto Marques",
        "usuario": "masterradar",
        "email": "viniciusamarques2026@gmail.com",
        "data_nascimento": "19/10/1975",
        "telefone": "+556256454544",
        "senha": "@Blm1975",
        "nao_resido_brasil": True,
        "termos_uso_privacidade": True,
        "avatar_letter": "V",
        "is_master": True,
        "criado_em": "2026-09-16T19:22:00"
    }
    
    paths = [
        os.path.join(USUARIOS_DIR, "Master", "dados_perfil.json"),
        os.path.join(USUARIOS_DIR, "masterradar", "dados_perfil.json"),
        os.path.join(DATA_DIR, "masterradar", "dados_perfil.json")
    ]
    
    for p in paths:
        d = os.path.dirname(p)
        os.makedirs(d, exist_ok=True)
        if not os.path.exists(p):
            with open(p, "w", encoding="utf-8") as f:
                json.dump(master_data, f, indent=2, ensure_ascii=False)
                
    return master_data

def get_user_profile(username: str) -> Optional[Dict[str, Any]]:
    """Carrega os dados de perfil de um usuário."""
    ensure_master_user_exists()
    clean_user = username.strip().lower()
    
    if clean_user in ["masterradar", "master"]:
        p = os.path.join(DATA_DIR, "masterradar", "dados_perfil.json")
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
        p_alt = os.path.join(USUARIOS_DIR, "masterradar", "dados_perfil.json")
        if os.path.exists(p_alt):
            with open(p_alt, "r", encoding="utf-8") as f:
                return json.load(f)
                
    p1 = os.path.join(DATA_DIR, clean_user, "dados_perfil.json")
    if os.path.exists(p1):
        with open(p1, "r", encoding="utf-8") as f:
            return json.load(f)
            
    p2 = os.path.join(USUARIOS_DIR, clean_user, "dados_perfil.json")
    if os.path.exists(p2):
        with open(p2, "r", encoding="utf-8") as f:
            return json.load(f)
            
    return None

def save_user_profile(username: str, data: Dict[str, Any]) -> bool:
    """Salva perfil em Usuario/<usuario> e data/<usuario>."""
    ensure_base_directories()
    clean_user = username.strip().lower()
    
    name = data.get("nome_completo", "")
    if name:
        data["avatar_letter"] = name.strip()[0].upper()
        
    targets = [
        os.path.join(USUARIOS_DIR, clean_user, "dados_perfil.json"),
        os.path.join(DATA_DIR, clean_user, "dados_perfil.json")
    ]
    
    if clean_user == "masterradar":
        targets.append(os.path.join(USUARIOS_DIR, "Master", "dados_perfil.json"))
        
    for target in targets:
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
    return True

def list_all_users() -> List[Dict[str, Any]]:
    """Lista todos os usuários registrados no sistema."""
    ensure_master_user_exists()
    users = []
    seen = set()
    
    if os.path.exists(USUARIOS_DIR):
        for entry in os.listdir(USUARIOS_DIR):
            p = os.path.join(USUARIOS_DIR, entry, "dados_perfil.json")
            if os.path.isfile(p):
                try:
                    with open(p, "r", encoding="utf-8") as f:
                        u = json.load(f)
                        login = u.get("usuario", entry).lower()
                        if login not in seen:
                            seen.add(login)
                            users.append(u)
                except Exception:
                    pass
                    
    if os.path.exists(DATA_DIR):
        for entry in os.listdir(DATA_DIR):
            p = os.path.join(DATA_DIR, entry, "dados_perfil.json")
            if os.path.isfile(p):
                try:
                    with open(p, "r", encoding="utf-8") as f:
                        u = json.load(f)
                        login = u.get("usuario", entry).lower()
                        if login not in seen:
                            seen.add(login)
                            users.append(u)
                except Exception:
                    pass
                    
    return users

def validate_email(email: str) -> bool:
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(pattern, email.strip()))

def validate_password_strength(password: str) -> Tuple[bool, List[str], int]:
    """Valida se a nova senha atende: mín 8 chars, maiúscula, minúscula, número e especial."""
    errors = []
    score = 0
    
    if len(password) >= 8:
        score += 25
    else:
        errors.append("Mínimo de 8 caracteres.")
        
    if re.search(r"[A-Z]", password):
        score += 25
    else:
        errors.append("Pelo menos uma letra maiúscula.")
        
    if re.search(r"[a-z]", password):
        score += 25
    else:
        errors.append("Pelo menos uma letra minúscula.")
        
    has_digit = bool(re.search(r"[0-9]", password))
    has_spec = bool(re.search(r"[\W_]", password))
    
    if has_digit and has_spec:
        score += 25
    else:
        if not has_digit:
            errors.append("Pelo menos um número.")
        if not has_spec:
            errors.append("Pelo menos um caractere especial.")
            
    is_valid = len(errors) == 0
    return is_valid, errors, score

def create_user(nome_completo: str, usuario: str, email: str, data_nascimento: str, telefone: str,
                senha: str, confirmar_senha: str, termos_uso: bool, nao_resido_brasil: bool = False) -> Tuple[bool, str]:
    """Cadastra novo usuário garantindo validação de duplicidade e regras de negócio."""
    if len(nome_completo.strip()) < 5:
        return False, "O Nome Completo deve ter no mínimo 5 caracteres."
        
    clean_user = usuario.strip().lower()
    if not clean_user or len(clean_user) < 3:
        return False, "O Usuário deve ter no mínimo 3 caracteres."
        
    if not re.match(r"^[a-zA-Z0-9_\.]+$", clean_user):
        return False, "O Usuário deve conter apenas letras, números, ponto ou underline."
        
    for u in list_all_users():
        if u.get("usuario", "").lower() == clean_user:
            return False, f"O Usuário '{clean_user}' já está cadastrado."
            
    clean_email = email.strip().lower()
    if not validate_email(clean_email):
        return False, "E-mail inválido. Utilize um formato válido (ex: nome@exemplo.com)."
        
    for u in list_all_users():
        if u.get("email", "").lower() == clean_email:
            return False, f"O E-mail '{clean_email}' já está em uso por outra conta."
            
    clean_nasc = data_nascimento.strip()
    if not clean_nasc:
        return False, "A Data de Nascimento é obrigatória."
        
    clean_tel = telefone.strip()
    if not clean_tel or len(clean_tel) < 8:
        return False, "O Telefone é obrigatório."
        
    is_valid_pwd, pwd_errors, _ = validate_password_strength(senha)
    if not is_valid_pwd:
        return False, "Senha não atende aos requisitos: " + " ".join(pwd_errors)
        
    if senha != confirmar_senha:
        return False, "A confirmação de senha não coincide com a nova senha digitada."
        
    if not termos_uso:
        return False, "É obrigatório concordar com os Termos de Uso e Política de Privacidade (LGPD)."
        
    new_profile = {
        "nome_completo": nome_completo.strip(),
        "usuario": clean_user,
        "email": clean_email,
        "data_nascimento": clean_nasc,
        "telefone": clean_tel,
        "senha": senha,
        "nao_resido_brasil": bool(nao_resido_brasil),
        "termos_uso_privacidade": True,
        "avatar_letter": nome_completo.strip()[0].upper(),
        "is_master": False,
        "criado_em": datetime.now().isoformat()
    }
    
    save_user_profile(clean_user, new_profile)
    return True, f"Usuário '{clean_user}' cadastrado com sucesso!"

def update_user_profile(username: str, nome_completo: str, data_nascimento: str, telefone: str,
                        nao_resido_brasil: bool, termos_uso: bool) -> Tuple[bool, str]:
    """Altera informações do perfil. Não permite alterar Usuário nem E-mail."""
    user_data = get_user_profile(username)
    if not user_data:
        return False, "Usuário não encontrado."
        
    if len(nome_completo.strip()) < 5:
        return False, "O Nome Completo deve ter no mínimo 5 caracteres."
        
    if not data_nascimento.strip():
        return False, "Data de nascimento é obrigatória."
        
    if not telefone.strip():
        return False, "Telefone é obrigatório."
        
    user_data["nome_completo"] = nome_completo.strip()
    user_data["data_nascimento"] = data_nascimento.strip()
    user_data["telefone"] = telefone.strip()
    user_data["nao_resido_brasil"] = bool(nao_resido_brasil)
    user_data["termos_uso_privacidade"] = bool(termos_uso)
    user_data["avatar_letter"] = nome_completo.strip()[0].upper()
    user_data["atualizado_em"] = datetime.now().isoformat()
    
    save_user_profile(username, user_data)
    return True, "Informações atualizadas com sucesso!"

def delete_user_account(username: str) -> Tuple[bool, str]:
    """Exclui permanentemente a conta e os dados de carteira do usuário."""
    clean_user = username.strip().lower()
    
    folders_to_delete = [
        os.path.join(USUARIOS_DIR, clean_user),
        os.path.join(DATA_DIR, clean_user)
    ]
    
    for folder in folders_to_delete:
        if os.path.exists(folder):
            try:
                shutil.rmtree(folder)
            except Exception as e:
                print(f"Erro ao remover pasta {folder}: {e}")
                
    revoke_all_user_kmsi_tokens(clean_user)
    return True, f"A conta do usuário '{clean_user}' e todos os seus dados foram apagados permanentemente."

def change_user_password(username: str, current_pwd: str, new_pwd: str, confirm_pwd: str) -> Tuple[bool, str]:
    """Altera a senha com verificação de requisitos de segurança."""
    user_data = get_user_profile(username)
    if not user_data:
        return False, "Usuário não encontrado."
        
    if user_data.get("senha") != current_pwd:
        return False, "A Senha Atual digitada está incorreta."
        
    is_valid, errors, _ = validate_password_strength(new_pwd)
    if not is_valid:
        return False, "A nova senha deve conter pelo menos 8 caracteres, ser composta por maiúscula, minúscula, um número e um caractere especial."
        
    if new_pwd != confirm_pwd:
        return False, "A confirmação não coincide com a nova senha."
        
    user_data["senha"] = new_pwd
    user_data["senha_atualizada_em"] = datetime.now().isoformat()
    save_user_profile(username, user_data)
    revoke_all_user_kmsi_tokens(username)
    return True, "Senha alterada com sucesso!"

def request_password_reset(email: str) -> Tuple[bool, str, Dict[str, Any]]:
    """
    Processa a solicitação de redefinição de senha:
    1. Valida o e-mail e localiza o usuário cadastrado correspondente.
    2. Gera uma senha provisória forte e compatível com as regras de segurança.
    3. Atualiza os dados de perfil do usuário (em Usuario/ e data/).
    4. Revoga as sessões ativas (KMSI) para segurança.
    5. Dispara o e-mail oficial com a nova senha provisória.
    """
    clean_email = email.strip().lower()
    if not validate_email(clean_email):
        return False, "E-mail inválido. Digite um e-mail correto.", {}
        
    found_user = None
    for u in list_all_users():
        if u.get("email", "").lower() == clean_email:
            found_user = u
            break
            
    if not found_user:
        return False, f"Nenhum usuário cadastrado com o e-mail '{clean_email}'.", {}

    username = found_user.get("usuario", "")
    full_profile = get_user_profile(username) or found_user
    user_display_name = full_profile.get("nome_completo", username)

    # Gerar senha provisória forte (maiúscula, minúscula, dígito e símbolo)
    from src.auth.email_service import generate_temporary_password, send_password_reset_email
    temp_pwd = generate_temporary_password()

    # Atualizar perfil do usuário com a nova senha provisória
    full_profile["senha"] = temp_pwd
    full_profile["senha_provisoria"] = True
    full_profile["senha_atualizada_em"] = datetime.now().isoformat()
    save_user_profile(username, full_profile)
    revoke_all_user_kmsi_tokens(username)

    # Disparar e-mail de redefinição com a senha provisória
    email_sent, email_msg = send_password_reset_email(
        to_email=clean_email,
        user_name=user_display_name,
        username=username,
        temp_password=temp_pwd
    )

    details = {
        "email": clean_email,
        "usuario": username,
        "nome_completo": user_display_name,
        "temp_pwd": temp_pwd,
        "email_sent": email_sent,
        "email_msg": email_msg
    }

    if email_sent:
        return True, f"E-mail de redefinição enviado com sucesso para {clean_email} com sua nova senha provisória! Verifique sua caixa de entrada e pasta de Spam.", details
    else:
        return True, f"Nova senha provisória ativada para sua conta! (Aviso: O serviço de e-mail não pôde enviar a mensagem automaticamente: {email_msg})", details

def authenticate_user(username_or_email: str, password: str) -> Optional[Dict[str, Any]]:
    """Autentica usuário por login ou e-mail."""
    ensure_master_user_exists()
    clean_id = username_or_email.strip().lower()
    
    for u in list_all_users():
        if clean_id in [u.get("usuario", "").lower(), u.get("email", "").lower()]:
            if u.get("senha") == password:
                return u
    return None

# -------------------------------------------------------------
# GESTÃO DE SESSÕES PROLONGADAS (KMSI - KEEP ME SIGNED IN)
# -------------------------------------------------------------
KMSI_FILE = os.path.join(USUARIOS_DIR, "kmsi_sessions.json")

def _load_kmsi_sessions() -> Dict[str, Any]:
    ensure_base_directories()
    if os.path.exists(KMSI_FILE):
        try:
            with open(KMSI_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def _save_kmsi_sessions(sessions: Dict[str, Any]):
    ensure_base_directories()
    try:
        with open(KMSI_FILE, "w", encoding="utf-8") as f:
            json.dump(sessions, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Erro ao salvar sessões KMSI: {e}")

def create_kmsi_token(username: str, days: int = 30) -> str:
    """Cria e armazena um token criptográfico para manter a sessão prolongada (KMSI)."""
    raw_token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(raw_token.encode("utf-8")).hexdigest()
    
    sessions = _load_kmsi_sessions()
    now = datetime.now()
    valid_sessions = {}
    for h, data in sessions.items():
        try:
            exp = datetime.fromisoformat(data.get("expires_at", ""))
            if exp > now:
                valid_sessions[h] = data
        except Exception:
            pass

    valid_sessions[token_hash] = {
        "usuario": username.strip().lower(),
        "created_at": now.isoformat(),
        "expires_at": (now + timedelta(days=days)).isoformat()
    }
    _save_kmsi_sessions(valid_sessions)
    return raw_token

def validate_kmsi_token(raw_token: str) -> Optional[str]:
    """Valida um token KMSI. Retorna o username se válido e não expirado, ou None."""
    if not raw_token or not isinstance(raw_token, str):
        return None
        
    token_hash = hashlib.sha256(raw_token.strip().encode("utf-8")).hexdigest()
    sessions = _load_kmsi_sessions()
    
    session = sessions.get(token_hash)
    if not session:
        return None
        
    try:
        expires_at = datetime.fromisoformat(session.get("expires_at", ""))
        if expires_at <= datetime.now():
            del sessions[token_hash]
            _save_kmsi_sessions(sessions)
            return None
        return session.get("usuario")
    except Exception:
        return None

def revoke_kmsi_token(raw_token: str) -> bool:
    """Revoga explicitamente um token KMSI (utilizado no logout)."""
    if not raw_token or not isinstance(raw_token, str):
        return False
    token_hash = hashlib.sha256(raw_token.strip().encode("utf-8")).hexdigest()
    sessions = _load_kmsi_sessions()
    if token_hash in sessions:
        del sessions[token_hash]
        _save_kmsi_sessions(sessions)
        return True
    return False

def revoke_all_user_kmsi_tokens(username: str) -> bool:
    """Revoga todos os tokens KMSI de um usuário (ao excluir conta ou alterar senha)."""
    clean_u = username.strip().lower()
    sessions = _load_kmsi_sessions()
    new_sessions = {h: data for h, data in sessions.items() if data.get("usuario") != clean_u}
    _save_kmsi_sessions(new_sessions)
    return True

def get_user_monthly_goal(username: str) -> float:
    """Retorna a meta mensal de proventos do usuário (em R$)."""
    profile = get_user_profile(username)
    if not profile:
        return 0.0
    try:
        return float(profile.get("meta_mensal", 0.0))
    except Exception:
        return 0.0

def set_user_monthly_goal(username: str, goal: float) -> bool:
    """Atualiza a meta mensal de proventos do usuário."""
    profile = get_user_profile(username)
    if not profile:
        return False
    try:
        profile["meta_mensal"] = max(0.0, round(float(goal), 2))
        return save_user_profile(username, profile)
    except Exception:
        return False

