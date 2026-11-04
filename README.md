# FIAP PBL - Fase 3: sistemas da colônia Aurora

Planejamento do sistema integrado da colônia: organização de dados, regras de decisão, regressão linear simples e análise energética.

**Estado atual: organização inicial. O sistema e o PDF ainda serão desenvolvidos nas issues.** Não há execução ou testes aprovados nesta versão inicial.

## Entrega e referência

- [Atividade no FIAP ON](https://on.fiap.com.br/mod/assign/view.php?id=616829), conferida em 04/11/2026.
- Prazo oficial: **11/11/2026 às 23h59**, horário de São Paulo.
- Meta interna sugerida: candidata em 08/11, revisão em 09/11 e pacote pronto em 10/11.
- Obrigatórios: um sistema Python organizado em funções, este repositório público, README com entrada/saída e relatório PDF objetivo com link do GitHub.
- O enunciado desta fase não fixa número de páginas nem exige bibliotecas avançadas. Não aplicar os limites da Fase 2.

## Equipe e divisão

| Integrante | GitHub | Issues planejadas | Responsabilidade |
|---|---|---|---|
| Guilherme Cardoso Bremenkamp | @bkampdev | 1, 10, 15 | Contratos, integração e entrega |
| Davi Coninck Cassaro | @daviconinck | 2, 6, 11 | Dados, cenários e validação |
| Lorenzo Mendes Rocha | @Rocha0306 | 3, 7, 12 | Decisões, prioridades e documentação |
| Eduardo Backes Klauck | @BackesEdu | 4, 8, 13 | Energia, validação matemática e documentação |
| Gabriel Gonzales | @ItsTheContext | 5, 9, 14 | Regressão, apresentação e consolidação documental |

As responsabilidades incluem código para os cinco integrantes. A conclusão depende de contribuição verificável, entendimento e revisão; quantidade de issues não mede esforço. Os convites de acesso precisam ser aceitos pelos colegas.

## Funcionamento planejado

`dados → validação e consulta hierárquica → balanço energético → ajuste e previsão → decisões atuais/futuras → saída explicada`

O cenário deverá usar listas para histórico, dicionários para acesso por identificador e estrutura hierárquica para os subsistemas. Solar e eólico compõem geração; suporte à vida tem prioridade sobre cargas não essenciais. A estimativa eólica participa do planejamento do próximo intervalo.

## Exemplos de aceite (a implementar)

| Entrada didática | Resultado a verificar |
|---|---|
| Geração 40 kWh, consumo 70 kWh no mesmo intervalo | Saldo -30 kWh e alerta de déficit; preservar essenciais |
| Geração 80 kWh, consumo 30 kWh | Saldo +50 kWh e sugestão de armazenamento |
| Geração 50 kWh, consumo 50 kWh | Equilíbrio |
| Histórico vento [8,10,12], energia [20,25,30]; vento previsto 11 m/s | Reta y=2,5x; previsão 27,5 kWh no intervalo do histórico |

Esses resultados são referências calculadas, não saídas de um programa já executado. Limites físicos e operacionais serão hipóteses didáticas identificadas.

## Execução

Ainda não disponível. A issue #10 implementará a entrada do programa e a #14 publicará o comando validado. Proposta: `python3 main.py --cenario deficit`; testes planejados: `python3 -m unittest discover -s tests -v`. Não executar esses comandos antes da implementação. O núcleo deverá funcionar com a biblioteca padrão; versão mínima final será conferida na integração.

## Organização

- `src/`: módulos a implementar para dados, energia, previsão, decisões, apresentação e integração.
- `dados/`: cenários e histórico sintéticos reproduzíveis.
- `tests/`: testes dos módulos e da integração.
- `docs/`: requisitos, contratos propostos, divisão, revisão e seções do relatório.
- `relatorio/`: fonte consolidada e PDF final, após a issue #14.

Consulte [requisitos](docs/requisitos.md), [contratos propostos](docs/contratos.md), [plano](docs/plano-trabalho.md) e [como contribuir](CONTRIBUTING.md).

## Grupo e envio no portal

Na consulta de 04/11/2026, a atividade estava com entrega pendente e o Grupo 20 mostrava somente Guilherme. A composição precisa ser regularizada e conferida na issue #15; convites GitHub não alteram o grupo FIAP. Publicação de arquivos e merge não comprovam envio acadêmico.
