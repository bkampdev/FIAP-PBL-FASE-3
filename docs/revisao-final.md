# Revisão final do sistema integrado — Issue #11

Responsável: Davi (@daviconinck)

Data: 11/11/2026

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
