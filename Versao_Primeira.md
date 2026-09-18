
======================================================================
Linguagem
======================================================================

projeto em Python 


======================================================================
Layout TOPO
======================================================================

Usar a logotipo opção 4

Titulo: B3 DIVIDEND RADAR | RELATÓRIO EXECUTIVO DE PROVENTOS
Subtitulo: Gestão de Carteira Real, Recomendação de Ações, Valuation (Bazin & Graham), Notícias e Frequência de Distribuição

TOPO lado direito: (antes de logar)
Cadastra-se
Entrar
 

TOPO lado direito: (apos logar)
masterradar(usuario logado)
 viniciusamarques2026@gmail.com 

Menu retratil quando clicar no icone do usuario, mostrar as opções abaixo

Minhas informações
Alterar senha
Ajuda

Modo Escuro (alternância liga/desliga)


Sair da conta


TOPO lado esquerdo:
Menu retratil com as opções de menu


======================================================================
Criar Tela Minhas informações:
======================================================================

Acessado ao clicar em "Minhas informações"

Minhas informações (Pode editar os dados)

Vinicius (avatar com a letra V)

viniciusamarques2026@gmail.com

Nome

Vinicius Augusto Marques

Data de nascimento

19/10/1975

Telefone

+556256454544

☑ Não resido no Brasil
☑ Termos de uso/Privacidade

Zona de Perigo (Bloco)

A exclusão da conta é permanente e não pode ser desfeita. Todos os seus dados serão apagados.

Excluir conta permanentemente (Botão)

Mostra pergunta se tem certeza em excluir a conta

Cancelar e Salvar


======================================================================
Criar Tela Alterar senha:
======================================================================

Acessado ao clicar em "Alterar senha"

Alterar senha

Senha atual

Campo de senha
Ícone para mostrar/ocultar senha

Nova Senha

Campo de senha
Ícone para mostrar/ocultar senha

ℹ️ A nova senha deve conter pelo menos 8 caracteres, ser composta por maiúscula, minúscula, um número e um caractere especial.

Confirmar nova senha

Campo de senha
Ícone para mostrar/ocultar senha

Botões:

Cancelar
Salvar

======================================================================
Criar Tela de login:
======================================================================

Acessado pelo link "Entrar"

Voltar

Entrar

Usuario
 Digite seu usuario.

Senha
 ••••••••

Esqueceu a sua senha? Redefinir senha

Entrar

Ou entre com o seu login social

Entrar com Google

Ao continuar você concorda com nossos Termos de Uso e Política de Privacidade

Ainda não possui uma conta? Cadastre-se

Observações da interface
Título principal: Entrar
Campos:
E-mail
Senha (com ícone para mostrar/ocultar senha)
Links:
Redefinir senha
Termos de Uso
Política de Privacidade
Cadastre-se
Botões:
Entrar
Entrar com Google

Recursos:
Card centralizado com máscara de senha e feedback instantâneo de validação.
Exibição do usuário conectado e botão 🚪 Sair / Logout na barra lateral para encerrar a sessão.

===================================
Criar usuario masterradar
===================================

Criar arquivo de json nas pasta Usuario, na pasta Master, para usuario masterradar

Nome completo: Vinicius Augusto Marques
Usuário: masterradar
Email: viniciusamarques2026@gmail.com
Data de nascimento: 19/10/1975
Telefone: +556256454544
Senha: @Blm1975
Não resido no Brasil: Marcado
Termos de uso/Privacidade: Marcado

Armazenamento persistente local em data/masterradar/dados_perfil.json.

======================================================================
Criar tela de "redefinir senha":
======================================================================

Acessado pelo link "Redefinir senha"

Voltar

Redefinir Senha

E-mail

Digite seu e-mail.

Enviar link de recuperação

======================================================================
Criar tela de cadastro de usuario:
======================================================================

Acessado pelo link "PERFIL" ou "Cadastra-se"

Estrutura dos Campos

	Nome completo: Mínimo de 5 carcateres. (Obrigatório)

	Usuario: Chave primária / login . (Obrigatório)

	E-mail: usar input type="email". (Obrigatório)

	Data de nascimento: usar mascara e validar

	Telefone: usar mascara e validar

	Senha: Mínimo 8 caracteres, com indicador de força. (Obrigatório)

	Confirmar senha: Validação deigualdade em tempo real. (Obrigatório)

	Termos de uso/Privacidade: Checkbox obrigatório (LGPD). (Obrigatório)


