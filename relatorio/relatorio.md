# Sistemas da Colônia Aurora

FIAP PBL Fase 3 | Relatório preliminar

O projeto propõe um programa Python para organizar os subsistemas da colônia, analisar a disponibilidade de energia e apoiar decisões em dois momentos. A regressão e a formatação da saída já têm testes isolados. O fluxo integrado e a revisão cruzada estão pendentes.

## 1. Organização dos dados

O cenário reúne geração solar e eólica, reserva, consumo dos sistemas e vento previsto. Dicionários permitem acessar campos como `reserva_kwh` pelo nome. A lista de sistemas registra o consumo, a prioridade e o caráter essencial de cada carga. A hierarquia permite percorrer colônia, energia e, por fim, solar ou eólico. O histórico usa listas pareadas de vento e energia em intervalos de mesma duração.

## 2. Balanço e decisões

O saldo é a geração solar mais a eólica observadas, menos o consumo do mesmo intervalo. Se a geração for 40 kWh e o consumo for 70 kWh, faltam 30 kWh. A reserva é um estoque à parte. Se houver 10 kWh disponíveis, a cobertura potencial deixa 20 kWh de déficit. Com geração e consumo iguais, há equilíbrio. Se a geração exceder o consumo, o saldo indica quanto poderia ser direcionado ao armazenamento.

No déficit, as regras propostas preservam o suporte à vida e avaliam reduzir cargas não essenciais por ordem de prioridade. Se a energia disponível não atender às cargas essenciais, o sistema deve emitir um alerta crítico. A apresentação exibe o estado, as ações e os respectivos motivos.

## 3. Previsão eólica

O modelo ajusta a reta `y = a*x + b` por mínimos quadrados. A variável x é o vento em m/s e y é a geração eólica em kWh no intervalo. Para o histórico sintético de 1 h com ventos de 8, 10 e 12 m/s e gerações de 20, 25 e 30 kWh, a soma dos produtos dos desvios é 20 e a soma dos quadrados dos desvios de vento é 8. Assim, a = 2,5 e b = 0. A consulta de 11 m/s retorna 27,5 kWh em teste.

A faixa histórica vai de 8 a 12 m/s nesse exemplo. O modelo avisa quando extrapola ou gera uma estimativa negativa. A reta aproxima apenas a relação local observada em dados sintéticos.

## 4. Planejamento do próximo intervalo

Mantendo a geração solar em 20 kWh e o consumo planejado em 45 kWh, a estimativa eólica de 20 kWh a 8 m/s deixaria um déficit de 5 kWh. A estimativa de 30 kWh a 12 m/s indicaria excedente de 5 kWh. Essa comparação ilustra quando preparar a redução de cargas não essenciais. As duas contas desconsideram a reserva e serão conferidas no programa integrado. As ações são recomendações didáticas, sem medição de economia ou controle de equipamentos.

[Repositório público no GitHub](https://github.com/bkampdev/FIAP-PBL-FASE-3)
