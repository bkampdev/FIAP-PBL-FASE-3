# Cenários reproduzíveis — Issue #6

Responsável: Davi (@daviconinck)

## Objetivo

Fornecer dados sintéticos e reproduzíveis para testar o
gerenciamento energético da colônia marciana.

Os cenários estão em `dados/cenarios.json` e o histórico
de vento está em `dados/historico_eolico.json`.

Os valores são fictícios e não representam medições reais.

## Histórico eólico

Dados utilizados:

| Vento (m/s) | Energia (kWh) |
|---|---|
| 8 | 20 |
| 10 | 25 |
| 12 | 30 |

Equação da regressão linear:

Energia prevista = 2,5 × velocidade do vento

Exemplos:

- Vento de 8 m/s: 20 kWh.
- Vento de 10 m/s: 25 kWh.
- Vento de 11 m/s: 27,5 kWh.
- Vento de 12 m/s: 30 kWh.

## Cenários

O saldo é calculado por:

Saldo = geração solar + geração eólica - consumo total.

A reserva é registrada separadamente.

Todos os valores de energia das tabelas estão em kWh por intervalo de 1 h.
Em todos os cenários, `suporte_vida` é essencial, prioridade 1 (P1), e
`laboratorio` é não essencial, prioridade 2 (P2). Menor número significa
maior prioridade; somente o laboratório é candidato a redução.

### Entradas dos oito cenários

| Cenário | Solar | Eólica atual | Reserva inicial | Suporte à vida (P1) | Laboratório (P2) | Consumo total |
|---|---:|---:|---:|---:|---:|---:|
| nominal | 35 | 25 | 15 | 30 | 20 | 50 |
| deficit | 20 | 20 | 15 | 35 | 35 | 70 |
| excedente | 50 | 30 | 10 | 20 | 10 | 30 |
| equilibrio | 30 | 20 | 0 | 35 | 15 | 50 |
| alerta_critico | 5 | 5 | 5 | 35 | 15 | 50 |
| fronteira_essencial | 20 | 10 | 5 | 35 | 15 | 50 |
| vento_baixo | 20 | 20 | 0 | 35 | 15 | 50 |
| vento_alto | 20 | 20 | 0 | 35 | 15 | 50 |

### Balanço atual esperado

`cobertura_potencial = min(reserva_inicial, max(0, -saldo))` e
`deficit_remanescente = max(0, -saldo) - cobertura_potencial`.
A cobertura não muda saldo/classificação nem representa descarga executada.

| Cenário | Geração total | Saldo atual | Cobertura potencial da reserva | Déficit remanescente | Classificação do balanço |
|---|---:|---:|---:|---:|---|
| nominal | 60 | +10 | 0 | 0 | excedente |
| deficit | 40 | -30 | 15 | 15 | deficit |
| excedente | 80 | +50 | 0 | 0 | excedente |
| equilibrio | 50 | 0 | 0 | 0 | equilibrio |
| alerta_critico | 10 | -40 | 5 | 35 | deficit |
| fronteira_essencial | 30 | -20 | 5 | 15 | deficit |
| vento_baixo | 40 | -10 | 0 | 10 | deficit |
| vento_alto | 40 | -10 | 0 | 10 | deficit |

O nome `nominal` identifica o cenário, enquanto seu balanço é `excedente`.
`alerta_critico` é o status esperado da decisão de risco; a classificação
matemática do seu balanço continua sendo `deficit`.

### Previsão esperada para os oito cenários

A regressão do histórico resulta em `a=2.5` e `b=0`.
Todos os ventos previstos estão na faixa histórica inclusiva de 8 a 12 m/s:
nenhum dos oito casos exige extrapolação ou produz estimativa negativa.

No próximo intervalo, mantêm-se a geração solar e o consumo total atuais,
substituindo **somente** a eólica observada pela prevista:
`saldo_futuro = solar + eolica_prevista - consumo_total`.
Não somar eólica atual e prevista nem multiplicar novamente os kWh pela
duração. Os saldos abaixo não incluem reserva ou redução de cargas.

| Cenário | Vento previsto (m/s) | Eólica prevista (kWh) | Geração futura estimada (kWh) | Saldo futuro estimado (kWh) |
|---|---:|---:|---:|---:|
| nominal | 10 | 25 | 60 | +10 |
| deficit | 11 | 27,5 | 47,5 | -22,5 |
| excedente | 12 | 30 | 80 | +50 |
| equilibrio | 8 | 20 | 50 | 0 |
| alerta_critico | 8 | 20 | 25 | -25 |
| fronteira_essencial | 10 | 25 | 45 | -5 |
| vento_baixo | 8 | 20 | 40 | -10 |
| vento_alto | 12 | 30 | 50 | 0 |

Se considerar reserva futura, usar apenas
`reserva_restante_hipotetica = reserva_inicial - cobertura_potencial`:
15 kWh em `nominal`, 10 kWh em `excedente` e zero nos demais.
Não reutilizar toda a reserva inicial no próximo intervalo.

### Prioridade e recomendações esperadas

Estas são referências de aceite das issues #3 e #10, ainda dependentes de
`src/decisoes.py` e `main.py`. Não representam execução integrada concluída,
redução física de cargas ou armazenamento realizado.

