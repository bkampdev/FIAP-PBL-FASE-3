"""Integração dos módulos de análise energética da Colônia Aurora (issue #10).

Coordena validação/normalização sem mutar entradas, consulta real à hierarquia,
balanço energético observado, regressão/previsão eólica e regras de decisão,
retornando sempre o envelope contratual de seis chaves sem imprimir no terminal.
"""

from copy import deepcopy
from math import isclose

from src.dados import buscar_subsistema, validar_cenario, validar_historico
from src.decisoes import decidir
from src.energia import analisar_energia
from src.previsao import ajustar_reta, prever_energia


def _copiar_estrutura(valor):
    """Cria cópia profunda preservando tipos não serializáveis para validação."""
    if type(valor) is dict:
        return {chave: _copiar_estrutura(item) for chave, item in valor.items()}
    if type(valor) is list:
        return [_copiar_estrutura(item) for item in valor]
    if type(valor) is tuple:
        return tuple(_copiar_estrutura(item) for item in valor)
    try:
        return deepcopy(valor)
    except TypeError:
        return valor


def _envelope_erro(mensagem):
    """Monta o envelope padrão quando o cenário ou cálculo atual é inválido."""
    return {
        "erro": mensagem,
        "cenario": None,
        "balanco": None,
        "previsao": None,
        "erro_previsao": None,
        "decisao": None,
    }


def _intervalos_compativeis(intervalo_cenario, intervalo_historico):
    return isclose(
        float(intervalo_cenario),
        float(intervalo_historico),
        rel_tol=1e-9,
        abs_tol=1e-9,
    )


def _processar_previsao(cenario_norm, historico):
    """Valida histórico, confere duração, ajusta a reta e estima a eólica."""
    if historico is None:
        return None, "Histórico eólico ausente."

    if not isinstance(historico, dict):
        erros = validar_historico(historico)
        return None, "; ".join(erros)

    historico_norm = _copiar_estrutura(historico)
    if "intervalo_h" not in historico_norm:
        historico_norm["intervalo_h"] = 1.0

    erros_historico = validar_historico(historico_norm)
    if erros_historico:
        return None, "; ".join(erros_historico)

    if not _intervalos_compativeis(
        cenario_norm["intervalo_h"], historico_norm["intervalo_h"]
    ):
        return None, (
            f"Duração do histórico ({historico_norm['intervalo_h']} h) "
            f"incompatível com a do cenário ({cenario_norm['intervalo_h']} h)."
        )

    try:
        modelo = ajustar_reta(
            historico_norm["vento_ms"],
            historico_norm["energia_eolica_kwh"],
        )
        previsao = prever_energia(modelo, cenario_norm["vento_previsto_ms"])
    except ValueError as erro:
        return None, str(erro)

    return previsao, None


def executar_cenario(cenario, historico):
    """Executa o fluxo integrado de um cenário e retorna o envelope completo."""
    if not isinstance(cenario, dict):
        erros = validar_cenario(cenario)
        return _envelope_erro("; ".join(erros))

    cenario_norm = _copiar_estrutura(cenario)
    if "intervalo_h" not in cenario_norm:
        cenario_norm["intervalo_h"] = 1.0

    erros_cenario = validar_cenario(cenario_norm)
    if erros_cenario:
        return _envelope_erro("; ".join(erros_cenario))

    try:
        folha_solar = buscar_subsistema(
            cenario_norm["hierarquia"], ["colonia", "energia", "solar"]
        )
        folha_eolica = buscar_subsistema(
            cenario_norm["hierarquia"], ["colonia", "energia", "eolico"]
        )
    except ValueError as erro:
        return _envelope_erro(str(erro))

    if folha_solar is None or folha_eolica is None:
        return _envelope_erro(
            "Hierarquia de energia incompleta: subsistemas solar e eolico são obrigatórios."
        )

    try:
        balanco = analisar_energia(cenario_norm)
    except ValueError as erro:
        return _envelope_erro(str(erro))

    previsao, erro_previsao = _processar_previsao(cenario_norm, historico)

    if previsao is not None:
        try:
            decisao = decidir(cenario_norm, balanco, previsao)
        except ValueError as erro:
            previsao = None
            erro_previsao = str(erro)
            try:
                decisao = decidir(cenario_norm, balanco, None)
            except ValueError as erro_atual:
                return _envelope_erro(str(erro_atual))
    else:
        try:
            decisao = decidir(cenario_norm, balanco, None)
        except ValueError as erro_atual:
            return _envelope_erro(str(erro_atual))

    return {
        "erro": None,
        "cenario": cenario_norm,
        "balanco": balanco,
        "previsao": previsao,
        "erro_previsao": erro_previsao,
        "decisao": decisao,
    }