Criar uma pasta Usuario, dentro criar as pastas com os nomes dos usuários

Criar arquivo de json por usuario em pasta criada

Ações: 
	incluir:
		validar se já existe o usuário
		validar se já existe o email
		validar os campos obrigatório
	alterar:
		não permitr alterar o Usuario
		não permitr alterar o E-mail
		validar se já existe o usuário
		validar se já existe o email
		validar os campos obrigatório
	excluir:


======================================================================
Layout CENTRAL ou DETALHES
======================================================================

Onde que irar mostra os deshboards, os indicadores e as abas

======================================================================
Criar 💼 Aba Minha Carteira
======================================================================

Lembrando que esta aba é por usuário

🏆 Painel dos 4 opções de visualizações na carteira:

💰 Cards de KPIs da Carteira:

	Total Investido de Compra
	Patrimônio Real Atual
	Lucro / Prejuízo Consolidado (R$ e %)
	Proventos Estimados Anuais & Mensais da sua Carteira
	Rentabilidade atual em relação ao mês anterior
	Total de Dividendos ganhos no mês
	Total de Dividendos ganhos desde a compra até hoje

🚨 Alertas de Dividendos do Mês da Carteira:

	Como Funciona:
	Cruza em tempo real a quantidade de ações em custódia com o calendário histórico de distribuições da B3.
	Exibe um Banner de Alerta Ativo destacando o valor total estimado em Reais (R$) que cairá na sua conta no mês corrente.
	Traz Cards Executivos para cada ação pagadora com: Quantidade em custódia, DPA estimado por distribuição e Total a Receber.
	Inclui um Seletor de Mês Interativo (Janeiro a Dezembro) para antecipar e simular os proventos de qualquer mês do ano, além do Radar do Próximo Mês.

