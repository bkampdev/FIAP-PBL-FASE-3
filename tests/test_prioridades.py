"""Validação de prioridades e da tabela de regras (issue #7).

Cada teste corresponde a uma linha de docs/regras.md.
"""

import unittest

from src.decisoes import decidir, ordenar_reducao
from src.energia import analisar_energia
from src.previsao import ajustar_reta, prever_energia


def sistema(id_, consumo, essencial, prioridade):
    return {"id": id_, "nome": id_.capitalize(), "consumo_kwh": consumo,
            "essencial": essencial, "prioridade": prioridade}


def cenario(solar, eolica, reserva, sistemas):
    return {"id": "regra", "intervalo_h": 1.0, "geracao_solar_kwh": solar,
            "geracao_eolica_kwh": eolica, "reserva_kwh": reserva,
            "vento_previsto_ms": 10.0, "sistemas": sistemas,
            "hierarquia": {"colonia": {"energia": {"solar": {}, "eolico": {}},
                           "consumidores": {s["id"]: {} for s in sistemas}}}}


def padrao():
    return [sistema("suporte_vida", 35.0, True, 1),
            sistema("laboratorio", 15.0, False, 2)]


def previsao(vento):
    return prever_energia(ajustar_reta([8.0, 10.0, 12.0], [20.0, 25.0, 30.0]), vento)


def decidir_cenario(c, prev=None):
    return decidir(c, analisar_energia(c), prev)


class TestTabelaDeRegras(unittest.TestCase):
    def test_deficit_com_reserva(self):
        # 40 - 50 = -10; reserva 15 cobriria tudo, mas segue déficit.
        d = decidir_cenario(cenario(20, 20, 15, padrao()))
        self.assertEqual(d["status"], "alerta_deficit")
        self.assertIn("reserva cobriria 10 kWh e restariam 0 kWh", d["acoes"][1]["motivo"])

    def test_deficit_sem_reserva(self):
        d = decidir_cenario(cenario(20, 20, 0, padrao()))
        self.assertEqual(d["status"], "alerta_deficit")
        self.assertIn("reserva cobriria 0 kWh e restariam 10 kWh", d["acoes"][1]["motivo"])

    def test_igualdade(self):
        self.assertEqual(decidir_cenario(cenario(30, 20, 0, padrao()))["status"], "equilibrio")

    def test_excedente(self):
        self.assertEqual(decidir_cenario(cenario(50, 30, 10, padrao()))["status"], "excedente")

    def test_essencial_maior_que_disponivel(self):
        # 5 + 5 + 5 = 15 < 35.
        d = decidir_cenario(cenario(5, 5, 5, padrao()))
        self.assertEqual(d["status"], "alerta_critico")
        self.assertIn("faltam 20 kWh", d["acoes"][0]["motivo"])

    def test_condicao_combinada_geracao_menor_que_essencial_mas_reserva_cobre(self):
        # geração 30 < essencial 35 E geração + reserva (35) >= essencial.
        d = decidir_cenario(cenario(20, 10, 5, padrao()))
        self.assertEqual(d["status"], "alerta_deficit")
        self.assertIn("Sinalizar dependência da reserva", [a["acao"] for a in d["acoes"]])


