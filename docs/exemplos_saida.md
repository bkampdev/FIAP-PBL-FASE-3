# Apresentação dos resultados

`formatar_resultado(resultado)` em `src/apresentacao.py` recebe o envelope já calculado pelo integrador (`src/sistema.py` / `main.py`) e devolve texto legível para o terminal, sem recalcular balanço energético, regressão linear ou regras de decisão e sem alterar os dicionários recebidos.

Os dados de `dados/cenarios.json` e `dados/historico_eolico.json` são sintéticos e reproduzíveis, em intervalos didáticos de 1 h. A saída separa explicitamente **Intervalo atual (dados observados)** de **Próximo intervalo (estimativa)** e informa unidades em todos os valores numéricos (`h`, `kWh`, `m/s` e `kWh/(m/s)`). As ações exibidas são alertas e recomendações didáticas, sem desligamento automático, descarga real de bateria ou garantia física de segurança.

## Envelope consumido pela apresentação

Na execução integrada (`executar_cenario` em `src/sistema.py`), o dicionário `resultado` possui seis chaves. Em falhas anteriores ao integrador na CLI (`main.py`), `formatar_resultado` também aceita o formato mínimo `{"erro": mensagem}`.

| Chave | Dados lidos por `formatar_resultado` |
|---|---|
| `erro` | Mensagem de entrada inválida (`str`) ou `None`. Quando preenchida, interrompe a formatação normal e exibe apenas `Erro de entrada: ...`. |
| `cenario` | `id`, `intervalo_h`, `geracao_solar_kwh`, `geracao_eolica_kwh`, `reserva_kwh` e `sistemas` (lista com `nome` e `essencial`). |
| `balanco` | `geracao_total_kwh`, `consumo_total_kwh`, `saldo_kwh` e `classificacao`. |
| `previsao` | Retorno de `prever_energia` (`a`, `b`, `vento_previsto_ms`, `energia_eolica_prevista_kwh` e `aviso` opcional) ou `None` quando indisponível. |
| `erro_previsao` | Motivo textual quando `previsao` é `None` (padrão `"modelo indisponível"` se omitido). |
| `decisao` | `status`, `acoes` (lista de dicionários com `acao` e `motivo`) e `recomendacao_futura` (`str` ou `None`). |

## Exemplos reais do programa integrado

A partir da raiz do repositório (use `python3` ou `python`, conforme o ambiente; em Windows, opcionalmente `-X utf8` ao redirecionar ou capturar a saída), liste os oito cenários disponíveis:

```bash
python3 main.py --listar
```

```text
nominal
deficit
excedente
equilibrio
alerta_critico
fronteira_essencial
vento_baixo
vento_alto
```

### 1. Cenário `nominal`

```bash
python3 main.py --cenario nominal
```

Saída (código de retorno `0`):

```text
Cenário nominal | Intervalo de 1 h

Intervalo atual (dados observados)
Solar: 35 kWh
Eólica: 25 kWh
Geração total: 60 kWh
Consumo total: 50 kWh
Saldo: 10 kWh (excedente)
Reserva disponível: 15 kWh
Sistemas essenciais: Suporte à vida
Estado atual: excedente
- Avaliar armazenamento ou uso planejado do excedente | Motivo: Excedente de 10 kWh; armazenamento real não é modelado

Próximo intervalo (estimativa)
Coeficientes: a = 2,5 kWh/(m/s), b = 0 kWh
Vento previsto: 10 m/s
Geração eólica estimada: 25 kWh
Recomendação futura: Com solar mantida em 35 kWh e consumo planejado em 50 kWh, a eólica estimada de 25 kWh leva a saldo futuro de 10 kWh. Reserva restante hipotética: 15 kWh. Avaliar armazenamento ou uso planejado do excedente estimado.
```

### 2. Cenário `deficit`

```bash
python3 main.py --cenario deficit
```

Saída (código de retorno `0`):

```text
Cenário deficit | Intervalo de 1 h

Intervalo atual (dados observados)
Solar: 20 kWh
Eólica: 20 kWh
Geração total: 40 kWh
Consumo total: 70 kWh
Saldo: -30 kWh (deficit)
Reserva disponível: 15 kWh
Sistemas essenciais: Suporte à vida
Estado atual: alerta_deficit
- Preservar Suporte à vida | Motivo: Consumidor essencial prioritário
- Avaliar redução do Laboratório | Motivo: Déficit de 30 kWh; reserva cobriria 15 kWh e restariam 15 kWh

Próximo intervalo (estimativa)
Coeficientes: a = 2,5 kWh/(m/s), b = 0 kWh
Vento previsto: 11 m/s
Geração eólica estimada: 27,5 kWh
Recomendação futura: Com solar mantida em 20 kWh e consumo planejado em 70 kWh, a eólica estimada de 27,5 kWh leva a saldo futuro de -22,5 kWh. Reserva restante hipotética: 0 kWh. Planejar redução de não essenciais.
```

