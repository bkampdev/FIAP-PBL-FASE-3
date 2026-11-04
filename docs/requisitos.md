# Requisitos conferidos

Fonte principal: [atividade FIAP ON 616829](https://on.fiap.com.br/mod/assign/view.php?id=616829), lida em 04/11/2026, e orientações RTF fornecidas localmente. Resumo autoral para organizar a execução; não reproduz os capítulos didáticos.

## Comportamentos obrigatórios

1. Organizar energia, consumo e clima em listas/chave-valor e representar hierarquia de sistemas, com navegação entre subsistemas.
2. Tomar decisões com regras simples/condições combinadas, prioridade para suporte à vida e saída objetiva.
3. Ajustar uma relação linear simples a um histórico e estimar novo valor; exemplo: vento → energia eólica.
4. Comparar geração, consumo e eventual reserva, produzindo alertas e sugestões para déficit e excedente.

## Entregáveis

- Repositório GitHub público com um único sistema Python funcional, organizado em funções e com separação entre dados, lógica e decisões.
- README com explicação simples e exemplo de entrada e saída.
- PDF explicando dados, regras, previsão e uso de energia, com link público do GitHub.
- Não há limite de páginas informado no enunciado atual. Biblioteca avançada não é necessária; usar conceitos dos capítulos, com foco em lógica e interpretação.

## Avaliação

| Critério | Peso |
|---|---|
| Estruturação de dados | 2 |
| Lógica de decisão | 2 |
| Modelagem e previsão | 2 |
| Implementação em Python | 2 |
| Documentação e organização | 2 |

## Prazo e pendências

Prazo oficial: 11/11/2026 às 23h59, America/Sao_Paulo. Na consulta de 04/11: entrega pendente; Grupo 20 com apenas Guilherme visível. Confirmar composição e anexos aceitos antes do envio (#15).

## Esclarecimentos da aula de dúvidas

A transcrição local da reunião de 28/10/2026 diferencia Fase 3, Global Solution e Challenge. Trechos 00:12:46–00:12:59 e 00:19:06 confirmam Fase 3 até 11/11; 00:22:28–00:22:59 reforça antecipação e entrega reduzida. Não misturar requisitos/prazos das três atividades. A transcrição é apoio e pode conter erros de reconhecimento; o portal atual prevalece.

## Cuidados de interpretação

Os números do enunciado são exemplos didáticos; não são limites físicos certificados. Nos pares vento [8,10,12]/energia [20,25,30], a reta dá 27,5 para vento 11, embora o texto ilustre aproximadamente 27. Documentar o cálculo sem forçar o arredondamento.

O sistema deve demonstrar previsão e interpretação, sem exigir uma API, banco, interface gráfica ou simulador físico. A ligação da previsão a uma recomendação do próximo intervalo é a opção de integração proposta pelo grupo.
