# Diagnóstico de Churn – Terra Signal

Relatório de diagnóstico do negócio. Fontes: pesquisa de mercado (Gemini), Notebook Dicionário de Dados, Notebook Análise Pacotes, Notebook Análise Risco 3Fatores e Notebook Análise Sentimento.

## 1. Resposta em uma página

**Por que os clientes saem?** Não por um único motivo. O churn se concentra onde se juntam contrato sem fidelidade, pagamento por Electronic check, ausência de suporte e fibra óptica.

Partimos de cinco causas típicas de telecom (pesquisa de mercado, Gemini) e testamos cada uma na base. O ponto de partida: 1.504 dos 5.634 clientes da history cancelaram, ou 26,7% (validado no Notebook Análise Risco 3Fatores, V1 e V6).

| Pilar | A base confirma? | Número-chave |
| --- | --- | --- |
| 1. Preço e percepção de valor | Em parte | Os 5 pacotes de maior valor têm churn baixo (validado no Notebook Análise Pacotes, V3) |
| 2. Tipo de conexão | Sim, na fibra | Fibra: 42,1% de churn, contra 26,7% da média (validado no Notebook Análise Risco 3Fatores, V6) |
| 3. Suporte e proteção | Sim | 49,1% sem TechSupport nem OnlineSecurity, contra 17,2% com pelo menos um (validado no Notebook Análise Pacotes, V5) |
| 4. Perfil de uso e composição | Contraria em parte | Só linha fixa: 8,5% de churn (base history) |
| 5. Contrato e pagamento | Sim | Mês a mês com Electronic check: 53,6% (validado no Notebook Análise Risco 3Fatores, V5) |

**Régua de risco (history):** o nível Crítico, com a trava de tenure, reúne 1.278 clientes, com 60,9% de churn, e captura 51,7% de todos os cancelamentos (validado no Notebook Análise Risco 3Fatores, V1).

## 2. Situação, complicação e pergunta

**Situação.** A Terra Signal tem cerca de 7 anos e vende telefonia fixa, internet (fibra ou DSL) e serviços adicionais de segurança, suporte e entretenimento. Os valores estão em R$ (perguntas de negócio).

**Complicação.** A empresa percebeu um aumento repentino de cancelamentos. Não tem time de retenção, processo de contato, histórico de descontos, meta de churn, meta de faturamento nem verba de contatos (perguntas de negócio).

**Pergunta.** Quais são as causas do churn e quais clientes têm maior risco?

**Como respondemos.** A pesquisa de mercado deu as hipóteses. O Notebook Dicionário de Dados validou a base. O Notebook Análise Pacotes, o Notebook Análise Risco 3Fatores e o Notebook Análise Sentimento as testaram. A régua de risco aplica o resultado à inference.

## 3. Base e definições

- **Churn:** “Yes” significa que o cliente cancelou o contrato. É uma foto do momento em que a base foi montada, e quem cancelou pode recontratar. A inadimplência não define churn (perguntas de negócio).
- **History e inference:** a history tem 5.634 clientes e a coluna Churn, e é a base da análise e do modelo. A inference tem 1.409 clientes e foi reservada para testar o modelo, por isso não tem Churn (validado no Notebook Dicionário de Dados, V1: sem cliente em comum entre as bases). As duas têm o mesmo recorte temporal: as bases foram baixadas no mesmo momento (mesmo dia e hora).
- **Tenure:** meses desde a assinatura do primeiro contrato, até o cancelamento para quem saiu e até a data de montagem da base para quem está ativo (perguntas de negócio).
- **Valores:** MonthlyCharges é o total pago no mês, com taxas e serviços. TotalCharges é a soma do que o cliente pagou ao longo do tenure (perguntas de negócio).
- **Internet:** existem só fibra e DSL. Segurança, backup, proteção, suporte e streaming exigem internet contratada (perguntas de negócio; validado no Notebook Dicionário de Dados, V3).
- **Pacotes:** o cliente não registra o combo contratado. Os “pacotes” deste relatório são combinações de serviços construídas no Notebook Análise Pacotes: 322 no total, 122 com 10 clientes ou mais e 30 com 30 clientes ou mais (validado no Notebook Análise Pacotes, V1). Pela quantidade de pacotes, presume-se que não há combos pré-montados (avaliação do analista).
- **Feedback:** a pesquisa de satisfação foi lançada depois do susto com os cancelamentos, com todos os clientes que a empresa conseguiu contatar, inclusive quem já tinha cancelado. Não tem data e pode ser de até alguns meses antes do resto da base. Existem todas as combinações: preencheu e cancelou, preencheu e recontratou, preencheu e manteve contrato, preencheu e manteve cancelado (perguntas de negócio).

