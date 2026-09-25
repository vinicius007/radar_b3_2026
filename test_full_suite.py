import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

"""
Bateria de Testes Automatizados para o DIVIDEND RADAR B3.
Valida integridade do usuário master, CRUD de contas, 7 KPIs da carteira,
Detector de Ações, 4 Grandes Rankings e Feeds de Notícias.
"""

import os
import json
import pandas as pd
from src.auth.user_manager import (
    get_user_profile,
    create_user,
    update_user_profile,
    change_user_password,
    delete_user_account,
    authenticate_user,
    validate_password_strength,
    ensure_master_user_exists
)
from src.data.portfolio_manager import (
    get_portfolio_summary,
    load_transactions,
    add_transaction,
    delete_transaction,
    get_portfolio_monthly_dividend_alerts,
    get_portfolio_dip_alerts,
    get_portfolio_dividend_history
)
from src.engine.recommender import get_ranked_recommendations
from src.agent.radarzinha_engine import RadarzinhaEngine, get_radarzinha_response

def test_master_user():
    print("=== [1/6] Testando Usuário Master ===")
    ensure_master_user_exists()
    
    paths = [
        os.path.join("Usuario", "Master", "dados_perfil.json"),
        os.path.join("Usuario", "masterradar", "dados_perfil.json"),
        os.path.join("data", "masterradar", "dados_perfil.json")
    ]
    for p in paths:
        assert os.path.exists(p), f"Arquivo não encontrado: {p}"
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
            assert data["usuario"] == "masterradar"
            assert data["email"] == "viniciusamarques2026@gmail.com"
            assert data["nome_completo"] == "Vinicius Augusto Marques"
            assert data["data_nascimento"] == "19/10/1975"
            assert data["telefone"] == "+556256454544"
            assert data["senha"] == "@Blm1975"
            assert data["nao_resido_brasil"] is True
            assert data["termos_uso_privacidade"] is True
            print(f"  ✓ Validado com sucesso: {p}")
            
    # Testar autenticação
    u1 = authenticate_user("masterradar", "@Blm1975")
    assert u1 is not None, "Falha ao autenticar por usuário masterradar"
    u2 = authenticate_user("viniciusamarques2026@gmail.com", "@Blm1975")
    assert u2 is not None, "Falha ao autenticar por e-mail"
    print("  ✓ Autenticação do masterradar por login e e-mail OK!")

def test_user_crud():
    print("=== [2/6] Testando CRUD de Novos Usuários e Validações ===")
    
    # 1. Senha fraca rejeitada
    ok, msg = create_user("Investidor Teste", "user_test", "teste@email.com", "01/01/1990", "+551199999999", "123", "123", True, declaracao_responsabilidade=True)
    assert not ok, "Deveria rejeitar senha fraca"
    print("  ✓ Senha fraca rejeitada com sucesso.")
    
    # 2. Cadastro sem confirmação da Declaração de Responsabilidade rejeitado
    ok_decl, msg_decl = create_user("Investidor Teste", "user_test", "teste@email.com", "01/01/1990", "+551199999999", "@Investidor2026", "@Investidor2026", True, declaracao_responsabilidade=False)
    assert not ok_decl, "Deveria rejeitar cadastro sem confirmação da Declaração de Responsabilidade"
    assert "Declaração de Responsabilidade" in msg_decl
    print("  ✓ Rejeição por falta de Declaração de Responsabilidade validada com sucesso.")

    # 3. Cadastro válido com Declaração Confirmada
    ok, msg = create_user("Investidor Teste", "user_test", "teste@email.com", "01/01/1990", "+551199999999", "@Investidor2026", "@Investidor2026", True, declaracao_responsabilidade=True)
    assert ok, f"Falha ao criar usuário: {msg}"
    print("  ✓ Usuário de teste criado com sucesso com Declaração confirmada.")
    
    # 4. Tentativa de duplicidade rejeitada
    ok_dup, _ = create_user("Investidor Teste 2", "user_test", "outro@email.com", "01/01/1990", "+551199999999", "@Investidor2026", "@Investidor2026", True, declaracao_responsabilidade=True)
    assert not ok_dup, "Deveria rejeitar duplicidade de login"
    print("  ✓ Duplicidade de login prevenida com sucesso.")

    # 4. Alteração de perfil
    ok_up, _ = update_user_profile("user_test", "Investidor Atualizado", "02/02/1992", "+551188888888", False, True)
    assert ok_up, "Falha ao atualizar perfil"
    prof = get_user_profile("user_test")
    assert prof["nome_completo"] == "Investidor Atualizado"
    assert prof["usuario"] == "user_test", "Usuário não deve ser alterado"
    print("  ✓ Alteração de perfil e proteção de login OK.")
    
    # 5. Exclusão permanente (Zona de Perigo)
    del_ok, _ = delete_user_account("user_test")
    assert del_ok, "Falha ao excluir conta"
    assert get_user_profile("user_test") is None, "Conta ainda existe após exclusão"
    print("  ✓ Exclusão permanente de conta OK.")

