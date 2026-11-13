# Análise inicial dos dados e perguntas de negócio

Grupo 1. Análise feita sobre `history.csv` (5.634 linhas) e `inference.csv` (1.409 linhas).

## 1. O que a área de negócio (TS) já respondeu

| Tema | Resposta |
|---|---|
| `MonthlyCharges` | Valor total pago no mês, com taxas, encargos e serviços. |
| `TotalCharges` | Basicamente a soma de `MonthlyCharges` ao longo do tempo. Os nulos vêm de perda de dados; a estratégia para eles fica a nosso critério. |
| Moeda | Considerar R$. |
| `tenure` | Em meses. |
| Período | A TS tem cerca de 7 anos. Todas as colunas são do mesmo instante, **exceto `CustomerFeedback`, que pode ser de alguns meses antes**. History e inference seguem o mesmo recorte temporal. |
| Uso do modelo | Evitar cancelamentos: identificar dores e tendências e propor um plano de ação. Ex.: conta alta para os serviços contratados → desconto preventivo. |
| Recall vs. precisão | O objetivo é financeiro: a estratégia não pode custar mais do que retorna. |
| `MultipleLines` | `No` = uma linha; `No phone service` só ocorre quando `PhoneService = No`. |
| Serviços adicionais | Podem ser contratados avulsos, mas costumam vir em combos que não estão registrados. Só existem para quem tem internet da TS. |

### Perguntas ainda sem resposta

- `Partner`: cônjuge ou parceiro comercial?
- `Dependents`: pessoas vinculadas ao contrato?
- `SeniorCitizen`: qual idade define? Existe pacote para a terceira idade?
- **O que é churn para o negócio?** `Churn = Yes` quer dizer que o serviço está cancelado hoje ou que o cliente já cancelou alguma vez?
- `tenure` conta até o cancelamento ou até a data atual?

## 2. Regras de negócio conferidas nos dados

| Regra | Resultado |
|---|---|
| `No phone service` ⇔ `PhoneService = No` | OK, 0 violações (history e inference). |
| `No internet service` nos 6 serviços adicionais ⇔ `InternetService = No` | OK, 0 violações. |
| Todo cliente tem telefone ou internet | OK. |
| `TotalCharges ≈ MonthlyCharges × tenure` | OK. Mediana da razão = 1,00; 90% dos casos entre 0,93 e 1,08. |
| `TotalCharges ≥ MonthlyCharges` | OK, 0 violações. |

## 3. Inconsistências encontradas (limpeza)

| Coluna | Problema | History | Inference | Tratamento sugerido |
|---|---|---|---|---|
| `tenure` | Texto `"unknown"` (coluna lida como string) | 19 | 4 | Recuperar por `TotalCharges / MonthlyCharges` ou pelo número de meses citado no feedback; se não der, imputar. |
| `tenure` | Valor 0 (cliente novo) | 10 | 1 | Manter. Em todos esses casos `TotalCharges` é nulo, o que faz sentido. |
| `PhoneService` | Mistura `Yes/No` com `yes/no` | 70 | — | Padronizar a capitalização. |
| `TotalCharges` | Nulo | 278 | 64 | Imputar `MonthlyCharges × tenure` (0 quando `tenure = 0`). |
| `MonthlyIncome` | Valores muito baixos (≤ R$ 500); 1 caso com renda < mensalidade | 190 | 55 | Confirmar com a TS se é a renda do cliente. |
| `CustomerFeedback` | Valores em `$`, enquanto a TS disse R$ | — | — | O valor citado bate 100% com `MonthlyCharges`; é só a moeda no texto. |

## 4. Primeiros sinais de churn (taxa de churn no history = 26,7%)

| Variável | Maior risco | Menor risco |
|---|---|---|
| `Contract` | Month-to-month: 42,7% | Two year: 3,3% |
| `tenure` | 0–6 meses: 52,4% | 49–72 meses: 9,5% |
| `InternetService` | Fiber optic: 42,1% | Sem internet: 7,2% |
| `PaymentMethod` | Electronic check: 45,1% | Cartão automático: 15,6% |
| `SeniorCitizen` | Idoso: 42,3% | Não idoso: 23,6% |
| `TechSupport` | Sem suporte: 41,8% | Com suporte: 15,3% |
| `MonthlyCharges` | R$ 70–90: 37,3% | Até R$ 35: 11,0% |
| `MonthlyIncome` | Sem efeito (26–28% em todos os quartis) | |

## 5. ⚠️ Vazamento do alvo em `CustomerFeedback`

Quando o feedback diz que o cliente **já cancelou** (por exemplo "decided to churn", "had to cancel", "canceled", "decided to switch"):

| | Churn = No | Churn = Yes |
|---|---|---|
| Texto diz que já cancelou | **0** | **1.475** |
| Texto não diz | 4.130 | 29 |

Só essa regra acerta 98% dos churns, sem nenhum falso positivo. Esse tipo de expressão aparece em **25,6%** dos textos do `inference.csv`.

