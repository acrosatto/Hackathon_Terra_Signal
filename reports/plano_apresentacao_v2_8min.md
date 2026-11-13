# Plano de conteúdo da apresentação (v2, 8 minutos)

Grupo 1. Versão curta da [v1](plano_apresentacao_v1.md): 9 slides, com cerca de 50 segundos cada, mantendo os 4 blocos e o destaque para o lift. Cada slide tem uma única mensagem, e o detalhe técnico vai para o apêndice, para responder à banca nas perguntas.

| Bloco | Slides | Tempo |
|---|---|---|
| Abertura | 1 | 0,5 min |
| Descobertas da análise | 2 e 3 | 1,5 min |
| Construção das variáveis | 4 | 1,5 min |
| Modelos testados | 5 | 1 min |
| Métricas, com o lift em destaque | 6, 7 e 8 | 2,5 min |
| Fechamento | 9 | 1 min |

## Abertura (0,5 min)

**1. "26,7% dos clientes saem, e levam 30,8% da receita"**
- São R$ 112 mil em risco de R$ 364 mil mensais, porque os churners pagam mais (R$ 74,63 contra R$ 60,96).
- O objetivo é uma lista priorizada de quem abordar antes de o cliente sair.

## Descobertas da análise (1,5 min)
*Origem: notebook 03 e `reports/analise_inicial_e_perguntas.md`*

**2. "O risco se concentra no contrato mensal, nos clientes novos e na fibra"**

| Fator | Maior risco | Menor risco |
|---|---|---|
| Contrato | Mensal: 42,7% | Dois anos: 3,3% |
| Tempo de casa | 0 a 6 meses: 52,4% | 49 a 72 meses: 9,5% |
| Internet | Fibra: 42,1% | Sem internet: 7,2% |
| Pagamento | Cheque eletrônico: 45,1% | Cartão automático: 15,6% |

- Destaque falado: entre os clientes novos com fibra, o churn é de 73,5%.

**3. "O que deixamos fora do modelo, e por quê"**
- **Feedback:** os textos que dizem que o cliente já cancelou são 1.475 de churners e nenhum de cliente ativo. Com ele, a AUC iria a 0,9996, mas o texto parece escrito depois da decisão de sair. Um modelo útil precisa agir antes.
- **Mensalidade:** segue uma tabela de preços exata (R² 0,999), então não há sobrepreço. O que pesa é o produto (fibra).
- **Renda:** é ruído uniforme, sem efeito no churn.

## Construção das variáveis (1,5 min)
*Origem: notebooks 06, 07 e 08*

**4. "Do dado bruto ao modelo em 4 passos"**
- Diagrama do fluxo, com um número em cada passo:
  1. **Limpeza:** 22 colunas, das quais 16 entram.
  2. **Imputação:** `tenure` "unknown" recuperado por `TotalCharges / MonthlyCharges` (erro de até 2 meses em 96% dos casos). `TotalCharges` nulo vira `MonthlyCharges × tenure` (erro mediano de 2,0%).
  3. **Discretização por AID:** o tempo de casa vira 6 faixas de risco (até 5 meses, 6 a 17, 18 a 43, 44 a 59, 60 a 70 e acima de 70).
  4. **Dummies:** 25 no total, sem precisar agrupar categorias (no máximo 4 por variável).
- Frase falada: testamos segmentar a base por contrato, o melhor corte pelo AID e pela árvore, mas um modelo único rende o mesmo.

## Modelos testados (1 min)
*Origem: notebook 09*

**5. "Logística, árvore e boosting: escolhemos a logística, que empata e é explicável"**

| Técnica | AUC |
|---|---|
| Boosting | 0,8449 |
| Regressão logística | 0,8448 |
| Árvore | 0,8254 |
| Referência (sem modelo) | 0,5000 |

- Validação cruzada aninhada, com 5 folds e 4 repetições, e o AID refeito dentro de cada fold.
- A logística é calibrada (erro médio de 0,8 ponto percentual por decil), então a probabilidade pode ser lida diretamente como risco.

## Métricas, com o lift em destaque (2,5 min)
*Origem: notebooks 09 e 10, mais o notebook 11 a fazer*

**6. "Nos 10% de maior risco, há 2,8 vezes mais churners do que numa lista aleatória"**
- Este é o slide principal. Mostra o gráfico de lift acumulado por decil, com uma linha de referência em 1.
- Lift por fatia da base: 2,84 em 10%, 2,53 em 20%, 2,23 em 30%, 1,98 em 40% e 1,75 em 50%.

**7. "Atendendo 20% da base, a retenção alcança metade dos churners"**
- Curva de churners encontrados: 50,6% com 20% da base e 79,1% com 40%.
- O ponto da capacidade da equipe fica marcado quando a TS responder.

**8. "As outras métricas confirmam o mesmo quadro"**
- AUC de 0,845.
- Acurácia de 80,1%, contra 73,3% de quem prevê sempre `No`.
- No corte de 0,5: precisão de 66,4%, recall de 51,8% e F1 de 0,581.

## Fechamento (1 min)

**9. "Como a TS usa isso amanhã"**
- A TS recebe a lista ranqueada por risco e age quando `p(churn) × aceite × valor > custo`.
- Prioridades: clientes novos em contrato mensal com fibra e a migração do cheque eletrônico para o pagamento automático.
- Próximos passos: definir com a TS o tamanho da lista e o corte.

## Apêndice (para as perguntas da banca)

- **A1. Imputação em detalhe:** quantidade de casos (19 + 4 e 278 + 64), a linha removida e o teste da categoria "Ausente".
- **A2. Método AID:** divisões binárias pelo qui-quadrado, mínimo de 5% por faixa, correção de Bonferroni, e por que `TotalCharges` ficou fora (+0,0006 de AUC e cortes instáveis).
- **A3. Segmentação:** contrato mensal contra os demais, com qui-quadrado de 899 e raiz da árvore em 200 de 200 bootstraps. Modelos separados não superam o único (−0,0005 ± 0,0024 de AUC).
- **A4. O que o modelo aprendeu:** razões de chance de tempo de casa, internet, contrato, `TechSupport` (0,70) e `OnlineSecurity` (0,72). Os streamings ficam com OR acima de 1. O OR mostra associação e não prova o efeito de uma ação.
- **A5. Limites:** AUC de 0,716 no grupo mensal com fibra, ausência de horizonte de tempo e definição de `tenure` e de churn a confirmar com a TS.

## O que ainda falta produzir

- **Gráficos de lift e de churners encontrados por decil** (slides 6 e 7), no notebook 11.
- **Diagrama do fluxo de preparação**, com as 6 faixas de tempo de casa (slide 4).
