# tests/test_energia.py
import unittest
from src.energia import calcular_balanco_energia

class TestEnergia(unittest.TestCase):
    
    def test_deficit_com_reserva(self):
        # Exemplo: Solar 20 + Eólica 20 = 40 geração, Consumo 70 -> Saldo -30
        res = calcular_balanco_energia(20, 20, 70, reserva_atual=50)
        self.assertEqual(res["saldo"], -30)
        self.assertEqual(res["status"], "DÉFICIT_COBERTO_POR_RESERVA")
        self.assertEqual(res["cobertura_reserva"], 30)

    def test_excedente(self):
        # Exemplo: Geração 80, Consumo 30 -> Saldo +50
        res = calcular_balanco_energia(50, 30, 30, reserva_atual=10)
        self.assertEqual(res["saldo"], 50)
        self.assertEqual(res["status"], "EXCEDENTE")
        self.assertIn("SUGESTÃO", res["mensagem"])

    def test_equilibrio(self):
        # Exemplo: Geração 50, Consumo 50 -> Saldo 0
        res = calcular_balanco_energia(25, 25, 50, reserva_atual=10)
        self.assertEqual(res["saldo"], 0)
        self.assertEqual(res["status"], "EQUILÍBRIO")

    def test_zeros(self):
        res = calcular_balanco_energia(0, 0, 0, reserva_atual=0)
        self.assertEqual(res["saldo"], 0)
        self.assertEqual(res["status"], "EQUILÍBRIO")



class TestContratoEnergia(unittest.TestCase):
    def cenario(self, solar=20, eolica=20, reserva=15, consumos=(35, 35)):
        return {'intervalo_h': 1.0, 'geracao_solar_kwh': solar,
                'geracao_eolica_kwh': eolica, 'reserva_kwh': reserva,
                'sistemas': [{'consumo_kwh': consumos[0], 'essencial': True},
                             {'consumo_kwh': consumos[1], 'essencial': False}]}

    def test_contrato_e_ausencia_de_mutacao(self):
        from copy import deepcopy
        from src.energia import analisar_energia
        cenario = self.cenario()
        original = deepcopy(cenario)
        self.assertEqual(analisar_energia(cenario), {
            'geracao_total_kwh': 40, 'consumo_total_kwh': 70,
            'consumo_essencial_kwh': 35, 'saldo_kwh': -30,
            'classificacao': 'deficit', 'reserva_usada_kwh': 15,
            'deficit_remanescente_kwh': 15})
        self.assertEqual(cenario, original)

    def test_reserva_zero_insuficiente_e_suficiente(self):
        from src.energia import analisar_energia
        for reserva, cobertura, restante in [(0, 0, 30), (15, 15, 15), (30, 30, 0), (50, 30, 0)]:
            with self.subTest(reserva=reserva):
                res = analisar_energia(self.cenario(reserva=reserva))
                self.assertEqual(res['saldo_kwh'], -30)
                self.assertEqual(res['classificacao'], 'deficit')
                self.assertEqual(res['reserva_usada_kwh'], cobertura)
                self.assertEqual(res['deficit_remanescente_kwh'], restante)

    def test_equilibrio_excedente_e_zeros(self):
        from src.energia import analisar_energia
        for solar, eolica, consumos, saldo, classe in [
            (50, 30, (15, 15), 50, 'excedente'),
            (25, 25, (25, 25), 0, 'equilibrio'),
            (0, 0, (0, 0), 0, 'equilibrio')]:
            with self.subTest(classe=classe, solar=solar):
                res = analisar_energia(self.cenario(solar, eolica, consumos=consumos))
                self.assertEqual(res['saldo_kwh'], saldo)
                self.assertEqual(res['classificacao'], classe)
                self.assertEqual(res['reserva_usada_kwh'], 0)
                self.assertEqual(res['deficit_remanescente_kwh'], 0)

    def test_rejeita_operandos_invalidos(self):
        from src.energia import analisar_energia
        for campo in ['geracao_solar_kwh', 'geracao_eolica_kwh', 'reserva_kwh']:
            for valor in [-1, True, '20', None, float('nan'), float('inf'), 10 ** 400]:
                with self.subTest(campo=campo, valor=repr(valor)), self.assertRaises(ValueError):
                    cenario = self.cenario()
                    cenario[campo] = valor
                    analisar_energia(cenario)

    def test_rejeita_cenario_sistemas_e_intervalo_invalidos(self):
        from src.energia import analisar_energia
        invalidos = [None, {}, self.cenario() | {'sistemas': []},
                     self.cenario() | {'sistemas': [None]},
                     self.cenario() | {'sistemas': [{'consumo_kwh': 1, 'essencial': 1}]}]
        for valor in [0, -1, True, float('nan'), float('inf'), '1']:
            invalidos.append(self.cenario() | {'intervalo_h': valor})
        for valor in [-1, True, float('nan'), float('inf'), '35']:
            cenario = self.cenario()
            cenario['sistemas'][0]['consumo_kwh'] = valor
            invalidos.append(cenario)
        for cenario in invalidos:
            with self.subTest(cenario=cenario), self.assertRaises(ValueError):
                analisar_energia(cenario)

    def test_soma_nao_finita(self):
        from src.energia import analisar_energia
        for cenario in [self.cenario(1e308, 1e308),
                        self.cenario(consumos=(1e308, 1e308))]:
            with self.subTest(cenario=cenario), self.assertRaises(ValueError):
                analisar_energia(cenario)

    def test_intervalo_nao_multiplica_kwh(self):
        from src.energia import analisar_energia
        cenario = self.cenario()
        cenario['intervalo_h'] = 2
        self.assertEqual(analisar_energia(cenario)['saldo_kwh'], -30)

    def test_api_original_rejeita_nan_e_reserva_negativa(self):
        for args in [(float('nan'), 20, 70, 0), (20, 20, 70, -10)]:
            with self.subTest(args=args), self.assertRaises(ValueError):
                calcular_balanco_energia(*args)


if __name__ == "__main__":
    unittest.main()
