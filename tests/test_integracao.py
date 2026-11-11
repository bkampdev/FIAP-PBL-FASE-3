
"""Testes complementares da revisão final — Issue #11."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


RAIZ = Path(__file__).resolve().parents[1]
PROGRAMA = RAIZ / "main.py"


def executar_programa(*argumentos):
    """Executa o programa usando UTF-8 para preservar acentos."""
    return subprocess.run(
        [sys.executable, "-X", "utf8", str(PROGRAMA), *argumentos],
        cwd=RAIZ,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="strict",
        timeout=30,
        check=False,
    )


class TestRevisaoIntegracao(unittest.TestCase):

    def test_deficit_preserva_suporte_vida(self):
        resultado = executar_programa("--cenario", "deficit")

        self.assertEqual(
            resultado.returncode, 0,
            msg=resultado.stderr,
        )
        self.assertIn(
            "Saldo: -30 kWh",
            resultado.stdout,
        )
        self.assertIn(
            "Preservar Suporte à vida",
            resultado.stdout,
        )
        self.assertIn(
            "Geração eólica estimada: 27,5 kWh",
            resultado.stdout,
        )

    def test_alerta_critico_sinalizado(self):
        resultado = executar_programa(
            "--cenario", "alerta_critico"
        )

        self.assertEqual(
            resultado.returncode, 0,
            msg=resultado.stderr,
        )
        self.assertIn(
            "Estado atual: alerta_critico",
            resultado.stdout,
        )
        self.assertIn(
            "Suporte à vida",
            resultado.stdout,
        )
        self.assertIn(
            "Acionar intervenção humana imediata",
            resultado.stdout,
        )

    def test_cenario_inexistente_rejeitado(self):
        resultado = executar_programa(
            "--cenario", "cenario_que_nao_existe"
        )

        self.assertNotEqual(
            resultado.returncode,
            0,
        )

    def test_consumo_negativo_no_json_rejeitado_sem_resultado_ficticio(self):
        for indice in (0, 1):
            with self.subTest(sistema=indice), tempfile.TemporaryDirectory() as pasta:
                cenarios = json.loads(
                    (RAIZ / "dados" / "cenarios.json").read_text(encoding="utf-8")
                )
                cenario = next(item for item in cenarios if item["id"] == "deficit")
                cenario["sistemas"][indice]["consumo_kwh"] = -5
                caminho = Path(pasta) / "cenarios_invalidos.json"
                caminho.write_text(
                    json.dumps([cenario], ensure_ascii=False), encoding="utf-8"
                )

                resultado = executar_programa(
                    "--cenario", "deficit", "--cenarios", str(caminho)
                )

                self.assertEqual(resultado.returncode, 1, msg=resultado.stderr)
                self.assertIn("Erro de entrada:", resultado.stdout)
                self.assertIn("consumo_kwh", resultado.stdout)
                for trecho in ("Saldo:", "Estado atual:", "Geração eólica estimada:"):
                    self.assertNotIn(trecho, resultado.stdout)
                self.assertEqual(resultado.stderr, "")


if __name__ == "__main__":
    unittest.main()
