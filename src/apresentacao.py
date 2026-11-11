"""Formatação da saída da colônia Aurora para o terminal."""


def _numero(valor):
    return format(valor, ".6g").replace(".", ",")


def formatar_resultado(resultado):
    """Devolve texto a partir de um resultado integrado, sem recalcular valores."""
    if resultado.get("erro"):
        return f"Erro de entrada: {resultado['erro']}"

    cenario = resultado["cenario"]
    balanco = resultado["balanco"]
    decisao = resultado["decisao"]
    essenciais = ", ".join(
        sistema["nome"] for sistema in cenario["sistemas"] if sistema["essencial"]
    )
    linhas = [
        f"Cenário {cenario['id']} | Intervalo de {_numero(cenario['intervalo_h'])} h",
        "",
        "Intervalo atual (dados observados)",
        f"Solar: {_numero(cenario['geracao_solar_kwh'])} kWh",
        f"Eólica: {_numero(cenario['geracao_eolica_kwh'])} kWh",
        f"Geração total: {_numero(balanco['geracao_total_kwh'])} kWh",
        f"Consumo total: {_numero(balanco['consumo_total_kwh'])} kWh",
        f"Saldo: {_numero(balanco['saldo_kwh'])} kWh ({balanco['classificacao']})",
        f"Reserva disponível: {_numero(cenario['reserva_kwh'])} kWh",
        f"Sistemas essenciais: {essenciais or 'nenhum informado'}",
        f"Estado atual: {decisao['status']}",
    ]
    for acao in decisao["acoes"]:
        linhas.append(f"- {acao['acao']} | Motivo: {acao['motivo']}")

    linhas.extend(("", "Próximo intervalo (estimativa)"))
    previsao = resultado["previsao"]
    if previsao is None:
        motivo = resultado.get("erro_previsao") or "modelo indisponível"
        linhas.append(f"Previsão eólica indisponível: {motivo}")
    else:
        linhas.extend(
            (
                f"Coeficientes: a = {_numero(previsao['a'])} kWh/(m/s), "
                f"b = {_numero(previsao['b'])} kWh",
                f"Vento previsto: {_numero(previsao['vento_previsto_ms'])} m/s",
                "Geração eólica estimada: "
                f"{_numero(previsao['energia_eolica_prevista_kwh'])} kWh",
            )
        )
        if previsao.get("aviso"):
            linhas.append(f"Aviso: {previsao['aviso']}")

    recomendacao = decisao["recomendacao_futura"]
    if recomendacao:
        linhas.append(f"Recomendação futura: {recomendacao}")
    else:
        linhas.append("Recomendação futura indisponível.")
    return "\n".join(linhas)
