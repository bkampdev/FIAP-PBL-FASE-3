# Checklist de entrega — Issue #15 (envio pendente)

Conferência de **11/11/2026** sobre a candidata `1bdde52388ef4e4964b8337323a9af694ff96ea4` da [PR #28](https://github.com/bkampdev/FIAP-PBL-FASE-3/pull/28), baseada na `main` `6f8435480293b1d38a146e399b4fbb54c2e6d9c3` ([PR #27](https://github.com/bkampdev/FIAP-PBL-FASE-3/pull/27)). A [auditoria detalhada](auditoria_entrega_final.md) contém todas as issues/PRs, fontes dos RMs, revisões e limites. O retrato histórico de `47e29ef` foi substituído; o [registro anterior permanece no histórico](https://github.com/bkampdev/FIAP-PBL-FASE-3/blob/1bdde52388ef4e4964b8337323a9af694ff96ea4/docs/checklist_entrega.md).

## Equipe e acesso

- [x] GitHub público confirmado pela API e HTTP 200 sem autenticação na página e no PDF da `main`.
- [x] Cinco colaboradores ativos: `@bkampdev` com `admin`; `@daviconinck`, `@Rocha0306`, `@BackesEdu` e `@ItsTheContext` com `write`. **Zero convites pendentes.** Notas antigas de convite pendente nas issues estão desatualizadas.
- [x] Nomes/RMs cruzados nos READMEs e PDFs públicos das Fases 1 e 2; fontes fixadas e tabela na auditoria. Não reutilizar o grupo de outra fase.
- [x] **Conferência do coordenador**, em sessão autenticada Chrome da [atividade correta 616829](https://on.fiap.com.br/mod/assign/view.php?id=616829): após regularização, leitura posterior mostrou **Grupo 20 com exatamente Eduardo, Guilherme, Davi, Gabriel e Lorenzo**. O acesso separado deste worker pelo Orca chegou ao login e não é segunda conferência autenticada.

## Programa e cinco critérios de avaliação

| Critério (peso 2) | Evidência na candidata `1bdde52` | Estado |
|---|---|---|
| Estruturação de dados | `src/dados.py`, JSONs, consumidores/hierarquia solar/eólico, folha `{}` distinta de `None`, oito cenários sintéticos | Técnico verificado; revisão pessoal restante na matriz |
| Lógica de decisão | `src/decisoes.py`, regras/testes, essenciais preservados e planejamento futuro explícito | Técnico verificado; Davi tem registros nas #3/#7/#12; falta Eduardo na #3 |
| Modelagem e previsão | `src/previsao.py`: a=2,5, b=0, vento 11 → 27,5 kWh; avisos e degeneração | Técnico verificado; #25 não representa revisão pessoal de Gabriel |
| Implementação em Python | CLI → integrador → cinco módulos; biblioteca padrão; **105 testes OK** | Reprodução limpa adicional registrada pela frente de dados; Windows atual não comprovado |
| Documentação e organização | README, nove exemplos reais, fonte/PDF de duas páginas na PR #28 | Candidata verificada; identificação/nova apresentação sob revisão da #14; integrar e conferir versão final |

- [x] Nesta auditoria: `python3 -B -m unittest discover -s tests -v` → **105 testes, OK**, Python 3.14.7/macOS, em `1bdde52`.
- [x] Exemplo `deficit`: geração 40 kWh, consumo 70 kWh, saldo observado -30 kWh, cobertura **potencial** 15 kWh, déficit restante 15 kWh, previsão 27,5 kWh, saldo futuro hipotético -22,5 kWh; reserva restante hipotética zero, sem reutilizar estoque.
- [ ] Revisões pessoais restantes registradas conforme a matriz; testes/auditoria não substituem aprovação de outra pessoa.
- [ ] Integrar a candidata final e revalidar o SHA integrado com as alterações da rodada. A versão da PR ainda não equivale à publicada na `main`.
- [ ] Código, README, fonte Markdown e PDF final correspondem ao mesmo commit; conferir todas as páginas e o link público após consolidação.

## Formulário e envio

- [x] Prazo registrado nos requisitos e confirmado pelo coordenador no portal: **11/11/2026 às 23h59, America/Sao_Paulo**.
- [x] **Conferência do coordenador** no formulário autenticado: até **20 anexos**, **256 MB por arquivo**; nenhuma restrição de extensão visível. Isso registra o mostrado, sem presumir aceitação de arquivo ainda não selecionado.
- [ ] Preparar/conferir anexos a partir do mesmo SHA final: nomes, tamanhos, abertura e formato solicitado pelo portal.
- [ ] **Envio no FIAP ON e comprovante/status confirmado.** Última leitura autenticada relatada pelo coordenador: **PENDENTE**, sem seleção/envio de arquivos. Esta auditoria não envia a atividade.

## Condição de encerramento

A #15 permanece **aberta** até confirmação real do envio, distinta do merge. Registrar então data/hora, SHA do pacote, nomes/versões dos anexos e status do portal, sem publicar e-mails ou credenciais. Davi confere execução e Gabriel artefatos conforme a issue, ou o coordenador registra explicitamente a decisão de substituição, sem atribuir revisão pessoal inexistente.

## Atualização da candidata consolidada

Após o retrato histórico acima, a branch `bkampdev/pbl-auditoria-final` reuniu as cinco auditorias. Nessa candidata, uma cópia Git limpa executou `python3 -B -m unittest discover -s tests` com **105 testes OK**, listou os oito cenários e reproduziu `deficit` com saldo atual de -30 kWh, previsão eólica de 27,5 kWh e saldo futuro de -22,5 kWh. O cenário inexistente retornou erro e código 1.

O PDF final de duas páginas foi regenerado de `relatorio/relatorio.md` com `scripts/gerar_relatorio.py` e comparado byte a byte ao arquivo versionado. A inspeção visual das duas páginas não mostrou cortes; os cinco nomes e RMs, o link público e as hipóteses do cálculo estão presentes. `README.md`, Markdown, gerador e PDF estão na mesma candidata. O arquivo `repositorio_github.txt` contém o link público para anexação, se solicitado pelo portal.

- [x] Candidata consolidada: código, README, Markdown e PDF conferidos no mesmo estado.
- [x] PDF e `repositorio_github.txt` preparados para a entrega; abrir e selecionar os anexos ainda é tarefa de envio.
- [ ] Integrar a PR consolidada à `main` e conferir o SHA publicado.
- [ ] Receber as revisões pessoais pendentes registradas na auditoria.
- [ ] Enviar no FIAP ON e guardar o comprovante real. O usuário reservou para si essa ação.
