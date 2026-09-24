
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

🌟 O que foi implementado:
Grade de 6 Indicadores Executivos (3x2):

Rentabilidade Mensal: Exibe -% (ou percentual do mês) + + 0,00% em relação ao mês anterior e ícone de tendência verde.
Meta Mensal: Exibe R$ 0,00 (ou o valor de meta personalizado salvo).
Meta Mensal Atingida: Exibe R$ 0,00 (ou total de proventos previstos do mês) + + 0,00% em relação ao mês anterior.
Rentabilidade atual: Exibe -% (ou rentabilidade acumulada sobre o capital) + + 0,00% em relação ao mês anterior.
Patrimônio atual: Exibe R$ 0,00 (ou valor total a mercado da carteira) + + 0,00% em relação ao mês anterior.
Proventos atual: Exibe R$ 0,00 (ou proventos correntes) + + 0,00% em relação ao mês anterior.
Configuração da "Meta Mensal":

Adicionado o botão 🎯 Meta Mensal no cabeçalho da seção, permitindo definir e salvar a meta de proventos em Reais de forma permanente no perfil do usuário.
Menu Retrátil para Métricas Detalhadas:

Conforme sua escolha, os 7 cards anteriores (Custo de Aquisição, Lucro/Prejuízo em R$ e %, Proventos Estimados Anuais, Proventos Acumulados desde a compra) foram preservados dentro de um menu retrátil:
📊 Ver Métricas Detalhadas de Custos e Posição (Custo de Aquisição, Lucro/Prejuízo em R$, etc.)

Isso mantém a página limpa e 100% alinhada ao visual executivo do modelo.
Estilo Visual e Ícones:

Cada cartão possui borda suave, cantos arredondados, elevação no hover e o ícone gráfico em formato de zigue-zague verde (trending-up) no canto superior direito, compatível com o tema escuro e claro.

======================================================================

Incluir dentro na aba ´Visão Geral do Mercado´, as abas ´Notícias Reais & Dados B3´ e ´Raio-X Individual (Bazin & Graham)´.

Tornar na aba ´Visão Geral do Mercado´, os topicos retratil:
´Calendário Anual de Proventos da B3´, 
´Agenda de dividendos de AÇÕES´
´Ranking Geral de Ações de Dividendos da B3´,
´Notícias Reais & Análise de Sentimento das Empresas da B3´,

Retirar da aba ´Minha Carteira: Desempenho´, os identificadores:
´Rentabilidade Mensal´, 
´Proventos atual´ e 
´Patrimônio atual´.

🌟 Resumo das Implementações:
1. Abas Integradas dentro de 📌 Visão Geral do Mercado
A barra de navegação principal no topo foi simplificada para 5 abas principais:

💼 Minha Carteira
🚨 Alertas B3
🏆 Grandes Rankings da B3
📌 Visão Geral do Mercado
💰 Simulador de Renda Passiva
Dentro de 📌 Visão Geral do Mercado, foram criadas sub-abas dedicadas:

📊 Panorama Geral & Agenda B3
📰 Notícias Reais & Dados B3
🔍 Raio-X Individual (Bazin & Graham)
2. Tópicos Retráteis (Expanders) na Aba "Visão Geral do Mercado"
Conforme solicitado, os tópicos foram encapsulados em painéis retráteis:

📊 Ranking Geral de Ações de Dividendos da B3: Painel retrátil com a tabela comparativa de ativos.
🗓️ Calendário Anual de Proventos da B3: Painel retrátil com o mapa de calor de pagamentos ao longo dos 12 meses.
📅 Agenda de dividendos de AÇÕES (Novo):
Painel retrátil integrado ao calendário.
Filtros DE e ATÉ: Seletores de intervalo por Data de Pagamento.
Filtros adicionais: Filtro por tipo (Dividendo, JCP, Todos) e campo para buscar por Ticker.
Paginação Completa: Seletor de quantidade de itens por página (5, 10, 15, 20, 50) e seletor de página (Página X de Y).
Colunas com Ticker, Empresa, Tipo, Data COM, Data Pagamento, Valor por Ação (R$), DY (%) e Status.
📰 Notícias Reais & Análise de Sentimento das Empresas da B3: Painel retrátil com o diagnóstico de sentimento, cotações ao vivo e feed de notícias.
3. Ajuste em "Minha Carteira: Desempenho"
Foram retirados os indicadores Rentabilidade Mensal, Proventos atual e Patrimônio atual.

