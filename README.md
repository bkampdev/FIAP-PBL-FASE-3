# FIAP PBL - Fase 3 | Colônia Aurora

A Colônia Aurora é um projeto didático em Python para organizar dados dos subsistemas, comparar geração e consumo, priorizar o suporte à vida e estimar a geração eólica do próximo intervalo.

**Estado desta versão.** O programa integrado está disponível pelo terminal, com validação de dados, consulta hierárquica, balanço energético, decisões e previsão eólica. A suíte contém 100 testes automatizados. O relatório em PDF permanece uma versão para revisão; a [revisão final do sistema](docs/revisao-final.md) registra as verificações e as pendências de aceite.

## Como reproduzir o que está disponível

Os módulos usam a biblioteca padrão. Os testes foram conferidos em Python 3.11 e 3.14.

```bash
git clone https://github.com/bkampdev/FIAP-PBL-FASE-3.git
cd FIAP-PBL-FASE-3
```

A partir da raiz, liste os oito cenários e execute a análise de déficit:

```bash
python main.py --listar
python main.py --cenario deficit
```

O cenário `deficit` apresenta geração de 40 kWh, consumo de 70 kWh e saldo atual de -30 kWh. A previsão eólica é de 27,5 kWh, com saldo futuro estimado de -22,5 kWh, mantendo a geração solar e o consumo. As recomendações preservam o suporte à vida e propõem avaliar a redução do laboratório.

Execute a suíte completa:

```bash
python -m unittest discover -s tests -v
```

Para reproduzir a previsão isolada, informe vento histórico de 8, 10 e 12 m/s, geração correspondente de 20, 25 e 30 kWh e vento previsto de 11 m/s:

```bash
python -c "from src.previsao import ajustar_reta, prever_energia; modelo = ajustar_reta([8, 10, 12], [20, 25, 30]); print(prever_energia(modelo, 11)['energia_eolica_prevista_kwh'])"
```

Saída em kWh para um intervalo didático de 1 h:

```text
27.5
```

O [exemplo de saída](docs/exemplos_saida.md) mostra como reproduzir o cenário sintético do teste de apresentação. Os oito cenários e seus resultados esperados estão documentados em [cenarios.md](docs/cenarios.md).

## Funcionamento

O fluxo começa com a validação e a consulta à hierarquia dos subsistemas. Depois, o balanço compara a geração solar e eólica observada com o consumo e informa a reserva separadamente. As decisões dão prioridade ao suporte à vida. A previsão estima a geração eólica futura a partir do histórico e serve de entrada ao planejamento do próximo intervalo.

- [Contratos do sistema](docs/contratos.md) e [requisitos da atividade](docs/requisitos.md).
- [Método de previsão e conta manual](docs/previsao.md).
- [Relatório em PDF](relatorio/relatorio.pdf) e [fonte editável](relatorio/relatorio.md).

Para regenerar o PDF, instale `reportlab` com `python -m pip install reportlab` e rode `python scripts/gerar_relatorio.py`. Essa dependência é exclusiva da geração do documento.

## Equipe

| Integrante | GitHub | Issues | Responsabilidade |
|---|---|---|---|
| Guilherme Cardoso Bremenkamp | @bkampdev | 1, 10, 15 | Contratos, integração e entrega |
| Davi Coninck Cassaro | @daviconinck | 2, 6, 11 | Dados, cenários e validação |
| Lorenzo Mendes Rocha | @Rocha0306 | 3, 7, 12 | Decisões, prioridades e documentação |
| Eduardo Backes Klauck | @BackesEdu | 4, 8, 13 | Energia, validação matemática e documentação |
| Gabriel Gonzales | @ItsTheContext | 5, 9, 14 | Regressão, apresentação e consolidação documental |

O [plano de trabalho](docs/plano-trabalho.md) detalha a divisão e a revisão cruzada. A atividade prevê a entrega de um programa integrado e do relatório até **11/11/2026 às 23h59**, no horário de São Paulo, conforme o [registro de requisitos](docs/requisitos.md).
