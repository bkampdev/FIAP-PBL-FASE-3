# Previsão de geração eólica

O módulo ajusta uma reta por mínimos quadrados ao histórico pareado. Cada par tem uma velocidade média do vento em m/s e a energia eólica gerada em kWh em um intervalo da mesma duração. Os exemplos usam dados sintéticos e intervalos de 1 h.

## Ajuste e conferência manual

Na reta `y = a*x + b`, `x` é a velocidade e `y` é a energia. A inclinação `a` é a soma dos produtos dos desvios em relação às médias dividida pela soma dos quadrados dos desvios de `x`. O intercepto `b` é a média de `y` menos `a` vezes a média de `x`.

Com vento `[8, 10, 12]` e energia `[20, 25, 30]`, as médias são 10 m/s e 25 kWh. Os desvios do vento são `[-2, 0, 2]` e os de energia, `[-5, 0, 5]`. A soma dos produtos é 20 e a soma dos quadrados dos desvios do vento é 8. Assim, `a = 20/8 = 2,5`, `b = 25 - 2,5*10 = 0` e, para 11 m/s, `y = 27,5 kWh`.

## Interface

```python
from src.previsao import ajustar_reta, prever_energia

modelo = ajustar_reta([8, 10, 12], [20, 25, 30])
previsao = prever_energia(modelo, 11)
assert previsao["energia_eolica_prevista_kwh"] == 27.5
```

- `ajustar_reta(x, y)` retorna `a`, `b`, `vento_min_ms` e `vento_max_ms`. As sequências precisam ter o mesmo tamanho e pelo menos dois pares, com pelo menos duas velocidades distintas.
- `prever_energia(modelo, vento)` recebe o modelo ajustado e retorna seus campos mais `vento_previsto_ms`, `energia_eolica_prevista_kwh`, `extrapolacao` e `aviso`. Os limites da faixa histórica são inclusivos. Neste exemplo, a faixa é de 8 a 12 m/s.
- Velocidade e energia de entrada precisam ser números finitos e não negativos. Um histórico degenerado ou um vento inválido gera `ValueError`.
- Uma previsão fora da faixa histórica recebe aviso de extrapolação. Se a reta produzir energia negativa, o resultado bruto é preservado com um aviso explícito de que é fisicamente inválido. O integrador deve tratar esse caso como previsão indisponível para o planejamento.

## Uso no próximo intervalo

Como exemplo didático, suponha solar de 20 kWh e consumo planejado de 45 kWh, mantidos nas duas consultas, com reserva desconsiderada. Com vento previsto de 8 m/s, a geração total estimada é 40 kWh e faltam 5 kWh, o que justifica preparar redução de cargas não essenciais. Com 12 m/s, a geração total estimada é 50 kWh e sobram 5 kWh, dispensando a redução por déficit previsto. As contas futuras são ilustrativas até a integração com o módulo de decisões.

A reta é uma aproximação local de um histórico pequeno. Ela não representa a curva de potência de uma turbina nem considera corte operacional, saturação ou incerteza do vento. Use a mesma duração de intervalo no histórico e na previsão.
