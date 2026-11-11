# Revisão final do sistema integrado — Issue #11

Responsável: Davi (@daviconinck)

Data: 11/11/2026

O registro original e a autorização do PR #24 estão preservados abaixo.
As revalidações de `47e29ef` e da candidata combinada estão nas seções
finais e não substituem a revisão pessoal pendente de Lorenzo.

## Objetivo

Verificar a execução do sistema energético da Colônia Aurora
em uma cópia limpa do repositório GitHub.

## Ambiente de revisão

- Sistema operacional: Windows
- Python: 3.14.7
- Commit da cópia limpa: 9d0b0d8
- Repositório: https://github.com/bkampdev/FIAP-PBL-FASE-3

## Reprodução em cópia limpa

Comandos executados:

    git clone https://github.com/bkampdev/FIAP-PBL-FASE-3.git FIAP-revisao-limpa
    cd FIAP-revisao-limpa
    python main.py --listar
    python main.py --cenario deficit
    python -m unittest discover -s tests -v

Resultados:
- 8 cenários listados.
- Cenário de déficit executado corretamente.
- 97 testes aprovados, nenhuma falha.
- Nenhuma alteração local na cópia limpa.

## Rastreamento do cenário deficit

| Etapa | Resultado |
|---|---|
| Leitura | JSON carregado |
| Hierarquia | Solar, eólico e consumidores identificados |
| Geração solar | 20 kWh |
| Geração eólica | 20 kWh |
| Geração total | 40 kWh |
| Consumo | 70 kWh |
| Saldo atual | -30 kWh |
| Reserva | 15 kWh |
| Vento previsto | 11 m/s |
| Previsão eólica | 27,5 kWh |
| Saldo futuro | -22,5 kWh |
| Decisão | Preservar suporte à vida e avaliar redução do laboratório |

## Testes complementares

Arquivo: tests/test_integracao.py

Casos verificados:
1. Déficit e preservação do suporte à vida.
2. Alerta crítico e intervenção humana.
3. Rejeição de cenário inexistente.

Resultado informado após inclusão dos testes:
- 100 testes executados.
- 100 testes aprovados.

## Achados

### Codificação de caracteres no Windows

Problema: dois testes complementares inicialmente falharam
porque a saída do subprocesso apresentava caracteres acentuados
incorretos durante a captura.

Esperado: textos em português preservados.

Obtido inicialmente: caracteres de substituição nos acentos.

Correção: executar o subprocesso Python com `-X utf8`.

Reteste: os três testes complementares passaram.

Estado: corrigido no teste complementar.

### Instruções de execução desatualizadas no README

Reprodução: consultar o README no commit `8a8e366`. O estado da versão
ainda apresenta a integração da issue #10 como pendente, e o comando
principal aparece como sujeito à conferência após a integração.

Esperado: instruções suficientes para listar os cenários e executar o
programa integrado a partir de uma cópia limpa.

Obtido: a integração já está disponível desde `9d0b0d8`, mas o README
não apresenta `python main.py --listar` e trata a execução integrada
como futura.

Responsável pela correção: Guilherme (@bkampdev).

Correção: atualizar o estado da versão, documentar os comandos de
listagem e análise e informar os resultados esperados do déficit.

Reteste: comandos de listagem e análise de déficit executados com sucesso;
oito cenários listados e valores conferidos com a tabela deste documento.
A suíte completa aprovou os 100 testes em macOS com Python 3.14.7.

Estado: corrigido neste PR.

## Conferência complementar e autorização de integração

Em 11/11/2026, a conferência do commit `8a8e366` e das correções
documentais deste PR verificou o diff, os critérios das issues e a suíte
completa. Também foram conferidos a listagem, o déficit, o alerta crítico,
a fronteira essencial e a rejeição de cenário inexistente.

Os módulos de dados e cenários das issues #2 e #6 já estão na `main`
desde o PR #21. Este PR acrescenta os três testes complementares e o
registro de revisão da issue #11, além da atualização do README.

Guilherme (@bkampdev) autorizou expressamente as correções, o commit
neste PR e o merge após validação. A revisão individual de Lorenzo
continua pendente; essa autorização não representa aprovação de Lorenzo
nem cumprimento automático de todos os critérios de aceite das issues.

## Pendências

- Solicitar a Lorenzo revisão independente dos arquivos
  de dados e testes produzidos por Davi.
- Registrar o resultado dessa revisão antes de concluir o aceite da
  issue #11. O merge autorizado por Guilherme não encerra essa pendência.

## Conclusão

A execução em cópia limpa foi bem-sucedida no commit
9d0b0d8, com 97 testes aprovados.

Posteriormente, na branch de desenvolvimento, foram
executados 100 testes após a inclusão dos três testes
complementares, conforme resultado informado pelo responsável.

