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
| `src/energia.py` — Eduardo | `analisar_energia(cenario)` | Geração total, consumo total/essencial, saldo, reserva e classificação |
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
