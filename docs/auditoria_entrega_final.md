# Auditoria de entrega, revisões e fechamento — 11/11/2026

## Base e alcance

Base local limpa inicial: `1bdde52388ef4e4964b8337323a9af694ff96ea4`, candidata da [PR #28](https://github.com/bkampdev/FIAP-PBL-FASE-3/pull/28). `main` pública consultada: `6f8435480293b1d38a146e399b4fbb54c2e6d9c3`, merge da [PR #27](https://github.com/bkampdev/FIAP-PBL-FASE-3/pull/27). As consultas de GitHub, PDFs e portal descrevem o estado observado em **11/11/2026**, sujeito ao avanço posterior pelo coordenador.

Foram lidos os critérios e comentários das **15 issues**, corpos dos **13 PRs (#16–#28)**, reviews formais, comentários de linha e conversas retornados pelas APIs paginadas. Também foram conferidos `CONTRIBUTING.md`, requisitos, contratos, checklist, fonte/PDF e código real de `src/dados.py`, `src/sistema.py`, `src/energia.py`, `src/previsao.py`, `src/decisoes.py` e `src/apresentacao.py`. Não foi encontrado `AGENTS.md` adicional na worktree ou nos diretórios ancestrais consultados; aplicam-se as instruções fornecidas na tarefa.

Validação técnica e revisão pessoal são evidências diferentes. Um comentário em conta do mantenedor não prova revisão de outro integrante; review automatizada também não substitui o colega indicado. Esta auditoria não altera autoria histórica, issues, PRs, colaboradores ou envio acadêmico. Somente este relatório e o checklist foram editados nesta worktree.

## Estado público e acesso GitHub

- O [repositório Fase 3](https://github.com/bkampdev/FIAP-PBL-FASE-3) está **público**, não arquivado, com branch padrão `main`. Página e [PDF raw da main](https://raw.githubusercontent.com/bkampdev/FIAP-PBL-FASE-3/main/relatorio/relatorio.pdf) retornaram HTTP 200 sem autenticação.
- Colaboradores: `@bkampdev` com `admin`; `@daviconinck`, `@Rocha0306`, `@BackesEdu` e `@ItsTheContext` com `write`; **0 convites pendentes**. Notas de atribuição/convite pendente nos corpos de algumas issues descrevem 04/11, não o acesso atual.
- Proteção da `main`: resolução de conversas exigida; mínimo de approvals **0**, sem code owner obrigatório, sem imposição a administradores. A ausência de trava técnica não dispensa os critérios escritos nas issues.
- Actions retornou **um run de revisão automatizada**, bem-sucedido em `b9c6d6262f7b28f0170e6bdb207537f368c22fb0` da integração #23 ([registro](https://github.com/bkampdev/FIAP-PBL-FASE-3/actions/runs/42954430285), evento `dynamic`, caminho `dynamic/agents/copilot-pull-request-reviewer`). Não é uma execução da suíte de testes. A #28 tinha `statusCheckRollup: []`; **105 testes locais não são CI da #28**.
- O PDF público da `main` ainda tinha **uma página preliminar**, integração descrita como pendente e exemplos ilustrativos de reserva 10 kWh/consumo futuro 45 kWh. SHA-256 `5891f31ebab0612cdb5de62c4d8778bf8c9e7b805f1112248bb73e4cdb5e0bf5`, idêntico ao PDF extraído de `6f84354`. A candidata `1bdde52` tem PDF atualizado de **duas páginas**; a existência em PR não atualiza o link padrão da `main`.

## RMs e fontes públicas verificadas

Somente nomes da equipe e RMs necessários à identificação acadêmica são reproduzidos. Os cinco pares coincidem nos dois READMEs, nas fontes Markdown e na **página 1 dos dois PDFs**, por extração textual e inspeção visual:

| Integrante | RM | GitHub |
|---|---|---|
| Davi Coninck Cassaro | RM572772 | `@daviconinck` |
| Guilherme Cardoso Bremenkamp | RM574229 | `@bkampdev` |
| Lorenzo Mendes Rocha | RM575361 | `@Rocha0306` |
| Gabriel Gonzales | RM574746 | `@ItsTheContext` |
| Eduardo Backes Klauck | RM575889 | `@BackesEdu` |

Fontes fixadas nos commits públicos consultados:

- **Fase 1**, commit `baac444aee6c1ed8b3cb3e080ec72d76386da1d0`: [README, linhas 123–129](https://github.com/bkampdev/FIAP-PBL-FASE-1/blob/baac444aee6c1ed8b3cb3e080ec72d76386da1d0/README.md#L123-L129), [fonte Markdown](https://github.com/bkampdev/FIAP-PBL-FASE-1/blob/baac444aee6c1ed8b3cb3e080ec72d76386da1d0/relatorio/relatorio-pre-decolagem.md), [PDF público](https://github.com/bkampdev/FIAP-PBL-FASE-1/blob/baac444aee6c1ed8b3cb3e080ec72d76386da1d0/relatorio/relatorio-pre-decolagem.pdf).
- **Fase 2**, commit `9d569e9fe78279118395067032521b9de21f9f3d`: [README, linhas 91–99](https://github.com/bkampdev/FIAP-PBL-FASE-2/blob/9d569e9fe78279118395067032521b9de21f9f3d/README.md#L91-L99), [fonte Markdown](https://github.com/bkampdev/FIAP-PBL-FASE-2/blob/9d569e9fe78279118395067032521b9de21f9f3d/doc/pdf.md), [PDF público](https://github.com/bkampdev/FIAP-PBL-FASE-2/blob/9d569e9fe78279118395067032521b9de21f9f3d/doc/relatorio_mgpeb.pdf).

| Comparação | Fase 1 | Fase 2 | Fase 3 em `1bdde52` |
|---|---|---|---|
| Arquivo | 15 páginas; 2.168.878 bytes | 8 páginas; 161.103 bytes | 2 páginas; 6.587 bytes |
| Identificação | Capa: fase, título, data, cinco nomes/RMs e link | Primeira página: fase, título, tabela equipe/RM/participação e introdução | Fase, título e data; **sem os cinco nomes/RMs** |
| Estrutura observada | Resumo/matriz; telemetria, algoritmo, Python, energia, análise, reflexão; evidências e referências | Seis etapas: módulos/fila, regras, Python, combustível, computação, ESG; anexo e referências | Dados; balanço/regras; regressão; planejamento; execução/verificação/limites |
| Apresentação observada | Capa gráfica, títulos, cores e capturas de execução | Cabeçalho/rodapé, tabela, circuito e paginação `01/08` | Texto compacto, títulos, numeração, link clicável p. 2; duas páginas sem cortes ou sobreposição observados |
| Aprendizado aplicável | Identificação clara e ligação com evidências | Equipe compacta e estrutura rastreável | Incluir identificação e manter quatro tópicos, exemplos reais e objetividade |

SHA-256 dos PDFs baixados: Fase 1 `dca2a62e7a86e2a2034c64d9dff5d1f4182eb97f5ddaf422f85ab20c545116f8`; Fase 2 `255378a620ca5f5bb1f1a8c4fdb0e8f9e1069d7616de05b731e8a13700a2d9c6`; Fase 3 base `666a27d4f39b8e9c82d9f89260257db9031cce845b2a90210026cd568fc070f0`.

Os [requisitos da Fase 3](requisitos.md) pedem quatro comportamentos, cinco critérios de peso 2 e PDF objetivo com link público; **não fixam páginas**. Os PDFs anteriores são referências de identificação/apresentação. Não transplantar seis etapas, limites de páginas ou Grupo 2 da Fase 2. A identificação ausente foi encaminhada à frente de apresentação, responsável por README/PDF; não foi editada aqui.

## Matriz de critérios e fechamento

`T` significa critério técnico comprovado na base, sem equivaler a aprovação pessoal. Cada linha segue os **quatro critérios de aceite**, na ordem da issue; a revisão prevista complementa o aceite. A decisão é recomendação ao coordenador, sem executar fechamento/reabertura.

| Issue / estado | Quatro critérios e evidência | Revisão / dependência | Recomendação |
|---|---|---|---|
| [#1](https://github.com/bkampdev/FIAP-PBL-FASE-3/issues/1) **fechada** | T: comportamentos/critérios; vocabulário; responsáveis/revisores documentados; escopo básico. Contratos/plano, PR #19. Compreensão individual não se prova por documento. | Fechamento registra **exceção explícita autorizada** para integrar sem approvals adicionais. | Preservar estado/ressalva; não inventar revisão dos quatro colegas. |
| [#2](https://github.com/bkampdev/FIAP-PBL-FASE-3/issues/2) **aberta** | T/T/T/T: listas/chaves/hierarquia; validação sem mascarar déficit; solar/eólico; testes válidos/inválidos. `src/dados.py`, testes, PRs #21/#24/#27. | Guilherme tem comentário técnico #21; falta registro pessoal de Gabriel sobre histórico. #25 é substitutiva. | Pronta tecnicamente; falta revisão restante ou substituição explicitamente decidida. |
| [#3](https://github.com/bkampdev/FIAP-PBL-FASE-3/issues/3) **aberta** | T/T/T/T: ação/motivo; condições/prioridades; essenciais/alerta; sem mutação/dependência da apresentação. `src/decisoes.py`, testes, PRs #22/#27. | Davi registrou revisão/testes; falta Eduardo sobre balanço. | Técnica pronta; aguardar conferência prevista de Eduardo. |
| [#4](https://github.com/bkampdev/FIAP-PBL-FASE-3/issues/4) **aberta** | T/T/T/T: contas; três estados; reserva/previsão separadas; unidades/intervalo. `src/energia.py`, testes, PRs #20/#25. | Sem registros pessoais Lorenzo/Gabriel; #20 tem comentários técnicos Guilherme; #25 explicita substituição. | Aguardar revisão/substituição documentada; integrar ajuste textual da rodada e retestar. |
| [#5](https://github.com/bkampdev/FIAP-PBL-FASE-3/issues/5) **fechada** | T/T/T/T: reta ajustada/usada; 27,5; degeneração; avisos/limites. `src/previsao.py`, testes, PR #16. | Fechamento registra 5 testes/merge; não localizadas revisões pessoais Eduardo/Davi no #16/#5. Conferência matemática técnica em #20/#25/rodada atual. | Técnica confirmada; preservar histórico e explicitar lacuna de revisão, sem aprovação retroativa. |
| [#6](https://github.com/bkampdev/FIAP-PBL-FASE-3/issues/6) **aberta** | T/T/T/T: JSONs portáveis; oito resultados; par preditivo; origem sintética/hipóteses. JSONs, `docs/cenarios.md`, PRs #21/#24/#27. | Eduardo e Lorenzo sem registros pessoais dos cenários. | Aguardar dois registros ou decisão explícita. |
| [#7](https://github.com/bkampdev/FIAP-PBL-FASE-3/issues/7) **fechada** | T/T/T/T: tabela/código; combinações/fronteiras; previsão verificável; alerta sem promessa de segurança. `docs/regras.md`, `tests/test_prioridades.py`. | Davi registrou conta independente da regra 2 e comparação com CLI. | Fechamento sustentado; retestar se regras mudarem. |
| [#8](https://github.com/bkampdev/FIAP-PBL-FASE-3/issues/8) **aberta** | T/T/T/T: conta independente; previsão/saldo; degeneração/unidades; limites/origem. `docs/validacao_matematica.md`, `tests/test_modelo_energia.py`, PRs #20/#25. | Guilherme documenta integração; falta revisão pessoal Gabriel das correções. | Técnica conferida; falta revisão ou substituição documentada. |
| [#9](https://github.com/bkampdev/FIAP-PBL-FASE-3/issues/9) **aberta** | T/T/T/T: entrada/ação/motivo; observado/estimado; sem recálculo; exemplos reais. `src/apresentacao.py`, testes/exemplos, PRs #17/#27. | Approval Guilherme no #17; Lorenzo sem registro pessoal. | Aguardar Lorenzo e reteste consolidado. |
| [#10](https://github.com/bkampdev/FIAP-PBL-FASE-3/issues/10) **fechada** | T/T/T/T: comando único; módulos usados; previsão→decisão futura; erros/imutabilidade. `main.py`, `src/sistema.py`, testes, PR #23. | Reprodução Davi/Windows histórica `9d0b0d8` preservada em revisão final/#24; demais responsáveis sem approvals pessoais no #23. | Integração confirmada; revisão histórica não equivale a Windows atual ou aprovação de todos. |
| [#11](https://github.com/bkampdev/FIAP-PBL-FASE-3/issues/11) **aberta** | T/T/T: reprodução limpa/SHA; rastreio; bloqueios explicitados. C4, conferência por outro integrante, **pendente de registro pessoal**. Revisão final, #24/rodada atual. | Lorenzo sem revisão prevista; Windows atual não retestado após timeouts. | Manter aberta até revisão restante ou decisão documentada. |
| [#12](https://github.com/bkampdev/FIAP-PBL-FASE-3/issues/12) **fechada** | T/T/T/T: estruturas reais; regras/limites; exemplo; seção curta revisada. `docs/secoes/dados_decisoes.md`, PR #22. | Davi registrou revisão com contas e execução integrada. | Fechamento sustentado; preservar crédito e revalidar texto se mudar. |
| [#13](https://github.com/bkampdev/FIAP-PBL-FASE-3/issues/13) **aberta** | T/T/T/T: fórmula/números; unidades; decisão futura; hipóteses/limites. `docs/secoes/previsao_energia.md`, PRs #20/#25. | Gabriel e Lorenzo sem registros pessoais da seção. | Aguardar revisão ou substituição documentada. |
| [#14](https://github.com/bkampdev/FIAP-PBL-FASE-3/issues/14) **aberta** | T/T/T: README executável; quatro tópicos/link; exemplos reais. C4: páginas conferidas, **revisões pessoais pendentes**. PR #28; nova identificação na frente de apresentação. | Eduardo (contas) e Lorenzo (regras/legibilidade) sem registros; integrar/conferir versão final. | Não fechar automaticamente. Coordenador removeu `Closes #14`; nova consulta: `closingIssuesReferences: []`. |
| [#15](https://github.com/bkampdev/FIAP-PBL-FASE-3/issues/15) **aberta** | C1: equipe confirmada pelo coordenador; C2: GitHub confirmado; C3: candidata coerente, **commit final integrado pendente**; C4: **sem comprovante de envio**. | Davi confere execução/Gabriel artefatos; técnico/substitutivo não atribui aprovação a eles. | **Não fechar**: falta pacote integrado e comprovante do portal. |

Nenhuma issue aberta recebe recomendação de fechamento incondicional nesta fotografia. #7/#12 já fechadas têm revisão prevista registrada; #1 tem exceção explícita; #5/#10 têm implementação confirmada com limites de revisão descritos. O coordenador pode registrar decisão explícita/fundamentada de substituição, mantendo o nome de quem efetivamente conferiu.

## Revisões e todos os PRs

Registros específicos de Davi: [#3, testes e revisão](https://github.com/bkampdev/FIAP-PBL-FASE-3/issues/3#issuecomment-6805687878), [#7, conta independente](https://github.com/bkampdev/FIAP-PBL-FASE-3/issues/7#issuecomment-6805221411), [#12, seção](https://github.com/bkampdev/FIAP-PBL-FASE-3/issues/12#issuecomment-6805514480). Não são aprovação de todo o projeto ou de alterações posteriores.

Reviews formais `APPROVED`: conta `@bkampdev` no [#17, SHA 53a53ed](https://github.com/bkampdev/FIAP-PBL-FASE-3/pull/17#pullrequestreview-5851546846) e [#22, SHA d161d7a](https://github.com/bkampdev/FIAP-PBL-FASE-3/pull/22#pullrequestreview-5853270871). Comentários técnicos #20/#21 e texto #25 não comprovam revisão pessoal de Eduardo, Lorenzo ou Gabriel. A #25 declara expressamente que a conferência substitutiva não representa revisão pessoal de Gabriel.

| PR | Estado | Evidência / limite |
|---|---|---|
| [#16](https://github.com/bkampdev/FIAP-PBL-FASE-3/pull/16) | Integrada | Previsão, Gabriel; sem review formal pessoal localizada |
| [#17](https://github.com/bkampdev/FIAP-PBL-FASE-3/pull/17) | Integrada | Apresentação, Gabriel; approval Guilherme; exemplos inicialmente sintéticos posteriormente atualizados |
| [#18](https://github.com/bkampdev/FIAP-PBL-FASE-3/pull/18) | Integrada | README/PDF preliminares, Gabriel; sem approval pessoal localizado |
| [#19](https://github.com/bkampdev/FIAP-PBL-FASE-3/pull/19) | Integrada | Contratos; exceção de revisão no fechamento #1 |
| [#20](https://github.com/bkampdev/FIAP-PBL-FASE-3/pull/20) | Integrada | Energia/modelo/seção, Eduardo; correções preservam original; comentários técnicos Guilherme, sem review formal |
| [#21](https://github.com/bkampdev/FIAP-PBL-FASE-3/pull/21) | Integrada | Dados/cenários, Davi; comentário técnico exige documentação/folhas; head posterior registra correções; sem review formal |
| [#22](https://github.com/bkampdev/FIAP-PBL-FASE-3/pull/22) | Integrada | Decisões/seção, Lorenzo; approval Guilherme; registros Davi nas issues |
| [#23](https://github.com/bkampdev/FIAP-PBL-FASE-3/pull/23) | Integrada | CLI/orquestração; fecha #10; reviews automatizadas não comprovam revisão humana |
| [#24](https://github.com/bkampdev/FIAP-PBL-FASE-3/pull/24) | Integrada | Reprodução/testes, Davi; preserva revisão Windows histórica; Lorenzo explicitamente pendente |
| [#25](https://github.com/bkampdev/FIAP-PBL-FASE-3/pull/25) | Integrada | Conferência substitutiva; não atribui revisão a Gabriel; sem review formal |
| [#26](https://github.com/bkampdev/FIAP-PBL-FASE-3/pull/26) | **Fechada sem merge** | Documentação cenários; não equivale a integração desta PR; mudanças correspondentes aparecem na #27 |
| [#27](https://github.com/bkampdev/FIAP-PBL-FASE-3/pull/27) | Integrada | Head `a358881`, merge `6f84354`, 105 testes; referências não concluem revisões/envio; sem reviews formais/threads |
| [#28](https://github.com/bkampdev/FIAP-PBL-FASE-3/pull/28) | **Aberta** | Head inicial `1bdde52`, base `6f84354`, dois commits; candidata PDF 2p; sem reviews formais/threads/CI nesse snapshot |

## FIAP ON: leitura própria e evidência do coordenador

Acesso próprio pelo navegador Orca à [atividade 616829](https://on.fiap.com.br/mod/assign/view.php?id=616829) redirecionou ao login `https://on.fiap.com.br/index.php`. Nenhuma credencial foi inserida ou arquivo selecionado/enviado por este worker. Essa tentativa não permite afirmar estado da equipe/entrega.

**Evidência distinta, relatada pelo coordenador após leitura autenticada no Chrome em 11/11/2026:** após regularização, leitura posterior da atividade correta mostrou **Grupo 20 com exatamente Eduardo, Guilherme, Davi, Gabriel e Lorenzo**. O formulário mostrava até **20 anexos**, **256 MB por arquivo**, sem restrição de extensão visível. Prazo **11/11/2026 às 23h59 (America/Sao_Paulo)**. Sem seleção/envio de arquivos; entrega **PENDENTE**. Não são publicados e-mails ou dados de sessão.

Composição e limites visíveis têm evidência do coordenador; aceitação de anexos concretos e envio não têm comprovante. Regularização de equipe é ação separada desta auditoria somente leitura e não conclui a #15.

## Verificações, alinhamentos e pendências

- Nesta worktree, `python3 -B -m unittest discover -s tests -v`: **105 testes, OK**, Python **3.14.7**, macOS, base `1bdde52`. Inspeção de código confirmou fluxo e contratos; não foram criados testes redundantes para documentos.
- PDFs abertos com PyMuPDF: contagem/texto, cinco identificações Fases 1/2 e links conferidos. Primeira página Fases 1/2 e **ambas as páginas Fase 3** renderizadas e inspecionadas. Fase 3 base legível/cobre dados/regras/previsão/energia; ausência de equipe encaminhada à apresentação.
- Frente de dados relatou clone remoto limpo `1bdde52`, 105 testes, oito cenários CLI=integrador, nove exemplos idênticos e rastreio das funções reais. Registro em `f4afeeb96b7aeb4bc89fb7b0423ad74ed15d3931`, `docs/revisao-final.md`. Windows atual não atestado após timeouts, limite aceito pelo coordenador; revisão histórica não é reteste atual.
- Frente de energia informou `6584922edec7cc968bd01f69b7a2ab61750f701c`: mensagem de reserva hipotética e documentação de integração real; 105 testes, 256 balanços e oito cenários; contratos/números preservados. Aceite técnico não atribuído a outra pessoa.
- Alinhamentos enviados a todos: base/critérios; RMs/fontes; revisões versus envio; comparação dos PDFs; PDF público versus candidata. Incorporados limites de dados/energia/portal; à apresentação foram entregues fontes fixadas e recomendação de identificação; decisões recebeu o estado de revisões e ausência de divergência numérica. Os alinhamentos não constituem revisão pessoal dos responsáveis.

Resta integrar os commits aprovados da rodada, resolver conflitos se houver, reexecutar suíte/exemplos no **SHA integrado**, conferir identificação/legibilidade/link do PDF final, verificar publicação pública e registrar decisões de revisão/fechamento com seus limites. O pacote deve corresponder ao mesmo SHA. Envio no FIAP ON fora desta tarefa; #15 aberta até comprovante real.

Consultas de leitura para reproduzir a parte administrativa (requerem acesso autorizado ao repositório):

```sh
gh issue list -R bkampdev/FIAP-PBL-FASE-3 --state all --limit 100 --json number,title,state,body,comments,assignees,url
gh pr list -R bkampdev/FIAP-PBL-FASE-3 --state all --limit 100 --json number,title,state,body,headRefOid,mergeCommit
gh api repos/bkampdev/FIAP-PBL-FASE-3/collaborators --paginate --jq 'map({login,role_name})'
gh api repos/bkampdev/FIAP-PBL-FASE-3/invitations --paginate --jq 'length'
gh pr view 28 -R bkampdev/FIAP-PBL-FASE-3 --json closingIssuesReferences,reviewDecision,statusCheckRollup
```

Para cada PR de 16 a 28, foram consultados separadamente `repos/bkampdev/FIAP-PBL-FASE-3/pulls/N/reviews`, `pulls/N/comments` e `issues/N/comments` com `gh api --paginate`. Dados temporários e imagens de inspeção ficaram fora do repositório; nenhum arquivo do portal foi versionado.
