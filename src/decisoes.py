"""Regras de decisão e prioridade do suporte à vida (issue #3).

Recebe cenário e balanço já validados e a previsão eólica (ou None) e
devolve um dicionário com status, ações e recomendação para o próximo
intervalo. Não imprime, não altera as entradas e não aciona equipamentos:
as ações são recomendações, nunca desligamentos executados.
"""

from math import isclose, isfinite

CHAVES_BALANCO = (
    "geracao_total_kwh",
    "consumo_total_kwh",
    "consumo_essencial_kwh",
    "saldo_kwh",
    "reserva_usada_kwh",
    "deficit_remanescente_kwh",
)


def _numero(valor, campo):
    """Aceita apenas int/float finito (bool é rejeitado)."""
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise ValueError(f"{campo} deve ser um número finito.")
    if not isfinite(valor):
        raise ValueError(f"{campo} deve ser um número finito.")
    return float(valor)


def _iguais(x, y):
    return isclose(x, y, rel_tol=1e-9, abs_tol=1e-9)


def _fmt(valor):
    """Formata kWh no padrão brasileiro: 27.5 -> '27,5'; 30.0 -> '30'."""
    valor = round(valor, 2) + 0.0  # + 0.0 evita exibir "-0"
    return f"{valor:g}".replace(".", ",")


def _conferir_entradas(cenario, balanco, previsao):
    """Levanta ValueError se as entradas violarem o contrato."""
    if not isinstance(cenario, dict) or not isinstance(balanco, dict):
        raise ValueError("Cenário e balanço devem ser dicionários.")

    for chave in CHAVES_BALANCO:
        if chave not in balanco:
            raise ValueError(f"Balanço sem a chave obrigatória: {chave}.")
        valor = _numero(balanco[chave], chave)
        if chave != "saldo_kwh" and valor < 0:
            raise ValueError(f"{chave} não pode ser negativo.")

    for campo in ("geracao_solar_kwh", "geracao_eolica_kwh", "reserva_kwh"):
        if campo not in cenario:
            raise ValueError(f"Cenário sem o campo obrigatório: {campo}.")
        if _numero(cenario[campo], campo) < 0:
            raise ValueError(f"{campo} não pode ser negativo.")

    sistemas = cenario.get("sistemas")
    if not isinstance(sistemas, list) or not sistemas:
        raise ValueError("sistemas deve ser uma lista não vazia.")
    for sistema in sistemas:
        if not isinstance(sistema, dict):
            raise ValueError("Cada sistema deve ser um dicionário.")
        for campo in ("id", "nome", "consumo_kwh", "essencial", "prioridade"):
            if campo not in sistema:
                raise ValueError(f"Sistema sem o campo obrigatório: {campo}.")
        if not isinstance(sistema["essencial"], bool):
            raise ValueError("essencial deve ser booleano.")
        if _numero(sistema["consumo_kwh"], "consumo_kwh") < 0:
            raise ValueError("consumo_kwh não pode ser negativo.")

    suporte = [s for s in sistemas if s["id"] == "suporte_vida"]
    if len(suporte) != 1 or suporte[0]["essencial"] is not True:
        raise ValueError("suporte_vida deve existir uma vez e ser essencial.")

    # Coerência entre cenário e balanço (evita decidir com números trocados).
    geracao = cenario["geracao_solar_kwh"] + cenario["geracao_eolica_kwh"]
    consumo = sum(s["consumo_kwh"] for s in sistemas)
    essencial = sum(s["consumo_kwh"] for s in sistemas if s["essencial"])
    if not _iguais(balanco["geracao_total_kwh"], geracao):
        raise ValueError("geracao_total_kwh não confere com o cenário.")
    if not _iguais(balanco["consumo_total_kwh"], consumo):
        raise ValueError("consumo_total_kwh não confere com o cenário.")
    if not _iguais(balanco["consumo_essencial_kwh"], essencial):
        raise ValueError("consumo_essencial_kwh não confere com o cenário.")
    if not _iguais(balanco["saldo_kwh"], geracao - consumo):
        raise ValueError("saldo_kwh não confere com geração menos consumo.")
    deficit = max(0.0, -balanco["saldo_kwh"])
    cobertura = min(cenario["reserva_kwh"], deficit)
    if not _iguais(balanco["reserva_usada_kwh"], cobertura):
        raise ValueError("reserva_usada_kwh não confere com o déficit e a reserva.")
    if not _iguais(balanco["deficit_remanescente_kwh"], deficit - cobertura):
        raise ValueError("deficit_remanescente_kwh não confere com a cobertura.")

    if previsao is not None:
        if not isinstance(previsao, dict):
            raise ValueError("Previsão deve ser um dicionário ou None.")
        if "energia_eolica_prevista_kwh" not in previsao:
            raise ValueError("Previsão sem energia_eolica_prevista_kwh.")
        _numero(previsao["energia_eolica_prevista_kwh"], "energia_eolica_prevista_kwh")