A seção agora exibe os 3 indicadores executivos em uma única linha harmoniosa:

Meta Mensal: Exibe R$ 0,00 (ou a meta configurada pelo usuário via botão 🎯 Meta Mensal).
Meta Mensal Atingida: Exibe R$ 0,00 (ou o valor de proventos previsto para o mês) com + 0,00% em relação ao mês anterior.
Rentabilidade atual: Exibe -% (ou percentual acumulado de rentabilidade) com + 0,00% em relação ao mês anterior.

======================================================================


Tornar na aba ´Minha Carteira´, os topicos retratil: 
´Minha Carteira: Desempenho´,
´Alertas de Proventos do Mês da Carteira´,
´Histórico: Dividendos´ e
´Posição Detalhada da Carteira por Ativo´

Na aba ´Visão Geral do Mercado´, no tópico ´Calendário Anual de Proventos da B3´, 
Incluir ´Agenda de dividendos de AÇÕES´ e retratil, com os filtros DE e ATÉ, paginado e podendo escolher quantos por pagina.

🌟 O que foi configurado:
1. Tópicos Retráteis na aba 💼 Minha Carteira
Os 4 tópicos foram encapsulados em menus retráteis (expanders):

📈 Minha Carteira: Desempenho: Menu retrátil com os 3 indicadores executivos (Meta Mensal, Meta Mensal Atingida e Rentabilidade atual), botão de ajuste de meta e o detalhamento das métricas de custo.
🚨 Alertas de Proventos do Mês da Carteira: Menu retrátil com o seletor interativo de meses de simulação (Jan a Dez), banner e cards das ações pagadoras da carteira.
📊 Histórico: Dividendos: Menu retrátil com o gráfico de histórico de proventos acumulados.
📋 Posição Detalhada da Carteira por Ativo: Menu retrátil com a tabela completa de ativos em custódia, Preço Médio e resultados.
2. Agenda de dividendos de AÇÕES dentro de Calendário Anual de Proventos da B3
Na aba 📌 Visão Geral do Mercado:

Dentro do tópico retrátil 🗓️ Calendário Anual de Proventos da B3, foi incluída a seção retrátil:
📅 Agenda de dividendos de AÇÕES

Funcionalidades da Agenda:
Filtros DE e ATÉ: Seletores de data do pagamento com inicialização dinâmica (sem erros de limites).
Filtro por Tipo: Dividendo, JCP ou Todos.
Busca por Ticker: Campo de busca rápida.
Paginação Completa: Escolha de quantos itens por página (5, 10, 15, 20, 50) e navegação de páginas (Página X de Y).
Colunas com Ticker, Empresa, Tipo, Data COM, Data Pagamento, Valor por Ação (R$), DY do Evento (%) e Status.

======================================================================

Tornar na aba ´Minha Carteira´, os topicos retratil: 
📊 Graficos
	🥧 Gráfico 1: Investimento dos Ativos Cadastrados
	🥧 Gráfico 2: Valor Real dos Ativos Cadastrados
	📊 Gráfico 3: Lucro / Perda dos Ativos Cadastrados

Tornar na aba ´Minha Carteira´, os topicos retratil:
📝 Cadastro Ativos	
	📝 Cadastrar / Atualizar Ativo na Carteira
	📜 Histórico Completo das Atualizações & Lançamentos