class TestPrioridade(unittest.TestCase):
    def sistemas(self):
        return [sistema("suporte_vida", 30.0, True, 1),
                sistema("agua", 10.0, True, 2),
                sistema("comunicacao", 5.0, False, 3),
                sistema("laboratorio", 10.0, False, 2),
                sistema("lazer", 5.0, False, 4),
                sistema("estufa", 5.0, False, 3)]

    def test_ordem_de_reducao(self):
        ordem = [s["id"] for s in ordenar_reducao(self.sistemas())]
        # Maior número primeiro; empate (3) pelo id alfabético.
        self.assertEqual(ordem, ["lazer", "comunicacao", "estufa", "laboratorio"])

    def test_trocar_ordem_dos_registros_nao_muda_prioridade(self):
        original = self.sistemas()
        invertido = list(reversed(original))
        # Geração 50, consumo 65, essencial 40 -> déficit (não crítico).
        a = decidir_cenario(cenario(30, 20, 0, original))
        b = decidir_cenario(cenario(30, 20, 0, invertido))
        self.assertEqual(a, b)
        self.assertEqual(a["status"], "alerta_deficit")
        self.assertEqual(a["acoes"][0]["acao"], "Preservar Suporte_vida")
        self.assertEqual(a["acoes"][1]["acao"], "Preservar Agua")

    def test_essenciais_nunca_sao_candidatos(self):
        for solar in [0, 10, 30, 50]:
            with self.subTest(solar=solar):
                d = decidir_cenario(cenario(solar, 0, 0, self.sistemas()))
                reducoes = [a["acao"] for a in d["acoes"] if "redução" in a["acao"]]
                self.assertFalse(any("Suporte_vida" in r or "Agua" in r for r in reducoes))

    def test_reducao_para_quando_deficit_coberto(self):
        # Geração 60, consumo 65 -> déficit 5; basta propor "lazer" (5 kWh).
        d = decidir_cenario(cenario(40, 20, 0, self.sistemas()))
        reducoes = [a["acao"] for a in d["acoes"] if "redução" in a["acao"]]
        self.assertEqual(reducoes, ["Avaliar redução do Lazer"])

    def test_reducao_acumula_ate_deficit_bruto_mesmo_com_reserva_parcial(self):
        # Geração 53, consumo 65, reserva 10 -> déficit bruto 12, cobertura 10, restante 2.
        # Fila segue o déficit bruto (12), com desempate alfabético em P3, parando antes do Laboratório.
        d = decidir_cenario(cenario(33, 20, 10, self.sistemas()))
        reducoes = [a for a in d["acoes"] if "redução" in a["acao"]]
        self.assertEqual(
            [a["acao"] for a in reducoes],
            ["Avaliar redução do Lazer", "Avaliar redução do Comunicacao", "Avaliar redução do Estufa"],
        )
        self.assertIn("Déficit de 12 kWh; reserva cobriria 10 kWh e restariam 2 kWh", reducoes[0]["motivo"])


class TestAtualVersusFuturo(unittest.TestCase):
    def test_vento_menor_muda_so_o_futuro(self):
        # Solar 20, consumo 50, reserva 0: vento 8 -> -10; vento 12 -> 0.
        c = cenario(20, 20, 0, padrao())
        balanco = analisar_energia(c)
        baixo = decidir(c, balanco, previsao(8.0))
        alto = decidir(c, balanco, previsao(12.0))
        self.assertEqual(baixo["status"], alto["status"])
        self.assertEqual(balanco, analisar_energia(c))
        self.assertIn("saldo futuro de -10 kWh", baixo["recomendacao_futura"])
        self.assertIn("Planejar redução", baixo["recomendacao_futura"])
        self.assertIn("saldo futuro de 0 kWh", alto["recomendacao_futura"])
        self.assertIn("Sem margem", alto["recomendacao_futura"])

    def test_risco_critico_futuro_sem_reaplicar_reserva_e_fronteira(self):
        # Geração 30, consumo 45 (essencial 35 + lab 10), reserva 15 -> reserva_restante = 0.
        c = cenario(10, 20, 15, [sistema("suporte_vida", 35.0, True, 1),
                                 sistema("laboratorio", 10.0, False, 2)])
        abaixo = decidir_cenario(c, previsao(8.0))   # 10 + 20 + 0 = 30 < 35
        fronteira = decidir_cenario(c, previsao(10.0))  # 10 + 25 + 0 = 35 == 35
        self.assertEqual(abaixo["status"], "alerta_deficit")
        self.assertIn("Reserva restante hipotética: 0 kWh", abaixo["recomendacao_futura"])
        self.assertIn("Risco de insuficiência para os essenciais", abaixo["recomendacao_futura"])
        self.assertNotIn("Risco de insuficiência", fronteira["recomendacao_futura"])
        self.assertIn("Planejar redução de não essenciais.", fronteira["recomendacao_futura"])

    def test_excedente_futuro_nao_altera_equilibrio_atual(self):
        d = decidir_cenario(cenario(30, 20, 0, padrao()), previsao(12.0))
        self.assertEqual(d["status"], "equilibrio")
        self.assertIn("saldo futuro de 10 kWh", d["recomendacao_futura"])
        self.assertIn("Avaliar armazenamento ou uso planejado do excedente estimado.", d["recomendacao_futura"])

    def test_critico_nao_promete_seguranca(self):
        d = decidir_cenario(cenario(5, 5, 5, padrao()), previsao(8.0))
        texto = " ".join(a["motivo"] for a in d["acoes"]).lower()
        self.assertIn("não há garantia de segurança", texto)
        self.assertNotIn("seguro", texto)


if __name__ == "__main__":
    unittest.main()
