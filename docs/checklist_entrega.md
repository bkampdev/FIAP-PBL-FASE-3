# Checklist de entrega e matriz de evidências — Issue #15 (envio pendente)

## Estado atualizado após a PR #27 e candidata da #14

- [x] A [PR #27](https://github.com/bkampdev/FIAP-PBL-FASE-3/pull/27) foi integrada à `main` no commit `6f8435480293b1d38a146e399b4fbb54c2e6d9c3`; a suíte foi reexecutada nessa base com **105 testes OK**.
- [x] A [PR #28](https://github.com/bkampdev/FIAP-PBL-FASE-3/pull/28) contém, no commit `9e586a126057dc026623eab91eb2829d2bb42064`, README com saída real da CLI e fonte/PDF do relatório final. O PDF tem duas páginas, as seções exigidas e link público clicável; as páginas foram inspecionadas visualmente. Esta é uma candidata em PR, ainda não um commit integrado à `main`.
- [ ] Revisões pessoais de Eduardo (contas) e Lorenzo (regras e legibilidade) da #14 registradas no GitHub.
- [ ] Cinco integrantes conferidos na atividade correta, formatos/anexos confirmados e pacote final correspondente ao mesmo commit integrado.
- [ ] Envio no FIAP ON realizado e comprovante/status do portal registrado. A issue #15 permanece aberta até essa confirmação.

## Registro da auditoria anterior (base `47e29ef`)

O registro abaixo preserva a conferência somente leitura executada em **11/11/2026** sobre a `main` anterior (`47e29ef694c251040551add30c9d8ed882fcb10d`). Seus estados e SHAs descrevem aquela base histórica; o estado atual está acima. Naquela auditoria, nenhuma entrega havia sido enviada ao FIAP ON, nenhuma alteração de equipe/convites havia sido realizada e os arquivos da issue #14 (`README.md`, `relatorio/relatorio.md`, `relatorio/relatorio.pdf`, `scripts/gerar_relatorio.py`) estavam intocados.

## 1. Status do checklist de entrega

- [x] Enunciado lido no FIAP ON em 04/11/2026 ([atividade 616829](https://on.fiap.com.br/mod/assign/view.php?id=616829)) e cruzado com `docs/requisitos.md`, separando Fase 3 de Global Solution e Challenge.
- [x] Prazo oficial conferido: **11/11/2026 às 23h59 (`America/Sao_Paulo`)**.
- [x] Repositório público confirmado (`visibility: public` em <https://github.com/bkampdev/FIAP-PBL-FASE-3>) e convites GitHub aceitos pelos quatro colegas com permissão `write` ativa (`@daviconinck`, `@Rocha0306`, `@BackesEdu`, `@ItsTheContext`), além de `@bkampdev` (`admin`), com **0 convites pendentes** na API do GitHub.
- [ ] Cinco integrantes conferidos na atividade FIAP ON atual (na leitura de 04/11 o Grupo 20 exibia apenas Guilherme; consulta sem sessão autenticada em 11/11 retorna `HTTP 303 -> https://on.fiap.com.br/index.php`, exigindo conferência autenticada pelo responsável sem expor dados pessoais).
- [x] Contratos acordados (`docs/contratos.md`, `docs/plano-trabalho.md`) e módulos do núcleo implementados em Python padrão pelos cinco responsáveis (`src/dados.py`, `src/decisoes.py`, `src/energia.py`, `src/previsao.py`, `src/apresentacao.py`, `src/sistema.py`, `main.py`).
- [x] Estruturas de dados, hierarquia, regras de decisão, regressão linear e balanço energético efetivamente usados no fluxo integrado (`python3 main.py --listar` e `python3 main.py --cenario deficit`).
- [x] Cenários e suíte de testes executados com resultados e SHAs registrados (`100/100` testes `OK` na `main` `47e29ef`; `101/101` na branch isolada `bkampdev/pbl-issue-11` em `3c1b959` / `db99667`; `105/105` na candidata combinada temporária `ad053608` validada pela #11).
- [ ] Reprodução em cópia limpa e revisão cruzada completas: reprodução limpa comprovada em `9d0b0d8` (PR #24) e revalidada em `47e29ef` (`52ab6ef` / `3c1b959` / `db99667`), mas **permanecem pendentes revisões humanas individuais** de colegas no GitHub (detalhadas na Seção 4).
- [x] `README.md` contém instruções de execução integrada e valores reais do cenário `deficit` desde o PR #24 (`98baa34`), restando ajuste pontual na #14 (nota sobre interpretador `python3`/`python` e atualização da referência ao exemplo de `docs/exemplos_saida.md`).
- [ ] PDF objetivo final com os quatro tópicos consolidados e todas as páginas revisadas: `relatorio/relatorio.pdf` atual (4044 bytes, 1 página, com link público `https://github.com/bkampdev/FIAP-PBL-FASE-3`) e `relatorio/relatorio.md` ainda são a versão preliminar do PR #18 (usam reserva ilustrativa de 10 kWh e afirmam fluxo integrado pendente); dependem da consolidação do usuário na **issue #14** a partir de `docs/secoes/dados_decisoes.md` (#12) e `docs/secoes/previsao_energia.md` (#13).
- [ ] Pacote correspondente ao mesmo commit final consolidado (código, `README.md` e `relatorio/relatorio.pdf` regenerado após merge da PR única e conclusão da #14) e formatos aceitos no formulário do portal confirmados em sessão autenticada.
- [ ] Envio realizado no FIAP ON e comprovante/status confirmado pelo portal registrado após submissão (sem incluir dados pessoais).

## 2. Matriz dos cinco critérios de avaliação (peso 2 cada — total 10)

| Critério (peso 2) | Arquivos principais | Execução e evidência comprovada na `main` (`47e29ef`) e branches da rodada | Estado / pendência |
|---|---|---|---|
| **1. Estruturação de dados** | `src/dados.py`, `dados/cenarios.json`, `dados/historico_eolico.json`, `docs/dados.md`, `docs/cenarios.md`, `tests/test_dados.py` | 8 cenários sintéticos e histórico pareado `[8, 10, 12]` m/s → `[20, 25, 30]` kWh em intervalos de `1 h`; `buscar_subsistema` distingue folha `{}` de caminho inexistente `None`; ajustes documentais em `07fa900` (#2) e `8880a67` (#6). | Técnico comprovado; pendente revisão humana de `@Rocha0306` (#6/#11) e `@BackesEdu` (#6). |
| **2. Lógica de decisão** | `src/decisoes.py`, `docs/regras.md`, `tests/test_decisoes.py`, `tests/test_prioridades.py` | Regras ordenadas (`alerta_critico`, `alerta_deficit`, `equilibrio`, `excedente`), suporte à vida preservado (P1 essencial), redução por prioridade numérica decrescente; rejeição direta de consumo negativo em `3bbacb2` (#3) e casos combinados/revisão manual em `61f3471` (#7). Revisão humana de `@daviconinck` registrada em #3 e #7. | Técnico comprovado; integrar `3bbacb2` e `61f3471` na PR consolidada. |
| **3. Modelagem e previsão** | `src/previsao.py`, `docs/previsao.md`, `docs/validacao_matematica.md`, `tests/test_previsao.py`, `tests/test_modelo_energia.py` | Regressão linear por mínimos quadrados (`a = 2,5`, `b = 0`), estimativa `27,5 kWh` para `11 m/s`, aviso de extrapolação (`13 m/s -> 32,5 kWh`) e bloqueio de histórico sem variação. Conta independente validada em #8 (PR #20) e conferida em PR #25 (`5e840c8`). | Técnico comprovado; pendente revisão pessoal de `@ItsTheContext` / `@daviconinck` onde aplicável. |
| **4. Implementação em Python** | `main.py`, `src/sistema.py`, `src/energia.py`, `src/apresentacao.py`, `tests/test_energia.py`, `tests/test_apresentacao.py`, `tests/test_sistema.py`, `tests/test_integracao.py`, `docs/revisao-final.md` | Núcleo apenas com biblioteca padrão; `python3 -B -m unittest discover -s tests -v` aprovou `100/100` em `47e29ef` (`101/101` em `3c1b959` da #11; `105/105` na candidata combinada `ad053608`). `python3 main.py --cenario deficit` retorna geração `40 kWh`, consumo `70 kWh`, saldo `-30 kWh`, reserva `15 kWh`, previsão `27,5 kWh` e saldo futuro `-22,5 kWh` (reserva restante hipotética `0 kWh`), sem mutar entradas. | Técnico comprovado; revalidar suíte no SHA consolidado e concluir revisão humana de `@Rocha0306` na #11. |
| **5. Documentação e organização** | `README.md`, `docs/contratos.md`, `docs/plano-trabalho.md`, `docs/exemplos_saida.md`, `docs/secoes/dados_decisoes.md`, `docs/secoes/previsao_energia.md`, `relatorio/relatorio.md`, `relatorio/relatorio.pdf`, `docs/checklist_entrega.md` | Seções #12 (`dados_decisoes.md`, revisada por `@daviconinck` no comentário `6805514480`) e #13 (`previsao_energia.md`) prontas em `47e29ef`; `docs/exemplos_saida.md` atualizado com 9 saídas reais da CLI em `2114e71` (#9). | **Bloqueador de entrega final:** consolidar `README.md` e `relatorio/relatorio.{md,pdf}` na **#14** (usuário) sobre o commit final e enviar no FIAP ON. |

## 3. Alinhamento entre issues dependentes nesta rodada

- **#11 (`bkampdev/pbl-issue-11` — commits `52ab6ef`, `3c1b959`, `db99667`):** preservou relato original de Davi (`9d0b0d8` / PR #24), adicionou cobertura de consumo inválido via CLI (`101/101` isolado) e validou em clone temporário (`ad053608`) a combinação de `#2` (`07fa900`), `#3` (`3bbacb2`), `#6` (`8880a67`), `#7` (`61f3471`), `#9` (`2114e71`) e `#11` (`3c1b959`) com **`105/105` testes OK**. Acordado manter explícita a ausência de revisão humana de `@Rocha0306` em `#2/#6/#11` e exigir revalidação no SHA consolidado final.
- **#9 (`bkampdev/pbl-issue-9` — commit `2114e71`):** substituiu o exemplo sintético provisório em `docs/exemplos_saida.md` por 9 execuções reais verificadas byte a byte contra `python3 main.py`, sem alterar código nem arquivos da #14. Acordado registrar pendência de revisão humana de `@Rocha0306` e de ajuste da referência na linha 49 do `README.md` pelo usuário na #14.
- **#12 (`bkampdev/pbl-issue-12` — `47e29ef`):** `docs/secoes/dados_decisoes.md` estável e aderente à CLI real, com revisão humana registrada de `@daviconinck` (`issuecomment-6805514480`) e conferência técnica no PR #25; depende apenas da consolidação na #14.
- **#13 (`bkampdev/pbl-issue-13` — `47e29ef`):** `docs/secoes/previsao_energia.md` estável e aderente às contas (`27,5 kWh`, `-30 kWh`, `-22,5 kWh`, extrapolação `32,5 kWh`), com conferência técnica no PR #25 (`docs/revisao-previsao-integracao.md`), pendente de revisões humanas pessoais (`@ItsTheContext` / `@Rocha0306`) e incorporação na #14.

## 4. Revisões humanas registradas vs. pendências reais

- **Revisões humanas registradas no GitHub (auditadas via API em 11/11/2026):**
  - `@daviconinck`: comentários de revisão em **#3** (`issuecomment-6805687878`), **#7** (`issuecomment-6805221411`) e **#12** (`issuecomment-6805514480`).
  - `@bkampdev`: reviews `APPROVED` nos PRs **#17** (`53a53ed`) e **#22** (`d161d7a`), e conferências técnicas documentadas nos PRs **#20**, **#21**, **#24** e **#25**.
- **Revisões humanas ainda não registradas no GitHub (não atribuídas sem registro pessoal):**
  - `@Rocha0306` (Lorenzo): revisão dos dados/cenários/testes de Davi (**#6**, **#11**), apresentação (**#9**), energia (**#4**), seção #13 e relatório final (**#14**).
  - `@BackesEdu` (Eduardo): revisão de **#3** (balanço), **#5** (matemática), **#6** (cenários) e **#14** (contas do PDF final).
  - `@ItsTheContext` (Gabriel): conferência pessoal de **#2** (histórico), **#4**/**#8**/**#13** (previsão/seção) e artefatos da **#15** (conferência técnica substitutiva registrada em `docs/revisao-previsao-integracao.md` sem atribuir aprovação pessoal a Gabriel).
- **Pendências operacionais obrigatórias antes de encerrar a #15 (ação humana do responsável):**
  1. Integrar a PR consolidada única pelo coordenador e revalidar o commit integrado.
  2. Concluir a **issue #14** (usuário): consolidar `relatorio/relatorio.md`, regenerar `relatorio/relatorio.pdf` conferindo todas as páginas e o link público, e alinhar `README.md` ao mesmo commit final.
  3. Autenticar no **FIAP ON** (`id=616829`), confirmar os **cinco integrantes** no grupo correto da Fase 3, verificar os formatos/anexos exigidos pelo formulário, realizar o envio até **11/11/2026 às 23h59 (`America/Sao_Paulo`)** e somente então registrar data/hora, anexos e confirmação do portal (preservando dados pessoais).