Tornar na aba ´Alertas B3´, os topicos retratil: 
	1. Alertas de Proventos do Mês da B3
	2. Alertas de Ações Abaixo do Valor de Compra (Preço < PM) da B3

Tornar na aba ´Grandes Rankings da B3´, os topicos retratil: 
	🎯 As Maiores Oportunidades (Maior Desconto vs Preço Justo)
		📋 Tabela das 15 Maiores Oportunidades em Relação ao Preço Justo
	💰 As Maiores Pagadoras de Dividendos (Últimos 12 Meses)
		📋 Tabela das 15 Maiores Pagadoras de Dividendos
	🚀 As Que Mais Cresceram (Expansão de Dividendos & Rentabilidade)
		📋 Tabela das 15 Ações com Maior Crescimento de Dividendos e Lucros
	🛡️ As Que Menos Cresceram (Mais Descontadas / Menor Preço)
		📋 Tabela das 15 Ações com Menor Crescimento de Cotação (Deep Value)

1. 💼 Aba Minha Carteira
📊 Graficos (Tópico Retrátil Principal):
	🥧 Gráfico 1: Investimento dos Ativos Cadastrados (Sub-tópico retrátil com o gráfico de investimento por custo de compra)
	🥧 Gráfico 2: Valor Real dos Ativos Cadastrados (Sub-tópico retrátil com o gráfico de valor a mercado)
	📊 Gráfico 3: Lucro / Perda dos Ativos Cadastrados (Sub-tópico retrátil com o gráfico de barras de ganho e perda acumulada)
📝 Cadastro Ativos (Tópico Retrátil Principal):
	📝 Cadastrar / Atualizar Ativo na Carteira (Sub-tópico retrátil com o formulário de cadastro de ações)
	📜 Histórico Completo das Atualizações & Lançamentos (Sub-tópico retrátil com a tabela de transações e ferramenta de exclusão)

2. 🚨 Aba Alertas B3
🚨 1. Alertas de Proventos do Mês da B3 (Tópico Retrátil): Monitor com seletor de mês e cruzamento com a custódia.
🔻 2. Alertas de Ações Abaixo do Valor de Compra (Preço < PM) da B3 (Tópico Retrátil): Diagnóstico de ações abaixo do preço médio com margens de Bazin e Graham.

3. 🏆 Aba Grandes Rankings da B3
Os 4 rankings agora são acessíveis simultaneamente como seções retráteis na página, cada uma com seus indicadores, gráfico e tabela interna retrátil:
🎯 As Maiores Oportunidades (Maior Desconto vs Preço Justo):
	📋 Tabela das 15 Maiores Oportunidades em Relação ao Preço Justo (Sub-tópico retrátil com os dados fundamentais)
💰 As Maiores Pagadoras de Dividendos (Últimos 12 Meses):
	📋 Tabela das 15 Maiores Pagadoras de Dividendos (Sub-tópico retrátil com os dados de yield e proventos)
🚀 As Que Mais Cresceram (Expansão de Dividendos & Rentabilidade):
	📋 Tabela das 15 Ações com Maior Crescimento de Dividendos e Lucros (Sub-tópico retrátil)
🛡️ As Que Menos Cresceram (Mais Descontadas / Menor Preço):
	📋 Tabela das 15 Ações com Menor Crescimento de Cotação (Deep Value) (Sub-tópico retrátil)

======================================================================

Na tela de Login, a opção Redefinir senha

1. Quando clicar, ira pedir o email do cadastro

2. Clicar no botão Redefinir a senha

2. Será enviado um email para o email digitado

======================================================================

Na tela de Login, quando clico na opção Redefinir senha

Abri a tela de Redefinir Senha

Digito o email, mas não esta sendo enviado um email para o email digitado, com a nova senha provisoria.

Modelo abaixo de E-mail de Redefinição de Senha

Assunto: Radar B3 - Redefinição de senha solicitada
		
Olá, [Nome do Usuário],

