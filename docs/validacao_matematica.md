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
- Saída Prevista ($y$): $2.5 \times 11 = 27.5 \approx 27$

---

## 2. Balanço Energético e Unidades
- **Definição de Unidades:** O sistema opera com consistência dimensional em **kW** (potência instantânea) ou **kWh** (energia acumulada no intervalo). Não se deve misturar as unidades nas somas.
- **Tratamento de Reservas:** A reserva de energia (baterias/armazenamento) atua exclusivamente como cobertura de déficit a posteriori, não sendo contabilizada como fonte ativa de geração primária para evitar duplicidade de contabilidade.