Isso **parece não combinar** com a resposta de que o feedback "pode ser de até alguns meses antes": nesses textos, o cliente escreve que já saiu. A base não tem a data do feedback, então a ordem no tempo é uma hipótese a confirmar com a TS. Consequências:

- Para o `prediction.csv`, usar o texto aumenta muito a nota.
- Para o caso de uso real (prever *antes* de o cliente sair), o modelo não pode depender do texto de cancelamento. Proposta: **dois modelos** — (a) completo, com NLP, para a submissão; (b) só com dados cadastrais/contratuais, para o time de vendas agir antes do churn — e mostrar isso à banca.

## 6. Novas perguntas sugeridas para a TS

1. **Feedback x cancelamento:** cerca de 1.360 feedbacks dizem que o cliente já cancelou, mas a resposta foi que o feedback é anterior aos dados. Os feedbacks foram coletados depois do cancelamento? No uso real, teremos feedback para clientes ativos?
2. **Clientes do `inference.csv`:** são clientes ativos hoje? (Alguns textos dizem que já cancelaram.)
3. **Economia da retenção:** quanto custa uma ação de retenção (desconto típico, custo da ligação)? Qual a taxa de aceite esperada? Qual o custo de aquisição de um cliente novo? Isso define o ponto de corte do modelo.
4. **`MonthlyIncome`:** é a renda do cliente? Como foi obtida? Há 245 clientes com renda ≤ R$ 500.
5. **Avaliação do `prediction.csv`:** qual métrica será usada (acurácia, F1, recall, AUC)? A previsão deve ser `Yes/No` ou uma probabilidade?

---

## 7. Perguntas analíticas: resultados

Feito em Python local sobre os CSVs. Para o modelo: validação cruzada estratificada com 5 folds.

### Parte 1: inconsistências

| # | Pergunta | Resultado |
|---|---|---|
| 2 | Os IDs seguem o padrão `NNNN-XXXXX`? | Sim, 100% nas duas bases. |
| 4 | Há faltantes disfarçados? | Só o `"unknown"` em `tenure`. Nenhum vazio, espaço ou "N/A" nas outras colunas. |
| 5 | Há variação de grafia? | Só em `PhoneService` (`yes/no`): 70 no history e 23 no inference. |
| 6 | Há linhas duplicadas ignorando o ID? | Não. |
| 10 | Onde `TotalCharges` difere mais de 15% de `Monthly × tenure`? | 113 linhas no history e 28 no inference, quase todas com tenure entre 2 e 8 meses (efeito de reajuste ou promoção, que pesa mais quando há poucos meses). Com tenure acima de 12 meses, só 0,4%. **Não parece erro.** |
| 11 | A mensalidade é coerente com os serviços? | **Sim, a tabela de preços é quase exata (R² = 0,999):** telefone R$ 20, linha extra +R$ 5, DSL R$ 25, **fibra R$ 50**, cada serviço de segurança, backup, proteção ou suporte +R$ 5, cada streaming +R$ 10. Resíduo de ±R$ 2,50. Nenhum cliente fora da tabela. |
| 12 | `MonthlyIncome` é plausível? | **Parece ruído aleatório:** distribuição uniforme de R$ 100 a R$ 10.000, correlação ≈ 0 com a mensalidade, mesma média para idosos e não idosos e para quem tem ou não dependentes, nenhum efeito no churn. Tirar a variável do modelo não muda nada (AUC 0,8276 → 0,8271). |
| 14 | Os meses citados no texto batem com `tenure`? | Sim. Das 3.084 menções no history, só 1 não bate (e 3 das 763 no inference). **O texto ajuda a recuperar `tenure = "unknown"`.** Com `TotalCharges / MonthlyCharges` mais o texto, sobra 1 caso sem tenure. |
| 15 | O tipo de internet citado no texto bate com a coluna? | Sim, praticamente 100% (fibra, DSL, sem internet). |
| 16 | A forma de pagamento citada bate com a coluna? | Sim. As poucas divergências são clientes de cheque eletrônico dizendo que *prefeririam* cartão. |
| 17 | Quem são os churns sem texto de cancelamento? | Ampliando as expressões ("had to cancel", "needed to cancel"), sobram só 29. Mesmo esses têm texto negativo. |
| 18 | Há drift entre history e inference? | Não. As proporções diferem no máximo 2,2 p.p. e as médias são praticamente iguais. |
| 19 | Nulos e textos de cancelamento são parecidos nas duas bases? | Nulos em `TotalCharges`: 4,9% contra 4,5%. Texto de cancelamento: 26,2% contra 25,6%. Isso é coerente com uma taxa de churn semelhante no inference. |

### Parte 2: modelo

**Fatores de churn**

