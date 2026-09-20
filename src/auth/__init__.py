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

from .email_service import (
    send_password_reset_email,
    generate_temporary_password,
    load_smtp_config,
    save_smtp_config,
    build_password_reset_email_text,
    build_password_reset_email_html
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
    "list_all_users",
    "send_password_reset_email",
    "generate_temporary_password",
    "load_smtp_config",
    "save_smtp_config",
    "build_password_reset_email_text",
    "build_password_reset_email_html"
]
