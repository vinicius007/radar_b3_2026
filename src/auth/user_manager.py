"""
Módulo de Gestão de Usuários e Autenticação do DIVIDEND RADAR B3.
Gerencia persistência em Usuario/<usuario>/ e data/<usuario>/,
regras de senha, cadastros, alterações de perfil, exclusão de conta e autenticação.
"""

import os
import json
import re
import shutil
from datetime import datetime
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
    return True, "Senha alterada com sucesso!"

def request_password_reset(email: str) -> Tuple[bool, str]:
    """Processa a solicitação de redefinição de senha."""
    clean_email = email.strip().lower()
    if not validate_email(clean_email):
        return False, "E-mail inválido. Digite um e-mail correto."
        
    found = False
    for u in list_all_users():
        if u.get("email", "").lower() == clean_email:
            found = True
            break
            
    if not found:
        return False, f"Nenhum usuário cadastrado com o e-mail '{clean_email}'."
        
    return True, f"Link de recuperação enviado com sucesso para {clean_email}! Verifique sua caixa de entrada."

def authenticate_user(username_or_email: str, password: str) -> Optional[Dict[str, Any]]:
    """Autentica usuário por login ou e-mail."""
    ensure_master_user_exists()
    clean_id = username_or_email.strip().lower()
    
    for u in list_all_users():
        if clean_id in [u.get("usuario", "").lower(), u.get("email", "").lower()]:
            if u.get("senha") == password:
                return u
    return None