Nenhum bloqueador funcional foi identificado nas execuções
registradas. A conferência complementar aprovou os 100 testes e
verificou as instruções atualizadas do README. A integração foi
autorizada por Guilherme; a aprovação independente de Lorenzo permanece
pendente e não foi atribuída a ele.

## Revalidação independente da candidata atual — 11/11/2026

### Base e ambiente efetivamente conferidos

- Issue #11 lida integralmente, incluindo os quatro critérios de aceite.
- PR #23: integração e CLI; PR #24: revisão histórica, três testes
  complementares e instruções; PR #25: conferência de previsão e balanço.
  Os três já estavam integrados; seus módulos e testes foram reutilizados.
- `origin/main`, após `git fetch origin main`:
  `47e29ef694c251040551add30c9d8ed882fcb10d` (merge do PR #25).
- Clone novo do GitHub em `/tmp/pbl-issue-11-revisao-20261111`, com o mesmo
  SHA completo. `git status --porcelain=v1` vazio antes e depois das execuções.
- macOS 26.0, build 25A5316i, arm64; Python 3.14.7.
- Núcleo e testes executados sem instalar pacotes externos. O gerador do
  PDF não faz parte desta conferência e não foi executado.

Esta é uma conferência técnica adicional desta entrega. Não representa
execução ou aprovação pessoal de Davi, Lorenzo ou outro integrante.
As alterações futuras da PR consolidada precisam de reteste no seu próprio
SHA; os resultados abaixo se referem exclusivamente à base indicada.

### Reprodução e adaptação de ambiente

O README foi seguido para clonar, listar, executar o déficit, rodar a suíte
e reproduzir a previsão isolada. Neste shell, `python` não existe, enquanto
`python3 --version` retorna `Python 3.14.7`. Antes de adaptar o ambiente,
`python --version` retorna `command not found`, código 127. As primeiras
execuções usaram `python3`; depois, os comandos com `python` do README
foram repetidos em um ambiente virtual criado pela biblioteca padrão:

```bash
git clone --no-local --branch main https://github.com/bkampdev/FIAP-PBL-FASE-3.git /tmp/pbl-issue-11-revisao-20261111
cd /tmp/pbl-issue-11-revisao-20261111
git rev-parse HEAD
git status --porcelain=v1
python3 -m venv /tmp/pbl-issue-11-venv-20261111
source /tmp/pbl-issue-11-venv-20261111/bin/activate
python --version
python main.py --listar
python main.py --cenario deficit
python -m unittest discover -s tests -v
python -c "from src.previsao import ajustar_reta, prever_energia; modelo = ajustar_reta([8, 10, 12], [20, 25, 30]); print(prever_energia(modelo, 11)['energia_eolica_prevista_kwh'])"
git status --porcelain=v1
git diff --check
```

Na execução registrada, o diretório `bin` do ambiente virtual foi colocado
no `PATH` dos subprocessos, equivalente à ativação acima. A suíte passou
**100 testes, sem falhas ou erros**, tanto com `python3` quanto com o
`python` desse ambiente; a listagem exibiu os oito IDs e a previsão isolada
retornou `27.5`. Os comandos válidos retornaram código 0; os dois comandos
Git de inspeção não apontaram alterações ou erros.

Achado documental: um usuário deste macOS precisa escolher `python3` ou
ativar um ambiente virtual antes de usar os exemplos com `python`.
Esperado: instruções suficientes para identificar o interpretador.
Obtido: o nome `python` não está disponível no shell inicial.
Responsabilidade: consolidação do README na #14, reservada ao usuário.
Estado: comunicado ao coordenador; adaptação retestada, ajuste do README
pendente. Nenhuma dependência externa ausente foi identificada no núcleo.

### Rastreio completo de `deficit`

Os valores abaixo foram confrontados com `dados/cenarios.json`,
`dados/historico_eolico.json`, `docs/cenarios.md` (#6) e a conta independente
de `docs/validacao_matematica.md` (#8), e comparados com o envelope real de
`executar_cenario` e o texto de `formatar_resultado`.

| Etapa e função executada | Entrada ou conta independente | Resultado observado |
|---|---|---|
| Leitura e validação, `carregar_cenarios` / `carregar_historico` | JSONs versionados, intervalo comum de 1 h | Oito cenários; `deficit` selecionado; histórico pareado válido |
| Consulta, `buscar_subsistema` | `colonia/energia/solar`, `colonia/energia/eolico` e caminho inexistente | `{}`, `{}` e `None`; folha vazia distinguida de ausência |
| Cadastro de consumidores | Suporte à vida: 35 kWh, essencial, P1; laboratório: 35 kWh, não essencial, P2 | Consumo total 70 kWh, essencial 35 kWh |
| Balanço, `analisar_energia` | Solar 20 + eólica observada 20 − consumo 70 | Geração 40 kWh, saldo −30 kWh, classificação `deficit` |
| Cobertura potencial | `min(15, 30) = 15`; déficit remanescente `30 − 15 = 15` | Reserva usada hipotética 15 kWh, remanescente 15 kWh; saldo observado continua −30 |
| Ajuste, `ajustar_reta` | Vento `[8, 10, 12]`, energia `[20, 25, 30]`; médias 10 e 25; `a = 20/8`, `b = 25 − 2,5 × 10` | `a=2.5`, `b=0.0` |
| Estimativa, `prever_energia` | Vento previsto 11 m/s; `2,5 × 11` | 27,5 kWh, `extrapolacao=False`, `aviso=None` |
| Decisão, `decidir` | Déficit atual e prioridade dos essenciais | `alerta_deficit`; preservar suporte à vida e avaliar redução do laboratório; motivo informa 30/15/15 kWh |
| Próximo intervalo hipotético | `20 + 27,5 − 70 = −22,5`; reserva restante `15 − 15 = 0` | Recomendação futura com −22,5 kWh e reserva hipotética 0 kWh; eólica observada não somada à prevista |
| Saída, `formatar_resultado` | Envelope de seis chaves | Cenário, intervalo, balanço atual, ações/motivos, coeficientes e previsão apresentados com acentos preservados |

O rastreio de chamadas com `sys.setprofile` confirmou a execução das funções
dos cinco módulos (`dados`, `energia`, `previsao`, `decisoes`, `apresentacao`)
e do integrador, em vez de inferir seu uso apenas pelos imports.
O envelope contém exatamente `erro`, `cenario`, `balanco`, `previsao`,
`erro_previsao`, `decisao`; os dois erros são `None`. Comparação profunda
antes/depois confirmou que cenário e histórico de entrada não foram mutados.
As ações são recomendações; não demonstram descarga, desligamento ou segurança
física do suporte à vida.

Para inspecionar novamente o envelope integral e a saída a partir da raiz
do clone, com o ambiente virtual ativo:

```bash
python - <<'PY'
import json
from src.dados import carregar_cenarios, carregar_historico
from src.sistema import executar_cenario
from src.apresentacao import formatar_resultado
cenario = next(c for c in carregar_cenarios("dados/cenarios.json") if c["id"] == "deficit")
resultado = executar_cenario(cenario, carregar_historico("dados/historico_eolico.json"))
print(json.dumps(resultado, ensure_ascii=False, indent=2))
print(formatar_resultado(resultado))
PY
```

### Limiares, erros e cobertura reutilizada

| Comando ou teste existente | Esperado e obtido nesta candidata |
|---|---|
| `python main.py --cenario alerta_critico` | Código 0; geração 10 + reserva 5 < essencial 35, falta 20 kWh; `alerta_critico`, preservação dos essenciais e intervenção humana imediata |
| `python main.py --cenario fronteira_essencial` | Código 0; geração 30 + reserva 5 = essencial 35; `alerta_deficit` e dependência da reserva, sem garantia de segurança |
| `python main.py --cenario cenario_que_nao_existe` | Código 1 e mensagem `Cenário inexistente`, sem balanço fictício |
| `python main.py --cenario deficit --historico /tmp/pbl-issue-11-historico-inexistente.json` | Código 0; saldo −30 e ações atuais preservados; previsão e recomendação futura indisponíveis, com motivo |
| `test_sistema.TestErrosEFronteirasSistema` | Cenário inválido bloqueia decisão; histórico inválido/degenerado/incompatível preserva análise atual; estimativa negativa preserva aviso sem planejamento físico inválido |
| `test_sistema.TestIntegracaoSistema` e `test_prioridades` | Oito cenários, limiares, consulta hierárquica real, prioridades, entrada imutável e ventos baixo/alto sem alterar balanço atual |
| Três testes de `tests/test_integracao.py` entregues no PR #24 | Déficit, alerta crítico e cenário inexistente aprovados; não foram duplicados nem reescritos |

Não foi encontrado bloqueador funcional nas execuções desta candidata.
A correção de validação direta de consumo negativo em `decidir`, comunicada
pela frente da #3, está fora deste SHA e deve ser integrada e retestada na
PR consolidada; o fluxo desta base já valida o cenário antes de decidir.

### Critérios e encaminhamento para #15

| Critério da #11 | Evidência ou pendência |
|---|---|
| Reprodução em cópia limpa com commit e resultados | Clone remoto limpo no SHA completo acima; Python/OS, comandos e 100 testes registrados |
| Um cenário rastreado de ponta a ponta | `deficit`, da leitura dos JSONs à hierarquia, contas, decisão e saída, com uso real dos cinco módulos |
| Bloqueadores corrigidos/retestados ou explicitados | Sem bloqueador funcional observado; adaptação `python3`/venv retestada; clareza do README encaminhada à #14; alterações posteriores requerem novo reteste |
| Partes do revisor conferidas por outro integrante | Pendente: revisão pessoal de Lorenzo dos dados/testes de Davi; esta revalidação não cumpre nem atribui essa revisão |

Conclusão para Guilherme: a base `47e29ef` reproduz o fluxo integrado com
100 testes aprovados e contas coerentes com #6/#8. O aceite completo da
#11 continua pendente da conferência humana indicada; merge anterior,
reteste automatizado e ausência de falha não equivalem a essa aprovação.
Nenhuma issue foi fechada e nenhuma entrega acadêmica foi realizada.

## Revalidação combinada das issues #3, #6 e #11 — 11/11/2026

### Base, candidata e reprodução

Nesta rodada foram relidas a issue #11 integralmente (sem comentários),
as descrições, comentários de conversa, reviews e comentários inline dos
PRs #22, #23, #24 e #25. O PR #24 continua sem review pessoal de Lorenzo.
Seu registro e o commit `52ab6ef592806ac9342f8039d0ec593b8f4e0ca3`
foram preservados, sem reescrita ou atribuição de nova revisão humana.

`git ls-remote origin refs/heads/main` confirmou novamente
`47e29ef694c251040551add30c9d8ed882fcb10d`. Um novo clone remoto em
`/tmp/pbl-issue-11-rodada2-20261111` começou e terminou a verificação da
main sem alterações locais, com **100 testes aprovados**. Ambiente:
macOS 26.0, build 25A5316i, arm64, Python 3.14.7; sem instalação de pacotes.

Apenas nesse clone, em HEAD destacado, foram combinados os commits:

- #11: `52ab6ef592806ac9342f8039d0ec593b8f4e0ca3`;
- #3: `3bbacb235d22059a36598ee901b9aee226fe31e1`, rejeição direta de consumo negativo;
- #6: `8880a67354f4e80a8a0f05f9ef8088ce8c89b643`, que preserva
  `bedd675f4f44f0e7e876fc3ee95c901b6ee255dd`, ambos documentais;
- o teste novo de CLI desta rodada, descrito abaixo.

O commit temporário resultante é
`8702be1e057ca90c4b4f6be54eac8915494f8508`, com **102 testes aprovados**
e `git status --porcelain=v1` vazio antes/depois. Ele identifica a candidata
efetivamente executada; não foi publicado nem deve ser usado como commit de
entrega. As branches originais, autores e commits não foram alterados pela
combinação. A branch isolada da #11, sem incorporar #3/#6, passou
**101 testes**: os 100 da main mais um teste CLI; a regressão direta da #3
é o teste adicional que leva a candidata combinada a 102.

Comandos da preparação e validação, a partir da raiz da worktree da #11:

```bash
git clone --no-local --branch main https://github.com/bkampdev/FIAP-PBL-FASE-3.git /tmp/pbl-issue-11-rodada2-20261111
cd /tmp/pbl-issue-11-rodada2-20261111
git rev-parse HEAD
git status --porcelain=v1
python3 -m unittest discover -s tests -v
git fetch '/Users/bkamp/orca/workspaces/PBL 3 - FASE 3/pbl-issue-11' bkampdev/pbl-issue-11 bkampdev/pbl-issue-3 bkampdev/pbl-issue-6
git checkout --detach 52ab6ef592806ac9342f8039d0ec593b8f4e0ca3
git merge --no-commit --no-ff 3bbacb235d22059a36598ee901b9aee226fe31e1 8880a67354f4e80a8a0f05f9ef8088ce8c89b643
cp '/Users/bkamp/orca/workspaces/PBL 3 - FASE 3/pbl-issue-11/tests/test_integracao.py' tests/test_integracao.py
git add tests/test_integracao.py
git commit -m 'test: candidata temporaria de integracao das issues 3, 6 e 11'
python3 -m unittest discover -s tests -v
git status --porcelain=v1
git diff --check
```

O arquivo de teste copiado tem blob Git
`04cc86e74ab747437aab4216d61e7f489cff55cf`; uma nova reprodução pode criar
outro SHA de commit devido à data, preservando o conteúdo conferido.
As instruções do README para listagem, déficit e previsão isolada também
foram reproduzidas com o `python` de um venv padrão em
`/tmp/pbl-issue-11-rodada2-venv-20261111`: oito IDs e resultado `27.5`.
O achado sobre escolha de `python3`/venv e a contagem do README continuam
encaminhados à #14, sem edição de seus arquivos nesta tarefa.

### Lacuna de cobertura fechada e reteste

Reprodução: fornecer `--cenarios` com JSON contendo consumo `-5` no
Suporte à vida ou no Laboratório do cenário `deficit`.

Esperado: código 1, mensagem de erro de entrada identificando `consumo_kwh`,
sem saldo, decisão atual ou previsão fictícios.

Obtido: ambos os casos rejeitados como esperado, sem traceback ou stderr.
O fluxo da CLI já rejeitava esses dados antes da correção direta da #3;
a lacuna comprovada era a ausência de cobertura explícita desse consumidor
inválido no caminho JSON → carregamento → CLI → saída. Foi adicionado
somente `test_consumo_negativo_no_json_rejeitado_sem_resultado_ficticio`,
em `tests/test_integracao.py`, com dois subcasos. Os três testes originais
do PR #24 foram mantidos. Responsabilidade e estado: #11, cobertura concluída.

Na candidata com #3, `decidir` também levantou
`ValueError: consumo_kwh não pode ser negativo.` para o balanço
aritmeticamente coerente da regressão direta; `executar_cenario` retornou
erro em `cenario.sistemas[1].consumo_kwh`, sem balanço ou decisão.
Isso confirma a correção da #3 sem copiar seu teste unitário para a #11.

### Integração e acordos entre as issues

Os oito cenários foram novamente executados por CLI e pelo integrador,
com igualdade entre o texto da CLI e `formatar_resultado`. Comparação
profunda confirmou cenário e histórico não mutados. `sys.setprofile`
confirmou chamadas reais a validação/consulta de dados, balanço, ajuste e
previsão, decisão, apresentação e integrador. O rastreio de `deficit` da
seção anterior permanece válido: 40 − 70 = −30 kWh; cobertura potencial
15 kWh; remanescente 15 kWh; `a=2.5`, `b=0`; eólica prevista 27,5 kWh;
futuro 20 + 27,5 − 70 = −22,5 kWh, reserva restante hipotética zero.

| Dependência | Comunicação e acordo nesta rodada |
|---|---|
| #2, dados de Davi | Confirmado `07fa900`, apenas `docs/dados.md`, sem lacuna funcional ou mudança de contrato/dados/testes; responsável confirmou ausência de revisão pessoal de Lorenzo sobre dados/testes de Davi |
| #3, decisões de Lorenzo | Confirmado SHA `3bbacb2`; responsável reproduziu erro direto, integrador e CLI; acordado que apenas #11 acrescenta cobertura CLI, sem duplicar teste direto |
| #6, cenários de Davi | Confirmado SHA `8880a67`, sem mudança de IDs/valores; responsável informou matriz/fronteiras de main com 100 testes, compatível com os oito cenários executados aqui; commits preservados |
| #9, apresentação de Gabriel | Confirmado `2114e71`, apenas exemplos documentais; acordado que o caso negativo CLI da #11 não duplica seus quatro testes; formatador/contrato preservados, revisão pessoal de Lorenzo ainda pendente |
| #15, checklist de Guilherme | Acordado separar main (100), #11 isolada (101) e candidata combinada (102), manter #14 intocada e a revisão pessoal de Lorenzo pendente |

Também foi confirmado com #8 que a cobertura CLI nova não muda as contas;
seu responsável informou 101 testes na candidata anterior sem esse teste.
As execuções informadas por outros responsáveis são distintas das
execuções diretas registradas nesta seção.

A frente #15 informou auditoria da API sem revisão humana de Lorenzo para
#2/#6/#11 e registrou revisões pessoais de Davi nas issues #3/#7/#12.
Esses registros existentes são preservados; esta conferência técnica não
os substitui nem os amplia. Sem bloqueador funcional observado nesta
candidata; o aceite da #11 permanece pendente de Lorenzo. Alterações
posteriores e o SHA da PR consolidada exigem nova verificação pelo
coordenador. README, relatório final, PDF e gerador da #14 ficaram intocados.

### Complemento após respostas finais de #2, #7 e #9

O commit de entrega `3c1b95984b771e76e9425d9a6c632e15ed0ab4bb` registra
o teste CLI e a conferência anterior da #11, preservando `52ab6ef`.
Após esse registro chegaram três commits que foram lidos e acrescentados
somente à cópia temporária, sem mudar as branches dos responsáveis:

- #2: `07fa9001cbee789d6a3ced97f69d85a32e1900c4`, atualização documental
  de integração, sem alteração de dados, código ou testes;
- #7: `61f3471d896b153f0962ff38763714565d157dc3`, três testes combinados
  adicionais de prioridades e atualização de `docs/regras.md`, preservando
  o registro da conta manual feita por Davi;
- #9: `2114e719f348fa6d111e518c58f8522e5e880460`, nove exemplos reais
  de CLI em `docs/exemplos_saida.md`, sem mudança funcional do formatador.

A candidata temporária ampliada
`ad05360861425d13a1bce0d2f2166b769208bd4f` contém esses três commits,
além de #3/#6/#11 já conferidos, e passou
`python3 -m unittest discover -s tests`: **105 testes, OK**.
O acréscimo de 102 para 105 corresponde exclusivamente aos três testes
da #7. A worktree isolada da #11 continua com 101; este complemento só
altera documentação. `git status --porcelain=v1` permaneceu vazio na
candidata e `git diff --check` não indicou erros.

Os nove pares comando/saída de `docs/exemplos_saida.md` foram extraídos
dos blocos Markdown e comparados com stdout integral da CLI nesta candidata:
listagem, nominal, déficit, excedente, vento baixo, vento alto, fronteira
essencial, alerta crítico e cenário inexistente. Todos coincidiram,
incluindo acentos e quebras de linha; retornos 0 nos válidos e 1 no
inexistente. A conferência foi comunicada às frentes #7/#9/#15.

Os acordos de #2/#3/#6/#9/#15 foram recebidos e respondidos por
`orca orchestration`; nenhuma divergência funcional ficou aberta.
Permanece a revisão pessoal de Lorenzo sobre dados/testes de Davi e a
revalidação no SHA final da PR consolidada, a cargo do coordenador.
Este resultado de integração não fecha issues, não publica PR individual
e não representa envio ao FIAP.

## Auditoria final das issues #2, #6 e #11 na PR #28 — 11/11/2026

### Candidata, ambiente e limites da conferência

Esta rodada confere a candidata documental e funcional
`1bdde52388ef4e4964b8337323a9af694ff96ea4`, da branch
`bkampdev/pbl-entrega-relatorio-final`, sobre o merge da PR #27
`6f8435480293b1d38a146e399b4fbb54c2e6d9c3`.
O clone remoto novo em `/private/tmp/pbl3-auditoria-dados-remoto-20261111`
começou e terminou sem alterações, com macOS 26.0, build 25A5316i,
Python 3.14.7 e nenhuma instalação adicional para o núcleo ou os testes.
Um clone local independente do mesmo SHA também aprovou os 105 testes.

As instruções atuais do README para `python3`, listagem, déficit, suíte e
regressão isolada foram reproduzidas. O bloco de saída de `deficit` do
README coincide integralmente com stdout, inclusive acentos e quebras de
linha. O achado histórico de escolha de interpretador foi resolvido pelo
README atual, que indica `python3` no macOS/Linux e `python` ou `py -3` no
Windows; os registros anteriores foram preservados como histórico.

**Windows não foi verificado nesta rodada.** O canal remoto retornou
`timed out` tanto na tentativa de obter versões/comandos quanto no health
check, sem saída que permitisse comprovar execução. O coordenador orientou
registrar essa limitação e concluir a conferência macOS, sem novas tentativas.
Os comandos equivalentes abaixo são instruções para reteste, não resultados
Windows atuais. A reprodução Windows de `9d0b0d8` no início deste documento
continua sendo evidência histórica daquele SHA e daquela contagem de testes.

### Comandos e resultados reproduzidos

```bash
git clone --no-local --branch bkampdev/pbl-entrega-relatorio-final https://github.com/bkampdev/FIAP-PBL-FASE-3.git /private/tmp/pbl3-auditoria-dados-remoto-20261111
cd /private/tmp/pbl3-auditoria-dados-remoto-20261111
git rev-parse HEAD
git status --porcelain=v1
python3 --version
python3 -B main.py --listar
python3 -B main.py --cenario deficit
python3 -B -m unittest discover -s tests -v
python3 -c "from src.previsao import ajustar_reta, prever_energia; modelo = ajustar_reta([8, 10, 12], [20, 25, 30]); print(prever_energia(modelo, 11)['energia_eolica_prevista_kwh'])"
git diff --check
git status --porcelain=v1
```

Saídas de referência desta execução: SHA completo acima;
`Python 3.14.7`; oito IDs na ordem do JSON; déficit com geração 40,
consumo 70, saldo −30, reserva 15 e eólica prevista 27,5 kWh;
`Ran 105 tests in 0.537s`, `OK`; previsão isolada `27.5`.
Todos esses comandos retornaram 0 e as inspeções Git não produziram saída.

Para Windows, na raiz de uma cópia da mesma candidata, substituir o
interpretador conforme o README:

```powershell
py -3 main.py --listar
py -3 main.py --cenario deficit
py -3 -B -m unittest discover -s tests -v
py -3 -c "from src.previsao import ajustar_reta, prever_energia; modelo = ajustar_reta([8, 10, 12], [20, 25, 30]); print(prever_energia(modelo, 11)['energia_eolica_prevista_kwh'])"
```

Pode-se usar `python` no lugar de `py -3` quando esse for o interpretador
disponível. Para captura UTF-8 explícita, inserir `-X utf8` após o comando
do interpretador, conforme já usado pelos testes complementares.

### Oito cenários e caminhos de erro

Os oito casos foram executados individualmente pela CLI e pelo integrador.
Cada stdout coincidiu com `formatar_resultado(resultado) + "\n"` e retornou
código 0, sem stderr. As contas abaixo foram comparadas com valores
esperados fixos, usando `math.isclose` com tolerâncias `1e-9`, e com as
tabelas de `docs/cenarios.md`. Todas as energias estão em kWh por intervalo.

| Cenário | Saldo atual | Cobertura potencial | Déficit remanescente | Eólica prevista | Saldo futuro | Status atual |
|---|---:|---:|---:|---:|---:|---|
| nominal | 10 | 0 | 0 | 25 | 10 | excedente |
| deficit | -30 | 15 | 15 | 27,5 | -22,5 | alerta_deficit |
| excedente | 50 | 0 | 0 | 30 | 50 | excedente |
| equilibrio | 0 | 0 | 0 | 20 | 0 | equilibrio |
| alerta_critico | -40 | 5 | 35 | 20 | -25 | alerta_critico |
| fronteira_essencial | -20 | 5 | 15 | 25 | -5 | alerta_deficit |
| vento_baixo | -10 | 0 | 10 | 20 | -10 | alerta_deficit |
| vento_alto | -10 | 0 | 10 | 30 | 0 | alerta_deficit |

Comparação profunda antes/depois confirmou entradas imutáveis. Todos os
envelopes têm exatamente as seis chaves contratuais e ambos os erros
ausentes nos casos válidos. As consultas reais de solar/eólico retornam
`{}` e o caminho nuclear inexistente retorna `None` em cada cenário.
O perfil de chamadas com `sys.setprofile` confirmou `validar_cenario`,
`buscar_subsistema`, `analisar_energia`, `ajustar_reta`, `prever_energia`,
`decidir`, `formatar_resultado` e `executar_cenario`: os cinco módulos são
usados no fluxo, além do integrador.

O rastreio completo de `deficit` das seções anteriores permanece válido
neste SHA: 40 − 70 = −30; cobertura potencial `min(15, 30)=15`;
remanescente 15; `a=2.5`, `b=0`; eólica futura `2.5 × 11=27.5`;
saldo futuro `20 + 27.5 − 70 = −22.5`; reserva restante hipotética zero.
O cenário crítico mantém falta de 20 kWh para essenciais e intervenção
humana; a igualdade `30 + 5 = 35` da fronteira sinaliza dependência da
reserva. A previsão nunca apaga o alerta atual dos dois cenários de vento.

| Execução adicional | Código e saída observados |
|---|---|
| `--cenario inexistente` | 1; erro de entrada, sem balanço/decisão fictícios |
| `--listar --cenarios <arquivo ausente>` | 1; erro de leitura amigável, sem traceback/stderr |
| `--listar --cenarios <JSON contendo apenas {>` | 1; JSON inválido identificado, sem resultado fictício |
| `--cenario deficit --historico <arquivo ausente>` | 0; saldo −30 e preservação dos essenciais; previsão indisponível com motivo |
| `--cenario deficit --historico <JSON contendo apenas {>` | 0; mesmo resultado atual válido; erro de leitura do histórico exibido |
| Nove pares comando/saída de `docs/exemplos_saida.md` | 9/9 stdout integrais idênticos; oito comandos válidos e um cenário inexistente |

A suíte existente também cobre `bool`, NaN, infinito, negativo, campos/IDs
inválidos, folhas incompatíveis, consumo negativo via JSON/CLI, histórico
degenerado/despareado/incompatível, limites de escala, estimativa negativa
com aviso, prioridade e consulta hierárquica. Nenhuma lacuna funcional nova
foi encontrada; não foram duplicados testes nem alterados módulos/dados.

### Matriz de aceite e revisão verificável

Foram lidas integralmente as issues [#2](https://github.com/bkampdev/FIAP-PBL-FASE-3/issues/2),
[#6](https://github.com/bkampdev/FIAP-PBL-FASE-3/issues/6) e
[#11](https://github.com/bkampdev/FIAP-PBL-FASE-3/issues/11), suas conversas,
descrições, conversas/reviews e threads inline dos PRs #21/#24/#27/#28.
As três issues estavam abertas e sem comentários; nenhum dos quatro PRs
tinha review formal ou thread inline. Ausência de review formal não apaga
registros de conversa, mas também não comprova revisão pessoal de integrante.

| Issue | Critério | Prova nesta candidata | Pendência |
|---|---|---|---|
| #2 | Listas, chave-valor e hierarquia demonstradas | JSON → lista/ID → árvore → integrador; exemplos em `docs/dados.md` | Sem lacuna técnica |
| #2 | Rejeitar malformados preservando déficit válido | Testes `test_dados`, `test_sistema` e CLI inválida; déficit retorna 0 com alerta | Sem lacuna técnica |
| #2 | Solar/eólico e consulta verificáveis | `{}`, `{}` e `None` nos oito cenários; perfil de chamadas | Sem lacuna técnica |
| #2 | Testes válida/inválida/navegação | Suíte completa: 105/105, incluindo `TestDados` | Conferência pessoal do histórico por Gabriel ainda não comprovada; registros técnicos da conta Guilherme não são ampliados para outras pessoas |
| #6 | JSONs independentes da máquina | Clone remoto limpo e execução com caminhos relativos; teste existente fora da raiz | Sem lacuna técnica; Windows atual não verificado |
| #6 | Resultados dos oito casos documentados | Tabelas acima e `docs/cenarios.md`, CLI = integrador | Sem lacuna técnica |
| #6 | Previsão usada no planejamento | Vento baixo/alto: mesmo saldo atual −10; futuros −10/0 | Sem lacuna técnica |
| #6 | Sintéticos e hipóteses identificados | `docs/cenarios.md` explicita dados sintéticos, solar/consumo mantidos e reserva hipotética | Revisões pessoais de Eduardo e Lorenzo ainda não comprovadas |
| #11 | Cópia limpa com commit/resultados | Clone remoto novo, SHA/ambiente/comandos/105 testes acima | Windows atual não verificado; histórico preservado |
| #11 | Cenário rastreado ponta a ponta | `deficit`, funções reais dos cinco módulos, contas/saída/envelope | Sem lacuna técnica |
| #11 | Bloqueadores corrigidos ou explicitados | README atual reproduzido; erros/fallback corretos; timeout Windows explícito | Retestar alterações posteriores no SHA consolidado |
| #11 | Partes do revisor conferidas por outro integrante | Sem registro novo atribuível a Lorenzo | Revisão pessoal de Lorenzo sobre dados/testes de Davi permanece pendente |

| PR | Estado conferido e rastreabilidade | Limite do aceite |
|---|---|---|
| [#21](https://github.com/bkampdev/FIAP-PBL-FASE-3/pull/21) | Integrado em `ac0891105a027274315cfc9e879c7fa434677465`; comentário técnico na conta `bkampdev` pediu documentos e folhas `dict`; correção `8d11aa5` presente | Descrição preserva conferências pessoais pendentes; não fecha #2/#6 |
| [#24](https://github.com/bkampdev/FIAP-PBL-FASE-3/pull/24) | Integrado em `ebab10a20fed613d0afcf71712627b471b53c412`; três testes originais e revisão Windows histórica preservados | Autorização de integração não substitui Lorenzo |
| [#27](https://github.com/bkampdev/FIAP-PBL-FASE-3/pull/27) | Integrado em `6f8435480293b1d38a146e399b4fbb54c2e6d9c3`; correção direta de consumo negativo e 105 testes presentes | Revisão automatizada e merge não suprem revisão pessoal |
| [#28](https://github.com/bkampdev/FIAP-PBL-FASE-3/pull/28) | Aberto, head `1bdde52388ef4e4964b8337323a9af694ff96ea4`; README novo conferido nesta rodada | Integração, revalidação final e aceite documental a cargo do coordenador |

### Acordos entre frentes e encaminhamento

O alinhamento foi enviado aos workers de decisões, energia, apresentação e
entrega pelo Orca. Energia confirmou a separação de saldo/reserva e futuro,
e informou o ajuste textual `6584922edec7cc968bd01f69b7a2ab61750f701c`,
sem mudança de campos/contas; esse commit não integra o SHA testado aqui.
Apresentação foi avisada da igualdade README/CLI, dos valores contratuais
e da ausência de revisão humana nova. Decisões recebeu os resultados dos
oito cenários e dos limites críticos; entrega recebeu as pendências de
revisão e a limitação Windows. O coordenador confirmou que essa limitação
não bloqueia a conclusão desta auditoria técnica macOS.

Encaminhamento: critérios técnicos de dados/cenários/integração atendidos
na candidata indicada; preservar as revisões humanas pendentes antes do
fechamento fundamentado das issues. Mudanças posteriores exigem reteste
no SHA consolidado. Esta rodada modifica somente este registro; não altera
README, relatório/PDF, checklist, autores históricos ou critérios de revisão,
e não publica PR, faz merge, fecha issue ou envia a atividade.
