
"""Leitura, validação e consulta dos dados da Colônia Aurora (issue #2).

Energia em kWh, vento em m/s e duração em horas. Nenhuma função altera
os objetos recebidos. Déficit é condição operacional válida, não erro.
"""

import json
import math
from copy import deepcopy
from pathlib import Path


_CAMPOS_CENARIO = (
    "id", "intervalo_h", "geracao_solar_kwh", "geracao_eolica_kwh",
    "reserva_kwh", "vento_previsto_ms", "sistemas", "hierarquia",
)
_CAMPOS_SISTEMA = ("id", "nome", "consumo_kwh", "essencial", "prioridade")


def numero_valido(valor):
    """Aceita somente int/float finitos e não negativos (nunca bool)."""
    if type(valor) not in (int, float):
        return False
    try:
        return math.isfinite(valor) and valor >= 0
    except (ValueError, TypeError, OverflowError):
        return False


def _texto_valido(valor):
    return isinstance(valor, str) and bool(valor.strip())


def _validar_numero(objeto, campo, erros, contexto, positivo=False):
    if campo not in objeto:
        return
    valor = objeto[campo]
    if not numero_valido(valor) or (positivo and valor == 0):
        requisito = "positivo" if positivo else "não negativo"
        erros.append(
            f"{contexto}.{campo}: deve ser número finito "
            f"{requisito} (sem bool)"
        )


def buscar_subsistema(hierarquia, caminho):
    """Percorre chaves como ['colonia', 'energia', 'solar'].

    Retorna None quando o caminho não existe.
    Uma folha vazia ({}) é um resultado válido.
    """
    if not isinstance(hierarquia, dict):
        raise ValueError("hierarquia deve ser um dicionário")

    if not isinstance(caminho, (list, tuple)) or not caminho:
        raise ValueError("caminho deve ser lista ou tupla não vazia")

    if any(not _texto_valido(chave) for chave in caminho):
        raise ValueError(
            "caminho deve conter somente chaves de texto não vazias"
        )

    atual = hierarquia

    for chave in caminho:
        if not isinstance(atual, dict):
            raise ValueError("hierarquia contém nó que não é dicionário")
        if chave not in atual:
            return None
        atual = atual[chave]

    if not isinstance(atual, dict):
        raise ValueError("subsistema encontrado não é dicionário")

    return atual


def _validar_hierarquia(hierarquia, ids_sistemas):
    erros = []

    if not isinstance(hierarquia, dict):
        return ["cenario.hierarquia: deve ser dicionário"]

    if set(hierarquia) != {"colonia"}:
        erros.append(
            "cenario.hierarquia: raiz única deve ser 'colonia'"
        )

    colonia = hierarquia.get("colonia")

    if not isinstance(colonia, dict):
        erros.append(
            "cenario.hierarquia.colonia: deve ser dicionário"
        )
        return erros

    if set(colonia) != {"energia", "consumidores"}:
        erros.append(
            "cenario.hierarquia.colonia: deve conter somente "
            "energia e consumidores"
        )

    energia = colonia.get("energia")

    if not isinstance(energia, dict):
        erros.append(
            "cenario.hierarquia.colonia.energia: deve ser dicionário"
        )
    else:
        if set(energia) != {"solar", "eolico"}:
            erros.append(
                "cenario.hierarquia.colonia.energia: "
                "deve conter solar e eolico"
            )

        for fonte in ("solar", "eolico"):
            if fonte in energia and energia[fonte] != {}:
                erros.append(
                    f"cenario.hierarquia.colonia.energia.{fonte}: "
                    "deve ser folha vazia"
                )

    consumidores = colonia.get("consumidores")

    if not isinstance(consumidores, dict):
        erros.append(
            "cenario.hierarquia.colonia.consumidores: "
            "deve ser dicionário"
        )
    else:
        if ids_sistemas is not None:
            if set(consumidores) != ids_sistemas:
                erros.append(
                    "cenario.hierarquia.colonia.consumidores: "
                    "IDs não correspondem aos sistemas"
                )

        for identificador, folha in consumidores.items():
            if not _texto_valido(identificador) or folha != {}:
                erros.append(
                    f"cenario.hierarquia: consumidor "
                    f"{identificador!r} deve ter folha vazia"
                )

    return erros


