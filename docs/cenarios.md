
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

| Cenário | Geração | Consumo | Saldo | Condição |
|---|---:|---:|---:|---|
| nominal | 60 | 50 | +10 | Operação normal |
| deficit | 40 | 70 | -30 | Déficit energético |
| excedente | 80 | 30 | +50 | Excedente energético |
| equilibrio | 50 | 50 | 0 | Equilíbrio |
| alerta_critico | 10 | 50 | -40 | Risco ao suporte à vida |
| fronteira_essencial | 30 | 50 | -20 | Geração + reserva igual à demanda essencial |
| vento_baixo | 40 | 50 | -10 | Previsão de vento baixo |
| vento_alto | 40 | 50 | -10 | Previsão de vento alto |

Todos os valores de energia estão em kWh.

## Prioridades

1. Suporte à vida: essencial, prioridade 1.
2. Laboratório: não essencial, prioridade 2.

Em caso de déficit, o módulo de decisões deve priorizar
a manutenção do suporte à vida.

No cenário `alerta_critico`, geração + reserva = 15 kWh,
enquanto o suporte à vida necessita de 35 kWh.
Portanto, existe insuficiência de 20 kWh mesmo antes
de atender ao laboratório.

No cenário `fronteira_essencial`, geração + reserva = 35 kWh,
exatamente igual à demanda essencial.

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
- Caminhos inexistentes na hierarquia, retornando None na consulta.

Déficit energético deve permanecer um cenário válido,
pois representa risco operacional e não erro de formato.

## Integração e revisão

Os arquivos devem ser utilizados pelo programa principal
da Issue #10.

A compatibilidade dos cálculos e das recomendações deverá
ser conferida com Eduardo e Lorenzo.

Não há registro de aprovação desses revisores neste documento.