## 4. Os cinco pilares

### 4.1 Preço e percepção de valor: confirma em parte

**Hipótese do mercado:** fatura alta sem uso dos adicionais, e saída quando a promoção acaba e a concorrência oferece pacote mais barato.

**Evidência** (Notebook Análise Pacotes):

- Entre os pacotes com 30 clientes ou mais e churn acima de 26,7%, o ticket médio varia de R$ 74,86 a R$ 104,88. Nos 10 de maior churn (a partir de 54,6%), varia de R$ 74,86 a R$ 100,07 (tabela Resumo de todos os pacotes, history\_pacotes).
- Os 5 pacotes de maior valor têm churn baixo. Quatro deles (P301, P276, P292 e P297) ficam entre 11,1% e 23,7%, incluem suporte e têm 30 clientes ou mais. E temos ainda o 5º pacote mais caro, na mesma faixa de churn baixo, que porém tem menos de 30 clientes. Entre os pacotes com 30 clientes ou mais, o seguinte mais caro (P272) já tem 46,4% de churn (validado no Notebook Análise Pacotes, V3).
- Pacotes com 100% de churn têm de 1 a 3 clientes, pouco para concluir (tabela Resumo de todos os pacotes, history\_pacotes).
- Não há informação de promoções, nem diferença relevante de preço entre clientes do mesmo pacote, inclusive por senioridade: idosos pagam R$ 80,01 e não idosos R$ 80,02 no mesmo pacote (validado no Notebook Análise Pacotes, V6). Essa parte da hipótese não tem dado que a sustente.

**Leitura:** o preço alto sozinho não explica o churn. Pacotes caros com churn alto, como P188, P316 e P318, são de fibra com streaming e sem suporte (ver 4.4).

### 4.2 Tipo de conexão: confirma na fibra

**Hipótese do mercado:** clientes de DSL migram para a fibra por limite de velocidade e instabilidade. Na fibra, as falhas pesam mais pela expectativa alta. Nesse sentido um bom suporte técnico tem peso.

**Evidência:**

- A fibra tem 42,1% de churn (1.042 de 2.477 clientes), contra 26,7% da média (validado no Notebook Análise Risco 3Fatores, V6). Exemplos: P130 com 56,8% (185 clientes) e P259 com 59,5% (131) (validado no Notebook Análise Pacotes, V8).
- O DSL tem 19,4% (373 de 1.924) (validado no Notebook Análise Risco 3Fatores, V6). A hipótese não diz que o DSL gera churn, então esse número serve de comparação e não a contraria.
- Feedback: Conexão é o tema com mais frases (seção 5).

**Leitura:** a base confirma o resultado esperado na fibra: churn alto, em linha com a ideia de expectativa alta.

### 4.3 Suporte e proteção: confirma

**Hipótese do mercado:** quem não tem TechSupport, DeviceProtection ou OnlineSecurity cancela mais. Quem os contrata tende a ficar.

**Evidência:**

- Com internet e sem TechSupport nem OnlineSecurity, o churn é 49,1% (1.011 de 2.058). Com pelo menos um dos dois, é 17,2% (404 de 2.343) (validado no Notebook Análise Pacotes, V5, e no Notebook Análise Risco 3Fatores, V6).
- Há 101 pacotes sem nenhum cancelamento, somando 522 clientes. Em 87 deles há TechSupport ou OnlineSecurity (validado no Notebook Análise Pacotes, V2). Todos têm no máximo 20 clientes (tabela Resumo de todos os pacotes, history\_pacotes).
- DeviceProtection: 23,4% de churn com o serviço contra 39,0% sem o serviço contratado. OnlineBackup: 22,3% contra 39,9% (validado no Notebook Análise Risco 3Fatores, V7). Os dois reduzem o churn, mas ficam fora dos 3 fatores da régua. A taxa é isolada, sem separar a sobreposição com suporte.
- Feedback: Atendimento quase não aparece no texto. Em Atendimento há 160 linhas (cliente × aspecto) na history, e Segurança tem 1 (validado no Notebook Análise Sentimento, V10). O peso vem dos pacotes (Notebook Análise Pacotes). Talvez o cliente não saiba identificar que precisa de Suporte como serviço contratado.

