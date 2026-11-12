# Plano de conteúdo da apresentação (v1, 15 minutos)

Grupo 1. O pitch tem 15 minutos, então o plano tem 16 slides, cerca de 1 minuto cada, divididos em abertura, 4 blocos e um fechamento. O título de cada slide é a conclusão dele, e não o tema. Ao lado de cada bloco está a origem dos números.

## Abertura (1 min)

**1. "26,7% dos clientes saem, e levam 30,8% da receita"**
- Os churners pagam mais: R$ 74,63 contra R$ 60,96 por mês. São R$ 112 mil em risco de R$ 364 mil mensais.
- O objetivo é uma lista priorizada de quem abordar antes de o cliente sair.

## Bloco 1: o que de fato foi relevante na análise (3,5 min)
*Origem: notebook 03 e `reports/analise_inicial_e_perguntas.md`*

**2. "O risco se concentra no contrato mensal, nos clientes novos e na fibra"**

| Fator | Maior risco | Menor risco |
|---|---|---|
| Contrato | Mensal: 42,7% | Dois anos: 3,3% |
| Tempo de casa | 0 a 6 meses: 52,4% | 49 a 72 meses: 9,5% |
| Internet | Fibra: 42,1% | Sem internet: 7,2% |
| Pagamento | Cheque eletrônico: 45,1% | Cartão automático: 15,6% |

- Destaque: entre os clientes novos com fibra, o churn é de 73,5%.

**3. "O feedback entrega a resposta, por isso ficou fora do modelo"**
- Textos que dizem que o cliente já cancelou: 1.475 churners e nenhum cliente ativo.
- Com o texto, a AUC é de 0,9996. Sem ele, fica em 0,84.
- O texto parece escrito depois da decisão de sair, e um modelo útil precisa agir antes. É um slide que mostra maturidade para a banca.

**4. "Duas variáveis que pareciam importantes não são"**
- `MonthlyCharges` segue uma tabela de preços exata (R² 0,999), então não existe sobrepreço. A hipótese de "conta alta para os serviços" não se confirma: o que pesa é o produto (fibra).
- `MonthlyIncome` é ruído uniforme e não tem efeito no churn.

## Bloco 2: construção das variáveis (3 min)
*Origem: notebooks 06, 07 e 08*

**5. "Do dado bruto ao modelo em 4 passos"**
- Diagrama do fluxo: limpeza → imputação → discretização por AID → dummies.
- São 22 colunas, das quais 16 entram e viram 25 dummies.
- Ficam fora `customerID`, `CustomerFeedback`, `MonthlyIncome`, `MonthlyCharges`, `TotalCharges` e `PhoneService`. `PhoneService` é redundante com `MultipleLines`.

**6. "Os vazios foram recuperados pela própria regra do negócio"**
- `tenure` "unknown" (19 + 4 casos) foi recuperado por `TotalCharges / MonthlyCharges`, com erro de até 2 meses em 96% dos casos.
- `TotalCharges` nulo (278 + 64 casos) virou `MonthlyCharges × tenure`, ou 0 para clientes novos. O erro mediano é de 2,0%.
- Removemos 1 linha sem nenhum dos dois valores. Testamos uma categoria "Ausente", que não trouxe ganho.

**7. "O AID dividiu o tempo de casa em 6 faixas de risco"**
- Gráfico de churn por faixa: até 5 meses, 6 a 17, 18 a 43, 44 a 59, 60 a 70 e acima de 70.
- O método faz divisões binárias sucessivas pelo qui-quadrado, com pelo menos 5% dos clientes por faixa e correção de Bonferroni.
- `TotalCharges` foi testada e descartada: ganho de apenas +0,0006 de AUC e cortes instáveis.

**8. "Agrupamento e segmentação: decisões testadas, não supostas"**
- Nenhuma categórica precisou de agrupamento: o máximo é de 4 categorias, e a menor tem 563 clientes. A referência de cada dummy é a categoria mais frequente.
- Para segmentar, o contrato mensal contra os demais é o melhor corte: qui-quadrado de 899, e a árvore o escolheu como raiz em 200 de 200 bootstraps.
- Mesmo assim, modelos separados não superam o modelo único (−0,0005 ± 0,0024 de AUC). Por isso, ficou um modelo único com `Contract` como dummy.

