"""Testes do módulo de decisões (issue #3)."""

import unittest
from copy import deepcopy

from src.decisoes import decidir, ordenar_reducao
from src.energia import analisar_energia
from src.previsao import ajustar_reta, prever_energia


def cenario_base(solar=20.0, eolica=20.0, reserva=15.0, vida=35.0, lab=35.0):
    return {
        "id": "teste",
        "intervalo_h": 1.0,
        "geracao_solar_kwh": solar,
        "geracao_eolica_kwh": eolica,
        "reserva_kwh": reserva,
        "vento_previsto_ms": 11.0,
        "sistemas": [
            {"id": "suporte_vida", "nome": "Suporte à vida", "consumo_kwh": vida,
             "essencial": True, "prioridade": 1},
            {"id": "laboratorio", "nome": "Laboratório", "consumo_kwh": lab,
             "essencial": False, "prioridade": 2},
        ],
        "hierarquia": {"colonia": {
            "energia": {"solar": {}, "eolico": {}},
            "consumidores": {"suporte_vida": {}, "laboratorio": {}},
        }},
    }


def previsao_para(vento):
    modelo = ajustar_reta([8.0, 10.0, 12.0], [20.0, 25.0, 30.0])
    return prever_energia(modelo, vento)


def rodar(cenario, previsao="padrao"):
    if previsao == "padrao":
        previsao = previsao_para(cenario["vento_previsto_ms"])
    return decidir(cenario, analisar_energia(cenario), previsao)


class TestStatus(unittest.TestCase):
    def test_exemplo_do_contrato_deficit(self):
        decisao = rodar(cenario_base())
        self.assertEqual(decisao["status"], "alerta_deficit")
        self.assertEqual(decisao["acoes"][0], {
            "acao": "Preservar Suporte à vida",
            "motivo": "Consumidor essencial prioritário"})
        self.assertEqual(decisao["acoes"][1], {
            "acao": "Avaliar redução do Laboratório",
            "motivo": "Déficit de 30 kWh; reserva cobriria 15 kWh e restariam 15 kWh"})
        self.assertIn("saldo futuro de -22,5 kWh", decisao["recomendacao_futura"])
        self.assertIn("Reserva restante hipotética: 0 kWh", decisao["recomendacao_futura"])

    def test_excedente(self):
        decisao = rodar(cenario_base(solar=50, eolica=30, reserva=10, vida=20, lab=10))
        self.assertEqual(decisao["status"], "excedente")
        self.assertIn("Excedente de 50 kWh", decisao["acoes"][0]["motivo"])

    def test_equilibrio(self):
        decisao = rodar(cenario_base(solar=25, eolica=25, vida=25, lab=25))
        self.assertEqual(decisao["status"], "equilibrio")

    def test_tudo_zero_e_equilibrio(self):
        decisao = rodar(cenario_base(0, 0, 0, 0, 0))
        self.assertEqual(decisao["status"], "equilibrio")

    def test_alerta_critico(self):
        # Geração 10 + reserva 5 = 15 < essencial 35 -> faltam 20 kWh.
        decisao = rodar(cenario_base(solar=5, eolica=5, reserva=5, lab=15))
        self.assertEqual(decisao["status"], "alerta_critico")
        self.assertIn("faltam 20 kWh", decisao["acoes"][0]["motivo"])
        textos = " ".join(a["acao"] + " " + a["motivo"] for a in decisao["acoes"])
        self.assertIn("intervenção humana", textos)
        self.assertNotIn("desligad", textos.lower())
        self.assertNotIn("Avaliar redução do Suporte", textos)

    def test_fronteira_critico_igualdade_nao_e_critico(self):
        # Geração 30 + reserva 5 = 35 == essencial 35 -> não é crítico.
        decisao = rodar(cenario_base(solar=20, eolica=10, reserva=5, lab=15))
        self.assertEqual(decisao["status"], "alerta_deficit")
        acoes = [a["acao"] for a in decisao["acoes"]]
        self.assertIn("Sinalizar dependência da reserva", acoes)

    def test_fronteira_critico_um_pouco_abaixo(self):
        decisao = rodar(cenario_base(solar=20, eolica=10, reserva=4.99, lab=15))
        self.assertEqual(decisao["status"], "alerta_critico")

    def test_deficit_sem_dependencia_da_reserva(self):
        # Geração 40 >= essencial 35: não precisa sinalizar dependência.
        acoes = [a["acao"] for a in rodar(cenario_base())["acoes"]]
        self.assertNotIn("Sinalizar dependência da reserva", acoes)

    def test_deficit_so_com_essenciais_informa_cobertura(self):
        cenario = cenario_base(solar=20, eolica=10, reserva=5, vida=35)
        cenario["sistemas"] = cenario["sistemas"][:1]
        cenario["hierarquia"]["colonia"]["consumidores"] = {"suporte_vida": {}}
        decisao = rodar(cenario, previsao=None)
        self.assertEqual(decisao["status"], "alerta_deficit")
        self.assertTrue(any(
            "Déficit de 5 kWh; reserva cobriria 5 kWh e restariam 0 kWh"
            in acao["motivo"] for acao in decisao["acoes"]
        ))
        self.assertFalse(any("redução" in acao["acao"] for acao in decisao["acoes"]))


