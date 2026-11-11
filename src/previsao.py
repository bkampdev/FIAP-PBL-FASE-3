"""Regressão linear para energia eólica por intervalo."""

from math import fsum, isfinite


def _numero_nao_negativo(valor, campo):
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise ValueError(f"{campo} deve ser um número finito e não negativo.")
    try:
        if isfinite(valor) and valor >= 0:
            return float(valor)
    except OverflowError:
        pass
    raise ValueError(f"{campo} deve ser um número finito e não negativo.")


def ajustar_reta(x, y):
    """Ajusta y = a*x + b a listas ou tuplas de vento (m/s) e energia (kWh)."""
    if not isinstance(x, (list, tuple)) or not isinstance(y, (list, tuple)):
        raise ValueError("Forneça duas sequências de valores pareados.")
    if len(x) != len(y) or len(x) < 2:
        raise ValueError("As sequências devem ter o mesmo tamanho e pelo menos dois pares.")

    ventos = [_numero_nao_negativo(valor, "Vento histórico") for valor in x]
    energias = [_numero_nao_negativo(valor, "Energia histórica") for valor in y]
    vento_minimo, vento_maximo = min(ventos), max(ventos)
    if vento_minimo == vento_maximo:
        raise ValueError("O histórico precisa de pelo menos duas velocidades distintas.")

    try:
        media_x = fsum(ventos) / len(ventos)
        media_y = fsum(energias) / len(energias)
        desvios_x = [vento - media_x for vento in ventos]
        variacao_x = fsum(desvio * desvio for desvio in desvios_x)
        variacao_conjunta = fsum(
            desvio * (energia - media_y)
            for desvio, energia in zip(desvios_x, energias)
        )
        a = variacao_conjunta / variacao_x
        b = media_y - a * media_x
    except (OverflowError, ZeroDivisionError, ValueError) as erro:
        raise ValueError("A escala dos valores impede um ajuste numérico válido.") from erro
    if not all(isfinite(valor) for valor in (variacao_x, a, b)):
        raise ValueError("A escala dos valores impede um ajuste numérico válido.")

    return {
        "a": a,
        "b": b,
        "vento_min_ms": vento_minimo,
        "vento_max_ms": vento_maximo,
    }


def prever_energia(modelo, vento):
    """Estima a energia no intervalo do histórico a partir da reta ajustada."""
    vento = _numero_nao_negativo(vento, "Vento previsto")
    estimativa = modelo["a"] * vento + modelo["b"]
    if not isfinite(estimativa):
        raise ValueError("A escala dos valores impede uma estimativa numérica válida.")

    extrapolacao = not modelo["vento_min_ms"] <= vento <= modelo["vento_max_ms"]
    avisos = []
    if extrapolacao:
        avisos.append("Extrapolação: vento previsto fora da faixa histórica.")
    if estimativa < 0:
        avisos.append("Estimativa negativa: o resultado é fisicamente inválido.")
    return {
        **modelo,
        "vento_previsto_ms": vento,
        "energia_eolica_prevista_kwh": estimativa,
        "extrapolacao": extrapolacao,
        "aviso": " ".join(avisos) or None,
    }
