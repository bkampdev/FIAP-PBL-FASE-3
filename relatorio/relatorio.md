# Sistemas da Colônia Aurora

FIAP PBL Fase 3 | Relatório do programa integrado | 11/11/2026

O programa em Python lê cenários sintéticos, organiza os subsistemas da colônia, compara geração e consumo e indica ações para o intervalo atual. Uma regressão linear estima a energia eólica do próximo intervalo e apoia o planejamento. O núcleo usa a biblioteca padrão; as 105 verificações automatizadas passaram na versão integrada. Os resultados são didáticos e não representam comando físico dos equipamentos.

## 1. Organização dos dados

`dados/cenarios.json` contém oito cenários. Cada cenário é um dicionário com duração do intervalo, geração solar e eólica em kWh, reserva em kWh, vento previsto em m/s, lista de sistemas consumidores e hierarquia. Cada sistema na lista informa ID, nome, consumo em kWh, se é essencial e prioridade. A lista permite percorrer e somar os consumos; as chaves nomeadas deixam explícito o significado de cada valor. A hierarquia de dicionários permite navegar de `colonia` para `energia` e depois `solar` ou `eolico`, ou para os consumidores. Uma folha existente retorna `{}`; um caminho ausente retorna `None`.

`dados/historico_eolico.json` guarda listas pareadas de vento `[8, 10, 12]` m/s e energia `[20, 25, 30]` kWh, todas referentes a intervalos de 1 h. `src/dados.py` valida os campos, os tipos, os valores finitos e a correspondência entre as listas antes da análise. `src/sistema.py` integra dados, energia, previsão, decisões e apresentação; `main.py` permite listar os cenários ou executar um pelo ID.

## 2. Balanço de energia e regras de decisão

O balanço observado é `geracao_solar_kwh + geracao_eolica_kwh - consumo_total_kwh`. No cenário versionado `deficit`, solar de 20 kWh e eólica observada de 20 kWh somam 40 kWh; suporte à vida e laboratório consomem 35 kWh cada, totalizando 70 kWh. O saldo é `40 - 70 = -30 kWh`. A reserva de 15 kWh fica separada do saldo: a cobertura potencial é `min(15, 30) = 15 kWh` e ainda restariam 15 kWh de déficit. Não houve descarga real, e o saldo observado continua -30 kWh.

O suporte à vida é essencial e tem prioridade 1. A decisão verifica primeiro se geração mais reserva atendem seu consumo; caso contrário, emite `alerta_critico` e recomenda intervenção humana. Em déficit não crítico, emite `alerta_deficit`, preserva o essencial e propõe avaliar redução do laboratório, não essencial de prioridade 2. Em equilíbrio, informa ausência de margem; em excedente, sugere avaliar armazenamento ou uso planejado. As regras ordenam os não essenciais por prioridade numérica decrescente e incluem o motivo de cada ação. No cenário `deficit`, 40 + 15 kWh superam os 35 kWh essenciais, portanto o estado é `alerta_deficit`, não `alerta_critico`.

## 3. Regressão e previsão eólica

`src/previsao.py` ajusta por mínimos quadrados a reta `y = a*x + b`, com vento `x` em m/s e energia eólica `y` em kWh por intervalo. Para o histórico citado, as médias são 10 m/s e 25 kWh; a soma dos produtos dos desvios é 20 e a soma dos quadrados dos desvios do vento é 8. Logo, `a = 20/8 = 2,5 kWh/(m/s)` e `b = 25 - 2,5*10 = 0 kWh`. Vento previsto de 11 m/s produz `2,5*11 = 27,5 kWh`. O programa sinaliza extrapolação fora de 8 a 12 m/s e estimativa negativa, que não deve ser tratada como geração disponível.

## 4. Planejamento do próximo intervalo

Para `deficit`, o planejamento mantém a solar de 20 kWh e o consumo de 70 kWh no próximo intervalo de 1 h, substituindo somente a eólica observada pela estimativa de 27,5 kWh. Assim, `20 + 27,5 - 70 = -22,5 kWh`. A reserva restante hipotética, se os 15 kWh fossem usados para cobrir parte do déficit atual, seria zero. A mesma reserva não é somada outra vez ao saldo futuro. A recomendação é planejar redução de cargas não essenciais e preservar o suporte à vida.

Os cenários `vento_baixo` e `vento_alto` isolam o efeito da previsão: ambos têm solar de 20 kWh, eólica observada de 20 kWh, consumo de 50 kWh, reserva zero e saldo atual de -10 kWh. Com vento previsto de 8 m/s, a eólica estimada é 20 kWh e o saldo futuro permanece -10 kWh. Com 12 m/s, a estimativa sobe a 30 kWh e o saldo futuro chega a zero. A previsão altera a recomendação futura, sem apagar o déficit observado.

## 5. Execução, verificação e limites

Na raiz do repositório, `python3 main.py --listar` mostra os oito cenários e `python3 main.py --cenario deficit` reproduz os valores deste relatório. `python3 -B -m unittest discover -s tests -v` executou 105 testes com resultado OK na versão integrada. O README documenta a alternativa de interpretador no Windows, e `docs/exemplos_saida.md` registra as saídas reais da CLI. O gerador deste PDF usa `reportlab` apenas na documentação; o programa principal não depende dele.

Todos os dados são sintéticos. O modelo linear usa três pares e não representa a curva física completa de uma turbina; perdas, incerteza meteorológica, capacidade de armazenamento e eficiência não são modeladas. Alertas e reduções são recomendações: o programa não desliga cargas, não carrega nem descarrega bateria e não garante segurança física. A conferência dos cinco integrantes e o envio no FIAP ON são etapas separadas do funcionamento do programa.

[Repositório público e código-fonte](https://github.com/bkampdev/FIAP-PBL-FASE-3)
