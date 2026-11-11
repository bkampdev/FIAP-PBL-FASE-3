import unittest
from copy import deepcopy

from src.apresentacao import formatar_resultado
from src.previsao import ajustar_reta, prever_energia


def resultado_de_teste(vento=11):
    """Simula os retornos do integrador enquanto a issue #10 estiver pendente."""
    modelo = ajustar_reta([8, 10, 12], [20, 25, 30])
    return {
        "cenario": {
            "id": "deficit",
            "intervalo_h": 1,
            "geracao_solar_kwh": 20,
            "geracao_eolica_kwh": 20,
            "reserva_kwh": 10,
            "sistemas": [
                {"nome": "Suporte à vida", "essencial": True},
                {"nome": "Laboratório", "essencial": False},
            ],
        },
        "balanco": {
            "geracao_total_kwh": 40,
            "consumo_total_kwh": 70,
            "saldo_kwh": -30,
            "classificacao": "déficit",
        },
        "previsao": prever_energia(modelo, vento),
        "decisao": {
            "status": "alerta de déficit",
            "acoes": [
                {"acao": "Reduzir a carga do laboratório", "motivo": "Priorizar suporte à vida"},
            ],
            "recomendacao_futura": "Planejar a redução de cargas não essenciais.",
        },
    }


class TestApresentacao(unittest.TestCase):
    def test_mostra_observacoes_estimativa_e_motivos_sem_mutar_entrada(self):
        resultado = resultado_de_teste()
        original = deepcopy(resultado)

        texto = formatar_resultado(resultado)

        for trecho in (
            "deficit",
            "1 h",
            "dados observados",
            "40 kWh",
            "70 kWh",
            "-30 kWh",
            "10 kWh",
            "Sistemas essenciais: Suporte à vida",
            "alerta de déficit",
            "Reduzir a carga do laboratório",
            "Priorizar suporte à vida",
            "estimativa",
            "11 m/s",
            "a = 2,5",
            "b = 0",
            "27,5 kWh",
            "Planejar a redução",
        ):
            with self.subTest(trecho=trecho):
                self.assertIn(trecho, texto)
        self.assertEqual(resultado, original)

    def test_exibe_aviso_de_extrapolacao(self):
        texto = formatar_resultado(resultado_de_teste(13))
        self.assertIn("fora da faixa histórica", texto)

    def test_erro_de_entrada_nao_apresenta_resultado(self):
        texto = formatar_resultado({"erro": "Cenário inexistente"})
        self.assertIn("Cenário inexistente", texto)
        self.assertNotIn("Intervalo atual", texto)
        self.assertNotIn("Geração eólica estimada", texto)

    def test_previsao_indisponivel_preserva_somente_os_dados_validos(self):
        resultado = resultado_de_teste()
        resultado["previsao"] = None
        resultado["erro_previsao"] = "histórico sem variação"
        resultado["decisao"]["recomendacao_futura"] = None

        texto = formatar_resultado(resultado)

        self.assertIn("Saldo: -30 kWh", texto)
        self.assertIn("Previsão eólica indisponível: histórico sem variação", texto)
        self.assertIn("Recomendação futura indisponível", texto)
        self.assertNotIn("Geração eólica estimada", texto)


if __name__ == "__main__":
    unittest.main()
