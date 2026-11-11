# src/energia.py

def calcular_balanco_energia(geracao_solar: float, geracao_eolica: float, consumo_total: float, reserva_atual: float = 0.0) -> dict:
    """
    Calcula o saldo energético somando a geração solar e eólica, subtraindo o consumo
    e avaliando a cobertura por reserva se houver déficit.
    
    Unidades padronizadas: kW ou kWh (deve ser consistente em todo o escopo).
    """
    geracao_total = geracao_solar + geracao_eolica
    saldo = geracao_total - consumo_total
    
    cobertura_reserva = 0.0
    saldo_restante_com_reserva = saldo
    
    if saldo < 0:
        deficit = abs(saldo)
        if reserva_atual >= deficit:
            cobertura_reserva = deficit
            saldo_restante_com_reserva = 0.0
            status = "DÉFICIT_COBERTO_POR_RESERVA"
            mensagem = f"ALERTA: Consumo maior que geração (Déficit de {deficit:.2f}). Coberto integralmente pela reserva."
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