def test_portfolio_7_kpis():
    print("=== [3/6] Testando os 7 KPIs e Carteira Segregada ===")
    ranked_df = get_ranked_recommendations(force_refresh=False)
    summary = get_portfolio_summary(ranked_df, username="masterradar")
    
    assert summary["is_empty"] is False, "Carteira do masterradar não deveria estar vazia"
    assert summary["total_invested"] > 0, "Total Investido deve ser positivo"
    assert summary["total_current_value"] > 0, "Patrimônio Real deve ser positivo"
    assert "total_profit_loss" in summary
    assert "total_profit_loss_pct" in summary
    assert summary["total_annual_dividends"] > 0, "Proventos anuais devem ser calculados"
    assert summary["total_monthly_dividends"] > 0, "Proventos mensais devem ser calculados"
    assert "monthly_return_pct" in summary, "Rentabilidade vs mês anterior deve estar presente"
    assert "current_month_dividends" in summary, "Dividendos do mês devem estar presentes"
    assert "total_dividends_since_purchase" in summary, "Proventos desde a compra devem estar presentes"
    
    print(f"  ✓ 1. Total Investido de Compra: R$ {summary['total_invested']:,.2f}")
    print(f"  ✓ 2. Patrimônio Real Atual: R$ {summary['total_current_value']:,.2f}")
    print(f"  ✓ 3. Lucro / Prejuízo Consolidado: R$ {summary['total_profit_loss']:,.2f} ({summary['total_profit_loss_pct']:+.2f}%)")
    print(f"  ✓ 4. Proventos Anuais & Mensais: R$ {summary['total_annual_dividends']:,.2f} (R$ {summary['total_monthly_dividends']:,.2f}/mês)")
    print(f"  ✓ 5. Rentabilidade vs Mês Anterior: {summary['monthly_return_pct']:+.2f}%")
    print(f"  ✓ 6. Total Dividendos no Mês: R$ {summary['current_month_dividends']:,.2f}")
    print(f"  ✓ 7. Total Dividendos Desde Compra: R$ {summary['total_dividends_since_purchase']:,.2f}")

def test_alerts_and_history():
    print("=== [4/6] Testando Alertas e Gráfico Histórico de Dividendos ===")
    ranked_df = get_ranked_recommendations(force_refresh=False)
    summary = get_portfolio_summary(ranked_df, username="masterradar")
    
    alerts = get_portfolio_monthly_dividend_alerts(summary, target_month=9)
    assert "target_month" in alerts
    print(f"  ✓ Alertas do Mês (Setembro): {len(alerts['paying_stocks'])} ações pagadoras detectadas.")
    
    dips = get_portfolio_dip_alerts(summary, ranked_df)
    assert "has_dip_alerts" in dips
    print(f"  ✓ Alertas Preço < PM: {dips['dip_count']} ações monitoradas.")

    hist = get_portfolio_dividend_history(summary, period_type="6m", meta_goal=2000.0)
    assert len(hist["month_codes"]) == 6
    assert len(hist["values"]) == 6
    print(f"  ✓ Histórico de Dividendos 6 Meses: {hist['month_codes']} - Total: R$ {hist['total_period']:,.2f}")