def ordenar_reducao(sistemas):
    """Fila de redução: só não essenciais, maior número de prioridade primeiro.

    Empates usam o id em ordem alfabética. Essenciais nunca entram na fila.
    """
    candidatos = [s for s in sistemas if not s["essencial"]]
    return sorted(candidatos, key=lambda s: (-s["prioridade"], s["id"]))


def _acoes_preservar(sistemas):
    essenciais = sorted(
        [s for s in sistemas if s["essencial"]],
        key=lambda s: (s["prioridade"], s["id"]),
    )
    return [
        {"acao": f"Preservar {s['nome']}", "motivo": "Consumidor essencial prioritário"}
        for s in essenciais
    ]


def _recomendacao_futura(cenario, balanco, previsao, acoes):
    """Texto do próximo intervalo ou None (com ação explicando o motivo)."""
    if previsao is None:
        acoes.append({
            "acao": "Planejamento do próximo intervalo indisponível",
            "motivo": "Previsão eólica ausente; vale apenas a decisão atual",
        })
        return None

    eolica_prevista = float(previsao["energia_eolica_prevista_kwh"])
    if eolica_prevista < 0:
        aviso = previsao.get("aviso") or "Estimativa negativa é fisicamente inválida."
        acoes.append({
            "acao": "Planejamento do próximo intervalo indisponível",
            "motivo": f"Estimativa eólica de {_fmt(eolica_prevista)} kWh não é usada. {aviso}",
        })
        return None

    # Hipóteses: mesma solar e mesmo consumo; só a eólica é substituída.
    solar = float(cenario["geracao_solar_kwh"])
    consumo = balanco["consumo_total_kwh"]
    essencial = balanco["consumo_essencial_kwh"]
    geracao_futura = _numero(solar + eolica_prevista, "geracao_futura_kwh")
    saldo_futuro = _numero(geracao_futura - consumo, "saldo_futuro_kwh")
    reserva_restante = max(0.0, cenario["reserva_kwh"] - balanco["reserva_usada_kwh"])
    disponibilidade_futura = _numero(
        geracao_futura + reserva_restante, "disponibilidade_futura_kwh")

    texto = (
        f"Com solar mantida em {_fmt(solar)} kWh e consumo planejado em "
        f"{_fmt(consumo)} kWh, a eólica estimada de {_fmt(eolica_prevista)} kWh "
        f"leva a saldo futuro de {_fmt(saldo_futuro)} kWh. "
        f"Reserva restante hipotética: {_fmt(reserva_restante)} kWh. "
    )
    if disponibilidade_futura < essencial:
        texto += ("Risco de insuficiência para os essenciais: "
                  "preparar intervenção humana e planejar redução de não essenciais.")
    elif saldo_futuro < 0:
        texto += "Planejar redução de não essenciais."
    elif saldo_futuro == 0:
        texto += "Sem margem prevista; manter monitoramento."
    else:
        texto += "Avaliar armazenamento ou uso planejado do excedente estimado."

    if previsao.get("aviso"):
        texto += f" Aviso: {previsao['aviso']}"
    return texto