### 3. Cenário `excedente`

```bash
python3 main.py --cenario excedente
```

Saída (código de retorno `0`):

```text
Cenário excedente | Intervalo de 1 h

Intervalo atual (dados observados)
Solar: 50 kWh
Eólica: 30 kWh
Geração total: 80 kWh
Consumo total: 30 kWh
Saldo: 50 kWh (excedente)
Reserva disponível: 10 kWh
Sistemas essenciais: Suporte à vida
Estado atual: excedente
- Avaliar armazenamento ou uso planejado do excedente | Motivo: Excedente de 50 kWh; armazenamento real não é modelado

Próximo intervalo (estimativa)
Coeficientes: a = 2,5 kWh/(m/s), b = 0 kWh
Vento previsto: 12 m/s
Geração eólica estimada: 30 kWh
Recomendação futura: Com solar mantida em 50 kWh e consumo planejado em 30 kWh, a eólica estimada de 30 kWh leva a saldo futuro de 50 kWh. Reserva restante hipotética: 10 kWh. Avaliar armazenamento ou uso planejado do excedente estimado.
```

### 4. Caso preditivo: comparação entre dois ventos previstos

Os cenários `vento_baixo` (8 m/s) e `vento_alto` (12 m/s) têm exatamente os mesmos dados observados no intervalo atual (solar 20 kWh, eólica 20 kWh, consumo 50 kWh, reserva 0 kWh e saldo `-10 kWh`). O bloco observado e o `Estado atual: alerta_deficit` permanecem idênticos; mudam apenas a geração eólica estimada e a recomendação futura:

```bash
python3 main.py --cenario vento_baixo
```

```text
Cenário vento_baixo | Intervalo de 1 h

Intervalo atual (dados observados)
Solar: 20 kWh
Eólica: 20 kWh
Geração total: 40 kWh
Consumo total: 50 kWh
Saldo: -10 kWh (deficit)
Reserva disponível: 0 kWh
Sistemas essenciais: Suporte à vida
Estado atual: alerta_deficit
- Preservar Suporte à vida | Motivo: Consumidor essencial prioritário
- Avaliar redução do Laboratório | Motivo: Déficit de 10 kWh; reserva cobriria 0 kWh e restariam 10 kWh

Próximo intervalo (estimativa)
Coeficientes: a = 2,5 kWh/(m/s), b = 0 kWh
Vento previsto: 8 m/s
Geração eólica estimada: 20 kWh
Recomendação futura: Com solar mantida em 20 kWh e consumo planejado em 50 kWh, a eólica estimada de 20 kWh leva a saldo futuro de -10 kWh. Reserva restante hipotética: 0 kWh. Planejar redução de não essenciais.
```

```bash
python3 main.py --cenario vento_alto
```

```text
Cenário vento_alto | Intervalo de 1 h

Intervalo atual (dados observados)
Solar: 20 kWh
Eólica: 20 kWh
Geração total: 40 kWh
Consumo total: 50 kWh
Saldo: -10 kWh (deficit)
Reserva disponível: 0 kWh
Sistemas essenciais: Suporte à vida
Estado atual: alerta_deficit
- Preservar Suporte à vida | Motivo: Consumidor essencial prioritário
- Avaliar redução do Laboratório | Motivo: Déficit de 10 kWh; reserva cobriria 0 kWh e restariam 10 kWh

Próximo intervalo (estimativa)
Coeficientes: a = 2,5 kWh/(m/s), b = 0 kWh
Vento previsto: 12 m/s
Geração eólica estimada: 30 kWh
Recomendação futura: Com solar mantida em 20 kWh e consumo planejado em 50 kWh, a eólica estimada de 30 kWh leva a saldo futuro de 0 kWh. Reserva restante hipotética: 0 kWh. Sem margem prevista; manter monitoramento.
```

### 5. Casos de fronteira e risco essencial (`fronteira_essencial` e `alerta_critico`)

