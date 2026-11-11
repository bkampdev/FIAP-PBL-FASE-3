
"""Testes do módulo de dados da colônia marciana."""

import copy
import json
import tempfile
import unittest
from pathlib import Path
from types import MappingProxyType

from src.dados import (
    buscar_subsistema,
    carregar_cenarios,
    carregar_historico,
    numero_valido,
    validar_cenario,
    validar_historico,
)


def cenario_exemplo():
    return {
        "id": "nominal",
        "intervalo_h": 1.0,
        "geracao_solar_kwh": 20.0,
        "geracao_eolica_kwh": 30.0,
        "reserva_kwh": 15.0,
        "vento_previsto_ms": 6.0,
        "sistemas": [
            {
                "id": "suporte_vida",
                "nome": "Suporte à vida",
                "consumo_kwh": 30.0,
                "essencial": True,
                "prioridade": 1,
            },
            {
                "id": "laboratorio",
                "nome": "Laboratório",
                "consumo_kwh": 15.0,
                "essencial": False,
                "prioridade": 2,
            },
        ],
        "hierarquia": {
            "colonia": {
                "energia": {
                    "solar": {},
                    "eolico": {},
                },
                "consumidores": {
                    "suporte_vida": {},
                    "laboratorio": {},
                },
            }
        },
    }


class TestDados(unittest.TestCase):

    def test_cenario_valido(self):
        self.assertEqual(validar_cenario(cenario_exemplo()), [])

    def test_rejeita_folhas_que_comparam_igual_a_dict_mas_nao_sao_dict(self):
        for grupo, identificador in (
            ("energia", "solar"),
            ("energia", "eolico"),
            ("consumidores", "suporte_vida"),
            ("consumidores", "laboratorio"),
        ):
            with self.subTest(grupo=grupo, identificador=identificador):
                cenario = cenario_exemplo()
                cenario["hierarquia"]["colonia"][grupo][identificador] = (
                    MappingProxyType({})
                )
                erros = validar_cenario(cenario)
                self.assertTrue(erros)
                self.assertTrue(any(identificador in erro for erro in erros))

    def test_deficit_e_valido(self):
        cenario = cenario_exemplo()
        cenario["geracao_solar_kwh"] = 0
        cenario["geracao_eolica_kwh"] = 0
        self.assertEqual(validar_cenario(cenario), [])

    def test_campo_obrigatorio_ausente(self):
        cenario = cenario_exemplo()
        del cenario["id"]
        self.assertTrue(validar_cenario(cenario))

    def test_valor_negativo(self):
        cenario = cenario_exemplo()
        cenario["geracao_solar_kwh"] = -10
        self.assertTrue(validar_cenario(cenario))

    def test_booleano_nao_e_numero(self):
        self.assertFalse(numero_valido(True))
        cenario = cenario_exemplo()
        cenario["geracao_eolica_kwh"] = True
        self.assertTrue(validar_cenario(cenario))

    def test_numero_infinito(self):
        self.assertFalse(numero_valido(float("inf")))
        self.assertFalse(numero_valido(float("nan")))

    def test_intervalo_zero(self):
        cenario = cenario_exemplo()
        cenario["intervalo_h"] = 0
        self.assertTrue(validar_cenario(cenario))

    def test_id_duplicado(self):
        cenario = cenario_exemplo()
        cenario["sistemas"][1]["id"] = "suporte_vida"
        self.assertTrue(validar_cenario(cenario))

    def test_suporte_vida_obrigatorio(self):
        cenario = cenario_exemplo()
        cenario["sistemas"][0]["id"] = "outro"
        self.assertTrue(validar_cenario(cenario))

    def test_consulta_solar(self):
        hierarquia = cenario_exemplo()["hierarquia"]
        resultado = buscar_subsistema(
            hierarquia, ["colonia", "energia", "solar"]
        )
        self.assertEqual(resultado, {})

    def test_consulta_eolica(self):
        hierarquia = cenario_exemplo()["hierarquia"]
        resultado = buscar_subsistema(
            hierarquia, ["colonia", "energia", "eolico"]
        )
        self.assertEqual(resultado, {})

    def test_caminho_inexistente(self):
        hierarquia = cenario_exemplo()["hierarquia"]
        resultado = buscar_subsistema(
            hierarquia, ["colonia", "energia", "nuclear"]
        )
        self.assertIsNone(resultado)

    def test_nao_modifica_entrada(self):
        cenario = cenario_exemplo()
        original = copy.deepcopy(cenario)
        validar_cenario(cenario)
        self.assertEqual(cenario, original)

    def test_historico_valido(self):
        historico = {
            "intervalo_h": 1,
            "vento_ms": [2, 4, 6, 8],
            "energia_eolica_kwh": [10, 20, 30, 40],
        }
        self.assertEqual(validar_historico(historico), [])

    def test_historico_despareado(self):
        historico = {
            "intervalo_h": 1,
            "vento_ms": [2, 4, 6],
            "energia_eolica_kwh": [10, 20],
        }
        self.assertTrue(validar_historico(historico))

    def test_carregar_json(self):
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "cenarios.json"
            caminho.write_text(
                json.dumps([cenario_exemplo()]),
                encoding="utf-8",
            )
            resultado = carregar_cenarios(caminho)
            self.assertEqual(len(resultado), 1)
            self.assertEqual(resultado[0]["id"], "nominal")

    def test_carregar_historico(self):
        historico = {
            "intervalo_h": 1,
            "vento_ms": [2, 4, 6],
            "energia_eolica_kwh": [10, 20, 30],
        }
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "historico.json"
            caminho.write_text(
                json.dumps(historico),
                encoding="utf-8",
            )
            resultado = carregar_historico(caminho)
            self.assertEqual(resultado, historico)


if __name__ == "__main__":
    unittest.main()
