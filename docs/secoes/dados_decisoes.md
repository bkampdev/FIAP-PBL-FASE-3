# Organização dos dados e regras de decisão

## Como os dados estão organizados

Os dados de entrada ficam em dois arquivos JSON sintéticos: `dados/cenarios.json` (lista de cenários) e `dados/historico_eolico.json` (histórico para a previsão). Eles são carregados e validados por `src/dados.py` (issue #2) e usam três estruturas básicas de Python:

- **Listas** guardam coleções ordenadas: a lista de cenários, a lista `sistemas` de cada cenário e as séries pareadas `vento_ms` / `energia_eolica_kwh` do histórico.
- **Dicionários (chave-valor)** guardam cada registro, acessado pelo nome do campo: `cenario["geracao_solar_kwh"]`, `sistema["consumo_kwh"]`, `sistema["essencial"]`.
- **Dicionários aninhados** formam a hierarquia da colônia: `colonia → energia → solar/eolico` e `colonia → consumidores → suporte_vida/laboratorio`. Folhas são `{}`; um caminho inexistente retorna `None`.

Exemplo real, cenário `deficit` de `dados/cenarios.json` (resumido):

```python
{
    "id": "deficit", "intervalo_h": 1.0,
    "geracao_solar_kwh": 20.0, "geracao_eolica_kwh": 20.0,
    "reserva_kwh": 15.0, "vento_previsto_ms": 11.0,
    "sistemas": [
        {"id": "suporte_vida", "nome": "Suporte à vida", "consumo_kwh": 35.0,
         "essencial": True, "prioridade": 1},
        {"id": "laboratorio", "nome": "Laboratório", "consumo_kwh": 35.0,
         "essencial": False, "prioridade": 2},
    ],
    "hierarquia": {"colonia": {
        "energia": {"solar": {}, "eolico": {}},
        "consumidores": {"suporte_vida": {}, "laboratorio": {}}}},
}
```

`buscar_subsistema(cenario["hierarquia"], ["colonia", "energia", "solar"])` percorre a árvore chave por chave e retorna `{}`. A árvore só referencia os IDs; os consumos ficam uma única vez em `sistemas`, evitando somar o mesmo valor duas vezes.

Essa estrutura atende à colônia porque cada sistema carrega junto o que a decisão precisa (consumo, se é essencial e prioridade), a lista permite somar consumos com um laço simples e a hierarquia mostra quais subsistemas pertencem a geração e a consumo.

## Regras de decisão

`decidir(cenario, balanco, previsao)` em `src/decisoes.py` recebe o cenário, o balanço de `analisar_energia` e a previsão eólica (ou `None`) e devolve `status`, `acoes` (cada uma com `acao` e `motivo`) e `recomendacao_futura`. As regras são avaliadas nesta ordem:

1. `geração + reserva < consumo essencial` → `alerta_critico`: informa quanto falta, preserva essenciais e recomenda intervenção humana.
2. `saldo < 0` → `alerta_deficit`: preserva essenciais e propõe avaliar redução dos não essenciais. Condição combinada: se `geração < essencial` **e** a reserva completa a diferença, sinaliza também dependência da reserva.
3. `saldo == 0` → `equilibrio`.
4. `saldo > 0` → `excedente`: sugere avaliar armazenamento.

**Prioridade:** `suporte_vida` é sempre essencial (prioridade 1). Essenciais nunca entram na fila de redução. Não essenciais são ordenados pelo maior número de `prioridade` primeiro (empate pelo `id`), e a ordem dos registros no arquivo não interfere. A tabela completa com fronteiras está em `docs/regras.md`.

**Próximo intervalo:** mantendo solar e consumo, troca-se só a eólica pela estimativa: `saldo_futuro = solar + eólica_prevista - consumo`. Sem previsão ou com estimativa negativa, `recomendacao_futura` é `None` e uma ação explica o motivo.

## Exemplo rastreável: entrada → condição → ação → motivo

Cenário `deficit` acima, com histórico de vento `[8, 10, 12]` → energia `[20, 25, 30]` e vento previsto 11 m/s:

| Etapa | Valor |
|---|---|
| Entrada | geração 20 + 20 = 40 kWh; consumo 35 + 35 = 70 kWh; essencial 35 kWh; reserva 15 kWh |
| Condição 1 | 40 + 15 = 55 ≥ 35 → não é crítico |
| Condição 2 | saldo 40 − 70 = −30 < 0 → `alerta_deficit` |
| Ações | “Preservar Suporte à vida” (consumidor essencial prioritário); “Avaliar redução do Laboratório” (déficit de 30 kWh; reserva cobriria 15 kWh e restariam 15 kWh) |
| Futuro | eólica estimada 27,5 kWh → 20 + 27,5 − 70 = −22,5 kWh; reserva restante hipotética 0 kWh → planejar redução de não essenciais |

Os mesmos números são verificados em `tests/test_decisoes.py` (`test_exemplo_do_contrato_deficit`).

## Limites

As saídas são alertas e recomendações. O programa não desliga equipamentos, não descarrega nem carrega reserva real e não garante a segurança do suporte à vida; esses controles não foram implementados.
