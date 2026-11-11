import unittest

from src.previsao import ajustar_reta, prever_energia


class TestPrevisao(unittest.TestCase):
    def test_exemplo_do_enunciado(self):
        modelo = ajustar_reta([8, 10, 12], [20, 25, 30])
        previsao = prever_energia(modelo, 11)

        self.assertAlmostEqual(modelo["a"], 2.5)
        self.assertAlmostEqual(modelo["b"], 0)
        self.assertAlmostEqual(previsao["energia_eolica_prevista_kwh"], 27.5)
        self.assertFalse(previsao["extrapolacao"])
        self.assertIsNone(previsao["aviso"])

    def test_dois_pares_com_intercepto_e_limites_inclusivos(self):
        modelo = ajustar_reta((2, 6), (5, 13))

        self.assertAlmostEqual(modelo["a"], 2)
        self.assertAlmostEqual(modelo["b"], 1)
        for vento, energia in ((2, 5), (6, 13)):
            with self.subTest(vento=vento):
                previsao = prever_energia(modelo, vento)
                self.assertFalse(previsao["extrapolacao"])
                self.assertAlmostEqual(previsao["energia_eolica_prevista_kwh"], energia)

    def test_extrapolacao_preserva_estimativa_e_sinaliza_valor_negativo(self):
        modelo = ajustar_reta([2, 4], [1, 3])

        abaixo = prever_energia(modelo, 0)
        acima = prever_energia(modelo, 5)

        self.assertTrue(abaixo["extrapolacao"])
        self.assertIn("fisicamente inválido", abaixo["aviso"])
        self.assertAlmostEqual(abaixo["energia_eolica_prevista_kwh"], -1)
        self.assertTrue(acima["extrapolacao"])
        self.assertIn("Extrapolação", acima["aviso"])
        self.assertAlmostEqual(acima["energia_eolica_prevista_kwh"], 4)

    def test_rejeita_historicos_invalidos(self):
        casos = (
            ([], []),
            ([1], [2]),
            ([1, 2], [1]),
            ([1, 1], [2, 3]),
            ([1, float("nan")], [2, 3]),
            ([1, 2], [2, float("inf")]),
            ([1, True], [2, 3]),
            ([1, 2], [2, -1]),
            ([1, 2], None),
        )
        for ventos, energias in casos:
            with self.subTest(ventos=ventos, energias=energias):
                with self.assertRaises(ValueError):
                    ajustar_reta(ventos, energias)

    def test_rejeita_vento_previsto_invalido(self):
        modelo = ajustar_reta([0, 1], [0, 2])

        for vento in (-1, float("inf"), float("nan"), "11", True):
            with self.subTest(vento=vento):
                with self.assertRaisesRegex(ValueError, "Vento previsto"):
                    prever_energia(modelo, vento)


if __name__ == "__main__":
    unittest.main()