Em `fronteira_essencial`, geração + reserva igualam exatamente o consumo essencial (`30 + 5 = 35 kWh`): o estado permanece `alerta_deficit` com sinalização explícita de dependência da reserva. Em `alerta_critico`, geração + reserva são insuficientes para os essenciais (`10 + 5 < 35 kWh`, faltam `20 kWh`), emitindo `alerta_critico` e recomendação de intervenção humana imediata (no cenário `equilibrio`, saldo observado e futuro são `0 kWh`, com estado `equilibrio` e monitoramento sem margem):

```bash
python3 main.py --cenario fronteira_essencial
```

```text
Cenário fronteira_essencial | Intervalo de 1 h

Intervalo atual (dados observados)
Solar: 20 kWh
Eólica: 10 kWh
Geração total: 30 kWh
Consumo total: 50 kWh
Saldo: -20 kWh (deficit)
Reserva disponível: 5 kWh
Sistemas essenciais: Suporte à vida
Estado atual: alerta_deficit
- Preservar Suporte à vida | Motivo: Consumidor essencial prioritário
- Sinalizar dependência da reserva | Motivo: Geração de 30 kWh é menor que o consumo essencial de 35 kWh
- Avaliar redução do Laboratório | Motivo: Déficit de 20 kWh; reserva cobriria 5 kWh e restariam 15 kWh

Próximo intervalo (estimativa)
Coeficientes: a = 2,5 kWh/(m/s), b = 0 kWh
Vento previsto: 10 m/s
Geração eólica estimada: 25 kWh
Recomendação futura: Com solar mantida em 20 kWh e consumo planejado em 50 kWh, a eólica estimada de 25 kWh leva a saldo futuro de -5 kWh. Reserva restante hipotética: 0 kWh. Planejar redução de não essenciais.
```

```bash
python3 main.py --cenario alerta_critico
```

```text
Cenário alerta_critico | Intervalo de 1 h

Intervalo atual (dados observados)
Solar: 5 kWh
Eólica: 5 kWh
Geração total: 10 kWh
Consumo total: 50 kWh
Saldo: -40 kWh (deficit)
Reserva disponível: 5 kWh
Sistemas essenciais: Suporte à vida
Estado atual: alerta_critico
- Alerta crítico: energia insuficiente para os sistemas essenciais | Motivo: Geração de 10 kWh e reserva de 5 kWh não cobrem o consumo essencial de 35 kWh; faltam 20 kWh
- Preservar Suporte à vida | Motivo: Consumidor essencial prioritário
- Acionar intervenção humana imediata | Motivo: O sistema apenas recomenda; não há garantia de segurança
- Avaliar redução do Laboratório | Motivo: Liberar toda energia possível para os essenciais

Próximo intervalo (estimativa)
Coeficientes: a = 2,5 kWh/(m/s), b = 0 kWh
Vento previsto: 8 m/s
Geração eólica estimada: 20 kWh
Recomendação futura: Com solar mantida em 5 kWh e consumo planejado em 50 kWh, a eólica estimada de 20 kWh leva a saldo futuro de -25 kWh. Reserva restante hipotética: 0 kWh. Risco de insuficiência para os essenciais: preparar intervenção humana e planejar redução de não essenciais.
```

## Erros de entrada, previsão indisponível e avisos

### Entrada inválida

Quando o cenário solicitado não existe ou os dados de entrada falham na validação, o programa retorna código `1` e não imprime seções de sucesso:

```bash
python3 main.py --cenario inexistente
```

```text
Erro de entrada: Cenário inexistente: inexistente. Use --listar.
```

### Previsão indisponível e extrapolação

- **Histórico ausente ou inválido:** quando `previsao` é `None` (por exemplo, `python3 main.py --cenario deficit --historico dados/ausente.json`, código de retorno `0`, ou `executar_cenario(cenario, None)`), os dados observados e as decisões atuais são preservados com a ação `- Planejamento do próximo intervalo indisponível | Motivo: Previsão eólica ausente; vale apenas a decisão atual`, e o bloco futuro exibe `Previsão eólica indisponível: <motivo>` seguido de `Recomendação futura indisponível.`.
- **Extrapolação e estimativa negativa:** quando `previsao["aviso"]` está presente (por exemplo, `13 m/s` fora da faixa histórica `[8, 12]` m/s), `formatar_resultado` inclui a linha `Aviso: Extrapolação: vento previsto fora da faixa histórica.` logo após a geração eólica estimada. Se a reta gerar valor negativo, o valor bruto e o aviso de invalidade física são exibidos sem truncamento para zero, com ação explicando a indisponibilidade do planejamento e `Recomendação futura indisponível.`.