## Bloco 3: modelos testados (2,5 min)
*Origem: notebook 09*

**9. "Testamos três técnicas com uma validação justa"**
- A validação é cruzada aninhada, com 5 folds e 4 repetições. O AID é refeito dentro de cada fold, para não vazar informação.

| Técnica | AUC |
|---|---|
| Boosting | 0,8449 |
| Regressão logística | 0,8448 |
| Árvore | 0,8254 |
| Referência (sem modelo) | 0,5000 |

**10. "Escolhemos a logística: empata com o boosting e é explicável"**
- A regra foi definida antes de ver o resultado: escolher a técnica mais simples dentro de 1 desvio da melhor.
- O boosting escolheu profundidade 1 em todos os folds, ou seja, efeitos aditivos. Isso combina com o fato de nenhuma das 199 interações testadas ter sobrevivido.
- A logística é calibrada, com erro médio de 0,8 ponto percentual por decil. Por isso, a probabilidade pode ser lida diretamente como risco.

**11. "O que o modelo aprendeu"**
- Razões de chance (OR):
  - Tempo de casa de até 5 meses: 4,76. Acima de 70 meses: 0,22.
  - Contrato de dois anos: 0,27.
  - Sem internet: 0,17.
  - Cartão automático: 0,71.
  - `TechSupport`: 0,70. `OnlineSecurity`: 0,72.
- Isso ajusta uma leitura da análise inicial: os streamings ficam com OR acima de 1. Logo, não são todos os serviços que seguram o cliente.
- Ressalva: o OR mostra uma associação e não prova o efeito de uma ação.

## Bloco 4: métricas, com destaque para o lift (3 min)
*Origem: notebooks 09 e 10, mais o notebook 11 a fazer*

**12. "Nos 10% de maior risco, há 2,8 vezes mais churners do que numa lista aleatória"**
- Este é o slide principal. Mostra o gráfico de lift acumulado por decil, com uma linha de referência em 1.
- Lift por fatia da base: 2,84 nos 10% de maior risco, 2,53 em 20%, 2,23 em 30%, 1,98 em 40% e 1,75 em 50%.

**13. "Atendendo 20% da base, a retenção alcança metade dos churners"**
- Curva de churners encontrados: 50,6% com 20% da base e 79,1% com 40%.
- O ponto da capacidade da equipe fica marcado quando a TS responder.

**14. "As outras métricas confirmam o mesmo quadro"**
- AUC de 0,845.
- Acurácia de 80,1%, contra 73,3% de quem prevê sempre `No`. Esse número mostra por que a acurácia engana nesta base.
- No corte de 0,5: precisão de 66,4%, recall de 51,8% e F1 de 0,581. O arquivo entregue marca 297 de 1.409 clientes.
- Limite: no grupo mensal com fibra, a AUC cai para 0,716.
- As bases `history` e `inference` são parecidas (AUC adversarial de 0,495), então o desempenho deve se manter no `inference`.

## Fechamento (2 min)

**15. "Como a TS usa isso amanhã"**
- A TS recebe a lista ranqueada por risco. A regra para agir é `p(churn) × aceite × valor > custo`.
- Prioridades:
  - Clientes novos em contrato mensal com fibra.
  - Migração do cheque eletrônico para o pagamento automático.
  - Oferta de `TechSupport` e `OnlineSecurity`, a validar com um piloto.

**16. "Limites e próximos passos"**
- O corte e o tamanho da lista dependem da TS.
- A base não tem horizonte de tempo.
- Falta confirmar a definição de `tenure` e de churn.

## O que ainda falta produzir

- **Gráficos de lift e de churners encontrados por decil** (slides 12 e 13), no notebook 11.
- **Gráfico de churn por faixa de tempo de casa** (slide 7), que precisa das taxas por faixa do notebook 07.
- **Diagrama do fluxo de preparação** (slide 5).

Se o tempo apertar, os slides 8 e 11 podem ir para um apêndice, junto com o detalhe do método AID.
