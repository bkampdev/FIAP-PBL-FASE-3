# Revisão final do sistema integrado — Issue #11

Responsável: Davi (@daviconinck)

Data: 11/11/2026

O registro original e a autorização do PR #24 estão preservados abaixo.
A revalidação da candidata `47e29ef` está na última seção e não substitui
a revisão pessoal pendente de Lorenzo.

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
