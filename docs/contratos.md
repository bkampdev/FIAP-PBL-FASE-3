# Contratos propostos para confirmação na issue #1

Estado: proposta inicial; não existe implementação destes contratos. Ajustes devem ser combinados entre autores e consumidores antes de codificar.

## Unidades e registros

- Intervalo didático comum: 1 h por padrão, explicitado em `intervalo_h`. Energia gerada/consumida no intervalo e reserva em kWh; vento em m/s. Se o grupo preferir potência, revisar todos os contratos e não somar kW com kWh.
- Cenário: `id`, `intervalo_h`, `geracao_solar_kwh`, `geracao_eolica_kwh`, `reserva_kwh`, `vento_previsto_ms`, `sistemas` e `hierarquia`.
- Cada sistema: `id`, `nome`, `consumo_kwh`, `essencial`, `prioridade` (menor número primeiro). Campo numérico finito, consumo não negativo.
- Histórico: listas pareadas `vento_ms` e `energia_eolica_kwh` para intervalos de mesma duração.
- Hierarquia com raiz `colonia`, nó `energia` e filhos `solar`/`eolico`, além dos sistemas consumidores. Percurso/consulta deve aparecer na demonstração.
- Os dados são sintéticos. Reserva é estoque, geração/consumo se referem ao intervalo. Não confundir estoque com fluxo.

## Funções sugeridas

| Módulo / autor | Interface proposta | Retorno / responsabilidade |
|---|---|---|
| `src/dados.py` — Davi | `carregar_cenarios(caminho)`, `validar_cenario(cenario)`, `buscar_subsistema(hierarquia, caminho)` | Cenários, lista de erros e nó encontrado; não decidir segurança energética |
| `src/energia.py` — Eduardo | `analisar_energia(cenario)` | Balanço em kWh conforme os campos abaixo; sem mutação nem escolha de cargas |
| `src/previsao.py` — Gabriel | `ajustar_reta(x,y)`, `prever_energia(modelo,vento)` | Coeficientes, faixa histórica, estimativa e aviso de extrapolação |
| `src/decisoes.py` — Lorenzo | `decidir(cenario,balanco,previsao)` | Status, ações/motivos atuais e recomendação futura |
| `src/apresentacao.py` — Gabriel | `formatar_resultado(resultado)` | Texto; sem recalcular regras ou números |
| `src/sistema.py` — Guilherme | `executar_cenario(cenario,historico)` | Resultado integrado que mantém entradas/valores observados e estimados distinguíveis |

Validação: funções matemáticas devem rejeitar dados inválidos com `ValueError` explicativo; a entrada principal trata e exibe o erro sem sucesso fictício. Decisões recebem dados já validados; risco operacional não deve ser confundido com entrada malformada.

## Regras a confirmar

Saldo atual = geração solar + eólica observadas - consumo do intervalo. Negativo indica déficit; zero, equilíbrio; positivo, excedente. Essenciais nunca são candidatos a desligamento automático. Falta para atendê-los gera alerta crítico.

Previsão eólica serve ao próximo intervalo: comparar `geracao_solar_kwh` mantida como hipótese declarada + energia eólica prevista com consumo planejado mantido como hipótese. Separar esse saldo previsto do observado; registrar limitações. Se houver reserva disponível para planejamento, não consumir o mesmo estoque duas vezes.

Sem implementação de armazenamento/controle físico, as saídas são recomendações. Não alegar economia medida, segurança real ou armazenamento realizado.

## Aceite numérico de referência

Com x=[8,10,12] e y=[20,25,30], `a=2.5`, `b=0`, e `y(11)=27.5`. Usar tolerância numérica nos testes. x sem variação não permite ajuste. Consulta fora da faixa deve produzir aviso; não substituir previsões ruins por um valor seguro silenciosamente.

## Retorno energético implementado (#4, PR #20)

`analisar_energia(cenario)` recebe o cenário com energias em kWh. Valida operandos matemáticos (incluindo consumos e `essencial` booleano), rejeitando `bool` como número, negativos, valores não finitos e somas que excedam a escala finita com `ValueError`. `intervalo_h` positivo tem padrão explícito de 1 h quando ausente, sem mutar a entrada. Não multiplica novamente energias pela duração. A validação completa de IDs, hierarquia e prioridades pertence ao módulo de dados.

Retorna `geracao_total_kwh`, `consumo_total_kwh`, `consumo_essencial_kwh`, `saldo_kwh`, `classificacao` (`deficit`, `equilibrio`, `excedente`), `reserva_usada_kwh` e `deficit_remanescente_kwh`. `reserva_usada_kwh` é cobertura potencial `min(reserva_kwh, max(0, -saldo_kwh))`; não altera estoque nem saldo bruto. Déficit remanescente é `max(0, -saldo_kwh) - reserva_usada_kwh`. A reserva disponível permanece no cenário.

A API numérica original `calcular_balanco_energia(solar, eolica, consumo, reserva_atual=0)` permanece disponível com validação e os retornos originais; consumidores integrados devem usar `analisar_energia`. O status legado `DÉFICIT_CRITICO` significa reserva insuficiente para o déficit total; a decisão sobre insuficiência essencial pertence ao módulo de decisões.
