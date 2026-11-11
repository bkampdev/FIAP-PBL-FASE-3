# Apresentação dos resultados

`formatar_resultado(resultado)` retorna texto para o terminal. O integrador passa valores e decisões já calculados.

## Estrutura proposta para a integração

Os contratos iniciais definem as funções, mas deixam abertas as chaves dos retornos. A estrutura abaixo é a usada pela apresentação e deve ser conferida com os responsáveis na integração da issue #10.

| Chave | Dados que a apresentação lê |
|---|---|
| `cenario` | `id`, `intervalo_h`, `geracao_solar_kwh`, `geracao_eolica_kwh`, `reserva_kwh` e `sistemas` (lista de registros com `nome` e `essencial`) |
| `balanco` | `geracao_total_kwh`, `consumo_total_kwh`, `saldo_kwh` e `classificacao` (texto) |
| `previsao` | Retorno de `prever_energia` ou `None` quando indisponível |
| `decisao` | `status`, `acoes` (lista de registros com textos `acao` e `motivo`) e `recomendacao_futura` (texto ou `None`) |
| `erro_previsao` | Mensagem opcional quando `previsao` é `None` |
| `erro` | Mensagem de entrada inválida. Quando presente e não vazia, basta passar essa chave. |

## Exemplo provisório de déficit

Saída do formatador com dados sintéticos de teste. O balanço e as decisões são fornecidos como entradas fixas, e a estimativa de 27,5 kWh vem da regressão implementada.

```text
Cenário deficit | Intervalo de 1 h

Intervalo atual (dados observados)
Solar: 20 kWh
Eólica: 20 kWh
Geração total: 40 kWh
Consumo total: 70 kWh
Saldo: -30 kWh (déficit)
Reserva disponível: 10 kWh
Sistemas essenciais: Suporte à vida
Estado atual: alerta de déficit
- Reduzir a carga do laboratório | Motivo: Priorizar suporte à vida

Próximo intervalo (estimativa)
Coeficientes: a = 2,5 kWh/(m/s), b = 0 kWh
Vento previsto: 11 m/s
Geração eólica estimada: 27,5 kWh
Recomendação futura: Planejar a redução de cargas não essenciais.
```

Para reproduzir a partir da raiz, com Python 3.11 ou 3.14:

```bash
python -X utf8 -c "import sys; sys.path.insert(0, 'tests'); from test_apresentacao import resultado_de_teste; from src.apresentacao import formatar_resultado; print(formatar_resultado(resultado_de_teste()))"
```

Após a issue #10, registrar as saídas do programa integrado para nominal, déficit, excedente e para a comparação de dois ventos previstos.
