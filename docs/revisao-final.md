
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

## Pendências

- Solicitar a Lorenzo revisão independente dos arquivos
  de dados e testes produzidos por Davi.
- Encaminhar a Guilherme a conclusão da revisão.
- Confirmar aprovação do Pull Request antes de integrar à main.

## Conclusão

A execução em cópia limpa foi bem-sucedida no commit
9d0b0d8, com 97 testes aprovados.

Posteriormente, na branch de desenvolvimento, foram
executados 100 testes após a inclusão dos três testes
complementares, conforme resultado informado pelo responsável.

Nenhum bloqueador funcional foi identificado nas execuções
registradas. A aprovação independente dos colegas permanece
pendente.
