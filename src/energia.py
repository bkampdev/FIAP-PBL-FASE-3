"""Balanço de energias em kWh para um mesmo intervalo, sem alterar estoque."""

from math import fsum, isfinite


def _energia_valida(valor, campo):
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise ValueError(f"{campo} deve ser número finito e não negativo.")
    try:
        if isfinite(valor) and valor >= 0:
            return float(valor)
    except OverflowError:
        pass
    raise ValueError(f"{campo} deve ser número finito e não negativo.")


def analisar_energia(cenario):
    """Retorna balanço observado; reserva representa cobertura apenas potencial.

    Recebe cenário validado pelo carregador; confere os operandos matemáticos.
    Energias e reserva em kWh; intervalo_h positivo (padrão 1 h quando ausente).
    Não multiplica energias pela duração e não modifica as entradas.
    """
    if not isinstance(cenario, dict):
        raise ValueError("Cenário deve ser um dicionário.")
    try:
        intervalo = _energia_valida(cenario.get("intervalo_h", 1.0), "intervalo_h")
        if intervalo == 0:
            raise ValueError("intervalo_h deve ser positivo.")
        solar = _energia_valida(cenario["geracao_solar_kwh"], "geracao_solar_kwh")
        eolica = _energia_valida(cenario["geracao_eolica_kwh"], "geracao_eolica_kwh")
        reserva = _energia_valida(cenario["reserva_kwh"], "reserva_kwh")
        sistemas = cenario["sistemas"]
        if not isinstance(sistemas, list) or not sistemas:
            raise ValueError("sistemas deve ser uma lista não vazia.")
        consumos, essenciais = [], []
        for sistema in sistemas:
            if not isinstance(sistema, dict) or not isinstance(sistema.get("essencial"), bool):
                raise ValueError("Cada sistema exige dicionário e essencial booleano.")
            consumo = _energia_valida(sistema["consumo_kwh"], "consumo_kwh")
            consumos.append(consumo)
            if sistema["essencial"]:
                essenciais.append(consumo)
        consumo_total = fsum(consumos)
        consumo_essencial = fsum(essenciais)
    except KeyError as erro:
        raise ValueError(f"Campo obrigatório ausente: {erro.args[0]}.") from erro
    except OverflowError as erro:
        raise ValueError("A soma de consumos excede a escala finita.") from erro

    balanco = calcular_balanco_energia(solar, eolica, consumo_total, reserva)
    saldo = balanco["saldo"]
    return {
        "geracao_total_kwh": balanco["geracao_total"],
        "consumo_total_kwh": consumo_total,
        "consumo_essencial_kwh": consumo_essencial,
        "saldo_kwh": saldo,
        "classificacao": "deficit" if saldo < 0 else "excedente" if saldo > 0 else "equilibrio",
        "reserva_usada_kwh": balanco["cobertura_reserva"],
        "deficit_remanescente_kwh": max(0.0, -balanco["saldo_restante"]),
    }


def calcular_balanco_energia(geracao_solar: float, geracao_eolica: float, consumo_total: float, reserva_atual: float = 0.0) -> dict:
    """
    Calcula o saldo energético somando a geração solar e eólica, subtraindo o consumo
    e avaliando a cobertura por reserva se houver déficit.
    
    API numérica original: todas as entradas em kWh do mesmo intervalo.
    Cobertura de reserva é hipotética; não altera estoque nem escolhe cargas.
    """
    geracao_solar = _energia_valida(geracao_solar, "geracao_solar")
    geracao_eolica = _energia_valida(geracao_eolica, "geracao_eolica")
    consumo_total = _energia_valida(consumo_total, "consumo_total")
    reserva_atual = _energia_valida(reserva_atual, "reserva_atual")
    geracao_total = geracao_solar + geracao_eolica
    if not isfinite(geracao_total):
        raise ValueError("A soma de geração excede a escala finita.")
    saldo = geracao_total - consumo_total
    
    cobertura_reserva = 0.0
    saldo_restante_com_reserva = saldo
    
    if saldo < 0:
        deficit = abs(saldo)
        if reserva_atual >= deficit:
            cobertura_reserva = deficit
            saldo_restante_com_reserva = 0.0
            status = "DÉFICIT_COBERTO_POR_RESERVA"
            mensagem = f"ALERTA: Consumo maior que geração (Déficit de {deficit:.2f} kWh). A reserva poderia cobrir integralmente esse déficit; nenhuma descarga foi executada."
        else:
            cobertura_reserva = reserva_atual
            saldo_restante_com_reserva = -(deficit - reserva_atual)
            status = "DÉFICIT_CRITICO"
            mensagem = f"ALERTA CRÍTICO: Déficit de {deficit:.2f} excede a reserva disponível ({reserva_atual:.2f})."
    elif saldo == 0:
        status = "EQUILÍBRIO"
        mensagem = "SISTEMA EM EQUILÍBRIO: Geração igual ao consumo."
    else:
        status = "EXCEDENTE"
        mensagem = f"SUGESTÃO: Armazenar energia excedente ({saldo:.2f})."
        
    return {
        "geracao_total": geracao_total,
        "consumo_total": consumo_total,
        "saldo": saldo,
        "status": status,
        "mensagem": mensagem,
        "cobertura_reserva": cobertura_reserva,
        "saldo_restante": saldo_restante_com_reserva
    }