def decidir(cenario, balanco, previsao):
    """Decide o status atual e as ações a partir do cenário e do balanço.

    Ordem de precedência das regras:
    1. geração + reserva < consumo essencial  -> "alerta_critico"
    2. saldo < 0                              -> "alerta_deficit"
    3. saldo == 0                             -> "equilibrio"
    4. saldo > 0                              -> "excedente"
    """
    _conferir_entradas(cenario, balanco, previsao)

    sistemas = cenario["sistemas"]
    geracao = balanco["geracao_total_kwh"]
    essencial = balanco["consumo_essencial_kwh"]
    saldo = balanco["saldo_kwh"]
    reserva = float(cenario["reserva_kwh"])
    cobertura = balanco["reserva_usada_kwh"]
    remanescente = balanco["deficit_remanescente_kwh"]
    acoes = []

    if geracao + reserva < essencial:
        # Nem com toda a reserva os essenciais seriam atendidos.
        status = "alerta_critico"
        falta = essencial - (geracao + reserva)
        acoes.append({
            "acao": "Alerta crítico: energia insuficiente para os sistemas essenciais",
            "motivo": (f"Geração de {_fmt(geracao)} kWh e reserva de {_fmt(reserva)} kWh "
                       f"não cobrem o consumo essencial de {_fmt(essencial)} kWh; "
                       f"faltam {_fmt(falta)} kWh"),
        })
        acoes.extend(_acoes_preservar(sistemas))
        acoes.append({
            "acao": "Acionar intervenção humana imediata",
            "motivo": "O sistema apenas recomenda; não há garantia de segurança",
        })
        for s in ordenar_reducao(sistemas):
            acoes.append({
                "acao": f"Avaliar redução do {s['nome']}",
                "motivo": "Liberar toda energia possível para os essenciais",
            })

    elif saldo < 0:
        status = "alerta_deficit"
        deficit = -saldo
        acoes.extend(_acoes_preservar(sistemas))
        if geracao < essencial:
            acoes.append({
                "acao": "Sinalizar dependência da reserva",
                "motivo": (f"Geração de {_fmt(geracao)} kWh é menor que o consumo "
                           f"essencial de {_fmt(essencial)} kWh"),
            })
        # Propõe reduções na ordem combinada até cobrir o déficit bruto.
        candidatos = ordenar_reducao(sistemas)
        motivo_deficit = (
            f"Déficit de {_fmt(deficit)} kWh; reserva cobriria "
            f"{_fmt(cobertura)} kWh e restariam {_fmt(remanescente)} kWh"
        )
        if not candidatos:
            acoes.append({
                "acao": "Informar déficit energético sem cargas não essenciais",
                "motivo": motivo_deficit,
            })
        reduzido = 0.0
        for s in candidatos:
            if reduzido >= deficit:
                break
            acoes.append({
                "acao": f"Avaliar redução do {s['nome']}",
                "motivo": motivo_deficit,
            })
            reduzido += s["consumo_kwh"]

    elif saldo == 0:
        status = "equilibrio"
        acoes.append({
            "acao": "Manter operação e monitorar",
            "motivo": "Geração igual ao consumo; sem margem de geração",
        })

    else:
        status = "excedente"
        acoes.append({
            "acao": "Avaliar armazenamento ou uso planejado do excedente",
            "motivo": (f"Excedente de {_fmt(saldo)} kWh; "
                       "armazenamento real não é modelado"),
        })

    recomendacao = _recomendacao_futura(cenario, balanco, previsao, acoes)
    return {"status": status, "acoes": acoes, "recomendacao_futura": recomendacao}