class TestPrevisao(unittest.TestCase):
    def test_sem_previsao(self):
        decisao = rodar(cenario_base(), previsao=None)
        self.assertEqual(decisao["status"], "alerta_deficit")
        self.assertIsNone(decisao["recomendacao_futura"])
        self.assertEqual(decisao["acoes"][-1]["acao"],
                         "Planejamento do próximo intervalo indisponível")

    def test_previsao_negativa_nao_planeja(self):
        modelo = ajustar_reta([2.0, 4.0], [1.0, 3.0])
        previsao = prever_energia(modelo, 0.0)  # -1 kWh
        decisao = rodar(cenario_base(), previsao=previsao)
        self.assertIsNone(decisao["recomendacao_futura"])
        self.assertIn("-1 kWh", decisao["acoes"][-1]["motivo"])
        self.assertEqual(decisao["status"], "alerta_deficit")

    def test_extrapolacao_mostra_aviso(self):
        decisao = rodar(cenario_base(), previsao=previsao_para(13.0))
        self.assertIn("Extrapolação", decisao["recomendacao_futura"])

    def test_rejeita_geracao_futura_infinita(self):
        cenario = cenario_base(solar=1e308, eolica=0, reserva=0, vida=1e308, lab=0)
        previsao = prever_energia(
            ajustar_reta([1.0, 2.0], [5e307, 1e308]), 2.0)
        with self.assertRaisesRegex(ValueError, "geracao_futura_kwh"):
            rodar(cenario, previsao=previsao)

    def test_rejeita_disponibilidade_futura_infinita(self):
        cenario = cenario_base(solar=1e308, eolica=0, reserva=1e308,
                              vida=1e308, lab=0)
        previsao = prever_energia(ajustar_reta([1.0, 2.0], [0.0, 0.0]), 2.0)
        with self.assertRaisesRegex(ValueError, "disponibilidade_futura_kwh"):
            rodar(cenario, previsao=previsao)


class TestContrato(unittest.TestCase):
    def test_nao_altera_entradas(self):
        cenario = cenario_base()
        balanco = analisar_energia(cenario)
        previsao = previsao_para(11.0)
        copias = deepcopy((cenario, balanco, previsao))
        decidir(cenario, balanco, previsao)
        self.assertEqual((cenario, balanco, previsao), copias)

    def test_formato_do_retorno(self):
        decisao = rodar(cenario_base())
        self.assertEqual(set(decisao), {"status", "acoes", "recomendacao_futura"})
        for acao in decisao["acoes"]:
            self.assertEqual(set(acao), {"acao", "motivo"})
            self.assertTrue(acao["acao"] and acao["motivo"])

    def test_balanco_incoerente_gera_erro(self):
        cenario = cenario_base()
        balanco = analisar_energia(cenario)
        balanco["saldo_kwh"] = 10.0
        with self.assertRaises(ValueError):
            decidir(cenario, balanco, None)

    def test_rejeita_consumo_negativo_mesmo_com_balanco_coerente(self):
        cenario = cenario_base(lab=-5)
        balanco = {
            "geracao_total_kwh": 40, "consumo_total_kwh": 30,
            "consumo_essencial_kwh": 35, "saldo_kwh": 10,
            "reserva_usada_kwh": 0, "deficit_remanescente_kwh": 0,
        }
        with self.assertRaisesRegex(ValueError, "consumo_kwh"):
            decidir(cenario, balanco, None)

    def test_balanco_sem_chave_gera_erro(self):
        cenario = cenario_base()
        balanco = analisar_energia(cenario)
        del balanco["consumo_essencial_kwh"]
        with self.assertRaises(ValueError):
            decidir(cenario, balanco, None)

    def test_cobertura_e_remanescente_incoerentes_geram_erro(self):
        cenario = cenario_base()
        original = analisar_energia(cenario)
        for campo in ("reserva_usada_kwh", "deficit_remanescente_kwh"):
            for valor in (-100.0, -1e-12, 0.0, 999.0):
                with self.subTest(campo=campo, valor=valor):
                    balanco = dict(original)
                    balanco[campo] = valor
                    with self.assertRaisesRegex(ValueError, campo):
                        decidir(cenario, balanco, None)
                    self.assertEqual(balanco[campo], valor)

    def test_rejeita_cobertura_inventada_no_excedente(self):
        cenario = cenario_base(solar=50, eolica=30, reserva=15, vida=20, lab=10)
        balanco = analisar_energia(cenario)
        balanco["reserva_usada_kwh"] = 1.0
        with self.assertRaisesRegex(ValueError, "reserva_usada_kwh"):
            decidir(cenario, balanco, None)

    def test_suporte_vida_nao_essencial_gera_erro(self):
        cenario = cenario_base()
        cenario["sistemas"][0]["essencial"] = False
        balanco = analisar_energia(cenario)
        with self.assertRaises(ValueError):
            decidir(cenario, balanco, None)

    def test_tipos_invalidos(self):
        cenario = cenario_base()
        balanco = analisar_energia(cenario)
        for args in [(None, balanco, None), (cenario, [], None), (cenario, balanco, "x")]:
            with self.subTest(args=repr(args)[:40]), self.assertRaises(ValueError):
                decidir(*args)
        balanco["saldo_kwh"] = True
        with self.assertRaises(ValueError):
            decidir(cenario, balanco, None)

    def test_ordenar_reducao_exclui_essenciais(self):
        self.assertEqual([s["id"] for s in ordenar_reducao(cenario_base()["sistemas"])],
                         ["laboratorio"])


if __name__ == "__main__":
    unittest.main()
