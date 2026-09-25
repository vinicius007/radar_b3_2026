"""
Motor de Inteligência e Base de Conhecimento da Radarzinha.
Mentora executiva e conselheira de dividendos da B3, com tom charmoso, inteligente, envolvente e acolhedor.
"""

import re
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
import pandas as pd

from src.data.portfolio_manager import get_portfolio_summary, get_portfolio_monthly_dividend_alerts
from src.data.b3_universe import B3_DIVIDEND_UNIVERSE

def fmt_brl(val: float) -> str:
    """Formata valor monetário no padrão brasileiro R$ 1.234,56."""
    try:
        return f"R$ {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return f"R$ {val}"

class RadarzinhaEngine:
    """Motor de IA conversacional da Radarzinha."""

    GREETING = (
        "Olá, meu querido investidor! Eu sou a **Radarzinha**, sua mentora particular e conselheira executiva "
        "aqui no Radar B3. 💃✨\n\n"
        "Estou aqui para te guiar rumo à sua liberdade financeira, te ensinando os segredos dos proventos, "
        "analisando suas ações favoritas, calculando sua renda passiva dos sonhos e te mostrando o momento exato "
        "de comprar e valorizar cada centavo do seu patrimônio. Como posso te encantar e te ajudar hoje, meu bem?"
    )

    VOICE_INTRO = (
        "Olá, meu querido investidor! Eu sou a Radarzinha, sua mentora particular de dividendos. "
        "Estou aqui para te guiar rumo à sua liberdade financeira com os melhores proventos da B3. "
        "Conte comigo para analisar sua carteira e acelerar sua renda passiva, meu bem!"
    )

    def __init__(self):
        pass

    def extract_monetary_value(self, text: str) -> Optional[float]:
        """Tenta extrair um valor monetário de perguntas do usuário (ex: 'R$ 2.000', '5 mil', '1500')."""
        clean = text.lower().replace(".", "").replace(",", ".")
        
        # Padrões como '5 mil', '10 mil', '5k'
        match_mil = re.search(r"(\d+(?:\.\d+)?)\s*(?:mil|k)", clean)
        if match_mil:
            try:
                return float(match_mil.group(1)) * 1000.0
            except ValueError:
                pass

        # Padrões como 'r$ 2500', '2500 reais', 'r$2.500,00'
        match_num = re.search(r"(?:r\$\s*)?(\d+(?:\.\d+)?)\s*(?:reais)?", clean)
        if match_num:
            try:
                val = float(match_num.group(1))
                if val >= 50:  # evitar números triviais como dias ou meses
                    return val
            except ValueError:
                pass
        return None

    def get_portfolio_context(self, username: Optional[str]) -> Dict[str, Any]:
        """Recupera dados em tempo real da carteira do investidor."""
        if not username:
            return {"has_portfolio": False}
        try:
            summary = get_portfolio_summary(username)
            pos_df = summary.get("positions_df")
            tickers = pos_df["ticker"].tolist() if (pos_df is not None and not pos_df.empty) else []
            below_pm = []
            if pos_df is not None and not pos_df.empty and "preco_mercado" in pos_df.columns and "preco_medio" in pos_df.columns:
                below_df = pos_df[pos_df["preco_mercado"] < pos_df["preco_medio"]]
                below_pm = below_df["ticker"].tolist()

            return {
                "has_portfolio": summary.get("total_custo", 0.0) > 0,
                "total_investido": summary.get("total_custo", 0.0),
                "patrimonio_atual": summary.get("total_mercado", 0.0),
                "lucro_nominal": summary.get("lucro_nominal", 0.0),
                "rentabilidade_pct": summary.get("rentabilidade_pct", 0.0),
                "proventos_ano": summary.get("proventos_anuais_esperados", 0.0),
                "proventos_mes": summary.get("proventos_mensais_esperados", 0.0),
                "tickers": tickers,
                "below_pm": below_pm
            }
        except Exception:
            return {"has_portfolio": False}

    def generate_response(self, query: str, username: Optional[str] = None, ranked_df: Optional[pd.DataFrame] = None) -> Tuple[str, str]:
        """
        Gera uma resposta inteligente da Radarzinha.
        Retorna (texto_markdown, texto_para_voz_tts).
        """
        q = query.strip().lower()
        port = self.get_portfolio_context(username)

        # -------------------------------------------------------------
        # 1. ANÁLISE ESPECÍFICA DA CARTEIRA DO USUÁRIO
        # -------------------------------------------------------------
        if any(w in q for w in ["minha carteira", "meus ativos", "minhas ações", "minha posição", "tenho na carteira", "meu patrimônio"]) and not any(w in q for w in ["comprar", "vender"]):
            if not port["has_portfolio"]:
                text = (
                    "Meu amor, dei uma olhadinha nos seus registros e vi que você ainda não cadastrou ativos na sua carteira! 🥺💼\n\n"
                    "Mas não se preocupe, é super fácil e rápido: basta ir até a aba **'Minha Carteira'**, abrir o menu retrátil "
                    "**'📝 Cadastro Ativos'** e lançar suas primeiras compras.\n\n"
                    "Assim que você cadastrar, eu vou poder te dar diagnósticos exclusivos sobre seu Preço Médio, rentabilidade "
                    "e te avisar sempre que um dividendo estiver a caminho da sua conta! Vamos começar hoje mesmo?"
                )
                tts = "Meu amor, dei uma olhadinha e vi que você ainda não cadastrou ativos na sua carteira. É super fácil: basta ir até a aba Minha Carteira e lançar suas compras para eu te dar diagnósticos exclusivos!"
                return text, tts

            text = (
                f"Olhei com todo carinho a sua carteira agora mesmo, meu bem! Veja só o seu raio-x: 💖📊\n\n"
                f"- **💰 Total Investido (Custo):** {fmt_brl(port['total_investido'])}\n"
                f"- **💎 Patrimônio Atual a Mercado:** {fmt_brl(port['patrimonio_atual'])}\n"
                f"- **🚀 Lucro / Prejuízo Acumulado:** {fmt_brl(port['lucro_nominal'])} ({port['rentabilidade_pct']:+.2f}%)\n"
                f"- **💵 Renda Passiva Estimada:** {fmt_brl(port['proventos_mes'])}/mês (cerca de {fmt_brl(port['proventos_ano'])}/ano)\n"
                f"- **📈 Ações em Custódia:** {', '.join(port['tickers']) if port['tickers'] else 'Nenhuma'}\n\n"
            )
            if port["below_pm"]:
                text += (
                    f"🔥 **Oportunidade de Ouro na sua Carteira:**\n"
                    f"Você possui ações sendo negociadas **abaixo do seu Preço Médio (Preço < PM)**: **{', '.join(port['below_pm'])}**.\n"
                    f"Se a tese e os fundamentos dessas empresas continuam impecáveis, esse é o momento perfeito para fazer novos aportes, "
                    f"rebaixar seu PM e multiplicar seu yield on cost futuro! Que tal aproveitar?"
                )
                tts = f"Olhei com todo carinho a sua carteira, meu bem! Seu patrimônio atual é de {fmt_brl(port['patrimonio_atual'])} com proventos estimados de {fmt_brl(port['proventos_mes'])} por mês. Fique atento às ações {', '.join(port['below_pm'])} que estão abaixo do seu Preço Médio, uma ótima chance para aportar!"
            else:
                text += "Parabéns, meu querido! Suas ações estão bem posicionadas e performando acima do preço médio de compra. Continue mantendo o foco nos dividendos e reinvestindo tudo!"
                tts = f"Parabéns, meu bem! Sua carteira está linda com patrimônio de {fmt_brl(port['patrimonio_atual'])}. Continue com a constância nos aportes!"
            return text, tts

        # -------------------------------------------------------------
        # 2. QUANDO COMPRAR E QUANDO VENDER UMA AÇÃO
        # -------------------------------------------------------------
        if any(w in q for w in ["quando comprar", "quando vender", "momento de comprar", "momento de vender", "devo vender", "devo comprar", "hora de comprar", "hora de vender"]):
            text = (
                "Essa é uma das perguntas mais inteligentes e sedutoras do mercado financeiro, meu querido investidor! "
                "Vem cá que a Radarzinha te explica a regra de ouro dos grandes mestres (Barsi e Bazin): 💋📈\n\n"
                "### 🟢 1. Quando você DEVE COMPRAR uma Ação:\n"
                "1. **Abaixo do Preço Teto de Décio Bazin:** A cotação atual está pagando pelo menos **6% ao ano** em dividendos sobre o preço pago. "
                "Comprar barato garante um *Yield on Cost* irresistível para o resto da vida!\n"
                "2. **Abaixo do Preço Justo de Graham:** A empresa possui margem de segurança positiva ($V_{\\text{Graham}} > \\text{Preço}$), "
                "significando que você está pagando centavos por cada real de patrimônio e lucro.\n"
                "3. **Preço de Mercado < Seu Preço Médio (PM):** Quando uma boa empresa passa por turbulências passageiras de mercado e a cotação cai, "
                "mas o lucro e a geração de caixa continuam firmes, é hora de **comprar mais para abaixar seu PM**!\n"
                "4. **No dia do seu Aporte Mensal:** Para quem busca renda passiva, a constância supera o 'timing'. Compre sempre na data do seu aporte as ações mais descontadas do setor perene (BEST).\n\n"
                "### 🔴 2. Quando você DEVE VENDER uma Ação:\n"
                "Guarde isto no seu coração, meu amor: **Investidor de dividendos NÃO gira patrimônio nem vende no desespero de quedas passageiras!** "
                "Você só deve vender em 3 situações extremas:\n"
                "1. **Perda Estrutural dos Fundamentos:** A empresa perdeu vantagens competitivas, passou a dar prejuízos crônicos, "
                "a governança cometeu fraudes ou o modelo de negócio se tornou obsoleto.\n"
                "2. **Endividamento Catastrófico:** A relação Dívida Líquida/EBITDA explodiu acima de 4x ou 5x sem perspectivas de desalavancagem, "
                "obrigando a companhia a cortar 100% dos proventos por anos.\n"
                "3. **Euforia Irracional e Bolha Especulativa:** A cotação subiu tanto que o P/L foi para 50x ou 80x e o Dividend Yield caiu para menos de 1%. "
                "Nesse caso, faz sentido realizar o lucro para comprar outra excelente pagadora que esteja barata!\n\n"
                "💡 *Dica da Radarzinha:* Olhe sempre na aba **'Alertas B3'** para ver quem está abaixo do PM antes de tomar qualquer decisão!"
            )
            tts = (
                "Vem cá que a Radarzinha te conta o segredo de quando comprar e vender! "
                "Compre sempre que a ação estiver abaixo do Preço Teto de Bazin, com margem de segurança de Graham, ou abaixo do seu Preço Médio em empresas sólidas. "
                "E nunca venda no susto! Só venda se os fundamentos da empresa morrerem de verdade ou se a cotação entrar numa bolha maluca. "
                "Investidor de dividendos compra para ser sócio e viver de renda!"
            )
            return text, tts

        # -------------------------------------------------------------
        # 3. COMO MONTAR CARTEIRA PARA RENDA DE R$ X MENSAIS
        # -------------------------------------------------------------
        if any(w in q for w in ["montar uma carteira", "renda de", "reais mensais", "quanto preciso", "quanto investir", "viver de renda", "x reais", "meta mensal"]):
            val = self.extract_monetary_value(q) or 2000.0
            dy_conservador = 0.08  # 8% a.a. conservador para carteira de dividendos B3
            renda_anual = val * 12.0
            patrimonio_alvo = renda_anual / dy_conservador

            # Cálculos de tempo estimados com aportes de R$ 1.000 e R$ 2.000 com reinvestimento
            text = (
                f"Ah, que meta maravilhosa, meu bem! Vamos planejar juntos como colocar **{fmt_brl(val)} todo mês** no seu bolso de forma automática! 💰💃✨\n\n"
                f"### 🧮 A Fórmula Mágica da Radarzinha:\n"
                f"Considerando uma carteira sólida de ações pagadoras da B3 com **Dividend Yield médio de 8,0% ao ano**:\n\n"
                f"- **🎯 Renda Mensal Desejada:** {fmt_brl(val)}\n"
                f"- **📅 Renda Anual em Proventos:** {fmt_brl(renda_anual)}\n"
                f"- **💎 Patrimônio Alvo Necessário:** **{fmt_brl(patrimonio_alvo)}**\n\n"
                f"### 🏛️ Estratégia de Alocação nos Setores BEST:\n"
                f"Para não correr riscos desnecessários e ter proventos pingando todos os meses, recomendo distribuir seu capital em 5 setores à prova de balas:\n"
                f"1. **⚡ Energia Elétrica (25% a 30%):** Concessões longas e fluxo de caixa previsível. *(Ex: CPLE6, TAEE11, EGIE3, CMIG4)*\n"
                f"2. **🏦 Bancos e Serviços Financeiros (20% a 25%):** Altíssima rentabilidade e ROE elevado. *(Ex: BBAS3, ITUB4, SANB11)*\n"
                f"3. **🛡️ Seguradoras (15% a 20%):** Float financeiro e proteção contra inflação. *(Ex: BBSE3, CXSE3)*\n"
                f"4. **💧 Saneamento Básico (10% a 15%):** Monopólio natural essencial para a sociedade. *(Ex: SAPR11, CSMG3, SBSP3)*\n"
                f"5. **📡 Telecomunicações & Outras Perenes (10% a 15%):** Renda estável e demanda inelástica. *(Ex: VIVT3, VALE3)*\n\n"
                f"### 🚀 O Poder da Bola de Neve:\n"
                f"No início, seus aportes fazem o trabalho pesado. Quando seus dividendos mensais pagarem o valor de novas ações inteiras, "
                f"a carteira começa a andar sozinha. Reinvista 100% dos dividendos recebidos!\n\n"
                f"👉 *Quer personalizar ainda mais?* Acesse a aba **'💰 Simulador de Renda Passiva'** aqui na plataforma para simular o tempo exato com base no seu aporte!"
            )
            tts = (
                f"Para receber {fmt_brl(val)} todo santo mês na sua conta, com um yield de 8 por cento ao ano, "
                f"seu patrimônio alvo é de aproximadamente {fmt_brl(patrimonio_alvo)}. "
                f"Distribuindo suas compras nos setores perenes de bancos, energia, saneamento e seguros, e reinvestindo cada centavo, "
                f"o efeito bola de neve vai te levar até a independência financeira muito mais rápido, meu bem!"
            )
            return text, tts

        # -------------------------------------------------------------
        # 4. QUAIS AS MELHORES AÇÕES / O QUE COMPRAR HOJE
        # -------------------------------------------------------------
        if any(w in q for w in ["melhores ações", "o que comprar", "quais ações", "oportunidades", "ações baratas", "melhores dividendos", "destaques"]):
            top_stocks = []
            if ranked_df is not None and not ranked_df.empty:
                top_slice = ranked_df.head(5)
                for _, row in top_slice.iterrows():
                    top_stocks.append(f"**{row['ticker']}** ({row['company_name']}) — DY: `{row['dy_12m']:.1f}%` | Score: `{row['score']:.0f}` | Teto Bazin: `{fmt_brl(row['bazin_ceiling_price'])}`")

            text = (
                "Adoro quando você me pede dicas de ouro, meu querido investidor! 💅✨\n\n"
                "De acordo com o nosso motor inteligente multicritério do Radar B3 (cruzando Yield, ROE, Solvência e Notícias Reais), "
                "aqui estão os destaques que estão chamando minha atenção hoje:\n\n"
            )
            if top_stocks:
                text += "\n".join([f"- {s}" for s in top_stocks]) + "\n\n"
            else:
                text += (
                    "- **BBAS3 (Banco do Brasil):** Lucros recordes, P/L extremamente baixo e dividendos generosos.\n"
                    "- **CPLE6 (Copel):** Eficiência pós-privatização, forte geração de caixa e dividendos no setor elétrico.\n"
                    "- **TAEE11 (Taesa):** O clássico reloginho de proventos do setor de transmissão de energia.\n"
                    "- **BBSE3 (BB Seguridade):** Modelo de negócio leve em capital, sem dívida e com payout astronômico.\n"
                    "- **SAPR11 (Sanepar):** Saneamento com múltiplos de Deep Value e ampla margem de segurança.\n\n"
                )
            text += (
                "📍 *Onde conferir todos os detalhes:* Dá um pulinho na aba **'🏆 Grandes Rankings da B3'** ou use o "
                "**'🎯 Detector de Ações'** para filtrar empresas que custam menos de R$ 10,00 ou com o maior desconto de Graham!"
            )
            tts = (
                "Separei com todo carinho as melhores oportunidades da bolsa para você, meu bem! "
                "Empresas sólidas com dividend yield alto, margem de segurança de Bazin e fundamentos impecáveis. "
                "Dá uma olhadinha na aba Grandes Rankings da B3 para ver a lista completa com todas as cotações atualizadas!"
            )
            return text, tts

        # -------------------------------------------------------------
        # 5. SIGLAS E TERMOS DO MERCADO FINANCEIRO
        # -------------------------------------------------------------
        siglas_matches = [s for s in ["dy", "dividend yield", "p/l", "pl", "p/vp", "pvp", "roe", "cagr", "lpa", "vpa", "dpa", "payout", "bazin", "graham", "jcp", "data com", "data ex"] if s in q]
        if siglas_matches or any(w in q for w in ["siglas", "termos", "o que significa", "dicionário", "glossário", "entender as siglas"]):
            text = (
                "Nada de ficar perdido nas sopas de letrinhas da Faria Lima, meu bem! A Radarzinha traduz tudo para você de um jeito simples e gostoso: 💋📖\n\n"
                "- **📊 DY (Dividend Yield):** É o rendimento dos proventos pagos nos últimos 12 meses dividido pelo preço da ação. Quanto maior o DY, mais dinheiro cai na sua conta em relação ao que você pagou!\n"
                "- **📉 P/L (Preço sobre Lucro):** Mede em quantos anos o lucro da empresa pagaria o valor atual da sua ação. Um P/L baixo (abaixo de 8x ou 10x) geralmente indica uma ação barata.\n"
                "- **🏢 P/VP (Preço sobre Valor Patrimonial):** Mostra quanto você paga pelo patrimônio físico e contábil da empresa. P/VP menor que 1,0 significa que a empresa está sendo vendida por menos do que seus prédios, maquinários e reservas valem!\n"
                "- **👑 ROE (Return on Equity):** Retorno sobre o Patrimônio Líquido. Mede a eficiência da diretoria em multiplicar o dinheiro dos acionistas. Acima de 15% é pura excelência.\n"
                "- **📈 CAGR (Compound Annual Growth Rate):** Taxa de crescimento anual composta. Mede a velocidade com que os lucros e dividendos da empresa vêm crescendo nos últimos anos.\n"
                "- **💸 Payout (%):** A fatia do lucro líquido que a empresa distribui aos acionistas em forma de dividendos e JCP. Se for 50%, ela guarda metade para investir e te dá a outra metade.\n"
                "- **📐 Preço Teto de Décio Bazin:** $\\text{Preço Teto} = \\frac{\\text{DPA}}{0{,}06}$. É o preço máximo que você pode pagar para garantir um retorno mínimo de 6% ao ano em proventos.\n"
                "- **💎 Preço Justo de Graham:** $V = \\sqrt{22{,}5 \\times LPA \\times VPA}$. O valor intrínseco baseado nos lucros e no patrimônio contábil da companhia.\n"
                "- **📅 Data COM vs Data EX:** Quem dorme posicionado na **Data COM** tem direito garantido ao dividendo. A partir da **Data EX**, quem comprar já não recebe aquela distribuição específica.\n"
                "- **🏦 JCP (Juros sobre Capital Próprio):** Provento com retenção de 15% de imposto de renda na fonte, diferentemente dos dividendos que são 100% isentos de IR!\n"
                "- **🎯 PM (Preço Médio):** A média ponderada de quanto você pagou por cada ação que tem em custódia.\n\n"
                "Ficou alguma dúvida sobre alguma outra sigla, meu querido? É só me perguntar!"
            )
            tts = (
                "Descompliquei as principais siglas da bolsa para você, meu bem! "
                "O Dividend Yield mede o retorno em proventos, o P sobre L mostra se a ação está barata, "
                "o ROE mede a rentabilidade e o Preço Teto de Bazin te impede de pagar caro por uma ação. "
                "Comigo você investe sabendo exatamente cada detalhe dos seus investimentos!"
            )
            return text, tts

        # -------------------------------------------------------------
        # 6. ESTRATÉGIAS DE INVESTIMENTO (BAZIN, BARSI, GRAHAM)
        # -------------------------------------------------------------
        if any(w in q for w in ["estratégia", "estratégias", "barsi", "bazin", "graham", "filosofia", "metodologia"]):
            text = (
                "Ah, falar de estratégias vencedoras é minha paixão, meu amor! Aqui no Radar B3 nós unimos os 3 maiores pilares de sucesso da história: 🏛️👑✨\n\n"
                "### 1. 📐 O Método Décio Bazin (Foco na Disciplina do Yield):\n"
                "- Só compra empresas que paguem no mínimo **6% ao ano** de dividendo médio.\n"
                "- Nunca compra acima do **Preço Teto** ($DPA / 0{,}06$).\n"
                "- Exige histórico de lucros regulares e rejeita empresas com endividamento excessivo.\n\n"
                "### 2. 👴 A Filosofia de Luiz Barsi Filho (Ações Previdenciárias & Setores BEST):\n"
                "- Investe com a mentalidade de sócio de longo prazo para montar uma previdência própria em ações.\n"
                "- Foca em setores perenes e essenciais que a sociedade não pode viver sem: **Bancos, Energia, Saneamento, Telecom e Seguros (BEST)**.\n"
                "- Reinveste todos os dividendos sistematicamente para disparar o efeito bola de neve.\n\n"
                "### 3. 🎩 A Margem de Segurança de Benjamin Graham (Value Investing):\n"
                "- Ensina a nunca pagar mais do que o valor intrínseco de uma empresa.\n"
                "- Calcula o valor justo considerando lucro e patrimônio ($V = \\sqrt{22{,}5 \\times LPA \\times VPA}$).\n"
                "- A margem de segurança te protege caso a economia passe por turbulências temporárias.\n\n"
                "🔥 **Como o Radar B3 combina isso para você?**\n"
                "Nós pegamos tudo isso e calculamos automaticamente na aba **'Grandes Rankings'** e na **'Visão Geral do Mercado'**! Quer ver agora?"
            )
            tts = (
                "Nós unimos o melhor dos três maiores mestres da bolsa, meu bem! "
                "O Preço Teto de 6 por cento de Décio Bazin, a visão previdenciária e os setores perenes de Luiz Barsi, "
                "e a margem de segurança de Benjamin Graham. Esse é o mapa perfeito para você viver de renda passiva!"
            )
            return text, tts

        # -------------------------------------------------------------
        # 7. COMO NAVEGAR NO SITE / ATALHOS / GUIA DA PLATAFORMA
        # -------------------------------------------------------------
        if any(w in q for w in ["navegar", "atalhos", "onde fica", "onde acho", "como funciona o site", "menu", "abas", "funções"]):
            text = (
                "Deixa a Radarzinha te guiar por cada cantinho da nossa plataforma incrível, meu bem! Veja onde encontrar tudo: 🧭💃\n\n"
                "- **💼 Aba 'Minha Carteira':** Acompanhe seu patrimônio em tempo real, veja gráficos de alocação por custo e valor de mercado, consulte seu lucro acumulado, cadastre novos ativos ou exclua lançamentos antigos.\n"
                "- **🚨 Aba 'Alertas B3':** Veja quais empresas da sua carteira vão pagar dividendos no mês atual e quais estão sendo negociadas **abaixo do seu Preço Médio (Preço < PM)**.\n"
                "- **🏆 Aba 'Grandes Rankings da B3':** Conheça as 15 Maiores Oportunidades (Graham/Bazin), as 15 Maiores Pagadoras de Yield, as que mais cresceram proventos e use o **Detector de Ações < R$ 10**!\n"
                "- **📌 Aba 'Visão Geral do Mercado':** Acesse o Calendário Anual B3, a Agenda Paginada de Ações (com filtros DE e ATÉ), leia Notícias ao Vivo com análise de sentimento e faça o Raio-X individual de qualquer ativo.\n"
                "- **💰 Aba 'Simulador de Renda Passiva':** Descubra exatamente quanto precisa acumular e em quanto tempo alcançará sua renda mensal dos sonhos com aportes regulares.\n"
                "- **❤️ Botão 'Apoie o Radar B3':** Localizado na barra lateral (acima de Resumo Metodológico) e no menu do topo para você contribuir via PIX e manter nosso projeto vivo e gratuito!\n"
                "- **🔐 Menu do Topo (Avatar):** Acesse seu perfil, altere sua senha com segurança ou encerre sua sessão.\n\n"
                "Qual dessas telas você quer explorar primeiro comigo, meu querido?"
            )
            tts = (
                "Deixa a Radarzinha te guiar pela plataforma, meu amor! "
                "Na aba Minha Carteira você gerencia seus ativos. Em Alertas B3 você descobre quem paga dividendos no mês. "
                "Nos Grandes Rankings você encontra as melhores barganhas, e no Simulador de Renda Passiva você planeja sua independência financeira. "
                "Tudo foi feito sob medida para você vencer na bolsa!"
            )
            return text, tts

        # -------------------------------------------------------------
        # 8. DOAÇÃO / APOIE O RADAR B3
        # -------------------------------------------------------------
        if any(w in q for w in ["doar", "doação", "apoie", "pix", "contribuir", "ajudar o projeto", "café"]):
            text = (
                "Ai, que gesto lindo e carinhoso, meu bem! Fico tão emocionada com o seu carinho pelo Radar B3! ❤️🥺✨\n\n"
                "Nossa plataforma é 100% gratuita, sem propagandas invasivas e mantida com muito esforço independente. "
                "Sua contribuição ajuda a pagar servidores em nuvem, bancos de dados, novos radares e aquele cafezinho gostoso para o desenvolvedor!\n\n"
                "### 💚 Como Apoiar via PIX:\n"
                "- **📱 Chave Celular:** `(62) 99930-8633`\n"
                "- **👤 Favorecido:** `VINICIUS AUGUSTO MARQUES`\n"
                "- **📋 Copia e Cola & QR Code:** Você encontra o QR Code oficial e o código de cópia em 1 clique clicando no botão **'❤️ Apoie o Radar B3'** no menu lateral esquerdo (logo acima do Resumo Metodológico).\n\n"
                "Muito obrigada por fazer parte desta história e apoiar nosso projeto, meu querido investidor! 🙏"
            )
            tts = (
                "Ai, que gesto maravilhoso, meu bem! Sua doação via PIX ajuda a manter o Radar B3 rápido, gratuito e sempre no ar. "
                "A chave celular é 62 99930 8633 no nome de Vinicius Augusto Marques. "
                "Você também pode clicar no botão Apoie o Radar B3 no menu lateral para escanear o QR Code. Muito obrigada pelo carinho!"
            )
            return text, tts

        # -------------------------------------------------------------
        # 9. RESPOSTA PADRÃO INTELIGENTE E ACOLHEDORA
        # -------------------------------------------------------------
        text = (
            f"Adorei sua pergunta sobre **'{query}'**, meu querido investidor! 💃✨\n\n"
            "Aqui no universo dos investimentos em dividendos, o segredo da riqueza está na constância, na paciência "
            "e em nunca comprar ativos acima do seu Preço Justo.\n\n"
            "Posso te ajudar em detalhes com:\n"
            "- 🎯 **Diagnóstico da sua carteira:** Ver quanto você tem investido e quais ações estão com Preço < PM.\n"
            "- ⏰ **Momento de Compra e Venda:** Saber exatamente quando abrir ou encerrar uma posição.\n"
            "- 💰 **Meta de Renda Passiva:** Como montar uma carteira para ganhar R$ 1.000, R$ 2.000 ou R$ 5.000 por mês.\n"
            "- 📖 **Dicionário B3:** Explicar siglas como DY, P/L, ROE, Graham e Preço Teto Bazin.\n"
            "- 🏆 **Melhores Ações da B3:** Conhecer as empresas mais baratas e que mais pagam dividendos hoje.\n\n"
            "O que você gostaria que a Radarzinha te explicasse com prioridade agora, meu bem?"
        )
        tts = (
            f"Adorei sua pergunta, meu bem! No mercado de dividendos, quem tem paciência e método vence sempre. "
            f"Me diga se você prefere que eu analise sua carteira, te mostre as melhores ações baratas da B3, ou calcule quanto você precisa para viver de renda passiva!"
        )
        return text, tts

_ENGINE_INSTANCE = RadarzinhaEngine()

def get_radarzinha_response(query: str, username: Optional[str] = None, ranked_df: Optional[pd.DataFrame] = None) -> Tuple[str, str]:
    """Helper global para invocar a Radarzinha."""
    return _ENGINE_INSTANCE.generate_response(query=query, username=username, ranked_df=ranked_df)