**Leitura:** entre os fatores de produto testados, é o que mais separa quem sai de quem fica. Os pacotes sem churn têm no máximo 20 clientes, então indicam um padrão, não uma regra.

### 4.4 Perfil de uso e composição: contraria em parte

**Hipótese do mercado:** linha fixa única, sem internet, cancela com facilidade. Streaming contratado e pouco usado gera a sensação de pagar por algo desnecessário.

**Evidência:**

- Só linha fixa (sem internet e sem MultipleLines): 953 clientes, churn de 8,5% e ticket médio de R$ 19,95, em todos os tipos de pagamento e de contrato (conforme base history; sem validação em notebook). O ticket de R$ 19,96 confere com o preço do PhoneService sozinho (validado no Notebook Análise Pacotes, V7).
- Todos os clientes sem internet somam 1.233, com 89 cancelamentos (7,2%), e todos têm PhoneService. Esse total é maior que 953 porque inclui quem tem MultipleLines (validado no Notebook Análise Risco 3Fatores, V7, e no Notebook Dicionário de Dados, V3).
- Fibra com streaming (TV ou filmes) tem churn mais alto que fibra sozinha, embora a fibra sozinha já seja alta.
- Sem suporte, a combinação lidera o churn entre os pacotes grandes: P188 com 76,3% (59 clientes), P316 com 71,7% (60) e P318 com 71,4% (84) (validado no Notebook Análise Pacotes, V2 e V8).

**Leitura:** a linha única (só Phone Service) contraria o mercado: a Terra Signal está na contramão. Sobre o streaming, a base não tem dado de uso, então não dá para dizer que é pouco usado. Dá para dizer que fibra com streaming e sem suporte concentra churn alto.

### 4.5 Contrato e pagamento: confirma

**Hipótese do mercado:** o contrato mês a mês é um dos fatores que mais pesam no churn. Boleto ou cheque têm mais churn que débito automático ou cartão.

**Evidência:**

- Contrato: mês a mês tem 42,7% de churn (1.322 de 3.099), 1 ano tem 11,6% (138 de 1.188) e 2 anos tem 3,3% (44 de 1.347). O mês a mês concentra 87,9% dos cancelamentos (validado no Notebook Análise Risco 3Fatores, V6).
- Pagamento: Electronic check tem 45,1% (852 de 1.888), cerca de 1,7 vez a média de 26,7% (18,4 p.p. acima). Os demais meios ficam entre 15,6% e 19,4% (validado no Notebook Análise Risco 3Fatores, V4).
- Juntos: mês a mês com Electronic check chega a 53,6% (784 de 1.464). Contrato de 2 anos fica entre 1,0% e 7,5% (validado no Notebook Análise Risco 3Fatores, V5).
- Preço do contrato: o preço do pacote não muda conforme o contrato, então o contrato longo não traz vantagem ao cliente. O preço praticado varia muito pouco em relação à soma dos serviços, um a um (validado no Notebook Análise Pacotes, V7).
- Feedback: clientes dizem gostar do mês a mês porque podem cancelar a qualquer momento (leitura direta da coluna CustomerFeedback da history).

**Leitura:** o contrato é o fator mais forte da base, e o Electronic check é um meio de pagamento problemático. O cheque por correio (19,4%) fica perto dos demais meios, então o problema está em um meio específico. E de certa forma o contrato month to month é uma facilidade para cancelamento (sem fidelidade no contrato).

## 5. O que os clientes dizem

O Notebook Análise Sentimento separou 25.362 frases de 5.634 clientes em aspectos e sentimentos (tabela de frases do feedback, history). O parágrafo de cada cliente é quebrado em frases para a análise, e a coluna Frases conta as frases encontradas por aspecto, não frases positivas ou negativas.