| # | Pergunta | Resultado |
|---|---|---|
| 23 | Interações | **Contrato mensal com até 6 meses: 54,6%.** Contrato de 2 anos: 0% no início e 3,6% depois. **Fibra sem TechSupport: 49,3%** (fibra com suporte: 22,9%). **Cheque eletrônico com fatura digital: 49,0%.** Idoso com fibra: 47,6%. |
| 24 | Mais serviços adicionais seguram o cliente? | **Muito.** 0 serviços: 50,9% → 3: 28,0% → 6: 6,9%. A queda é monotônica. |
| 25 | Pagar acima do preço esperado aumenta o churn? | **Não.** Não existe "sobrepreço" (pergunta 11), e o churn fica entre 25% e 28% em todos os quintis do resíduo. A hipótese da TS de "conta alta para os serviços" não se confirma como sobrepreço. O que pesa é a **conta alta em si** (fibra). |
| 26 | O peso da conta na renda explica o churn? | Só o quintil mais baixo difere (13,8% contra cerca de 30%), e isso vem da mensalidade baixa, não da renda. Não acrescenta informação. |
| 27 | Onde o churn de clientes novos (≤ 6 meses) se concentra? | **Fibra: 73,5%** (DSL 48,8%, sem internet 21,1%). Cheque eletrônico: 66,4%. 95% dos clientes novos estão no contrato mensal. |

**Feedback (NLP)**

| # | Pergunta | Resultado |
|---|---|---|
| 28 | Quais dores aparecem e quais se ligam ao churn? | **Preço**: 42,7% dos churners mencionam, e 100% de quem menciona cancelou. **Contrato/flexibilidade**: 68,2% dos churners. **Velocidade**: 37,6%. **Pagamento**: 30,5%. **Instabilidade**: 24,5%. **Atendimento**: 5,5%. **Mudança de vida**: 5,7%, com 100% de churn. |
| 29 | Clientes ativos reclamam? | Quase nunca: só 129 dos 4.130 não churners têm texto negativo, e "estou pensando em sair" aparece só em 5 textos, todos de churners. No inference, só 40 textos são negativos sem falar em cancelamento. **O conteúdo do feedback dos churners indica que foi escrito depois da decisão de sair, mas a base não tem a data do texto: falta a TS confirmar como e quando ele é coletado.** Para clientes ativos, o texto quase não traz sinal antecipado. |

**Desenho do modelo**

| # | Pergunta | Resultado |
|---|---|---|
| 31 | Quanto se ganha com e sem o texto? | **Só dados cadastrais:** regressão logística com AUC 0,840, F1 0,595 e acurácia 80,1%. **Com indicadores do texto:** AUC 0,9996, F1 0,990 e acurácia 99,5%. O texto quase resolve o problema sozinho, o que confirma o vazamento. |
| 32 | Há variáveis redundantes? | `tenure` e `TotalCharges` têm correlação 0,83, e `TotalCharges` é praticamente `Monthly × tenure`. `MonthlyCharges` é a soma dos serviços. Funcionam bem para modelos de árvore, mas causam colinearidade na regressão logística. |

**Valor financeiro**

| # | Pergunta | Resultado |
|---|---|---|
| 33 | Quanto da receita está em risco? | Os churners são 26,7% dos clientes, mas **30,8% da receita mensal** (R$ 112 mil de R$ 364 mil), porque pagam mais: R$ 74,63 contra R$ 60,96. A receita perdida vem **86% do contrato mensal, 82% de fibra e 60% de cheque eletrônico**. |
| 34 | A partir de que probabilidade vale agir? | Depende do custo da ação e da taxa de aceite, que **precisamos pedir à TS**. Regra: agir quando `p(churn) × taxa_aceite × valor_do_cliente > custo_da_ação`. |
| 35 | Quais clientes valem mais? | Faixa de R$ 70–90: 37,7% de churn. Acima de R$ 90: 33,8%. Os churners ficam em média 18,4 meses, contra 37,4 dos que ficam. Os clientes de fibra no começo do contrato são o grupo de maior valor em risco. |

## 8. Implicações para o modelo e o plano de ação

- **Limpeza:** padronizar `PhoneService`; recuperar `tenure` por `TotalCharges / MonthlyCharges` ou pelo texto; imputar `TotalCharges = Monthly × tenure`; avaliar se vale tirar `MonthlyIncome`.
- **Duas versões do modelo:**
  - (a) **Submissão**: dados cadastrais + texto. A acurácia esperada é de cerca de 99%.
  - (b) **Uso real pelo time de vendas**: só dados cadastrais, com AUC de cerca de 0,84. É a que antecipa o churn de verdade.
- **Variáveis úteis:** número de serviços adicionais, fibra sem suporte, contrato mensal × tenure, cheque eletrônico × fatura digital.
- **Plano de ação que os dados sustentam:**
  1. **Onboarding de fibra:** acompanhamento nos 6 primeiros meses (73,5% de churn) e TechSupport incluído para clientes de fibra.
  2. **Migração de contrato:** oferecer desconto para sair do mensal para o anual ou o de 2 anos, onde o churn cai de 42,7% para 11,6% ou 3,3%.
  3. **Bundles de serviços adicionais:** cada serviço a mais reduz o churn.
  4. **Débito automático:** incentivar a troca do cheque eletrônico.
  5. **Preço:** é a dor mais citada pelos churners. Ofertas de desconto preventivo para clientes de fibra com conta alta.
