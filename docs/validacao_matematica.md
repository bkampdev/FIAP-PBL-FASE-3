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

## 4. Conferência da candidata final em 11/11/2026

Base examinada: `1bdde52388ef4e4964b8337323a9af694ff96ea4`, head da [PR #28](https://github.com/bkampdev/FIAP-PBL-FASE-3/pull/28), sobre o merge da [PR #27](https://github.com/bkampdev/FIAP-PBL-FASE-3/pull/27), `6f8435480293b1d38a146e399b4fbb54c2e6d9c3`. A conferência técnica abaixo não constitui revisão pessoal dos integrantes indicados nas issues.

### Método independente e resultados

Além dos testes existentes, a regressão foi refeita com aritmética racional (`fractions.Fraction`) e a fórmula por somatórios brutos, diferente do cálculo por desvios empregado no módulo:

`a = (n*Σxy - Σx*Σy) / (n*Σx² - (Σx)²)`; `b = (Σy - a*Σx)/n`.

Para os três pares versionados, `n=3`, `Σx=30`, `Σy=75`, `Σxy=770` e `Σx²=308`: `a=(2310-2250)/(924-900)=60/24=5/2`, `b=0`. As consultas 11 e 13 resultam, respectivamente, em `55/2=27,5` e `65/2=32,5 kWh`. Somente a segunda extrapola. Como conferência adicional não colinear, os pares `(1,3)`, `(2,4)`, `(4,8)` dão `a=12/7`, `b=1` e previsão `43/7` para vento 3; os resultados do módulo concordam com tolerância numérica.

O balanço numérico foi confrontado com aritmética racional em todas as 256 combinações de solar, eólica, consumo e reserva escolhidos em `{0, 5, 30, 70}` kWh. Em cada caso foram verificados `saldo = solar + eólica - consumo`, `cobertura = min(reserva, max(0, -saldo))` e `saldo_restante = saldo + cobertura`. Nenhuma divergência foi encontrada.

Os oito cenários reais também foram recalculados independentemente e comparados ao integrador, sem mutação das entradas. Valores em kWh:

| Cenário | Geração | Consumo | Saldo atual | Cobertura potencial | Déficit remanescente | Saldo futuro |
|---|---:|---:|---:|---:|---:|---:|
| `nominal` | 60 | 50 | 10 | 0 | 0 | 10 |
| `deficit` | 40 | 70 | -30 | 15 | 15 | -22,5 |
| `excedente` | 80 | 30 | 50 | 0 | 0 | 50 |
| `equilibrio` | 50 | 50 | 0 | 0 | 0 | 0 |
| `alerta_critico` | 10 | 50 | -40 | 5 | 35 | -25 |
| `fronteira_essencial` | 30 | 50 | -20 | 5 | 15 | -5 |
| `vento_baixo` | 40 | 50 | -10 | 0 | 10 | -10 |
| `vento_alto` | 40 | 50 | -10 | 0 | 10 | 0 |

Os saldos futuros usam as hipóteses de solar e consumo mantidos e substituem somente a eólica pela previsão. A reserva não integra esses saldos. Nos cenários `deficit`, `alerta_critico` e `fronteira_essencial`, a cobertura atual hipotética esgotaria a reserva. No cenário crítico, geração 10 mais reserva 5 fica 20 kWh abaixo do consumo essencial 35. Na fronteira, geração 30 mais reserva 5 iguala 35: há dependência da reserva e déficit total, mas a regra atual não é crítica. Os estados reais coincidem com essas contas.

### Correspondência documental e reprodução

`README.md` e `relatorio/relatorio.md` da candidata usam os mesmos valores de déficit, reserva e previsão; a saída de déficit no README foi comparada integralmente com a CLI. O texto das duas páginas do PDF da base foi extraído com PDFKit e contém as mesmas contas, inclusive -30, 15, 27,5 e -22,5 kWh. O comparativo de ventos do relatório usa consumo de 50 kWh e saldo futuro -10/0, agora também descrito em `docs/previsao.md`. A mensagem da API numérica para reserva suficiente foi ajustada para indicar possibilidade de cobertura, sem afirmar descarga executada; seus campos, status e cálculos foram preservados.

- `python3 -B -m unittest discover -s tests -v`: 105 testes, OK.
- `python3 -B main.py --cenario deficit`: saldo -30, cobertura potencial 15 e futuro -22,5 kWh.
- `python3 -B main.py --cenario vento_baixo` e `python3 -B main.py --cenario vento_alto`: saldo atual -10 nos dois casos e futuro -10/0 kWh.

### Aceites técnicos e revisões documentadas

| Issue | Evidência técnica | Registro de revisão e pendência |
|---|---|---|
| [#4](https://github.com/bkampdev/FIAP-PBL-FASE-3/issues/4) | Totais, três classificações, zeros, cobertura separada, unidades e duração conferidos | A [PR #20](https://github.com/bkampdev/FIAP-PBL-FASE-3/pull/20#issuecomment-6783579487) registra correções e validação na conta `bkampdev`; não há registro pessoal de Lorenzo ou Gabriel nessa issue ou nas PRs examinadas. |
| [#5](https://github.com/bkampdev/FIAP-PBL-FASE-3/issues/5) | Ajuste, 27,5 kWh, casos degenerados, extrapolação e limites conferidos | Já fechada e integrada pela [PR #16](https://github.com/bkampdev/FIAP-PBL-FASE-3/pull/16), de Gabriel; o comentário de fechamento é de `bkampdev`. Autoria não comprova revisão cruzada de Eduardo/Davi. |
| [#8](https://github.com/bkampdev/FIAP-PBL-FASE-3/issues/8) | Conta independente, previsão com balanço, reserva sem repetição e limites conferidos | A [PR #25](https://github.com/bkampdev/FIAP-PBL-FASE-3/pull/25) registra a conferência na conta `bkampdev` e afirma expressamente que ela não é revisão pessoal de Gabriel. |
| [#13](https://github.com/bkampdev/FIAP-PBL-FASE-3/issues/13) | Seção Markdown coerente com implementação, unidades e planejamento futuro | Revisão técnica registrada nas PRs #20/#25/#27; não foi encontrada revisão pessoal de Gabriel/Lorenzo. |

Consulta às APIs de reviews e threads das PRs #16/#20/#25/#27/#28: listas vazias nesta conferência. Os resumos automáticos existentes não contam como revisão humana. A PR #28 ainda declara pendentes as revisões de Eduardo e Lorenzo da #14. Este registro preserva a autoria original de Gabriel na previsão e de Eduardo na energia; não fecha issues, não registra aprovação pessoal dos colegas e não comprova envio no FIAP ON.
