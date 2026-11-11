# Dados, validação e hierarquia — Issue #2

Responsável pelo módulo: Davi (@daviconinck).

O módulo `src/dados.py` usa a biblioteca padrão para carregar JSONs UTF-8,
validar registros e consultar a árvore de subsistemas. Os arquivos em `dados/`
são sintéticos. Energia e consumo estão em kWh por intervalo, vento em m/s e
duração em horas. O [contrato de integração](contratos.md) define os campos.

## Carregamento, listas e acesso por chave

Execute os exemplos Python a partir da raiz do projeto:

```python
from pathlib import Path
from src.dados import carregar_cenarios, carregar_historico

cenarios = carregar_cenarios(Path("dados/cenarios.json"))  # list[dict]
historico = carregar_historico("dados/historico_eolico.json")  # dict

print(len(cenarios))  # 8
print(cenarios[0]["id"])  # nominal: índice da lista e chave do dicionário
por_id = {cenario["id"]: cenario for cenario in cenarios}
deficit = por_id["deficit"]
print(deficit["geracao_solar_kwh"])  # 20.0
print([sistema["id"] for sistema in deficit["sistemas"]])
# ['suporte_vida', 'laboratorio']
print(historico["vento_ms"])  # [8.0, 10.0, 12.0]
print(historico["energia_eolica_kwh"])  # [20.0, 25.0, 30.0]
```

Os carregadores aceitam `str` ou `pathlib.Path`. `carregar_cenarios` exige
lista não vazia com IDs únicos; `carregar_historico` exige um dicionário.
Ambos retornam registros validados e explicitam `intervalo_h=1.0` em uma
cópia quando o campo está ausente. Um intervalo informado inválido não é
substituído. Erros de JSON ou esquema geram `ValueError` explicativo;
arquivo inexistente ou inacessível propaga `OSError` (incluindo
`FileNotFoundError`).

## Regras de validação

`validar_cenario` e `validar_historico` recebem registros já normalizados,
retornam uma lista de mensagens (`[]` significa válido) e não alteram a
entrada. Em chamada direta, `intervalo_h` é obrigatório; somente os
carregadores aplicam o padrão quando ausente.

- Cenário: exige `id`, `intervalo_h`, `geracao_solar_kwh`,
  `geracao_eolica_kwh`, `reserva_kwh`, `vento_previsto_ms`, `sistemas` e
  `hierarquia`. IDs e nomes são textos não vazios.
- Números: somente `int` e `float` finitos e não negativos, rejeitando
  `bool`, strings numéricas, `NaN`, infinitos e inteiros fora da escala
  finita. `intervalo_h` deve ser estritamente positivo.
- Sistemas: lista não vazia de dicionários com `id`, `nome`,
  `consumo_kwh`, `essencial` booleano e `prioridade` inteira positiva,
  sem aceitar `bool` como prioridade. IDs são únicos no cenário;
  `suporte_vida` é obrigatório, essencial e de prioridade 1.
- Hierarquia: dicionários aninhados com raiz única `colonia`, contendo
  somente `energia` e `consumidores`. Energia tem `solar` e `eolico`;
  consumidores correspondem exatamente aos IDs de `sistemas`. Toda folha
  deve ser um `dict` vazio `{}`, inclusive nas chamadas Python diretas.
- Histórico: `intervalo_h`, `vento_ms` e `energia_eolica_kwh` obrigatórios.
  As séries são listas ou tuplas com o mesmo comprimento, pelo menos dois
  pares finitos não negativos e duas velocidades distintas. O par na
  posição `i` representa vento e energia do mesmo intervalo; não ordenar
  uma série separadamente. Os JSONs usam listas.

A igualdade da duração do cenário e do histórico deve ser conferida pelo
integrador (#10). Energias em kWh não são multiplicadas novamente pela
duração. A árvore apenas referencia os consumidores; ela não fornece uma
segunda parcela de consumo para somar.

```python
from copy import deepcopy
from src.dados import validar_cenario, validar_historico

print(validar_cenario(deficit))  # []: déficit é condição operacional válida
print(validar_historico(historico))  # []
invalido = deepcopy(deficit)
invalido["geracao_solar_kwh"] = True
print(validar_cenario(invalido))
# ['cenario.geracao_solar_kwh: deve ser número finito não negativo (sem bool)']
print(deficit["geracao_solar_kwh"])  # 20.0: entrada original preservada
```

Geração menor que consumo deve chegar ao módulo de decisões; não é erro
de formato nem motivo para substituir dados por zero.

## Consulta hierárquica

`buscar_subsistema(hierarquia, caminho)` percorre uma lista ou tupla não
vazia de chaves de texto não vazio. Retorna o nó `dict` encontrado, ou
`None` se um caminho válido não existir. Argumentos malformados ou um nó
percorrido que não seja dicionário geram `ValueError`.

```python
from src.dados import buscar_subsistema

arvore = deficit["hierarquia"]
solar = buscar_subsistema(arvore, ["colonia", "energia", "solar"])
eolico = buscar_subsistema(arvore, ("colonia", "energia", "eolico"))
ausente = buscar_subsistema(arvore, ["colonia", "energia", "nuclear"])
print(solar, eolico, ausente)  # {} {} None

for nome, no in (("solar", solar), ("eolico", eolico), ("nuclear", ausente)):
    if no is None:
        print(nome, "ausente")
    else:
        print(nome, "encontrado")
# solar encontrado
# eolico encontrado
# nuclear ausente
```

Uma folha válida `{}` e `None` são ambos falsos em uma condição simples.
Use `is None` para distinguir ausência de folha vazia. No fluxo integrado
da issue #10, `src/sistema.py` executa essas consultas para `solar` e
`eolico` em `executar_cenario`, enquanto `main.py` carrega os JSONs por
`carregar_cenarios` e `carregar_historico`.

## Verificação

```bash
python3 -m unittest discover -s tests -p test_dados.py -v
python3 -m unittest discover -s tests -v
python3 main.py --listar
python3 main.py --cenario deficit
```

Os oito cenários e as contas esperadas estão em [cenarios.md](cenarios.md).