Recebemos uma solicitação para redefinir a senha da sua conta [usuário].

Segue abaixo a senha provisoria: 

[senha provisoria]

Lembre-se de alterar a senha após logar.

Se você não solicitou a redefinição, ignore este e-mail. Sua senha atual continuará funcionando normalmente.

Por segurança, nunca compartilhe sua senha com ninguém.

Se precisar de ajuda, entre em contato com nosso suporte: [constecinf@gmail.com].

Atenciosamente,

Equipe  Radar B3

https://relatorio-executivo-de-proventos.onrender.com


🛠️ O que foi implementado

1. 📩 Serviço Oficial de Envio de E-mail (src/auth/email_service.py)

Modelo Exato Solicitado: O e-mail disparado segue à risca o padrão informado (com versão em texto puro e versão HTML com identidade visual executiva do Radar B3):

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

	Geração de Senha Provisória Forte: Gera automaticamente senhas de 10 dígitos (com letras maiúsculas, minúsculas, números e caracteres especiais) que atendem com nota máxima às regras de segurança do validador.
	Conexão SMTP Segura: Suporte nativo ao Gmail (smtp.gmail.com:587 com criptografia STARTTLS ou porta 465 SSL).

2. 🔐 Atualização Automática da Conta (src/auth/user_manager.py)
	Ao solicitar a redefinição, o sistema localiza a conta associada ao e-mail informado.
	A nova senha provisória é imediatamente salva no cadastro do usuário e todas as sessões anteriores são revogadas por segurança.
	O usuário já consegue efetuar login imediatamente com a nova senha provisória gerada.

3. 🎨 Tela de Redefinição de Senha e Configuração SMTP (src/ui/auth_views.py)
	Feedback Completo:
		Quando o e-mail é enviado via SMTP: exibe mensagem verde orientando a checar a caixa de entrada e spam.
		Mecanismo de Segurança: Caso o servidor ainda não possua uma Senha de Aplicativo do Gmail configurada ou ocorra instabilidade de rede, a senha provisória gerada é exibida na tela em destaque para que o usuário nunca fique bloqueado do sistema.
	Painel Retrátil de Configuração SMTP:
		Adicionado um menu retrátil na própria tela de redefinição: ⚙️ Configuração do Envio de E-mail (SMTP / Gmail).
		Nele você pode informar ou atualizar a Senha de App do Google (16 caracteres) do e-mail remetente (constecinf@gmail.com) e testar o envio com 1 clique no botão 🧪 Enviar E-mail Teste.

🔑 Como habilitar o envio real pelo Gmail (constecinf@gmail.com)

Para que o Gmail permita o envio automático via SMTP:

1. Acesse sua Conta Google em: https://myaccount.google.com/apppasswords
 (é necessário que a Verificação em Duas Etapas esteja ativa).
2. Crie uma nova senha de app com o nome "Radar B3".
3. O Google gerará uma senha de 16 letras (ex: abcd efgh ijkl mnop).
4. Abra a tela de Redefinir Senha no sistema, abra o menu ⚙️ Configuração do Envio de E-mail (SMTP / Gmail), 
	cole as 16 letras no campo de senha e clique em 💾 Salvar Configurações.
5. Em seguida, clique em 🧪 Enviar E-mail Teste para confirmar o recebimento direto na sua caixa de entrada!


A aplicação está rodando normalmente e atualizada em http://localhost:8501

======================================================================

1. 📍 Opção no Menu Lateral (Sidebar)

Localizada exatamente acima do bloco ### 📌 Resumo Metodológico:
	Botão com destaque visual: ❤️ Apoie o Radar B3 (sb_btn_donation).
	Também disponível no menu suspenso do perfil do usuário no cabeçalho superior.