def validar_cenario(cenario):
    """Retorna uma lista de erros, sem modificar o cenário."""
    if not isinstance(cenario, dict):
        return ["cenario: deve ser dicionário"]

    erros = []

    for campo in _CAMPOS_CENARIO:
        if campo not in cenario:
            erros.append(
                f"cenario.{campo}: campo obrigatório ausente"
            )

    if "id" in cenario:
        if not _texto_valido(cenario["id"]):
            erros.append("cenario.id: deve ser texto não vazio")

    campos_numericos = (
        "intervalo_h",
        "geracao_solar_kwh",
        "geracao_eolica_kwh",
        "reserva_kwh",
        "vento_previsto_ms",
    )

    for campo in campos_numericos:
        _validar_numero(
            cenario,
            campo,
            erros,
            "cenario",
            positivo=(campo == "intervalo_h"),
        )

    sistemas = cenario.get("sistemas")
    ids = set()
    ids_completos = None

    if "sistemas" in cenario:
        if not isinstance(sistemas, list) or not sistemas:
            erros.append(
                "cenario.sistemas: deve ser lista não vazia"
            )
        else:
            ids_completos = set()
            encontrou_suporte = False

            for i, sistema in enumerate(sistemas):
                contexto = f"cenario.sistemas[{i}]"

                if not isinstance(sistema, dict):
                    erros.append(
                        f"{contexto}: deve ser dicionário"
                    )
                    continue

                for campo in _CAMPOS_SISTEMA:
                    if campo not in sistema:
                        erros.append(
                            f"{contexto}.{campo}: "
                            "campo obrigatório ausente"
                        )

                identificador = sistema.get("id")

                if "id" in sistema:
                    if not _texto_valido(identificador):
                        erros.append(
                            f"{contexto}.id: deve ser texto não vazio"
                        )
                    elif identificador in ids:
                        erros.append(
                            f"{contexto}.id: identificador "
                            f"duplicado {identificador!r}"
                        )
                    else:
                        ids.add(identificador)
                        ids_completos.add(identificador)

                if "nome" in sistema:
                    if not _texto_valido(sistema["nome"]):
                        erros.append(
                            f"{contexto}.nome: deve ser texto não vazio"
                        )

                _validar_numero(
                    sistema,
                    "consumo_kwh",
                    erros,
                    contexto,
                )

                if "essencial" in sistema:
                    if type(sistema["essencial"]) is not bool:
                        erros.append(
                            f"{contexto}.essencial: deve ser booleano"
                        )

                if "prioridade" in sistema:
                    prioridade = sistema["prioridade"]
                    if (
                        type(prioridade) is not int
                        or prioridade <= 0
                    ):
                        erros.append(
                            f"{contexto}.prioridade: "
                            "deve ser inteiro positivo (sem bool)"
                        )

                if identificador == "suporte_vida":
                    encontrou_suporte = True

                    if sistema.get("essencial") is not True:
                        erros.append(
                            f"{contexto}.essencial: "
                            "suporte_vida deve ser essencial"
                        )

                    prioridade = sistema.get("prioridade")
                    if (
                        type(prioridade) is not int
                        or prioridade != 1
                    ):
                        erros.append(
                            f"{contexto}.prioridade: "
                            "suporte_vida deve ter prioridade 1"
                        )

            if not encontrou_suporte:
                erros.append(
                    "cenario.sistemas: suporte_vida é obrigatório"
                )

    if "hierarquia" in cenario:
        erros.extend(
            _validar_hierarquia(
                cenario["hierarquia"],
                ids_completos,
            )
        )

    return erros


def validar_historico(historico):
    """Verifica séries pareadas para regressão eólica."""
    if not isinstance(historico, dict):
        return ["historico: deve ser dicionário"]

    erros = []

    campos = (
        "intervalo_h",
        "vento_ms",
        "energia_eolica_kwh",
    )

    for campo in campos:
        if campo not in historico:
            erros.append(
                f"historico.{campo}: campo obrigatório ausente"
            )

    _validar_numero(
        historico,
        "intervalo_h",
        erros,
        "historico",
        positivo=True,
    )

    for campo in ("vento_ms", "energia_eolica_kwh"):
        if campo not in historico:
            continue

        serie = historico[campo]

        if (
            not isinstance(serie, (list, tuple))
            or len(serie) < 2
        ):
            erros.append(
                f"historico.{campo}: deve ser lista ou "
                "tupla de pelo menos 2 números"
            )
            continue

        for i, valor in enumerate(serie):
            if not numero_valido(valor):
                erros.append(
                    f"historico.{campo}[{i}]: deve ser "
                    "número finito não negativo"
                )

    x = historico.get("vento_ms")
    y = historico.get("energia_eolica_kwh")

    if (
        isinstance(x, (list, tuple))
        and isinstance(y, (list, tuple))
    ):
        if len(x) != len(y):
            erros.append(
                "historico: vento_ms e energia_eolica_kwh "
                "devem ter mesmo comprimento"
            )

        if (
            len(x) >= 2
            and all(numero_valido(v) for v in x)
            and len(set(x)) < 2
        ):
            erros.append(
                "historico.vento_ms: pelo menos dois ventos "
                "distintos são necessários"
            )

    return erros


def _rejeitar_constante(valor):
    raise ValueError(
        f"Constante não finita proibida no JSON: {valor}"
    )


def _ler_json(caminho):
    """Lê JSON e rejeita constantes não finitas."""
    with Path(caminho).open(
        "r", encoding="utf-8"
    ) as arquivo:
        try:
            return json.load(
                arquivo,
                parse_constant=_rejeitar_constante,
            )
        except (json.JSONDecodeError, UnicodeError) as erro:
            raise ValueError(
                f"JSON inválido em {caminho}: {erro}"
            ) from erro


def carregar_cenarios(caminho):
    """Lê e valida uma lista de cenários de um arquivo JSON."""
    bruto = _ler_json(caminho)

    if not isinstance(bruto, list) or not bruto:
        raise ValueError(
            "dados/cenarios.json deve conter lista não vazia"
        )

    resultado = []
    ids = set()

    for i, item in enumerate(bruto):
        if not isinstance(item, dict):
            raise ValueError(
                f"cenario[{i}]: deve ser dicionário"
            )

        cenario = deepcopy(item)

        if "intervalo_h" not in cenario:
            cenario["intervalo_h"] = 1.0

        erros = validar_cenario(cenario)

        if erros:
            raise ValueError(
                f"cenario[{i}]: " + "; ".join(erros)
            )

        if cenario["id"] in ids:
            raise ValueError(
                f"cenario[{i}].id: duplicado "
                f"{cenario['id']!r}"
            )

        ids.add(cenario["id"])
        resultado.append(cenario)

    return resultado


def carregar_historico(caminho):
    """Lê e valida o histórico eólico de um arquivo JSON."""
    bruto = _ler_json(caminho)

    if not isinstance(bruto, dict):
        raise ValueError(
            "historico: deve ser dicionário"
        )

    historico = deepcopy(bruto)

    if "intervalo_h" not in historico:
        historico["intervalo_h"] = 1.0

    erros = validar_historico(historico)

    if erros:
        raise ValueError(
            "historico: " + "; ".join(erros)
        )

    return historico
