"""Testes integrados do sistema e da interface de linha de comando (issue #10)."""

from copy import deepcopy
import json
from math import isclose
from pathlib import Path
import subprocess
import sys
import tempfile
from types import MappingProxyType
import unittest
from unittest.mock import patch

from src.apresentacao import formatar_resultado
from src.dados import buscar_subsistema, carregar_cenarios, carregar_historico
from src.sistema import executar_cenario


RAIZ = Path(__file__).resolve().parent.parent
MAIN_PY = RAIZ / "main.py"
CAMINHO_CENARIOS = RAIZ / "dados" / "cenarios.json"
CAMINHO_HISTORICO = RAIZ / "dados" / "historico_eolico.json"
CHAVES_ENVELOPE = {
    "erro",
    "cenario",
    "balanco",
    "previsao",
    "erro_previsao",
    "decisao",
}


class TestIntegracaoSistema(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cenarios_lista = carregar_cenarios(CAMINHO_CENARIOS)
        cls.cenarios = {item["id"]: item for item in cls.cenarios_lista}
        cls.historico = carregar_historico(CAMINHO_HISTORICO)

    def test_envelope_seis_chaves_em_todos_os_cenarios_versionados(self):
        for cenario in self.cenarios_lista:
            with self.subTest(cenario=cenario["id"]):
                resultado = executar_cenario(cenario, self.historico)
                self.assertEqual(set(resultado), CHAVES_ENVELOPE)
                self.assertIsNone(resultado["erro"])
                self.assertIsNone(resultado["erro_previsao"])
                self.assertIsNotNone(resultado["cenario"])
                self.assertIsNotNone(resultado["balanco"])
                self.assertIsNotNone(resultado["previsao"])
                self.assertIsNotNone(resultado["decisao"])
                texto = formatar_resultado(resultado)
                self.assertIn(f"Cenário {cenario['id']}", texto)

    def test_cenario_nominal(self):
        resultado = executar_cenario(self.cenarios["nominal"], self.historico)
        self.assertIsNone(resultado["erro"])
        self.assertEqual(resultado["balanco"]["geracao_total_kwh"], 60.0)
        self.assertEqual(resultado["balanco"]["consumo_total_kwh"], 50.0)
        self.assertEqual(resultado["balanco"]["saldo_kwh"], 10.0)
        self.assertEqual(resultado["balanco"]["classificacao"], "excedente")
        self.assertEqual(resultado["decisao"]["status"], "excedente")
        self.assertTrue(
            isclose(
                resultado["previsao"]["energia_eolica_prevista_kwh"],
                25.0,
                rel_tol=1e-9,
                abs_tol=1e-9,
            )
        )
        self.assertIn("saldo futuro de 10 kWh", resultado["decisao"]["recomendacao_futura"])

    def test_cenario_deficit_contrato(self):
        resultado = executar_cenario(self.cenarios["deficit"], self.historico)
        self.assertIsNone(resultado["erro"])
        balanco = resultado["balanco"]
        self.assertEqual(balanco["geracao_total_kwh"], 40.0)
        self.assertEqual(balanco["consumo_total_kwh"], 70.0)
        self.assertEqual(balanco["consumo_essencial_kwh"], 35.0)
        self.assertEqual(balanco["saldo_kwh"], -30.0)
        self.assertEqual(balanco["classificacao"], "deficit")
        self.assertEqual(balanco["reserva_usada_kwh"], 15.0)
        self.assertEqual(balanco["deficit_remanescente_kwh"], 15.0)

        previsao = resultado["previsao"]
        self.assertTrue(isclose(previsao["a"], 2.5, rel_tol=1e-9, abs_tol=1e-9))
        self.assertTrue(isclose(previsao["b"], 0.0, rel_tol=1e-9, abs_tol=1e-9))
        self.assertTrue(
            isclose(
                previsao["energia_eolica_prevista_kwh"],
                27.5,
                rel_tol=1e-9,
                abs_tol=1e-9,
            )
        )
        self.assertFalse(previsao["extrapolacao"])
        self.assertIsNone(previsao["aviso"])

        decisao = resultado["decisao"]
        self.assertEqual(decisao["status"], "alerta_deficit")
        self.assertIn("-22,5 kWh", decisao["recomendacao_futura"])
        self.assertIn("Reserva restante hipotética: 0 kWh", decisao["recomendacao_futura"])

    def test_cenario_excedente(self):
        resultado = executar_cenario(self.cenarios["excedente"], self.historico)
        self.assertIsNone(resultado["erro"])
        self.assertEqual(resultado["balanco"]["geracao_total_kwh"], 80.0)
        self.assertEqual(resultado["balanco"]["consumo_total_kwh"], 30.0)
        self.assertEqual(resultado["balanco"]["saldo_kwh"], 50.0)
        self.assertEqual(resultado["balanco"]["classificacao"], "excedente")
        self.assertEqual(resultado["balanco"]["reserva_usada_kwh"], 0.0)
        self.assertEqual(resultado["decisao"]["status"], "excedente")
        self.assertTrue(
            any("armazenamento" in acao["acao"].lower() for acao in resultado["decisao"]["acoes"])
        )

    def test_cenario_equilibrio(self):
        resultado = executar_cenario(self.cenarios["equilibrio"], self.historico)
        self.assertIsNone(resultado["erro"])
        self.assertEqual(resultado["balanco"]["geracao_total_kwh"], 50.0)
        self.assertEqual(resultado["balanco"]["consumo_total_kwh"], 50.0)
        self.assertEqual(resultado["balanco"]["saldo_kwh"], 0.0)
        self.assertEqual(resultado["balanco"]["classificacao"], "equilibrio")
        self.assertEqual(resultado["balanco"]["reserva_usada_kwh"], 0.0)
        self.assertEqual(resultado["decisao"]["status"], "equilibrio")

    def test_cenario_essenciais_insuficientes_e_fronteira(self):
        critico = executar_cenario(self.cenarios["alerta_critico"], self.historico)
        self.assertIsNone(critico["erro"])
        self.assertEqual(critico["decisao"]["status"], "alerta_critico")
        textos_acoes = [acao["acao"] for acao in critico["decisao"]["acoes"]]
        self.assertIn("Preservar Suporte à vida", textos_acoes)
        self.assertTrue(any("intervenção humana" in texto.lower() for texto in textos_acoes))
        self.assertFalse(
            any(
                "redução" in texto.lower() and "suporte à vida" in texto.lower()
                for texto in textos_acoes
            )
        )
        self.assertTrue(
            any("faltam 20 kWh" in acao["motivo"] for acao in critico["decisao"]["acoes"])
        )

        fronteira = executar_cenario(self.cenarios["fronteira_essencial"], self.historico)
        self.assertIsNone(fronteira["erro"])
        self.assertEqual(fronteira["decisao"]["status"], "alerta_deficit")
        self.assertTrue(
            any(
                acao["acao"] == "Sinalizar dependência da reserva"
                for acao in fronteira["decisao"]["acoes"]
            )
        )

    def test_dois_ventos_mudam_recomendacao_futura_sem_mudar_balanco_atual(self):
        baixo = executar_cenario(self.cenarios["vento_baixo"], self.historico)
        alto = executar_cenario(self.cenarios["vento_alto"], self.historico)

        self.assertEqual(baixo["balanco"], alto["balanco"])
        self.assertEqual(baixo["balanco"]["saldo_kwh"], -10.0)
        self.assertEqual(baixo["decisao"]["status"], "alerta_deficit")
        self.assertEqual(alto["decisao"]["status"], "alerta_deficit")
        self.assertEqual(baixo["decisao"]["acoes"], alto["decisao"]["acoes"])

        self.assertTrue(
            isclose(
                baixo["previsao"]["energia_eolica_prevista_kwh"],
                20.0,
                rel_tol=1e-9,
                abs_tol=1e-9,
            )
        )
        self.assertTrue(
            isclose(
                alto["previsao"]["energia_eolica_prevista_kwh"],
                30.0,
                rel_tol=1e-9,
                abs_tol=1e-9,
            )
        )
        self.assertNotEqual(
            baixo["decisao"]["recomendacao_futura"],
            alto["decisao"]["recomendacao_futura"],
        )
        self.assertIn("-10 kWh", baixo["decisao"]["recomendacao_futura"])
        self.assertIn("saldo futuro de 0 kWh", alto["decisao"]["recomendacao_futura"])

    def test_consulta_hierarquica_real_solar_e_eolico(self):
        cenario = deepcopy(self.cenarios["nominal"])
        with patch("src.sistema.buscar_subsistema", wraps=buscar_subsistema) as spy:
            resultado = executar_cenario(cenario, self.historico)
            self.assertIsNone(resultado["erro"])
            caminhos_consultados = [chamada.args[1] for chamada in spy.call_args_list]
            self.assertIn(["colonia", "energia", "solar"], caminhos_consultados)
            self.assertIn(["colonia", "energia", "eolico"], caminhos_consultados)

        with patch("src.sistema.buscar_subsistema", side_effect=[{}, None]):
            ausente = executar_cenario(cenario, self.historico)
            self.assertEqual(set(ausente), CHAVES_ENVELOPE)
            self.assertIsNotNone(ausente["erro"])
            self.assertIsNone(ausente["decisao"])

    def test_preservacao_de_entradas_e_normalizacao_sem_mutacao(self):
        cenario_sem_intervalo = deepcopy(self.cenarios["deficit"])
        del cenario_sem_intervalo["intervalo_h"]
        historico_sem_intervalo = {
            "vento_ms": [8.0, 10.0, 12.0],
            "energia_eolica_kwh": [20.0, 25.0, 30.0],
        }
        copia_cenario = deepcopy(cenario_sem_intervalo)
        copia_historico = deepcopy(historico_sem_intervalo)

        resultado = executar_cenario(cenario_sem_intervalo, historico_sem_intervalo)

        self.assertEqual(cenario_sem_intervalo, copia_cenario)
        self.assertEqual(historico_sem_intervalo, copia_historico)
        self.assertNotIn("intervalo_h", cenario_sem_intervalo)
        self.assertNotIn("intervalo_h", historico_sem_intervalo)
        self.assertIsNone(resultado["erro"])
        self.assertEqual(resultado["cenario"]["intervalo_h"], 1.0)
        self.assertIsNot(resultado["cenario"], cenario_sem_intervalo)
        self.assertIsNot(
            resultado["cenario"]["sistemas"], cenario_sem_intervalo["sistemas"]
        )


class TestErrosEFronteirasSistema(unittest.TestCase):
    def setUp(self):
        self.cenario_valido = carregar_cenarios(CAMINHO_CENARIOS)[1]  # deficit
        self.historico_valido = carregar_historico(CAMINHO_HISTORICO)

    def _assert_erro_cenario(self, resultado):
        self.assertEqual(set(resultado), CHAVES_ENVELOPE)
        self.assertIsInstance(resultado["erro"], str)
        self.assertTrue(resultado["erro"].strip())
        self.assertIsNone(resultado["cenario"])
        self.assertIsNone(resultado["balanco"])
        self.assertIsNone(resultado["previsao"])
        self.assertIsNone(resultado["erro_previsao"])
        self.assertIsNone(resultado["decisao"])

    def _assert_apenas_erro_previsao(self, resultado, status_esperado="alerta_deficit"):
        self.assertEqual(set(resultado), CHAVES_ENVELOPE)
        self.assertIsNone(resultado["erro"])
        self.assertIsNotNone(resultado["cenario"])
        self.assertIsNotNone(resultado["balanco"])
        self.assertIsNone(resultado["previsao"])
        self.assertIsInstance(resultado["erro_previsao"], str)
        self.assertTrue(resultado["erro_previsao"].strip())
        self.assertEqual(resultado["decisao"]["status"], status_esperado)
        self.assertIsNone(resultado["decisao"]["recomendacao_futura"])

    def test_cenarios_invalidos_retornam_erro_sem_decisao(self):
        sem_id = deepcopy(self.cenario_valido)
        del sem_id["id"]

        energia_bool = deepcopy(self.cenario_valido)
        energia_bool["geracao_solar_kwh"] = True

        energia_nan = deepcopy(self.cenario_valido)
        energia_nan["geracao_eolica_kwh"] = float("nan")

        energia_inf = deepcopy(self.cenario_valido)
        energia_inf["reserva_kwh"] = float("inf")

        energia_negativa = deepcopy(self.cenario_valido)
        energia_negativa["geracao_solar_kwh"] = -5.0

        intervalo_zero = deepcopy(self.cenario_valido)
        intervalo_zero["intervalo_h"] = 0

        intervalo_nulo = deepcopy(self.cenario_valido)
        intervalo_nulo["intervalo_h"] = None

        ids_duplicados = deepcopy(self.cenario_valido)
        ids_duplicados["sistemas"][1]["id"] = "suporte_vida"

        suporte_nao_essencial = deepcopy(self.cenario_valido)
        suporte_nao_essencial["sistemas"][0]["essencial"] = False

        folha_proxy = deepcopy(self.cenario_valido)
        folha_proxy["hierarquia"]["colonia"]["energia"]["solar"] = MappingProxyType({})

        casos = [
            ("none", None),
            ("lista", []),
            ("sem_id", sem_id),
            ("energia_bool", energia_bool),
            ("energia_nan", energia_nan),
            ("energia_inf", energia_inf),
            ("energia_negativa", energia_negativa),
            ("intervalo_zero", intervalo_zero),
            ("intervalo_nulo", intervalo_nulo),
            ("ids_duplicados", ids_duplicados),
            ("suporte_nao_essencial", suporte_nao_essencial),
            ("folha_proxy", folha_proxy),
        ]
        for nome, invalido in casos:
            with self.subTest(caso=nome):
                resultado = executar_cenario(invalido, self.historico_valido)
                self._assert_erro_cenario(resultado)

    def test_calculo_observado_invalido_por_escala_retorna_erro_sem_decisao(self):
        soma_geracao_infinita = deepcopy(self.cenario_valido)
        soma_geracao_infinita["geracao_solar_kwh"] = 1e308
        soma_geracao_infinita["geracao_eolica_kwh"] = 1e308

        soma_consumo_infinita = deepcopy(self.cenario_valido)
        soma_consumo_infinita["sistemas"][0]["consumo_kwh"] = 1e308
        soma_consumo_infinita["sistemas"][1]["consumo_kwh"] = 1e308

        for nome, cenario in (
            ("geracao_overflow", soma_geracao_infinita),
            ("consumo_overflow", soma_consumo_infinita),
        ):
            with self.subTest(caso=nome):
                resultado = executar_cenario(cenario, self.historico_valido)
                self._assert_erro_cenario(resultado)

    def test_historico_ausente_malformado_degenerado_duracao_e_falha_numerica(self):
        casos = [
            ("ausente_none", None),
            ("nao_dict_lista", [8.0, 10.0]),
            ("vazio", {}),
            (
                "despareado",
                {"intervalo_h": 1.0, "vento_ms": [8.0, 10.0], "energia_eolica_kwh": [20.0]},
            ),
            (
                "um_par",
                {"intervalo_h": 1.0, "vento_ms": [8.0], "energia_eolica_kwh": [20.0]},
            ),
            (
                "booleano_na_serie",
                {
                    "intervalo_h": 1.0,
                    "vento_ms": [8.0, True],
                    "energia_eolica_kwh": [20.0, 25.0],
                },
            ),
            (
                "vento_constante_degenerado",
                {
                    "intervalo_h": 1.0,
                    "vento_ms": [10.0, 10.0, 10.0],
                    "energia_eolica_kwh": [20.0, 25.0, 30.0],
                },
            ),
            (
                "duracao_incompativel",
                {
                    "intervalo_h": 2.0,
                    "vento_ms": [8.0, 10.0, 12.0],
                    "energia_eolica_kwh": [20.0, 25.0, 30.0],
                },
            ),
            (
                "intervalo_historico_invalido_zero",
                {
                    "intervalo_h": 0,
                    "vento_ms": [8.0, 10.0, 12.0],
                    "energia_eolica_kwh": [20.0, 25.0, 30.0],
                },
            ),
            (
                "falha_numerica_regressao",
                {
                    "intervalo_h": 1.0,
                    "vento_ms": [0.0, 1e308],
                    "energia_eolica_kwh": [0.0, 1e308],
                },
            ),
        ]
        for nome, historico in casos:
            with self.subTest(caso=nome):
                resultado = executar_cenario(self.cenario_valido, historico)
                self._assert_apenas_erro_previsao(resultado)

        cenario_2h = deepcopy(self.cenario_valido)
        cenario_2h["intervalo_h"] = 2.0
        historico_sem_intervalo = {
            "vento_ms": [8.0, 10.0, 12.0],
            "energia_eolica_kwh": [20.0, 25.0, 30.0],
        }
        resultado_2h = executar_cenario(cenario_2h, historico_sem_intervalo)
        self._assert_apenas_erro_previsao(resultado_2h)
        self.assertIn("incompatível", resultado_2h["erro_previsao"])

        cenario_limite = deepcopy(self.cenario_valido)
        cenario_limite["geracao_solar_kwh"] = 1e308
        cenario_limite["geracao_eolica_kwh"] = 0.0
        cenario_limite["reserva_kwh"] = 0.0
        cenario_limite["vento_previsto_ms"] = 2.0
        cenario_limite["sistemas"][0]["consumo_kwh"] = 1e308
        cenario_limite["sistemas"][1]["consumo_kwh"] = 0.0
        historico_grande = {
            "intervalo_h": 1.0,
            "vento_ms": [1.0, 2.0],
            "energia_eolica_kwh": [5e307, 1e308],
        }
        resultado_limite = executar_cenario(cenario_limite, historico_grande)
        self._assert_apenas_erro_previsao(resultado_limite, status_esperado="equilibrio")

    def test_estimativa_negativa_preservada_com_aviso_sem_planejamento_fisico_invalido(self):
        cenario = deepcopy(self.cenario_valido)
        cenario["vento_previsto_ms"] = 0.0
        historico = {
            "intervalo_h": 1.0,
            "vento_ms": [2.0, 4.0],
            "energia_eolica_kwh": [1.0, 3.0],
        }

        resultado = executar_cenario(cenario, historico)

        self.assertEqual(set(resultado), CHAVES_ENVELOPE)
        self.assertIsNone(resultado["erro"])
        self.assertIsNone(resultado["erro_previsao"])
        self.assertIsNotNone(resultado["previsao"])
        self.assertTrue(
            isclose(
                resultado["previsao"]["energia_eolica_prevista_kwh"],
                -1.0,
                rel_tol=1e-9,
                abs_tol=1e-9,
            )
        )
        self.assertTrue(resultado["previsao"]["extrapolacao"])
        self.assertIn("fisicamente inválido", resultado["previsao"]["aviso"])
        self.assertEqual(resultado["decisao"]["status"], "alerta_deficit")
        self.assertIsNone(resultado["decisao"]["recomendacao_futura"])
        self.assertTrue(
            any("-1 kWh" in acao["motivo"] for acao in resultado["decisao"]["acoes"])
        )

        texto = formatar_resultado(resultado)
        self.assertIn("-1 kWh", texto)
        self.assertIn("fisicamente inválido", texto)
        self.assertIn("Recomendação futura indisponível.", texto)

    def test_nao_mascara_keyerror_de_defeito_interno(self):
        with patch("src.sistema.ajustar_reta", return_value={"b": 0.0}):
            with self.assertRaises(KeyError):
                executar_cenario(self.cenario_valido, self.historico_valido)


class TestCliMainSubprocess(unittest.TestCase):
    def _executar_cli(self, *args, cwd=RAIZ):
        return subprocess.run(
            [sys.executable, str(MAIN_PY), *args],
            cwd=str(cwd),
            capture_output=True,
            text=True,
            check=False,
        )

    def test_cli_listar_e_cenario_com_arquivos_temporarios(self):
        cenarios = carregar_cenarios(CAMINHO_CENARIOS)[:2]  # nominal e deficit
        historico = carregar_historico(CAMINHO_HISTORICO)

        with tempfile.TemporaryDirectory() as pasta:
            arq_cenarios = Path(pasta) / "cenarios_temp.json"
            arq_historico = Path(pasta) / "historico_temp.json"
            arq_cenarios.write_text(json.dumps(cenarios), encoding="utf-8")
            arq_historico.write_text(json.dumps(historico), encoding="utf-8")

            listagem = self._executar_cli("--listar", "--cenarios", str(arq_cenarios))
            self.assertEqual(listagem.returncode, 0, msg=listagem.stderr)
            self.assertEqual(listagem.stdout.strip().splitlines(), ["nominal", "deficit"])

            execucao = self._executar_cli(
                "--cenario",
                "deficit",
                "--cenarios",
                str(arq_cenarios),
                "--historico",
                str(arq_historico),
            )
            self.assertEqual(execucao.returncode, 0, msg=execucao.stderr)
            self.assertIn("Cenário deficit", execucao.stdout)
            self.assertIn("Saldo: -30 kWh (deficit)", execucao.stdout)
            self.assertIn("Estado atual: alerta_deficit", execucao.stdout)
            self.assertIn("Geração eólica estimada: 27,5 kWh", execucao.stdout)
            self.assertIn("-22,5 kWh", execucao.stdout)

    def test_cli_erros_cenario_inexistente_arquivo_ausente_e_json_invalido(self):
        with tempfile.TemporaryDirectory() as pasta:
            ausente = Path(pasta) / "nao_existe.json"
            corrompido = Path(pasta) / "invalido.json"
            corrompido.write_text("{json quebrado", encoding="utf-8")

            inexistente = self._executar_cli("--cenario", "inexistente")
            self.assertNotEqual(inexistente.returncode, 0)
            self.assertIn("Erro de entrada:", inexistente.stdout)
            self.assertIn("inexistente", inexistente.stdout)

            arq_ausente = self._executar_cli(
                "--cenario", "deficit", "--cenarios", str(ausente)
            )
            self.assertNotEqual(arq_ausente.returncode, 0)
            self.assertIn("Erro de entrada:", arq_ausente.stdout)

            json_ruim = self._executar_cli("--listar", "--cenarios", str(corrompido))
            self.assertNotEqual(json_ruim.returncode, 0)
            self.assertIn("Erro de entrada:", json_ruim.stdout)

    def test_cli_historico_ausente_ou_invalido_mantem_resultado_atual(self):
        cenarios = carregar_cenarios(CAMINHO_CENARIOS)
        with tempfile.TemporaryDirectory() as pasta:
            arq_cenarios = Path(pasta) / "cenarios.json"
            arq_cenarios.write_text(json.dumps(cenarios), encoding="utf-8")
            hist_ausente = Path(pasta) / "historico_ausente.json"
            hist_invalido = Path(pasta) / "historico_invalido.json"
            hist_invalido.write_text(
                json.dumps({"intervalo_h": 1.0, "vento_ms": [5.0, 5.0], "energia_eolica_kwh": [10.0, 12.0]}),
                encoding="utf-8",
            )

            for caminho_hist in (hist_ausente, hist_invalido):
                with self.subTest(historico=caminho_hist.name):
                    res = self._executar_cli(
                        "--cenario",
                        "deficit",
                        "--cenarios",
                        str(arq_cenarios),
                        "--historico",
                        str(caminho_hist),
                    )
                    self.assertEqual(res.returncode, 0, msg=res.stderr)
                    self.assertIn("Saldo: -30 kWh (deficit)", res.stdout)
                    self.assertIn("Estado atual: alerta_deficit", res.stdout)
                    self.assertIn(
                        "Previsão eólica indisponível: Não foi possível carregar histórico eólico:",
                        res.stdout,
                    )
                    self.assertIn("Recomendação futura indisponível.", res.stdout)

    def test_import_main_sem_execucao(self):
        proc = subprocess.run(
            [sys.executable, "-c", "import main"],
            cwd=str(RAIZ),
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, msg=proc.stderr)
        self.assertEqual(proc.stdout, "")
        self.assertEqual(proc.stderr, "")

    def test_cli_execucao_fora_da_raiz(self):
        with tempfile.TemporaryDirectory() as pasta_externa:
            listagem = self._executar_cli("--listar", cwd=pasta_externa)
            self.assertEqual(listagem.returncode, 0, msg=listagem.stderr)
            self.assertIn("deficit", listagem.stdout.splitlines())
            self.assertIn("nominal", listagem.stdout.splitlines())

            execucao = self._executar_cli(
                "--cenario", "deficit", cwd=pasta_externa
            )
            self.assertEqual(execucao.returncode, 0, msg=execucao.stderr)
            self.assertIn("Cenário deficit", execucao.stdout)
            self.assertIn("Geração eólica estimada: 27,5 kWh", execucao.stdout)


if __name__ == "__main__":
    unittest.main()
