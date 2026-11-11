# Tabela de regras de decisão

Regras implementadas em `src/decisoes.py` (`decidir(cenario, balanco, previsao)`, issue #3) e conferidas em `tests/test_prioridades.py` (issue #7). Todos os valores em kWh do mesmo intervalo de 1 h. As ações são **recomendações**: nenhuma carga é desligada pelo programa e nenhuma regra garante segurança real.

## Decisão atual (ordem de precedência)

A primeira condição verdadeira define o `status`.

| # | Condição | `status` | Ação principal | Motivo | Exemplo calculável |
|---|---|---|---|---|---|
| 1 | `geração + reserva < consumo essencial` | `alerta_critico` | Alerta crítico, preservar essenciais, acionar intervenção humana, avaliar redução de todos os não essenciais | Faltam `essencial - (geração + reserva)` kWh; sem garantia de segurança | Geração 10, reserva 5, essencial 35 → faltam **20** |
| 2 | `saldo < 0` (e não crítico) | `alerta_deficit` | Preservar essenciais; avaliar redução de não essenciais na fila até cobrir o déficit | Déficit bruto, cobertura potencial da reserva e restante | Geração 40, consumo 70, reserva 15 → déficit 30, cobriria 15, restam 15 |
| 2a | `saldo < 0` **e** `geração < essencial` **e** `geração + reserva >= essencial` | `alerta_deficit` | Acrescenta “Sinalizar dependência da reserva” | Essenciais só ficam atendidos com reserva | Geração 30, reserva 5, essencial 35 (fronteira: 35 = 35) |
| 3 | `saldo == 0` | `equilibrio` | Manter operação e monitorar | Sem margem de geração | Geração 50, consumo 50 |
| 4 | `saldo > 0` | `excedente` | Avaliar armazenamento ou uso planejado | Armazenamento real não é modelado | Geração 80, consumo 30 → excedente 50 |

**Fronteiras:** a comparação crítica é estrita (`<`). Com geração + reserva exatamente igual ao consumo essencial, o status é `alerta_deficit`, não crítico. Reserva cobrindo todo o déficit não muda a classificação: continua déficit.

## Prioridade

- `suporte_vida` é obrigatório, essencial e prioridade 1. Sistemas com `essencial=True` **nunca** entram na fila de redução.
- Fila de redução (`ordenar_reducao`): apenas não essenciais, **maior número de prioridade primeiro**; empate pelo `id` em ordem alfabética. Ex.: `lazer(4)`, `comunicacao(3)`, `estufa(3)`, `laboratorio(2)`.
- No déficit, os candidatos são propostos em ordem até que a soma dos consumos alcance o déficit bruto. Ex.: déficit 5 → só `lazer` (5 kWh).
- Sem consumidores não essenciais, uma ação informa o déficit e a cobertura potencial mesmo sem fila de redução. Ex.: geração 30, consumo essencial 35 e reserva 5 → déficit 5, cobertura 5 e remanescente 0 kWh.
- A ordem dos registros no JSON não altera a decisão (testado invertendo a lista).

## Próximo intervalo (`recomendacao_futura`)

Hipóteses: mesma geração solar e mesmo consumo; só a eólica é trocada pela estimativa.

`saldo_futuro = solar + eólica_prevista - consumo_total`
`reserva_restante = reserva - reserva_usada` (não reaplica a reserva inteira)

| Condição | Texto |
|---|---|
| Sem previsão (`None`) | `None` + ação “Planejamento do próximo intervalo indisponível” |
| Estimativa eólica negativa | `None` + ação com o aviso de invalidade física |
| `solar + eólica_prevista + reserva_restante < essencial` | Risco de insuficiência para os essenciais |
| `saldo_futuro < 0` | Planejar redução de não essenciais |
| `saldo_futuro == 0` | Sem margem prevista; manter monitoramento |
| `saldo_futuro > 0` | Avaliar armazenamento ou uso do excedente estimado |

Exemplo: solar 20, consumo 50, reserva 0. Vento 8 m/s → eólica 20 → saldo futuro **-10** (planejar redução). Vento 12 m/s → eólica 30 → saldo futuro **0** (sem margem). O balanço atual (-10) e o status atual não mudam.

## Erros de entrada

`decidir` recebe cenário e balanço já validados por `src/dados.py`/`src/sistema.py` e, em chamada direta, levanta `ValueError` sem retornar ações se: cenário/balanço não forem dicionários, faltar chave obrigatória, houver número inválido (`bool`, `NaN`, infinito ou inteiro sem representação `float` finita), `intervalo_h` informado não positivo, energia/reserva/`consumo_kwh` negativos, `id`/`nome` vazios ou não textuais, `id` de sistema duplicado, `prioridade` não inteira positiva (`bool` rejeitado), o balanço não conferir com o cenário, `suporte_vida` faltar, não for essencial ou não tiver prioridade 1, ou a previsão não for `dict`/`None` (ou trouxer `aviso` que não seja texto/`None`).

Cobertura e déficit remanescente devem ser não negativos e corresponder a `min(reserva, max(0, -saldo))` e `max(0, -saldo) - cobertura`, respectivamente. A geração, o saldo e a disponibilidade calculados para o próximo intervalo também precisam ser finitos; transbordamento numérico gera `ValueError`.

## Conferência independente

Concluída por Davi (@daviconinck) na [issue #7 (`#issuecomment-6805221411`)](https://github.com/bkampdev/FIAP-PBL-FASE-3/issues/7#issuecomment-6805221411), sem consultar o código: para a regra 2 (`alerta_deficit`, geração de 40 kWh, consumo de 70 kWh, reserva de 15 kWh e consumo essencial de 35 kWh), o cálculo manual indicou saldo de -30 kWh, cobertura disponível de 15 kWh, déficit restante de 15 kWh, estado `alerta_deficit`, preservação do suporte à vida e recomendação de redução dos não essenciais, coincidindo sem divergências com `python main.py --cenario deficit`.
