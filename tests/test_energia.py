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

if __name__ == "__main__":
    unittest.main()