| Cenário | Status atual esperado | Prioridade e recomendação esperadas |
|---|---|---|
| nominal | excedente | Preservar suporte à vida; informar sobra de 10 kWh e avaliar armazenamento/uso planejado. Sobra futura estimada de 10 kWh. |
| deficit | alerta_deficit | Preservar suporte à vida; propor redução do laboratório, informando déficit bruto de 30 kWh, cobertura potencial de 15 kWh e remanescente de 15 kWh. Planejar saldo futuro de -22,5 kWh, sem reaplicar a reserva inicial. |
| excedente | excedente | Preservar suporte à vida; avaliar armazenamento/uso planejado da sobra de 50 kWh, também prevista no futuro. |
| equilibrio | equilibrio | Preservar suporte à vida e informar ausência de margem de geração, também no futuro. |
| alerta_critico | alerta_critico | Geração + reserva = 15 kWh para demanda essencial de 35 kWh: faltam 20 kWh mesmo sem laboratório. Preservar essenciais e recomendar intervenção humana; reduzir laboratório não resolve a insuficiência essencial. No futuro, geração de 25 kWh ainda fica 10 kWh abaixo da demanda essencial, sem reserva hipotética restante. |
| fronteira_essencial | alerta_deficit | Geração + reserva = 35 kWh, exatamente a demanda essencial. Explicitar dependência da reserva e propor redução do laboratório; não declarar suporte à vida seguro. Futuro com déficit total de 5 kWh e sem reserva hipotética restante. |
| vento_baixo | alerta_deficit | Preservar suporte à vida e propor redução do laboratório diante do déficit atual de 10 kWh, sem reserva. Déficit futuro estimado permanece em 10 kWh. |
| vento_alto | alerta_deficit | Manter alerta do déficit atual de 10 kWh e prioridade do suporte à vida; planejar equilíbrio futuro com vento maior, sem antecipá-lo ao intervalo atual. |

Reduções recomendadas e coberturas hipotéticas não apagam o déficit observado
nem demonstram segurança física. As contas seguem [contratos.md](contratos.md).

## Comparação das condições de vento

Os cenários `vento_baixo` e `vento_alto` possuem as mesmas
condições iniciais:

- Geração atual: 40 kWh.
- Consumo atual: 50 kWh.
- Saldo atual: -10 kWh.
- Reserva: 0 kWh.

A diferença está na previsão:

| Cenário | Vento previsto | Energia eólica prevista |
|---|---:|---:|
| vento_baixo | 8 m/s | 20 kWh |
| vento_alto | 12 m/s | 30 kWh |

Considerando a geração solar de 20 kWh constante:

- Vento baixo: geração planejada de 40 kWh e déficit de 10 kWh.
- Vento alto: geração planejada de 50 kWh e equilíbrio energético.

Esses resultados são referências para testar o planejamento.
A recomendação final depende das regras do módulo de decisões.

## Validação dos arquivos

Executar na raiz do projeto:

    python -m json.tool dados/cenarios.json
    python -m json.tool dados/historico_eolico.json

Carregar os arquivos pelo módulo de dados:

    from src.dados import carregar_cenarios, carregar_historico

    cenarios = carregar_cenarios("dados/cenarios.json")
    historico = carregar_historico("dados/historico_eolico.json")

    print(len(cenarios))
    print(historico["vento_ms"])

Resultado esperado:

    8
    [8.0, 10.0, 12.0]

## Testes de fronteira e entradas inválidas

O módulo de dados deve rejeitar:

- Campos obrigatórios ausentes.
- Valores negativos indevidos.
- Tipos incorretos.
- Valores booleanos usados como números.
- Identificadores duplicados.
- Duração zero.
- Histórico eólico com séries de tamanhos diferentes.

Caminho hierárquico bem formado, mas inexistente, retorna `None`; não é
rejeição do cenário. Folha válida retorna `{}`; usar `is None` para
distinguir ausência (veja [dados.md](dados.md)).

Déficit energético deve permanecer um cenário válido,
pois representa risco operacional e não erro de formato.

## Integração e revisão

Os arquivos devem ser utilizados pelo programa principal
da Issue #10.

A compatibilidade dos cálculos e das recomendações deverá
ser conferida com Eduardo e Lorenzo.

Não há registro de aprovação desses revisores neste documento.

## Reprodução do balanço e da previsão

Execute a partir da raiz do projeto:

```python
from src.dados import carregar_cenarios, carregar_historico
from src.energia import analisar_energia
from src.previsao import ajustar_reta, prever_energia

cenarios = carregar_cenarios("dados/cenarios.json")
historico = carregar_historico("dados/historico_eolico.json")
modelo = ajustar_reta(historico["vento_ms"], historico["energia_eolica_kwh"])
for cenario in cenarios:
    assert cenario["intervalo_h"] == historico["intervalo_h"]
    balanco = analisar_energia(cenario)
    previsao = prever_energia(modelo, cenario["vento_previsto_ms"])
    futuro = (cenario["geracao_solar_kwh"]
              + previsao["energia_eolica_prevista_kwh"]
              - balanco["consumo_total_kwh"])
    print(cenario["id"], balanco["saldo_kwh"],
          balanco["reserva_usada_kwh"], balanco["deficit_remanescente_kwh"],
          previsao["energia_eolica_prevista_kwh"], futuro)
```

As colunas são ID, saldo atual, cobertura potencial, déficit remanescente,
eólica prevista e saldo futuro. Para `deficit`, a linha é
`deficit -30.0 15.0 15.0 27.5 -22.5`, conforme as tabelas.
A conferência independente por Eduardo e Lorenzo e a demonstração integrada
permanecem pendentes; este documento não fecha automaticamente as issues.
