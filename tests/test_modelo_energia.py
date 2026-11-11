"""Contas independentes da regressão e de sua combinação com energia."""
import copy
import unittest

from src.energia import analisar_energia
from src.previsao import ajustar_reta, prever_energia


class TestModeloEnergia(unittest.TestCase):
    def setUp(self):
        self.modelo = ajustar_reta([8, 10, 12], [20, 25, 30])

    def test_coeficientes_e_previsao_manual(self):
        self.assertAlmostEqual(self.modelo['a'], 2.5)
        self.assertAlmostEqual(self.modelo['b'], 0)
        previsao = prever_energia(self.modelo, 11)
        self.assertAlmostEqual(previsao['energia_eolica_prevista_kwh'], 27.5)
        self.assertFalse(previsao['extrapolacao'])
        self.assertIsNone(previsao['aviso'])

    def test_extrapolacao(self):
        previsao = prever_energia(self.modelo, 13)
        self.assertAlmostEqual(previsao['energia_eolica_prevista_kwh'], 32.5)
        self.assertTrue(previsao['extrapolacao'])
        self.assertTrue(previsao['aviso'])

    def test_historicos_invalidos(self):
        for x, y in [([], []), ([8, 10], [20]), ([8, 8], [20, 25])]:
            with self.subTest(x=x, y=y), self.assertRaises(ValueError):
                ajustar_reta(x, y)

    def test_previsao_com_saldo_sem_reaplicar_reserva(self):
        cenario = {
            'intervalo_h': 1.0, 'geracao_solar_kwh': 20,
            'geracao_eolica_kwh': 20, 'reserva_kwh': 15,
            'sistemas': [{'consumo_kwh': 35, 'essencial': True},
                         {'consumo_kwh': 35, 'essencial': False}],
        }
        original = copy.deepcopy(cenario)
        atual = analisar_energia(cenario)
        futuro = copy.deepcopy(cenario)
        futuro['geracao_eolica_kwh'] = prever_energia(
            self.modelo, 11)['energia_eolica_prevista_kwh']
        futuro['reserva_kwh'] -= atual['reserva_usada_kwh']
        previsto = analisar_energia(futuro)
        self.assertAlmostEqual(atual['saldo_kwh'], -30)
        self.assertAlmostEqual(atual['reserva_usada_kwh'], 15)
        self.assertAlmostEqual(previsto['saldo_kwh'], -22.5)
        self.assertAlmostEqual(previsto['reserva_usada_kwh'], 0)
        self.assertAlmostEqual(previsto['deficit_remanescente_kwh'], 22.5)
        self.assertEqual(cenario, original)


if __name__ == '__main__':
    unittest.main()
