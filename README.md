# 📈 B3 Dividend Radar — Plataforma Executiva de Recomendação e Gestão de Dividendos

Uma plataforma corporativa em Python com **interface executiva no estilo Power BI Dark Slate** voltada para triagem, recomendação, valuation e gestão de carteira real de ações pagadoras de dividendos da **B3 (Bolsa de Valores Brasileira)**.

🌐 **Acesse online**: [https://relatorio-executivo-de-proventos.onrender.com](https://relatorio-executivo-de-proventos.onrender.com)

---

## 🔐 1. Acesso, Autenticação e Perfis Multi-Usuário

A plataforma conta com um sistema robusto de autenticação, controle de sessão persistente e gerenciamento de perfis individuais:

### Credenciais Padrão Pré-Configuradas
- **Usuário Master**: `masterradar` *(ou `Master`)* &bull; **Senha**: `@Blm1975`
- **Usuário Cadastrado**: `constecinf` &bull; **Senha**: `@Blm1975`
- **Ambiente de Demonstração / Sandbox**: Cada usuário possui seu próprio isolamento de transações e histórico em `data/<usuario>/` e `Usuario/<usuario>/`.

### Recursos de Segurança e Sessão
1. **Permanecer Conectado (KMSI - Keep Me Signed In)**:
   - Mantém o usuário conectado mesmo após fechar o navegador ou reiniciar o dispositivo através de tokens criptográficos persistentes com validade de 30 dias gravados em `Usuario/kmsi_sessions.json`.
2. **Alternância de Visibilidade de Senha**:
   - Botões com ícones dinâmicos (**👁️ Mostrar senha** / **🔒 Ocultar senha**) disponíveis nas telas de Login, Cadastro, Alteração e Redefinição de Senha.
3. **Validação Rigorosa de Senhas**:
   - Sistema de verificação com pontuação de força (0 a 100%): mínimo de 8 caracteres, pelo menos uma letra maiúscula, uma minúscula, um número e um caractere especial (`!@#$%&*`).
4. **Cadastro Completo de Usuários**:
   - Validações de tamanho de nome, unicidade de login, padrão de e-mail e telefone internacional.
5. **Central do Usuário (Header Popover)**:
   - Menu suspenso com avatar personalizado, atalhos rápidos para *Meu Perfil*, *Alterar Senha*, *Central de Ajuda* e botão seguro de *Encerrar Sessão (Logout)* que revoga tokens ativos.

---

## 📩 2. Redefinição de Senha & Envio de E-mail (Senha Provisória)

O módulo de recuperação de conta (`src/auth/email_service.py` e `src/auth/user_manager.py`) permite aos investidores recuperarem seu acesso de forma automatizada:

### Como Funciona o Fluxo de Redefinição
1. Na tela de Login, o usuário clica em **"🔑 Redefinir senha"**.
2. Informa o e-mail cadastrado e clica em **"✉️ Enviar Senha Provisória por E-mail"**.
3. O sistema valida o e-mail, localiza a conta e gera uma **senha provisória aleatória de 10 caracteres** em total conformidade com as regras de segurança (ex.: `B3Vs%17@Py`).
4. A nova senha provisória é imediatamente gravada no perfil do usuário, e todas as sessões anteriores são invalidadas para garantir a segurança.
5. Um e-mail transacional é disparado contendo a mensagem oficial nos formatos **Texto Puro** e **HTML Executivo**:

```text
Assunto: Radar B3 - Redefinição de senha solicitada
		
Olá, [Nome do Usuário],

Recebemos uma solicitação para redefinir a senha da sua conta [[usuário]].

Segue abaixo a senha provisoria: 

[senha provisoria]

Lembre-se de alterar a senha após logar.

Se você não solicitou a redefinição, ignore este e-mail. Sua senha atual continuará funcionando normalmente.

Por segurança, nunca compartilhe sua senha com ninguém.

Se precisar de ajuda, entre em contato com nosso suporte: [constecinf@gmail.com].

Atenciosamente,

Equipe  Radar B3

https://relatorio-executivo-de-proventos.onrender.com
```

6. **Mecanismo de Segurança (Fallback)**: Caso o servidor SMTP ainda não esteja configurado ou ocorra indisponibilidade de rede, a senha provisória gerada é apresentada em um card de segurança destacado na tela, **garantindo que o investidor nunca fique bloqueado da sua conta**.

---

## 🔑 3. Como Habilitar o Envio Real de E-mails pelo Gmail

Para que a plataforma envie e-mails reais de recuperação para qualquer destinatário através da sua conta Gmail (`constecinf@gmail.com` ou outra):

O Google não permite mais autenticação direta por senha comum em conexões SMTP. É necessário gerar uma **Senha de Aplicativo (Google App Password)** de 16 caracteres.

### Passo 1: Gerar a Senha de Aplicativo no Google
1. Acesse sua Conta Google: [https://myaccount.google.com/](https://myaccount.google.com/).
2. No menu lateral, acesse **Segurança**.
3. Certifique-se de que a **Verificação em duas etapas** está **ATIVADA**.
4. Acesse diretamente a página de Senhas de App: [https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords).
5. No campo **Nome do app**, digite: `Radar B3` e clique em **Criar**.
6. O Google exibirá uma janela com uma senha de **16 letras** (ex.: `abcd efgh ijkl mnop`). Copie essa chave.

### Passo 2: Configurar no Sistema (3 Opções Disponíveis)

#### Opção A: Pela Interface Gráfica da Aplicação (Mais Rápido e Fácil)
1. Na tela inicial de Login, clique em **"🔑 Redefinir senha"**.
2. Abra o menu retrátil: **`⚙️ Configuração do Envio de E-mail (SMTP / Gmail)`**.
3. Verifique os campos:
   - **Servidor SMTP**: `smtp.gmail.com`
   - **E-mail Remetente (Gmail)**: `constecinf@gmail.com`
   - **Porta**: `587`
   - **Senha de App Google (16 letras)**: Cole a senha gerada de 16 letras (pode colar com ou sem espaços).
4. Clique em **💾 Salvar Configurações** (as credenciais serão salvas em `data/smtp_config.json`).
5. Clique em **🧪 Enviar E-mail Teste** para confirmar o recebimento na sua caixa de entrada!

#### Opção B: Via Arquivo Local `data/smtp_config.json`
Crie ou edite o arquivo `data/smtp_config.json`:
```json
{
  "server": "smtp.gmail.com",
  "port": 587,
  "user": "constecinf@gmail.com",
  "password": "abcdefghijklmnop",
  "sender_name": "Radar B3",
  "use_tls": true,
  "use_ssl": false,
  "support_email": "constecinf@gmail.com",
  "platform_url": "https://relatorio-executivo-de-proventos.onrender.com"
}
```

#### Opção C: No Servidor de Produção (Render / Cloud) via Variáveis de Ambiente
No painel do Render (ou serviço de hospedagem), adicione em **Environment Variables**:
- `SMTP_SERVER` = `smtp.gmail.com`
- `SMTP_PORT` = `587`
- `SMTP_USER` = `constecinf@gmail.com`
- `SMTP_PASSWORD` = `abcdefghijklmnop`
- `SMTP_SENDER_NAME` = `Radar B3`

---

## 💼 4. Módulo "Minha Carteira" (Estrutura Retrátil)

Toda a experiência da carteira foi modularizada em **menus retráteis (`st.expander`)** com abertura padrão (`expanded=True`), permitindo ao investidor recolher e expandir seções conforme sua preferência:

1. **📈 Minha Carteira: Desempenho** (Retrátil):
   - 🎯 **Meta Mensal (R$)**: Meta configurável de renda passiva mensal do investidor.
   - 🏆 **Meta Mensal Atingida (%)**: Percentual alcançado com base nas distribuições previstas.
   - 🚀 **Rentabilidade Atual (%)**: Ganho ou perda de capital atualizado sobre o patrimônio.
2. **🚨 Alertas de Proventos do Mês da Carteira** (Retrátil):
   - Seletor dinâmico de mês (Janeiro a Dezembro) que cruza a quantidade de ações em custódia com o calendário de pagamentos da B3, prevendo o valor exato a receber.
3. **📊 Histórico: Dividendos** (Retrátil):
   - Gráfico de barras verticais verde esmeralda com **valores monetários formatados no topo de cada barra (`R$ XX,XX`)**.
   - Seletor de período (*Últimos 6 Meses, 12 Meses ou Ano Atual*).
   - Linha de Meta Mensal configurável com cálculo da média mensal e total acumulado.
4. **📊 Graficos** (Retrátil Principal com Sub-gráficos Retráteis):
   - 🥧 **Gráfico 1: Investimento dos Ativos Cadastrados**: Distribuição percentual e em R$ por custo de aquisição (preço pago).
   - 🥧 **Gráfico 2: Valor Real dos Ativos Cadastrados**: Distribuição por ação a valor a mercado atualizado na B3.
   - 📊 **Gráfico 3: Lucro / Perda dos Ativos Cadastrados**: Barras de ganho nominal e percentual por ativo.
5. **📋 Posição Detalhada da Carteira por Ativo** (Retrátil):
   - Tabela com Ticker, Empresa, Quantidade, Preço Médio (PM), Preço Atual B3, Total Investido, Valor Atual, Saldo (+/- R$), Rentabilidade (%), DY 12M e Teto Bazin.
6. **📝 Cadastro Ativos** (Retrátil):
   - 📝 **Cadastrar / Atualizar Ativo na Carteira**: Formulário com sugestão de cotação atual da B3, cálculo instantâneo do valor total e persistência imediata.
   - 📜 **Histórico Completo das Atualizações & Lançamentos**: Tabela com ordenação cronológica decrescente e ferramenta para exclusão de lançamentos individuais com recálculo automático do Preço Médio (PM).

---

## 🚨 5. Central de Alertas B3 (Menus Retráteis)

1. **🚨 1. Alertas de Proventos do Mês da B3** (Retrátil):
   - Monitor de fluxo de dividendos com seletor interativo de mês de referência para a carteira.
2. **🔻 2. Alertas de Ações Abaixo do Valor de Compra (Preço < PM) da B3** (Retrátil):
   - Avalia ações da carteira cuja cotação de mercado caiu abaixo do preço médio de compra, cruzando com a margem de segurança de Bazin e Graham para apontar oportunidades de rebaixamento do PM.

---

## 🏆 6. Grandes Rankings da B3 (Todos Retráteis)

Os 4 pilares estratégicos de classificação agora são exibidos diretamente na página em formato retrátil com tabelas fundamentais acopladas:

1. 🎯 **As Maiores Oportunidades (Maior Desconto vs Preço Justo)**:
   - Margem de segurança de Graham e Bazin, métricas de teto e gráfico horizontal de upside.
   - Sub-expander: **📋 Tabela das 15 Maiores Oportunidades em Relação ao Preço Justo**.
2. 💰 **As Maiores Pagadoras de Dividendos (Últimos 12 Meses)**:
   - Maiores índices de Dividend Yield e DPA da bolsa.
   - Sub-expander: **📋 Tabela das 15 Maiores Pagadoras de Dividendos**.
3. 🚀 **As Que Mais Cresceram (Expansão de Dividendos & Rentabilidade)**:
   - Taxa de crescimento anualizado de proventos (CAGR 3 anos) e retorno sobre capital (ROE).
   - Sub-expander: **📋 Tabela das 15 Ações com Maior Crescimento de Dividendos e Lucros**.
4. 🛡️ **As Que Menos Cresceram (Mais Descontadas / Menor Preço)**:
   - Menores múltiplos de P/L e P/VP para estratégias de *Deep Value*.
   - Sub-expander: **📋 Tabela das 15 Ações com Menor Crescimento de Cotação (Deep Value)**.
5. 🎯 **Detector de Ações de Dividendos**:
   - Caixa para digitar qualquer valor máximo por ação (ex.: R$ 10,00), slider de desconto vs preço teto e filtro por periodicidade (mensal, bimestral, trimestral).

---

## 📌 7. Visão Geral do Mercado (Consolidação em Sub-Abas)

A aba **Visão Geral do Mercado** integra as análises de mercado em sub-abas organizadas:

### Sub-aba 1: 📊 Panorama Geral & Agenda B3
- **🎯 Matriz de Oportunidades (DY x ROE)**: Gráfico de dispersão quadrante identificando as empresas *High Yield / High Quality*.
- **📊 Ranking Geral de Ações de Dividendos da B3** (Retrátil): Matriz fundamentalista completa com color grading corporativo estilo Power BI.
- **🗓️ Calendário Anual de Proventos da B3** (Retrátil): Grade anual de previsões mês a mês.
  - **📅 Agenda de dividendos de AÇÕES** (Retrátil Interno):
    - Filtro de período com data **DE** e data **ATÉ** (com ajuste dinâmico aos limites dos dados).
    - **Paginação completa** (ex.: Página 1 de N) com seletor de quantos registros exibir por página (5, 10, 15, 20, 50).

### Sub-aba 2: 📰 Notícias Reais & Dados B3
- **📰 Notícias Reais & Análise de Sentimento das Empresas da B3** (Retrátil): Feed ao vivo via Google News RSS Brasil com analisador de sentimento financeiro (Positivo, Neutro, Negativo) e termômetro visual.

### Sub-aba 3: 🔍 Raio-X Individual (Bazin & Graham)
- Diagnóstico profundo por ação selecionada, comparando Preço Atual vs Preço Teto Bazin e Preço Justo Graham, com termômetro de margem de segurança e gráficos de múltiplos.

---

## 💰 8. Simulador de Renda Passiva

- Ferramenta interativa de cálculo reverso: o investidor define a **Renda Mensal Desejada em Proventos** (ex.: R$ 2.500,00/mês) e a plataforma calcula:
  - Quantidade de ações necessárias para atingir o objetivo.
  - Patrimônio total estimado a ser acumulado.
  - Tempo estimado para alcançar a meta com aportes regulares.

---

## 📐 9. Metodologia de Valuation Fundamentalista

- **Preço Teto de Décio Bazin (Yield 6%)**:
  $$\text{Preço Teto} = \frac{\text{DPA Médio (12M)}}{0{,}06}$$
- **Valor Justo de Benjamin Graham**:
  $$V_{\text{Graham}} = \sqrt{22{,}5 \times \text{LPA} \times \text{VPA}}$$
- **Score Multicritério B3 (0 a 100)**:
  - Dividend Yield & Valuation (35%)
  - Rentabilidade & ROE (25%)
  - Solvência, Dívida Líquida e Payout (20%)
  - Sentimento de Notícias Reais da B3 (20%)

---

## 📁 10. Estrutura Atualizada do Projeto

```
b3_dividend_radar/
├── app.py                     # Ponto de entrada da aplicação Streamlit (Layout Power BI)
├── requirements.txt           # Bibliotecas e dependências Python
├── README.md                  # Documentação completa e guia de uso
├── test_engine.py             # Testes unitários do motor de dividendos e mercado
├── test_full_suite.py         # Suite completa de testes de regressão
├── Usuario/                   # Diretório de persistência de usuários e sessões KMSI
│   ├── Master/dados_perfil.json
│   ├── masterradar/dados_perfil.json
│   ├── constecinf/dados_perfil.json
│   └── kmsi_sessions.json     # Sessões do recurso Permanecer Conectado
├── data/                      # Dados da carteira e configurações SMTP
│   ├── smtp_config.json       # Credenciais do serviço de envio de e-mail
│   ├── portfolio_transactions.json
│   ├── constecinf/            # Dados e lançamentos do usuário constecinf
│   └── masterradar/           # Dados e lançamentos do usuário masterradar
└── src/
    ├── auth/                  # Módulo de Autenticação, Usuários e E-mails
    │   ├── __init__.py
    │   ├── user_manager.py    # Gestão de perfis, senhas, KMSI e redefinição
    │   └── email_service.py   # Serviço SMTP Gmail, templates e senha provisória
    ├── data/                  # Fontes de dados e motores de cálculo
    │   ├── __init__.py
    │   ├── b3_universe.py     # Universo de mais de 33 ações selecionadas da B3
    │   ├── market_data.py     # Coletor de cotações, múltiplos e Bazin/Graham
    │   ├── dividend_engine.py # Motor de periodicidade (Mensal, Bimestral, Trimestral)
    │   └── portfolio_manager.py # Motor da carteira real, PM e projeções
    ├── engine/
    │   ├── __init__.py
    │   └── recommender.py     # Motor do Score Multicritério (0 a 100)
    ├── news/
    │   ├── __init__.py
    │   ├── news_collector.py  # Coletor de notícias ao vivo via Google News RSS
    │   └── sentiment_analyzer.py # Analisador de sentimento léxico PT-BR
    └── ui/                    # Camada de Apresentação e Componentes Gráficos
        ├── __init__.py
        ├── powerbi_theme.py   # CSS executivo corporativo Dark Slate Power BI
        ├── header.py          # Cabeçalho executivo corporativo e popover de usuário
        ├── auth_views.py      # Telas de Login, Cadastro, KMSI, Senha e SMTP
        ├── components.py      # Rankings, agenda paginada, notícias e Raio-X
        └── portfolio_components.py # Gráficos de rosca, barras e tabela da carteira
```

---

## 🚀 11. Como Instalar e Executar Localmente

### 1. Clonar ou Acessar o Diretório
```powershell
cd C:\Users\Vinic\.gemini\antigravity\scratch\b3_dividend_radar
```

### 2. Ativar o Ambiente Virtual
```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Instalar as Dependências
```powershell
pip install -r requirements.txt
```

### 4. Executar os Testes Automatizados (Opcional)
```powershell
python test_full_suite.py
```

### 5. Iniciar a Aplicação
```powershell
python -m streamlit run app.py
```
Acesse no navegador: **`http://localhost:8501`**.

Para entrar, utilize o login **`constecinf`** (ou **`masterradar`**) com a senha **`@Blm1975`**.