2. 📄 Nova Página: ❤️ Apoie o Radar B3 (

A página foi construída seguindo a identidade visual corporativa Dark Slate do Radar B3, contendo:

Título em Destaque com Letras Maiores:
❤️ Apoie o Radar B3 (38px, peso 900, em cor de destaque).
Subtítulo: Seu apoio mantém este projeto vivo.
Mensagem de Apresentação:
Explicação sobre a missão do Radar B3 como projeto independente, prático e gratuito.
🚀 Por que doar? (Cards explicativos com os 5 pilares):
🌐 Infraestrutura e Hospedagem
🛠️ Novas Funcionalidades
🔒 Segurança e Confiabilidade
📈 Evolução Contínua
☕ Café para o Desenvolvedor
💚 Seção de Contribuição via PIX:
📱 Chave PIX: (62) 99930-8633
👤 Favorecido: VINICIUS AUGUSTO MARQUES
📋 Código PIX Copia e Cola: Caixa com botão nativo de cópia rápida em 1 clique:
text


00020126710014BR.GOV.BCB.PIX0114+55629993086330231Ajudando a continuidade do site5204000053039865802BR5924VINICIUS AUGUSTO MARQUES6009SAO PAULO6226052279ZshPqrzBFOYSWAL1iZmY630451FA
🖼️ QR Code PIX: Renderização em alta definição da imagem do QR Code Itaú salvo em 
assets/pix_qrcode.png
.
🙏 Mensagem de Agradecimento:
Reconhecimento da importância do apoio da comunidade.
↩️ Botão de Retorno no Final da Página:
Botão em largura total ← 🏠 Voltar à Plataforma, redirecionando instantaneamente ao Dashboard principal.

======================================================================


Criar um agente feminino, nome Radarzinha, com voz feminia sexy, contendo todas as informações do site, 

Siglas, 
Termos, 
atalhos para as funçõesm abas, ou opções,
duvidas,
sugestões,
sobre investimento, 
como investir,
como qual momento devo comprar e vender determinada ação da minha carteira,
como as melhores estrategias de investimentos,
como montar uma carteira de dividendos, para ter retorno de X reias mensais,

e o que mais achar devido.

======================================================================

💼 Minha Carteira
	📊 Minha Carteira: Desempenho

	📊 Ver Métricas Detalhadas de Custos e Posição (Custo de Aquisição, Lucro/Prejuízo em R$, etc.)

	🚨 Alertas de Proventos do Mês da Carteira

	📊 Histórico: Dividendos

	Graficos: 
		🥧 Gráfico 1: Investimento dos Ativos Cadastrados
		🥧 Gráfico 2: Valor Real dos Ativos Cadastrados
		📊 Gráfico 3: Lucro / Perda dos Ativos Cadastrados

	📋 Posição Detalhada da Carteira por Ativo

📝 Cadastro Ativos	
	📝 Cadastrar / Atualizar Ativo na Carteira

	📜 Histórico Completo das Atualizações & Lançamentos


🚨 Alertas B3
	1. Alertas de Proventos do Mês da B3
	2. Alertas de Ações Abaixo do Valor de Compra (Preço < PM) da B3

🏆 Grandes Rankings da B3
	1. 🎯 As Maiores Oportunidades (Maior Desconto vs Preço Justo)
		📋 Tabela das 15 Maiores Oportunidades em Relação ao Preço Justo
	2. 💰 As Maiores Pagadoras de Dividendos (Últimos 12 Meses)
		📋 Tabela das 15 Maiores Pagadoras de Dividendos
	3. 🚀 As Que Mais Cresceram (Expansão de Dividendos & Rentabilidade)
		📋 Tabela das 15 Ações com Maior Crescimento de Dividendos e Lucros
	4. 🛡️ As Que Menos Cresceram (Mais Descontadas / Menor Preço)
		📋 Tabela das 15 Ações com Menor Crescimento de Cotação (Deep Value)


📌 Visão Geral do Mercado

	📰 Notícias Reais & Dados B3

	🔍 Raio-X Individual (Bazin & Graham)

💰 Simulador de Renda Passiva





