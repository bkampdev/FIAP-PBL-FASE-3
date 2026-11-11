# Previsão e eficiência energética

A colônia usa um histórico **sintético** de vento `[8, 10, 12]` m/s e geração eólica `[20, 25, 30]` kWh, em intervalos de **1 h**. O módulo `src/previsao.py` ajusta uma regressão linear simples por mínimos quadrados, `y = a*x + b`, em que `x` é vento em m/s e `y` é energia eólica em kWh no intervalo. O coeficiente `a` tem unidade kWh/(m/s), e `b`, kWh.

As médias são 10 e 25. A soma dos produtos dos desvios é 20 e a soma dos quadrados dos desvios de vento é 8: `a = 20/8 = 2,5`, `b = 25 - 2,5*10 = 0`. Para vento previsto de 11 m/s, a estimativa é **27,5 kWh**, sem arredondar para 27. `docs/validacao_matematica.md` detalha a conta; `tests/test_modelo_energia.py` compara o resultado real do módulo com esses valores independentes.

## Balanço observado

`analisar_energia(cenario)` soma a geração solar/eólica e os consumos dos sistemas, identificando separadamente o consumo essencial. O saldo é geração menos consumo, sem incluir a reserva. As energias de entrada são não negativas e finitas; dados inválidos produzem `ValueError`. O módulo não modifica os dados nem escolhe sistemas para desligamento.

| Solar | Eólica | Consumo | Reserva | Saldo observado | Classificação | Cobertura potencial | Déficit remanescente |
|---|---|---|---|---|---|---|---|
| 20 | 20 | 70 | 15 | -30 | déficit | 15 | 15 |
| 50 | 30 | 30 | 10 | +50 | excedente | 0 | 0 |
| 25 | 25 | 50 | 10 | 0 | equilíbrio | 0 | 0 |

Todos os valores da tabela estão em kWh. Reserva é estoque disponível; sua cobertura é **hipotética**, sem descarga executada. A classificação continua déficit mesmo se a reserva puder cobri-lo integralmente. Excedente permite sugerir avaliação de armazenamento; capacidade e carga real não estão implementadas. A prioridade de suporte à vida e as recomendações de redução pertencem ao módulo de decisões, não ao cálculo do balanço.

## Planejamento do próximo intervalo

No primeiro cenário, supondo explicitamente a mesma geração solar de 20 kWh e consumo planejado de 70 kWh no próximo intervalo de 1 h, substituímos somente a geração eólica observada pela estimativa de 27,5 kWh: `saldo_futuro = 20 + 27,5 - 70 = -22,5 kWh`. Não somamos a eólica observada e prevista. Se a cobertura potencial atual de 15 kWh for considerada, a reserva restante hipotética é `15 - 15 = 0 kWh`; não podemos reaplicar os mesmos 15 kWh ao futuro.

A estimativa permite antecipar um déficit menor que o atual e orientar avaliação de redução das cargas não essenciais, preservando essenciais. Essa conta é uma hipótese de planejamento, sem economia medida, desligamento realizado ou garantia de segurança. O teste de integração entre previsão e energia confere os saldos -30 e -22,5 e a ausência de reaplicação da reserva, sem alterar o cenário original.

## Limitações

O histórico contém apenas três pares sintéticos. A reta é aproximação local, não a curva física completa de uma turbina. Para 13 m/s, fora da faixa histórica, o modelo fornece 32,5 kWh com aviso de extrapolação. Dados sem variação de vento impedem o ajuste. Uma estimativa negativa é preservada com aviso de invalidade física e não deve entrar no planejamento como geração disponível.

Histórico e cenário precisam ter a mesma duração de intervalo. A API de balanço recebe energias em kWh e estoque em kWh; não recebe potência em kW nem multiplica novamente energia por horas. `intervalo_h` positivo tem padrão didático de 1 h quando ausente, sem alterar a entrada. Perdas, eficiência, capacidade de armazenamento, incerteza meteorológica e operação física não são modeladas.
