
"""Testes complementares da revisão final — Issue #11."""

import subprocess
import sys
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


if __name__ == "__main__":
    unittest.main()
