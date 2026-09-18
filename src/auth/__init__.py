"""
Módulo de Autenticação e Gestão de Usuários do DIVIDEND RADAR B3.
"""

from .user_manager import (
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
    ensure_master_user_exists,
    list_all_users
)

__all__ = [
    "get_user_profile",
    "save_user_profile",
    "create_user",
    "update_user_profile",
    "delete_user_account",
    "change_user_password",
    "request_password_reset",
    "authenticate_user",
    "validate_password_strength",
    "validate_email",
    "ensure_master_user_exists",
    "list_all_users"
]