💰 Gráficos da Carteira:

	🥧 Gráfico 1: Investimento dos Ativos Cadastrados (Formato Pizza / Donut):
	Distribuição percentual e em R$ por ação com base no Custo de Aquisição (Preço de Compra).
	Exibição destacada do Total do Valor Investido.

	🥧 Gráfico 2: Valor Real dos Ativos Cadastrados (Formato Pizza / Donut):
	Distribuição por ação com base na Cotação Real Atualizada da B3.
	Exibição destacada do Patrimônio Total Real Atualizado.

	📊 Gráfico 3: Lucro / Perda dos Ativos Cadastrados (Formato Barra Vertical):
	Variação em R$ e Rentabilidade (%) por ação.
	Cores condicionais automáticas: Verde (#059669) para Lucro e Vermelho (#DC2626) para Prejuízo.
	Exibição do resultado total consolidado da carteira no cabeçalho do gráfico.

	📊 Gráfico "Histórico: Dividendos" na Guia da Carteira

	Estrutura Visual:

	Título corporativo: 📊 Histórico: Dividendos > com seletor de período (6 Meses, 12 Meses, Ano Atual) e ajuste de Meta Mensal.
	Barras verticais verde esmeralda (#00D084) com cantos superiores arredondados.
	Valores monetários formatados no topo de cada barra no padrão brasileiro (56,33, 307,23, 202,57, 55,63, 636,71, 325,85, etc.).
	Linha sutil de referência para a Meta Mensal configurada.

	Rodapé Informativo: Estrutura com exemplo

	Legenda à esquerda: 🟩 Ações e ⬜ Meta 2.000 (ou o valor de meta definido).
	Métricas à direita: Média 6 meses: R$ 264,05 e Total no período: R$ 1.584,32 ℹ️.
	Nota de rodapé: * Histórico de pagamentos de proventos em R$.

	Detalhamento Interativo: Expansor com breakdown dos ativos e valores pagos mês a mês.

📝 Cadastro de Ativos e Atualizações da Carteira:

	Estrutura Visual:

	Campos: Ação (Ticker B3), Data da Operação, Quantidade de Ações, Preço Unitário Pago (R$) e Observações.
	
	Atualização automática da posição consolidada e recálculo instantâneo do Preço Médio.
	
	Armazenamento persistente local em data/usuarioportfolio_transactions.json.

	📜 Histórico Completo das Atualizações & Lançamentos:
	Tabela cronológica com todas as compras registradas (ID, Data, Ação, Quantidade, Preço Pago, Valor Total Investido e Notas).
	Botão para exclusão/gerenciamento de lançamentos individuais.


======================================================================
Criar 💼 Aba Alertas B3
======================================================================

🚨 Alertas de Dividendos do Mês da B3

	Como Funciona:
	Cruza em tempo real a quantidade de ações em custódia com o calendário histórico de distribuições da B3.
	Exibe um Banner de Alerta Ativo destacando o valor total estimado em Reais (R$) que cairá na sua conta no mês corrente.
	Traz Cards Executivos para cada ação pagadora com: Quantidade em custódia, DPA estimado por distribuição e Total a Receber.
	Inclui um Seletor de Mês Interativo (Janeiro a Dezembro) para antecipar e simular os proventos de qualquer mês do ano, além do Radar do Próximo Mês.

🔻 2. Alertas de Ações Abaixo do Valor de Compra (Preço < PM) da B3

Como Funciona:
	Compara automaticamente a cotação a mercado da B3 com o seu Preço Médio (PM) de compra.
	Quando um ativo fica abaixo do preço pago, o sistema dispara um card de alerta com o desconto percentual e nominal.
	Cruza com o Preço Teto de Décio Bazin (Yield 6%) e Valor Justo de Benjamin Graham para diagnosticar:
		💡 Oportunidade de Baixar Preço Médio: Se a cotação está com margem de segurança positiva frente ao Preço Teto Bazin / Graham.
		⚠️ Monitorar Resultados: Se requer acompanhamento dos balanços trimestrais.



======================================================================
Criar 🏆 Aba Grandes Rankings da B3
======================================================================

🏆 Painel dos 4 Grandes Rankings da B3:

🥇 AS MAIORES OPORTUNIDADES: Ações com maior potencial de crescimento em relação ao Preço Justo de Graham e Preço Teto de Décio Bazin.
💰 AS MAIORES PAGADORAS DE DIVIDENDOS: Ranking das empresas com maior Dividend Yield (DY 12M) e DPA.
🚀 AS QUE MAIS CRESCERAM: Ações com maior taxa anualizada de crescimento de proventos (CAGR 3 anos) e retorno sobre capital (ROE).
🛡️ AS QUE MENOS CRESCERAM: Ações com menor crescimento de cotação / múltiplos de valuation mais descontados (menor P/L e menor P/VP para Value Investing).
🎯 DETECTOR DE AÇÕES: 
	Como Funciona:
		Digitar a valor, para procurar ações com Alto Potencial, abaixo deste valor
		Triagem dedicada para investidores focados em ativos de baixo valor nominal (ideais para pequenos aportes e reinvestimento fracionado de dividendos).
		Inclui slider ajustável de teto de preço (R56aR 5aR 15) e filtro de DY mínimo.
		Traz ativos de referência da B3 abaixo do valor digitado
	Exemplo: Digito 10, o sistema ira procurar as ações abaixo de 10 reais com Alto Potencial

Ações com Potencial Crescimento
Ações que geram Dividendos mensais
Ações que geram Dividendos bimestrais
Ações que geram Dividendos trimestrais


======================================================================
Criar 💼 Aba Noticias reias
======================================================================

Analisar notícias reais das empresa que geram dividendos
Avaliar dados da B3 reais das empresa que geram dividendos

....E outras ideias que tenha



======================================================================

Quando for moddo escuro, e os botões forem claros, colocar uma cor mais escura para sobresair

======================================================================

Retirar as opções(botões) no topo direito e trocar por um menu retratil
Quando clicar no icone do usuario, mostrar as opções abaixo em uma menu retratil

Minhas informações
Alterar senha
Ajuda

Modo Escuro (alternância liga/desliga)


Sair da conta

======================================================================

Quando sair e voltar para a tela de login, limpar os campos

Quando entrar na tela de cadastro de usuario, limpar os campos

Retirar o botão Voltar, 
Retirar o botão mode escuro 
deixando somente os botões os botões Cadasdar e Entrar, quanmmdo sair.
Melhorar os botões Cadasdar e Entrar.