def test_detector_and_rankings():
    print("=== [5/6] Testando Detector de Ações e 4 Grandes Rankings ===")
    ranked_df = get_ranked_recommendations(force_refresh=False)
    
    # Detector abaixo de R$ 10
    sub10 = ranked_df[ranked_df["price"] <= 10.0]
    print(f"  ✓ Ações abaixo de R$ 10,00 detectadas na B3: {len(sub10)} ativos.")
    
    # 4 Rankings
    opp = ranked_df.sort_values(by="graham_margin_safety", ascending=False)
    print(f"  ✓ 1. Maior Oportunidade Graham: {opp.iloc[0]['ticker_clean']} ({opp.iloc[0]['graham_margin_safety']:+.1f}%)")
    
    div = ranked_df.sort_values(by="dy_12m", ascending=False)
    print(f"  ✓ 2. Maior Pagadora DY 12M: {div.iloc[0]['ticker_clean']} ({div.iloc[0]['dy_12m']:.2f}%)")
    
    grow = ranked_df.sort_values(by="dividend_cagr_3y", ascending=False)
    print(f"  ✓ 3. Que Mais Cresceu CAGR 3Y: {grow.iloc[0]['ticker_clean']} ({grow.iloc[0]['dividend_cagr_3y']:+.1f}%)")
    
    val = ranked_df[ranked_df["pl"] > 0].sort_values(by="pl", ascending=True)
    print(f"  ✓ 4. Que Menos Cresceu / Menor P/L: {val.iloc[0]['ticker_clean']} (P/L {val.iloc[0]['pl']:.1f}x)")

def test_radarzinha_agent():
    print("=== [6/6] Testando Agente Inteligente Radarzinha (Voz & Conhecimento) ===")
    engine = RadarzinhaEngine()
    
    # 1. Teste de Saudação e Voz
    assert "Radarzinha" in engine.GREETING, "Saudação deve conter nome da Radarzinha"
    assert "liberdade financeira" in engine.VOICE_INTRO, "Intro de voz deve mencionar liberdade financeira"
    print("  ✓ Persona e saudações da Radarzinha validadas com sucesso.")

    # 2. Teste de Extração de Valores Monetários
    val1 = engine.extract_monetary_value("Quero receber 2.000 reais mensais")
    assert val1 == 2000.0, f"Falha na extração de 2000: {val1}"
    val2 = engine.extract_monetary_value("Como ganhar 5 mil por mês?")
    assert val2 == 5000.0, f"Falha na extração de 5 mil: {val2}"
    print("  ✓ Extração de metas monetárias (R$ X mensais) OK.")

    # 3. Teste de Dúvida: Momento de Compra e Venda
    ans_cv, tts_cv = engine.generate_response("em qual momento devo comprar e vender determinada ação da minha carteira?")
    assert "DEVE COMPRAR" in ans_cv
    assert "DEVE VENDER" in ans_cv
    assert "Teto" in ans_cv
    assert len(tts_cv) > 20
    print("  ✓ Orientações de Momento de Compra e Venda validadas.")

    # 4. Teste de Dúvida: Montagem de Carteira de R$ X
    ans_x, tts_x = engine.generate_response("como montar uma carteira para ter retorno de 3000 reais mensais")
    assert "3.000" in ans_x
    assert "BEST" in ans_x
    print("  ✓ Planejamento de carteira para meta mensal (R$ 3.000) validado.")

    # 5. Teste de Dúvida: Siglas e Termos da B3
    ans_sig, tts_sig = engine.generate_response("me explique o que é DY, P/L, ROE e Preço Teto de Bazin")
    assert "Dividend Yield" in ans_sig
    assert "Lucro" in ans_sig
    assert "Bazin" in ans_sig
    print("  ✓ Glossário e siglas da B3 explicados com precisão.")

    # 6. Teste de Contexto da Carteira do Usuário
    ans_usr, tts_usr = engine.generate_response("como está minha carteira?", username="masterradar")
    assert "Total Investido" in ans_usr or "carteira" in ans_usr
    print("  ✓ Integração contextual com a carteira real do investidor OK.")

def main():
    print("\n🚀 INICIANDO TESTES DO DIVIDEND RADAR B3...\n")
    test_master_user()
    test_user_crud()
    test_portfolio_7_kpis()
    test_alerts_and_history()
    test_detector_and_rankings()
    test_radarzinha_agent()
    print("\n=======================================================")
    print("🎉 TODOS OS TESTES PASSARAM COM 100% DE SUCESSO!")
    print("=======================================================\n")

if __name__ == "__main__":
    main()
