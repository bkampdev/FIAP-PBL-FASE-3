# Plano de trabalho e mapa de integração

Plano consolidado em 10/11/2026 para a [issue #1](https://github.com/bkampdev/FIAP-PBL-FASE-3/issues/1), a partir de `docs/requisitos.md`, `CONTRIBUTING.md`, das issues e do código em revisão. Campos, unidades, retornos e erros ficam em [contratos.md](contratos.md). Planejamento, PR aberto, aprovação, merge e envio ao portal são estados distintos.

## 1. Escopo e quatro comportamentos esperados

Um único sistema em Python básico: biblioteca padrão no núcleo, funções separadas para dados, energia, previsão, decisões, integração e apresentação. Sem banco, API, interface web, controle físico ou modelo avançado obrigatório. Identificar dados sintéticos e hipóteses didáticas. Geradores do PDF podem ter dependências próprias, separadas da execução principal.

| Comportamento obrigatório | Demonstração e aceite |
|---|---|
| 1. Organizar energia, consumo e clima em listas/chave-valor e representar/navegar hierarquia | Lista de cenários/sistemas, histórico pareado e consulta real a `colonia → energia → solar/eolico`, com consumidores por ID; folha `{}` diferente de caminho ausente `None`. |
| 2. Decidir com condições combinadas e suporte à vida prioritário | Ação/motivo por regra; menor prioridade numérica preservada primeiro, essenciais fora da redução; insuficiência essencial gera alerta crítico, sem promessa de segurança. |
| 3. Ajustar relação linear e estimar novo valor | Mínimos quadrados: `[8, 10, 12]` / `[20, 25, 30]` gera `a=2.5`, `b=0`, `y(11)=27.5 kWh`; extrapolação/estimativa negativa sinalizadas, sem inventar valor seguro. |
| 4. Comparar geração, consumo e reserva, com alertas/sugestões | `40/70 → -30`, `80/30 → +50`, `50/50 → 0 kWh`; reserva como cobertura potencial separada; previsão muda recomendação futura, distinguindo observado/estimado e sem reutilizar estoque. |

## 2. Estado observado e limites da entrega #1

Snapshot GitHub de 10/11/2026: `main` em `c8a0400d158d484b6aa0c09e65649b4d18bfccb3`, com estrutura/documentação inicial e `src/__init__.py`, sem módulos funcionais integrados. Issues #1–#15 abertas. Os cinco responsáveis já constam como assignees; avisos antigos de atribuição pendente nos corpos não comprovam pendência atual.

| Trabalho em revisão | Branch → base | Evidência disponível / pendência |
|---|---|---|
| [PR #16](https://github.com/bkampdev/FIAP-PBL-FASE-3/pull/16), #5 — Gabriel | `codex/issue-5-previsao` → `main` | Código/testes de regressão em `198da5e25434fffb6ce79c657245bd66f8c1c9df`; falta revisão/integração. |
| [PR #17](https://github.com/bkampdev/FIAP-PBL-FASE-3/pull/17), #9 — Gabriel | `codex/issue-9-apresentacao` → `codex/issue-5-previsao` | Formatador/testes em `53a53ede60237f74d8fe9971169941020d0f9af6`; balanço/decisão dos exemplos são sintéticos; falta revisão/integração e saída real de #10. |
| [PR #18](https://github.com/bkampdev/FIAP-PBL-FASE-3/pull/18), #14 — Gabriel | `codex/issue-14-relatorio` → `codex/issue-9-apresentacao` | README/relatório preliminares, dependentes de #10/#11/#12/#13; não equivalem ao pacote final validado. |

O PR de #1 altera somente `docs/contratos.md` e `docs/plano-trabalho.md`; não implementa módulos nem integra PRs dos colegas. Mapa de apoio local, materiais didáticos e transcrição ficam fora do repositório. Estado posterior precisa de nova conferência no GitHub; este snapshot não é acompanhamento automático.

## 3. Matriz requisito → issue → arquivo → evidência

Evidências abaixo são aceites a produzir/conferir pelos responsáveis. A última coluna distingue o que existe em revisão do que exige execução integrada.

| Requisito / critério de avaliação | Peso | Issues | Arquivos responsáveis | Evidência de aceite |
|---|---|---|---|---|
| Estruturação de dados; comportamento 1 | 2 | #1, #2, #6, #11 | `docs/contratos.md`, `src/dados.py`, `tests/test_dados.py`, `dados/cenarios.json`, `dados/historico_eolico.json`, `docs/dados.md`, `docs/cenarios.md`, `tests/test_integracao.py` | Cenários reproduzíveis, histórico pareado, consulta solar/eólico/caminho ausente; inválidos rejeitados sem rejeitar déficit. Implementação/reprodução pendentes. |
| Lógica de decisão; comportamento 2 | 2 | #3, #6, #7, #10, #12 | `src/decisoes.py`, `tests/test_decisoes.py`, `tests/test_prioridades.py`, `docs/regras.md`, `docs/secoes/dados_decisoes.md` | Ações/motivos, fronteiras, prioridades e insuficiência essencial rastreáveis; dois ventos mudam só recomendação futura. Pendente. |
| Modelagem e previsão; comportamento 3 | 2 | #5, #8, #10, #13 | `src/previsao.py`, `tests/test_previsao.py`, `tests/test_modelo_energia.py`, `docs/previsao.md`, `docs/validacao_matematica.md`, `docs/secoes/previsao_energia.md` | Conta manual `2.5*x`, estimativa `27.5`, extrapolação, casos degenerados/negativos; código/testes no PR #16, auditoria cruzada/integração pendentes. |
| Implementação em Python; integração dos comportamentos 1–4 | 2 | #2–#11 | `src/dados.py`, `src/energia.py`, `src/previsao.py`, `src/decisoes.py`, `src/apresentacao.py`, `src/sistema.py`, `main.py`, `tests/test_energia.py`, `tests/test_apresentacao.py`, `tests/test_sistema.py`, `tests/test_integracao.py`, `docs/revisao-final.md` | Execução única, importação sem iniciar CLI, suíte/cópia limpa seguindo README; contas `-30/+50/0`, reserva sem dupla contagem e previsão indisponível sem apagar observação válida. Apenas previsão/apresentação em PR; ponta a ponta pendente. |
| Documentação e organização; explicação dos comportamentos 1–4 | 2 | #1, #9, #12–#15 | `docs/plano-trabalho.md`, `docs/contratos.md`, `docs/exemplos_saida.md`, `docs/secoes/dados_decisoes.md`, `docs/secoes/previsao_energia.md`, `README.md`, `relatorio/relatorio.md`, `relatorio/relatorio.pdf`, `docs/checklist_entrega.md` | Autoria/revisão registradas, comandos/entradas/saídas reais do mesmo commit, PDF legível com link público e recibo de envio. PRs #17/#18 preliminares; documento final/recibo pendentes. |

Cinco critérios de peso 2, total 10. A análise energética (comportamento 4) aparece na execução Python, interpretação da previsão e documentação; não constitui um sexto critério independente.

## 4. Autoria, arquivos delimitados e revisão cruzada

Cada integrante tem três issues e contribuição Python identificável. Revisores são os definidos nas issues; indicação/solicitação não significa aprovação. Ajustes no código de outro autor devem ser combinados e preservar crédito.

| Issue | Autor responsável | Arquivos / resultado delimitado | Revisores |
|---|---|---|---|
| [#1](https://github.com/bkampdev/FIAP-PBL-FASE-3/issues/1) | Guilherme — @bkampdev | `docs/contratos.md`, `docs/plano-trabalho.md` | Davi e autores dos quatro módulos: Lorenzo, Eduardo, Gabriel |
| [#2](https://github.com/bkampdev/FIAP-PBL-FASE-3/issues/2) | Davi — @daviconinck | `src/dados.py`, `tests/test_dados.py`, `docs/dados.md` | Guilherme; Gabriel confere histórico |
| [#3](https://github.com/bkampdev/FIAP-PBL-FASE-3/issues/3) | Lorenzo — @Rocha0306 | `src/decisoes.py`, `tests/test_decisoes.py` | Davi; Eduardo confere balanço |
| [#4](https://github.com/bkampdev/FIAP-PBL-FASE-3/issues/4) | Eduardo — @BackesEdu | `src/energia.py`, `tests/test_energia.py` | Lorenzo; Gabriel confere previsão |
| [#5](https://github.com/bkampdev/FIAP-PBL-FASE-3/issues/5) | Gabriel — @ItsTheContext | `src/previsao.py`, `tests/test_previsao.py`, `docs/previsao.md` | Eduardo confere matemática; Davi confere entradas |
| [#6](https://github.com/bkampdev/FIAP-PBL-FASE-3/issues/6) | Davi — @daviconinck | `dados/cenarios.json`, `dados/historico_eolico.json`, `docs/cenarios.md` | Eduardo e Lorenzo |
| [#7](https://github.com/bkampdev/FIAP-PBL-FASE-3/issues/7) | Lorenzo — @Rocha0306 | `tests/test_prioridades.py`, `docs/regras.md` | Davi |
| [#8](https://github.com/bkampdev/FIAP-PBL-FASE-3/issues/8) | Eduardo — @BackesEdu | `tests/test_modelo_energia.py`, `docs/validacao_matematica.md` | Gabriel confere correções; Guilherme confere integração |
| [#9](https://github.com/bkampdev/FIAP-PBL-FASE-3/issues/9) | Gabriel — @ItsTheContext | `src/apresentacao.py`, `tests/test_apresentacao.py`, `docs/exemplos_saida.md` | Lorenzo; Guilherme confere comando principal |
| [#10](https://github.com/bkampdev/FIAP-PBL-FASE-3/issues/10) | Guilherme — @bkampdev | `main.py`, `src/sistema.py`, `tests/test_sistema.py` | Davi e autores dos módulos caso precisem de ajustes |
| [#11](https://github.com/bkampdev/FIAP-PBL-FASE-3/issues/11) | Davi — @daviconinck | `docs/revisao-final.md`, `tests/test_integracao.py` | Lorenzo; conclusão entregue a Guilherme |
| [#12](https://github.com/bkampdev/FIAP-PBL-FASE-3/issues/12) | Lorenzo — @Rocha0306 | `docs/secoes/dados_decisoes.md` | Davi |
| [#13](https://github.com/bkampdev/FIAP-PBL-FASE-3/issues/13) | Eduardo — @BackesEdu | `docs/secoes/previsao_energia.md` | Gabriel; Lorenzo confere regras citadas |
| [#14](https://github.com/bkampdev/FIAP-PBL-FASE-3/issues/14) | Gabriel — @ItsTheContext | `README.md`, `relatorio/relatorio.md`, `relatorio/relatorio.pdf`, `scripts/gerar_relatorio.py` se usado | Eduardo confere matemática; Lorenzo confere regras/legibilidade |
| [#15](https://github.com/bkampdev/FIAP-PBL-FASE-3/issues/15) | Guilherme — @bkampdev | `docs/checklist_entrega.md` e entrega no FIAP ON | Davi confere execução; Gabriel confere artefatos |

## 5. Sequência rumo a #10, #14 e #15

1. **Contrato (#1):** publicar PR dos dois documentos contra `main`, com `Refs #1`, comandos, entradas/saídas e SHA. Solicitar @daviconinck, @Rocha0306, @BackesEdu e @ItsTheContext. Resolver divergências com autores/consumidores antes de integrar; fechar após revisão/merge.
2. **Bases (#2–#5):** cada autor entrega seu módulo conforme contrato. #5 já tem PR #16; Eduardo/Davi revisam matemática/entradas. #2 fornece validação/hierarquia; #3 decide; #4 calcula balanço. Cada PR exige revisão/merge, sem transferir autoria a quem integra.
3. **Dados, saída e conferências (#6–#9):** #6 depende de #2 e fornece cenários com resultados esperados; #7 cruza #3/#6; #8 cruza #4/#5; #9 alinha retornos de #3/#4/#5. Após merge de #16, conferir/ajustar base de #17 para `main`, sem presumir redirecionamento automático. Revisar/integrar apresentação; exemplos permanecem sintéticos até #10. #7/#8 podem avançar em paralelo à integração, mas resolver achados antes da candidata final.
4. **Programa único (#10):** integrar #1/#2/#3/#4/#5/#6/#9 disponíveis na `main`. Fluxo: carregar cenários/histórico → validar → consultar solar/eólico na hierarquia → balanço observado → ajuste/previsão → decisão atual/futura → formatação na CLI. Entrada inválida bloqueia decisão; histórico indisponível mantém só resultados atuais válidos. Demonstrar nominal, déficit, excedente, equilíbrio, insuficiência essencial, erros e dois ventos. Entregar a Gabriel comandos, entradas, saídas reais e SHA.
5. **Auditoria e seções (#11–#13):** #11 reproduz #10 em cópia limpa, registrando Python, SO, commit, achados/retestes. #12 usa dados/regras implementados e revisados em #2/#3/#6/#7. #13 usa regressão/energia conferidas em #4/#5/#8. Saídas finais dependem da integração; fixtures não comprovam execução do sistema completo.
6. **README/PDF (#14):** atualizar branch do PR #18 com a `main` integrada, conferindo base após #17. Incorporar #10/#11/#12/#13 e resolver achados de #7/#8; preservar autoria, substituir exemplos provisórios de #9 por saídas reais e gerar PDF correspondente. Revisão Eduardo/Lorenzo, inspeção de todas as páginas/links e merge da candidata coerente.
7. **Pacote/portal (#15):** após #10/#11/#14, conferir cinco critérios contra commit final, código/README/PDF, acesso público, equipe na atividade e anexos aceitos. Administração pode começar antes; conclusão exige envio e status/recibo observado no FIAP ON. Merge/publicação no GitHub não comprova entrega acadêmica.

## 6. Conferência e critérios para avançar

Seguir `CONTRIBUTING.md`: `git switch main`, `git pull --ff-only`, branch própria, exemplo pequeno, testes úteis normal/fronteira/erro, commit/push e revisão. Alterar somente arquivos da issue. No PR registrar comandos realmente executados, entrada, saída, limitações e hash; não atribuir revisão sem registro do colega.

Para #1, conferir código/testes de #16/#17 sem incorporá-los nesta branch; executar os testes fora do checkout e passar o exemplo completo de `docs/contratos.md` ao formatador real. Conferir contas de referência e `git diff --check`; verificar diff exclusivo dos dois documentos. Isso valida compatibilidade com os commits inspecionados, sem comprovar o sistema completo. O PR registra resultados observados.

Após #10, executar os comandos-alvo abaixo na revisão limpa #11; até lá são critérios planejados, ainda indisponíveis na `main` inicial:

```bash
python3 -m unittest discover -s tests -v
python3 main.py --listar
python3 main.py --cenario deficit
```

Acrescentar nominal, excedente, equilíbrio, essencial insuficiente e dois ventos definidos em #6, com nomes reais combinados por Davi/Guilherme. #11 registra resultados e #14 usa comandos reais. Verificar importação de `main.py` sem executar CLI, apresentação sem recalcular valores e ausência de alteração das entradas/estoque para fazer um caso passar.

## 7. Prazo e fechamento

Prazo registrado em `docs/requisitos.md` e nas issues: **11/11/2026 às 23h59, America/Sao_Paulo**. Fonte acadêmica consultada em 04/11; sem nova conferência do portal nesta issue. Metas antigas de 05–09/11 eram internas e não comprovam execução. Em 10/11, priorizar contratos/módulos, integração e candidata ao README/PDF; reservar 11/11 para validação/envio com margem. Reavaliar viabilidade com o estado real dos PRs.

Composição do grupo e formatos aceitos no portal pertencem a #15; acesso GitHub não inclui colegas na FIAP. Não misturar com Enterprise Challenge ou Global Solution. Não publicar materiais didáticos, transcrição integral ou dados pessoais desnecessários. #15 permanece pendente sem confirmação de envio; #1 permanece pendente sem revisão dos colegas e integração.