| Aspecto | Frases | Churn com menção negativa | Churn com menção positiva |
| --- | --- | --- | --- |
| Conexão | 8.708 | 92,9% | 13,2% |
| Cobrança | 6.228 | 86,6% | 16,4% |
| Contrato | 2.420 | 97,2% | 8,9% |
| Atendimento | 171 | sem menção negativa | 24,1% |

Preço fica fora da tabela porque muitas frases citam o valor sem criticar, então o dado não é conclusivo.

- **Dores:** Conexão é o tema com mais frases. Menção negativa em Conexão e em Cobrança vem com churn de 92,9% e 86,6%. Em Contrato vai a 97,2%, o maior entre os aspectos.
- **Sentimento de saída:** após uma melhoria no regex, o texto passou a ter o aspecto Saída. Quando o cliente usa termos ligados a saída (como “churn”) em frase com tom positivo, o sentimento é Negativo, ainda que não haja palavra negativa. O inverso também vale: “no churn”, por exemplo, é classificado como permanência (Positivo), ainda que não haja palavra de elogio. Só é classificado como Saída quando a frase não tem elogio nem reclamação, mas tem termos como “churn”.
- **Regras sobre o texto** (history, Notebook Análise Sentimento):
  - **R1:** sentimento do aspecto Saída. Se existe pelo menos uma citação Negativa, Churn Yes. Considera o que o cliente diz sobre sair e não indica motivo.
  - **R2:** sentimento dos aspectos Conexão, Preço, Cobrança e Contrato. Se existe pelo menos uma citação Negativa, Churn Yes.
  - **R:** sentimento de todos os aspectos (R1 + R2). Se existe pelo menos uma citação Negativa em Saída, Conexão, Preço, Cobrança ou Contrato, Churn Yes. Sem citação Negativa, Churn No.
- **Resultado das regras:** com o sentimento de saída, as regras reproduzem o Churn com 100% de acerto (R1), 97% (R) e 87% (R2), contra 73,3% se todos fossem classificados como “No” (validado no Notebook Análise Sentimento, V2 e V4, e no Notebook Análise Risco 3Fatores, V7). A meta era de 75% de acerto, e as três a atingem. Os clientes que cancelaram (1.504) têm 100% de cobertura em R1 e R.
- **Objetivo do feedback:** ser uma informação a mais no atendimento, trazendo o “humor” do cliente conforme seu último feedback. A informação contida no feedback se mostrou valiosa para embasar conclusões, e um feedback melhor estruturado, um formulário que direcione melhor o cliente a responder questões importantes de forma direta, tornaria esse dado mais confiável e de maior valia ainda.
- **Cuidado com vazamento:** os dados disponibilizados dessa coluna não têm data e podem ter sido escritos depois do cancelamento. Usá-la para prever churn seria data leakage, e a régua de risco não usa o texto.

## 6. Régua de risco (Notebook Análise Risco 3Fatores)

A régua do Notebook Análise Risco 3Fatores classifica cada cliente por 3 fatores, de 1 ponto cada:

1. **Conexão:** fibra óptica, ou StreamingTV, ou StreamingMovies. Como o streaming só existe com internet, o fator pega a fibra e também o DSL com streaming.
2. **Suporte:** sem TechSupport e sem OnlineSecurity.
3. **Contrato:** mês a mês com Electronic check.

Os três fatores correspondem aos cortes de maior churn (validado no Notebook Análise Risco 3Fatores, V6). O nível vem da soma: 3 fatores = Crítico, 2 = Alto, 1 = Moderado, 0 = Baixo. O tenure ajusta o nível em dois pontos, com corte em 24 meses (cortes de 12 e 18 meses foram testados e se mostraram menos eficientes):

- Com 2 fatores e tenure até 24 meses, sobe de Alto para Crítico. Cliente novo não tem hábito nem custo de troca acumulado.
- Com 3 fatores e tenure acima de 24 meses, cai de Crítico para Alto. Cliente antigo tem mais vínculo com a marca.

Resultado na history (validado no Notebook Análise Risco 3Fatores, V1):

