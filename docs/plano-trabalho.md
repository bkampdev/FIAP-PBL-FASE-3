# Plano de trabalho

Divisão inicial: três issues por integrante, incluindo implementação Python para os cinco. Responsabilidades e critérios detalhados ficam nas próprias issues. Planejamento não comprova execução ou revisão.

| Issue | Responsável | Resultado |
|---|---|---|
| [#1](https://github.com/bkampdev/FIAP-PBL-FASE-3/issues/1) | @bkampdev | Definir contratos, escopo e mapa de integração da colônia |
| [#2](https://github.com/bkampdev/FIAP-PBL-FASE-3/issues/2) | @daviconinck | Implementar dados, validação e hierarquia dos sistemas |
| [#3](https://github.com/bkampdev/FIAP-PBL-FASE-3/issues/3) | @Rocha0306 | Implementar regras de decisão e prioridade do suporte à vida |
| [#4](https://github.com/bkampdev/FIAP-PBL-FASE-3/issues/4) | @BackesEdu | Implementar balanço de geração, consumo e reserva de energia |
| [#5](https://github.com/bkampdev/FIAP-PBL-FASE-3/issues/5) | @ItsTheContext | Implementar regressão linear simples para previsão eólica |
| [#6](https://github.com/bkampdev/FIAP-PBL-FASE-3/issues/6) | @daviconinck | Preparar cenários reproduzíveis e casos de fronteira |
| [#7](https://github.com/bkampdev/FIAP-PBL-FASE-3/issues/7) | @Rocha0306 | Validar prioridades e tabela de regras com casos combinados |
| [#8](https://github.com/bkampdev/FIAP-PBL-FASE-3/issues/8) | @BackesEdu | Conferir o modelo de regressão e as contas de energia |
| [#9](https://github.com/bkampdev/FIAP-PBL-FASE-3/issues/9) | @ItsTheContext | Programar apresentação clara dos resultados e previsões |
| [#10](https://github.com/bkampdev/FIAP-PBL-FASE-3/issues/10) | @bkampdev | Integrar os módulos em um único programa executável |
| [#11](https://github.com/bkampdev/FIAP-PBL-FASE-3/issues/11) | @daviconinck | Revisar o sistema integrado em cópia limpa |
| [#12](https://github.com/bkampdev/FIAP-PBL-FASE-3/issues/12) | @Rocha0306 | Escrever as seções de dados e decisões do relatório |
| [#13](https://github.com/bkampdev/FIAP-PBL-FASE-3/issues/13) | @BackesEdu | Escrever as seções de previsão e eficiência energética |
| [#14](https://github.com/bkampdev/FIAP-PBL-FASE-3/issues/14) | @ItsTheContext | Consolidar README e relatório PDF objetivo |
| [#15](https://github.com/bkampdev/FIAP-PBL-FASE-3/issues/15) | @bkampdev | Conferir equipe, pacote final e envio no FIAP ON |

## Sequência sugerida

- 05/11: combinar contratos (#1) e começar os módulos.
- 06/11: primeiras versões de dados, regras, energia e regressão (#2–#5).
- 07–08/11: cenários, apresentação, validação e integração (#6–#10).
- 09/11: revisão limpa e seções do relatório (#11–#13).
- 10/11: README/PDF e conferência da entrega (#14–#15).
- Prazo oficial: 11/11/2026 às 23h59, São Paulo. Metas anteriores são propostas internas.

## Matriz requisito → evidência planejada

| Requisito | Issues | Arquivos/evidência a produzir |
|---|---|---|
| Dados, chave-valor e hierarquia | #1, #2, #6 | `src/dados.py`, `dados/`, `docs/dados.md` |
| Condições, prioridades e ações | #3, #7 | `src/decisoes.py`, `docs/regras.md` e testes |
| Regressão e estimativa | #5, #8 | `src/previsao.py`, conta manual e testes |
| Energia e interpretação | #4, #8, #13 | `src/energia.py`, saldo e exemplos |
| Um único sistema Python | #9, #10, #11 | `main.py`, integração e reprodução limpa |
| README e PDF com link público | #12–#15 | `README.md`, `relatorio/relatorio.pdf` e checklist |

## Revisão cruzada

Davi revisa contratos/regras/integração; Lorenzo revisa energia e as partes de Davi; Eduardo revisa regressão e contas; Gabriel revisa previsão/energia documentadas e saídas; Guilherme confere integração e coerência final. A issue detalha quem precisa revisar cada parte. Nome indicado não equivale a aprovação realizada.

Cada autor trabalha nos arquivos delimitados. Apenas Gabriel consolida o relatório/README em #14; Guilherme integra o programa em #10 e o pacote em #15. Alterações necessárias nos arquivos dos outros devem ser combinadas e creditadas.
