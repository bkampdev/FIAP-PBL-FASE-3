# Contratos de integração da Colônia Aurora

Especificação consolidada na [issue #1](https://github.com/bkampdev/FIAP-PBL-FASE-3/issues/1), sujeita à revisão de Davi e dos responsáveis pelos quatro módulos antes da integração. Consolidação não equivale a aceite dos colegas. Escopo desta issue: somente este documento e `docs/plano-trabalho.md`.

Referências de compatibilidade inspecionadas em 10/11/2026: [PR #16](https://github.com/bkampdev/FIAP-PBL-FASE-3/pull/16), `198da5e25434fffb6ce79c657245bd66f8c1c9df` (`src/previsao.py`), e [PR #17](https://github.com/bkampdev/FIAP-PBL-FASE-3/pull/17), `53a53ede60237f74d8fe9971169941020d0f9af6` (`src/apresentacao.py`). Ambos estão em revisão; os demais módulos abaixo são contratos a implementar nas respectivas issues. Mudanças nesses PRs exigem nova conferência.

## 1. Unidades, tempo e validação comum

- `intervalo_h`: duração estritamente positiva em horas, padrão `1.0`. Carregador e integrador explicitam esse padrão em uma cópia quando ausente; valor informado inválido nunca é substituído. A validação recebe o registro normalizado, sem modificar a entrada original.
- Geração solar/eólica e consumo são energias em `kWh` do intervalo atual; `reserva_kwh` é estoque disponível no início desse intervalo. Vento é velocidade em `m/s`. Não somar `kW`, `kWh` ou `%`; este contrato não recebe potência nem porcentagem de bateria.
- Histórico e previsão referem-se a intervalos da mesma duração do cenário. Não multiplicar energia em `kWh` novamente por `intervalo_h`. Outra duração exige histórico compatível ou transformação explicitamente acordada, nunca conversão implícita.
- Números de entrada: `int` ou `float`, rejeitando `bool`, strings numéricas, `NaN`, infinitos e valores sem representação finita nos cálculos. Energias de entrada e vento são não negativos; duração é positiva. `essencial` exige `bool`; `prioridade` exige inteiro positivo e rejeita `bool`.
- Saldos e coeficientes `a`/`b` podem ser negativos. A estimativa linear também pode ser negativa: preservá-la com aviso e excluí-la do planejamento, conforme seção 4. Não confundir essas saídas com entradas energéticas não negativas.
- Funções matemáticas levantam `ValueError` explicativo para entrada inválida ou escala que impeça resultado finito. Sem fallback para zero ou valor supostamente seguro. Testes numéricos usam tolerância, por exemplo `math.isclose(..., rel_tol=1e-9, abs_tol=1e-9)`; não arredondar cálculos para formatar a tela.
- Funções não alteram dicionários/listas recebidos. Lógica não imprime, lê teclado, aciona equipamentos ou depende do texto apresentado. Déficit (`geração < consumo`) é cenário operacional válido e deve chegar às decisões.

## 2. Esquemas de entrada

### Cenário e sistemas

`dados/cenarios.json` terá uma lista não vazia de cenários, com `id` único. Cada cenário normalizado é um dicionário com todos os campos abaixo:

| Campo | Tipo e significado |
|---|---|
| `id` | `str` não vazia, identificador do cenário |
| `intervalo_h` | Número finito positivo; padrão explícito `1.0` h |
| `geracao_solar_kwh` | Número finito não negativo, energia solar observada no intervalo atual |
| `geracao_eolica_kwh` | Número finito não negativo, energia eólica observada no intervalo atual |
| `reserva_kwh` | Número finito não negativo, estoque disponível separado da geração |
| `vento_previsto_ms` | Número finito não negativo, entrada estimada para o próximo intervalo |
| `sistemas` | Lista não vazia dos consumidores descritos abaixo |
| `hierarquia` | Dicionário em árvore com raiz `colonia`, conforme abaixo |

Cada item de `sistemas` possui `id` e `nome` (`str` não vazia), `consumo_kwh` (número finito não negativo), `essencial` (`bool`) e `prioridade` (inteiro positivo). Os IDs são únicos dentro do cenário. Menor número significa maior prioridade; `suporte_vida` é obrigatório, com `essencial=True` e `prioridade=1`. Outros consumidores também podem ser essenciais e nunca entram na redução. Candidatos não essenciais são ordenados por prioridade decrescente; empates usam o `id` em ordem alfabética. Assim, os mais prioritários são preservados primeiro.

### Hierarquia e navegação

Usar dicionários aninhados: chaves são identificadores dos nós, valores são dicionários com filhos e folha é `{}`. A raiz única `colonia` contém `energia` com `solar` e `eolico`, além de `consumidores` com uma folha para cada `id` de `sistemas`. A árvore referencia os mesmos consumidores, sem duplicar valores para somá-los outra vez. É finita e sem ciclos; JSON não possui referências cíclicas.

```python
cenario = {
    "id": "deficit",
    "intervalo_h": 1.0,
    "geracao_solar_kwh": 20.0,
    "geracao_eolica_kwh": 20.0,
    "reserva_kwh": 15.0,
    "vento_previsto_ms": 11.0,
    "sistemas": [
        {"id": "suporte_vida", "nome": "Suporte à vida", "consumo_kwh": 35.0,
         "essencial": True, "prioridade": 1},
        {"id": "laboratorio", "nome": "Laboratório", "consumo_kwh": 35.0,
         "essencial": False, "prioridade": 2},
    ],
    "hierarquia": {
        "colonia": {
            "energia": {"solar": {}, "eolico": {}},
            "consumidores": {"suporte_vida": {}, "laboratorio": {}},
        }
    },
}
```

`buscar_subsistema(cenario["hierarquia"], ["colonia", "energia", "solar"])` retorna `{}`; a consulta a `eolico` também funciona. Folha `{}` é diferente de `None` (caminho inexistente): testar com `is None`, não apenas pela veracidade do dicionário. #10 efetua essas consultas e #2/#11 as verificam, demonstrando percurso real entre subsistemas.

### Histórico eólico

`dados/historico_eolico.json` terá um dicionário separado, passado como `historico` ao integrador:

```python
historico = {
    "intervalo_h": 1.0,
    "vento_ms": [8.0, 10.0, 12.0],
    "energia_eolica_kwh": [20.0, 25.0, 30.0],
}
```

`intervalo_h` segue o padrão `1.0` quando ausente e deve coincidir com o cenário. `vento_ms` e `energia_eolica_kwh` são listas pareadas por índice, de igual comprimento, com pelo menos dois pares finitos não negativos e duas velocidades distintas. O ajuste também aceita tuplas em chamadas Python, como no PR #16; JSON usa listas. Não reorganizar uma série sem reorganizar a outra. São dados sintéticos de intervalos anteriores, não a geração atual nem uma previsão pronta.

## 3. Interfaces dos seis módulos e da CLI

Onde não há implementação na `main`, as assinaturas descrevem aceite esperado, sem afirmar entrega realizada.

| Arquivo / autoria | Assinatura, entrada e retorno | Erros e responsabilidade |
|---|---|---|
| `src/dados.py` — Davi, #2 | `carregar_cenarios(caminho)` recebe `str` ou `pathlib.Path` de JSON UTF-8 e retorna `list[dict]` de cenários normalizados/validados, com IDs únicos. `validar_cenario(cenario)` retorna `list[str]`: `[]` se válido, mensagens com campo/caminho se inválido. `buscar_subsistema(hierarquia, caminho)` recebe árvore e lista/tupla não vazia de chaves `str`; retorna nó `dict` ou `None` se caminho inexistente. | Carregamento propaga `OSError` para arquivo ausente/inacessível; JSON/esquema inválido gera `ValueError` explicativo. Validador acumula erros inclusive de tipo do próprio registro; déficit não é erro. Consulta malformada gera `ValueError`; caminho válido ausente retorna `None`. Validar campos, IDs, suporte à vida, prioridades e correspondência da hierarquia. |
| `src/energia.py` — Eduardo, #4 | `analisar_energia(cenario)` recebe cenário válido e retorna `balanco` da seção 4. | Validar operandos matemáticos; rejeitar `bool`, negativos indevidos e resultado não finito com `ValueError`. Não escolher cargas nem modificar reserva. |
| `src/previsao.py` — Gabriel, #5 / PR #16 | `ajustar_reta(x, y)` recebe listas/tuplas pareadas e retorna `modelo`. `prever_energia(modelo, vento)` recebe modelo produzido pelo ajuste e vento finito não negativo, retornando `previsao` da seção 4. | `ValueError` para histórico inválido/degenerado, vento inválido ou cálculo não finito. O PR #16 pressupõe modelo válido: não promete validar dicionário arbitrário de coeficientes. #10 usa diretamente o retorno de `ajustar_reta`, sem aceitar modelo externo nem mascarar `KeyError`/bugs como déficit. |
| `src/decisoes.py` — Lorenzo, #3 | `decidir(cenario, balanco, previsao)` recebe cenário/balanço validados e previsão retornada pelo módulo ou `None`; retorna `decisao` da seção 4. | Checar coerência das entradas; violações do contrato geram `ValueError` antes das ações. Previsão negativa é saída conhecida com aviso: manter decisão atual, indisponibilizar planejamento futuro e explicar o motivo. Sem `print` nem mutação. |
| `src/apresentacao.py` — Gabriel, #9 / PR #17 | `formatar_resultado(resultado)` recebe envelope da seção 4 e retorna `str`. Se `erro` contiver texto, aceita inclusive apenas `{"erro": mensagem}`. | Exibir erro sem simular sucesso; com previsão `None`, exibir `erro_previsao` ou “modelo indisponível”. Não validar/recalcular regras. Envelope incompleto sem `erro` viola pré-condição e pode gerar `KeyError`; #10 garante o envelope. Não exigir exibição de campos que o PR ainda não lê, como cobertura detalhada da reserva. |
| `src/sistema.py` — Guilherme, #10 | `executar_cenario(cenario, historico)` retorna sempre o envelope completo da seção 4, sem imprimir. Normaliza cópia do intervalo; valida cenário, consulta hierarquia, calcula balanço, ajusta/estima e decide. | Cenário/cálculo atual inválido: `erro` explicativo, sem decisão. Histórico inválido, duração incompatível ou falha numérica da regressão: `erro_previsao`, previsão `None`, decisão apenas atual. Não capturar indiscriminadamente `Exception` para esconder defeitos de programação. |
| `main.py` — Guilherme, #10 | `main(argv=None)` recebe argumentos e retorna código inteiro; lista/seleciona cenário, lê o JSON histórico com `json`, chama integrador e imprime `formatar_resultado`. Comandos-alvo: `python3 main.py --listar` e `python3 main.py --cenario deficit`. | Tratar arquivo/cenário inexistente e JSON inválido com mensagem amigável. Falha de cenário/carregamento: saída não zero; déficit válido: saída zero com alerta. Histórico indisponível permite resultado atual com aviso. Guarda `if __name__ == "__main__"`, sem executar ao importar. Comandos são aceite de #10, ainda indisponíveis na `main` inicial. |

Antes de `decidir`, #10 verifica e registra erros: cenário inválido impede toda decisão; histórico inválido impede só recomendação preditiva, passando `None`, nunca dados malformados, ao decisor. Erro ao ler cenários interrompe o fluxo; erro ao ler histórico é comunicado como indisponibilidade de previsão, mantendo apenas cálculos atuais válidos.

## 4. Retornos exatos e interpretação

### Balanço observado

`analisar_energia` retorna todas estas chaves numéricas, mais a classificação:

| Chave | Definição |
|---|---|
| `geracao_total_kwh` | `geracao_solar_kwh + geracao_eolica_kwh`, observadas |
| `consumo_total_kwh` | Soma de `consumo_kwh` de todos os sistemas, uma única vez |
| `consumo_essencial_kwh` | Soma de `consumo_kwh` dos sistemas com `essencial=True` |
| `saldo_kwh` | `geracao_total_kwh - consumo_total_kwh`, sem reserva |
| `classificacao` | `"deficit"` se saldo < 0; `"equilibrio"` se saldo == 0; `"excedente"` se saldo > 0 |
| `reserva_usada_kwh` | `min(reserva_kwh, max(0, -saldo_kwh))`: cobertura **potencial informativa**, apesar do nome mantido para integração |
| `deficit_remanescente_kwh` | `max(0, -saldo_kwh) - reserva_usada_kwh` |

A reserva disponível continua em `cenario["reserva_kwh"]`, como lida pelo PR #17. Cobertura não muda saldo/classificação e não significa descarga executada. Excedente é energia potencialmente disponível; sem capacidade de bateria, eficiência de carga ou atualização física, não afirmar armazenamento realizado.

### Modelo e previsão

`modelo` contém exatamente `a`, `b`, `vento_min_ms`, `vento_max_ms`, números finitos; `a` tem unidade `kWh/(m/s)` e `b`, `kWh`. Mínimos quadrados: `a = soma((x-media_x)*(y-media_y)) / soma((x-media_x)**2)` e `b = media_y - a*media_x`.

`previsao` contém as quatro chaves do modelo e `vento_previsto_ms`, `energia_eolica_prevista_kwh` (`a * vento + b`), `extrapolacao` (`bool`) e `aviso` (`str` ou `None`): oito chaves, sem renomear. Limites históricos são inclusivos; fora deles, `extrapolacao=True` com aviso. Extrapolação não negativa pode orientar sugestão didática com ressalva, sem garantia física.

Compatibilidade com PR #16: estimativa negativa permanece no retorno com `aviso` de invalidade física, inclusive quando também extrapolada. Não truncar para zero, não somar geração negativa ao planejamento nem inventar energia segura. `previsao` permanece no envelope para o PR #17 exibir número/aviso; `decidir` retorna `recomendacao_futura=None` e ação/motivo explicando a indisponibilidade. `erro_previsao` é reservado à ausência do modelo/previsão; não substitui `aviso`.

### Decisão atual e próximo intervalo

Retorno exato: `decisao` tem `status` (`str`), `acoes` (`list[dict]`) e `recomendacao_futura` (`str` ou `None`). Cada ação é `{"acao": str, "motivo": str}` com textos não vazios, nunca lista de strings/tuplas. O PR #17 imprime status/classificação como textos, sem depender de enumeração; novos produtores usam os status abaixo. Textos com acentos/espaços dos testes provisórios do PR #17 continuam aceitos pelo formatador.

| Condição atual, em ordem de precedência | `status` | Ação e motivo |
|---|---|---|
| Geração + reserva disponível < consumo essencial | `"alerta_critico"` | Informar insuficiência mesmo com cobertura hipotética; preservar essenciais e recomendar intervenção humana, sem prometer segurança |
| Saldo < 0, sem condição crítica acima | `"alerta_deficit"` | Informar déficit bruto e cobertura potencial/remanescente; propor redução de não essenciais na ordem combinada, sem declarar desligamento executado |
| Saldo == 0 | `"equilibrio"` | Informar equilíbrio sem margem de geração |
| Saldo > 0 | `"excedente"` | Informar excedente e sugerir avaliar armazenamento/uso planejado, sem afirmar carga realizada |

Quando geração < consumo essencial, explicitar dependência da reserva mesmo se ela puder cobrir a diferença. Disponibilidade hipotética não autoriza declarar suporte à vida seguro. Reduções recomendadas e cobertura potencial não apagam déficit observado.

Para o próximo intervalo, declarar as hipóteses de mesma geração solar observada e mesmos consumos planejados. Substituir apenas a eólica: `saldo_futuro = geracao_solar_kwh + energia_eolica_prevista_kwh - consumo_total_kwh`. Não somar eólica observada e prevista. Registrar no texto o saldo estimado, as hipóteses e avisos.

Se considerar reserva no futuro, usar apenas `reserva_restante_hipotetica = reserva_kwh - balanco["reserva_usada_kwh"]`. É hipótese conservadora de continuidade, não mutação de estoque nem geração. Não reaplicar toda a reserva original ao futuro. Não combinar redução hipotética de consumo e cobertura integral de reserva como resultados já realizados. Sem previsão válida para planejamento, `recomendacao_futura=None` e motivo explícito; ações atuais permanecem disponíveis.

### Envelope do integrador

`resultado` contém exatamente seis chaves: `erro`, `cenario`, `balanco`, `previsao`, `erro_previsao`, `decisao`.

| Situação | `erro` | `cenario` / `balanco` / `decisao` | `previsao` / `erro_previsao` |
|---|---|---|---|
| Cenário e previsão válidos | `None` | Cenário normalizado e retornos completos | Previsão / `None` |
| Atual válido; histórico inválido/ausente ou regressão impossível | `None` | Valores atuais preservados; decisão sem recomendação preditiva | `None` / mensagem explicativa |
| Previsão calculada negativa | `None` | Decisão atual e motivo de planejamento indisponível | Previsão negativa com `aviso` / `None` |
| Cenário/carregamento/cálculo atual inválido | Mensagem não vazia | `None` / `None` / `None` | `None` / `None` |

A CLI pode montar o envelope de erro para falhas anteriores ao integrador. O formatador aceita envelope completo e caso mínimo `{"erro": mensagem}` já testado no PR #17. Resultado atual válido nunca contém simultaneamente `previsao=None` e `erro_previsao=None`.

Exemplo completo para `cenario` e `historico` da seção 2. Balanço/decisão são referências sintéticas de aceite, não execução de módulos ainda ausentes:

```python
resultado = {
    "erro": None,
    "cenario": cenario,
    "balanco": {
        "geracao_total_kwh": 40.0,
        "consumo_total_kwh": 70.0,
        "consumo_essencial_kwh": 35.0,
        "saldo_kwh": -30.0,
        "classificacao": "deficit",
        "reserva_usada_kwh": 15.0,
        "deficit_remanescente_kwh": 15.0,
    },
    "previsao": {
        "a": 2.5,
        "b": 0.0,
        "vento_min_ms": 8.0,
        "vento_max_ms": 12.0,
        "vento_previsto_ms": 11.0,
        "energia_eolica_prevista_kwh": 27.5,
        "extrapolacao": False,
        "aviso": None,
    },
    "erro_previsao": None,
    "decisao": {
        "status": "alerta_deficit",
        "acoes": [
            {"acao": "Preservar Suporte à vida", "motivo": "Consumidor essencial prioritário"},
            {"acao": "Avaliar redução do Laboratório",
             "motivo": "Déficit de 30 kWh; reserva cobriria 15 kWh e restariam 15 kWh"},
        ],
        "recomendacao_futura": (
            "Com solar mantida em 20 kWh e consumo planejado em 70 kWh, "
            "a eólica estimada de 27,5 kWh leva a saldo futuro de -22,5 kWh. "
            "Reserva restante hipotética: 0 kWh. Planejar redução de não essenciais."
        ),
    },
}
```

## 5. Aceites verificáveis

| Entrada / situação | Resultado esperado e responsável pela evidência |
|---|---|
| Geração 40 / consumo 70 kWh; essencial 35; reserva 15 | Saldo `-30`, `deficit`, cobertura potencial `15`, remanescente `15`; futuro `-22.5` com solar 20 e eólica prevista 27.5, sem reutilizar reserva. #4/#8/#10 |
| Geração 80 / consumo 30 kWh | Saldo `+50`, `excedente`, cobertura `0`, sugestão sem armazenamento fictício. #4/#8 |
| Geração 50 / consumo 50 kWh | Saldo `0`, `equilibrio`, cobertura `0`. #4/#8 |
| Vento `[8, 10, 12]`, energia `[20, 25, 30]`, consulta 11 | `a=2.5`, `b=0`, estimativa `27.5 kWh`, sem extrapolação. #5/#8 |
| Mesmo histórico, consulta 13 | `32.5 kWh`, `extrapolacao=True`, aviso. #5/#9 |
| Vento `[2, 4]`, energia `[1, 3]`, consulta 0 | `-1 kWh` preservado, extrapolação/aviso de invalidade; planejamento indisponível sem substituir por zero. #5/#3/#10 |
| Solar 20, consumo planejado 50, reserva zero; vento de 8 para 12 no histórico de referência | Futuro passa de `-10` a `0 kWh`; recomendação muda, balanço atual não muda. #3/#6/#10 |
| Geração 10, consumo essencial 35, reserva 5 | Insuficiência essencial potencial de 20 kWh, `alerta_critico`, nenhum essencial candidato a desligamento. #3/#7 |
| Geração/consumo/reserva zero, mantendo suporte à vida no cadastro | Entrada válida, saldo `0`, sem divisão por consumo zero. #2/#4 |
| Campo ausente obrigatório, `True` como energia, `NaN`, infinito, negativo indevido, IDs duplicados ou suporte à vida não essencial | Erro de entrada antes de decidir; déficit legítimo não integra esta lista. #2/#10 |
| Histórico vazio, comprimentos diferentes, vento constante ou duração incompatível | Previsão indisponível com motivo; dados atuais válidos permanecem, sem recomendação preditiva. #5/#10 |
| Consultas às folhas solar/eólico e caminho inexistente | `{}`, `{}` e `None`, respectivamente; percurso demonstrado na integração. #2/#10/#11 |

## 6. Limites didáticos e aceite humano

Python básico com biblioteca padrão no núcleo: listas, dicionários, funções, condições e somatórios. Banco, API, interface web, modelos avançados e bibliotecas de aprendizado de máquina não são obrigatórios. A reta aproxima localmente dados sintéticos, não a curva física completa de uma turbina.

As regras produzem alertas e recomendações. Não há controle físico, armazenamento real, economia medida ou segurança absoluta demonstrados. Capacidade, perdas, eficiência, incerteza meteorológica e continuidade de estoque reais não foram modeladas. #3/#4/#5/#10 preservam essas limitações; #14 as explicita no README/PDF.

A confirmação de campos/hipóteses fica no PR de #1: @daviconinck e autores @Rocha0306, @BackesEdu, @ItsTheContext. Revisão solicitada não equivale a aprovação. Fechar #1 somente após revisão dos colegas e integração, conforme `CONTRIBUTING.md`.
