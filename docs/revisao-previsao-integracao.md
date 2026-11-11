# Conferência de previsão, balanço e seções

Revisão da base `ebab10a20fed613d0afcf71712627b471b53c412`, referente às
conferências previstas nas issues #2, #4, #8, #12 e #13. Esta conferência foi
realizada nesta entrega; não representa uma aprovação pessoal de Gabriel.

## Histórico e modelo (#2 e #8)

O arquivo `dados/historico_eolico.json` contém três pares sintéticos: vento
8, 10 e 12 m/s e energia 20, 25 e 30 kWh, em intervalos de 1 h. O carregamento
valida séries pareadas; o fluxo integrado também confere a duração do histórico
com a do cenário antes de ajustar a reta. Histórico inválido ou incompatível
impede a previsão, mas preserva o balanço e as decisões do intervalo atual.

Conta independente: médias 10 m/s e 25 kWh; soma dos produtos dos desvios
20 e soma dos quadrados dos desvios do vento 8. Logo, `a = 20/8 = 2,5` e
`b = 25 - 2,5 × 10 = 0`. Para 11 m/s, `y = 27,5 kWh` e não há extrapolação;
para 13 m/s, `y = 32,5 kWh` com aviso. Vento histórico constante não permite
ajuste. `tests/test_modelo_energia.py` confronta esses resultados com valores
fixos e cobre histórico degenerado, além da integração com o balanço.

## Balanço e previsão (#4 e #8)

No cenário `deficit`, a conta observada é `20 + 20 - 70 = -30 kWh`.
A reserva de 15 kWh cobriria hipoteticamente 15 kWh, deixando 15 kWh de
déficit. No próximo intervalo, supondo solar de 20 kWh e consumo de 70 kWh,
troca-se a eólica observada pela previsão: `20 + 27,5 - 70 = -22,5 kWh`.
Se a cobertura atual hipotética ocorrer integralmente, restam 0 kWh de
reserva; ela não é contada novamente. O programa não realiza descarga ou
controle físico. A energia está em kWh por intervalo, não em kW.

## Seções do relatório (#12 e #13)

- `docs/secoes/previsao_energia.md` apresenta a conta, as hipóteses, os
  intervalos, a separação entre observado e previsto e as limitações do modelo.
- `docs/secoes/dados_decisoes.md` apresenta as estruturas e um exemplo
  rastreável de entrada, condição, ação e motivo. A saída executada para
  `deficit` confirma o alerta, a preservação do suporte à vida e a recomendação
  de avaliar a redução do laboratório, bem como o saldo futuro.
- As seções são coerentes com o exemplo reproduzido e deixam claro que as
  ações são recomendações. A conferência não substitui a revisão dos demais
  responsáveis nem comprova uma economia real ou uma operação física.

## Reprodução

Na base acima, `python3 -m unittest discover -s tests` executou 100 testes com
resultado `OK`. `python3 main.py --cenario deficit` exibiu saldo atual de
-30 kWh, previsão eólica de 27,5 kWh e saldo futuro de -22,5 kWh com reserva
restante hipotética de 0 kWh. Os dados são didáticos e não medições reais.
