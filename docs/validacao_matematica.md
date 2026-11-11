# Validação Matemática e Modelo Preditivo - Colônia Inteligente

## 1. Modelo de Regressão Linear Simples
Para estimar a geração de energia eólica a partir da velocidade do vento, utilizamos o método dos mínimos quadrados ordinários (MQO) ajustando uma reta no formato:
$$y = ax + b$$

Onde:
- $x$: Velocidade histórica do vento (ex: $[8, 10, 12]$)
- $y$: Energia gerada correspondente (ex: $[20, 25, 30]$)
- $a$: Inclinação (coeficiente angular)
- $b$: Intersecção (coeficiente linear)

### Exemplo de Cálculo Manual
- Dados de Entrada: $X = [8, 10, 12]$, $Y = [20, 25, 30]$
- Médias: $\bar{x} = 10$, $\bar{y} = 25$
- Cálculo de $a$:
  $$a = \frac{(8-10)(20-25) + (10-10)(25-25) + (12-10)(30-25)}{(8-10)^2 + (10-10)^2 + (12-10)^2} = \frac{10 + 0 + 10}{4 + 0 + 4} = \frac{20}{8} = 2.5$$
- Cálculo de $b$:
  $$b = \bar{y} - a\bar{x} = 25 - (2.5 \times 10) = 0$$
- Equação Ajustada: $y = 2.5x$

### Previsão para Nova Entrada
- Entrada ($x$): $11$
- Saída Prevista ($y$): $2.5 \times 11 = 27.5$

---

## 2. Balanço Energético e Unidades
- **Definição de Unidades:** Geração e consumo são energias em **kWh** do mesmo intervalo; reserva é estoque em **kWh**, e vento, **m/s**. `intervalo_h` é positivo, com padrão didático de **1 h** quando ausente. Não se aceita potência em kW nesta API nem se multiplica novamente energia pela duração. Histórico e cenário precisam usar intervalos de igual duração.
- **Tratamento de Reservas:** A reserva de energia (baterias/armazenamento) atua exclusivamente como cobertura de déficit a posteriori, não sendo contabilizada como fonte ativa de geração primária para evitar duplicidade de contabilidade.

## 3. Conferência com a implementação

Os dados são sintéticos, em intervalos comuns de 1 h, com vento em m/s e energia em kWh. Para 11 m/s, `src/previsao.py` retorna `a=2.5`, `b=0`, previsão `27.5` e `extrapolacao=False`; para 13 m/s retorna `32.5`, `extrapolacao=True` e aviso. Histórico constante impede ajuste com `ValueError`. O histórico pequeno e a aproximação linear não garantem geração física; estimativa negativa é preservada com aviso e não deve orientar planejamento como energia disponível.

A integração testada usa solar 20, eólica observada 20, consumo 70 (35 essenciais) e reserva 15 kWh: saldo observado `-30`, cobertura potencial `15`, déficit remanescente `15`. Para o próximo intervalo, com solar e consumo mantidos como hipóteses e eólica estimada de 27,5, o saldo é `20 + 27.5 - 70 = -22.5 kWh`. A reserva restante hipotética é zero; portanto o déficit futuro permanece 22,5 kWh. O teste não reaplica a reserva original nem altera o cenário observado.

Comando: `python3 -m unittest discover -s tests -v`. Os testes comparam os retornos efetivos dos módulos a valores manuais independentes, usando tolerância numérica. Cobrem também zeros, equilíbrio, excedente, reserva zero/insuficiente/suficiente, entradas inválidas e somas não finitas. A seção para consolidação no relatório está em `docs/secoes/previsao_energia.md`.