| Nível | Sem ajuste: clientes (churn) | Com ajuste: clientes (churn) | % da history, com ajuste |
| --- | --- | --- | --- |
| Crítico | 882 (63,4%) | 1.278 (60,9%) | 22,7% |
| Alto | 1.257 (40,0%) | 861 (33,0%) | 15,3% |
| Moderado | 1.889 (16,2%) | 1.889 (16,2%) | 33,5% |
| Baixo | 1.606 (8,5%) | 1.606 (8,5%) | 28,5% |

O churn cai a cada nível nas duas versões. A régua será validada ao listar os clientes de maior risco da inference e atuar sobre eles.

**Ganho de assertividade:** a régua foi comparada com o churn real da history, para checar se os pilares levantados pelo Gemini fazem sentido nos dados. O Crítico com ajuste de tenure captura 51,7% dos cancelamentos, contra 37,2% do original: 39% mais cancelamentos capturados (de 559 para 778). O acerto do Crítico cai pouco, de 63,4% para 60,9% (validado no Notebook Análise Risco 3Fatores, V1 e V2).

**Impacto financeiro:** os 1.504 cancelamentos geram perda de R$ 112.242,90 por mês, sobre uma receita mensal de R$ 364.010,05 (30,8%) (validado no Notebook Análise Risco 3Fatores, V6, e no Notebook Análise Pacotes, V9). Os 8 pacotes de maior perda somam R$ 40.190,05 por mês, ou 35,8% da perda, com 31,2% dos cancelamentos (validado no Notebook Análise Pacotes, V9).

## 7. Fechamento: prováveis maiores causas de churn

Os fatores se sobrepõem. Quem reúne os três fatores da régua (Crítico sem ajuste) tem churn de 63,4% (559 de 882) (validado no Notebook Análise Risco 3Fatores, V1). Pela força dos números, a ordem provável é:

1. Contrato mês a mês com Electronic check (4.5).
2. Ausência de TechSupport e OnlineSecurity (4.3).
3. Fibra, mais forte com streaming e sem suporte (4.2 e 4.4).
4. Preço: sozinho não explica.

## 8. Limites

- **Feedback sem data:** o texto pode ter sido escrito antes ou depois do cancelamento, o que limita a leitura de causa e efeito.
- **Pacotes construídos:** não há registro dos combos, e muitos pacotes têm poucos clientes.
- **Dados que a base não tem:** desempenho técnico da conexão, migração de DSL para fibra, uso real do streaming, região do cliente e promoções.
- **Sobreposição de fatores:** DeviceProtection e OnlineBackup foram avaliados de forma isolada, sem separar a sobreposição com suporte.
- **Dados faltantes:** tenure nulo em 19 clientes da history e 4 da inference. Nesses 23, o tempo de casa aparece no texto do feedback e pode ser recuperado (TotalCharges ÷ MonthlyCharges serve de conferência). TotalCharges é nulo em 12 clientes: os 11 com tenure 0 (10 da history e 1 da inference), que são clientes novos e é esperado, e o cliente 9651-GTSAQ, que tem tenure e TotalCharges nulos e só o feedback informa o tempo (“mais de quatro anos”) (validado no Notebook Dicionário de Dados, V4).
- **Sem estrutura de retenção:** as premissas de custo e de capacidade da ação virão da nossa proposta (perguntas de negócio).

## 9. Apêndice: fontes

| Fonte | O que sustenta |
| --- | --- |
| Pesquisa de mercado (Gemini) | Os cinco pilares e suas hipóteses |
| Notebook Dicionário de Dados | Integridade da base: IDs, MultipleLines, serviços de internet e tenure |
| Notebook Análise Pacotes | Pacotes, preço por serviço, perda mensal por pacote e impacto financeiro |
| Notebook Análise Risco 3Fatores | Churn geral, contrato, pagamento, conexão, suporte, linha única, régua de risco e ganho de assertividade |
| Notebook Análise Sentimento | Frases, aspectos, sentimentos, regras R, R1 e R2 e vazamento do feedback |
| Perguntas de negócio | Definições, contexto da pesquisa de satisfação e ausência de estrutura de retenção |
