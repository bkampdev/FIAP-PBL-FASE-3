"""Entrada pelo terminal para o sistema didático da Colônia Aurora."""

import argparse
from pathlib import Path

from src.apresentacao import formatar_resultado


def main(argv=None):
    """Seleciona um cenário e retorna o código de saída, sem iniciar ao importar."""
    raiz = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description="Análise energética da Colônia Aurora")
    selecao = parser.add_mutually_exclusive_group(required=True)
    selecao.add_argument("--listar", action="store_true", help="listar cenários disponíveis")
    selecao.add_argument("--cenario", help="identificador do cenário a executar")
    parser.add_argument(
        "--cenarios", type=Path, default=raiz / "dados" / "cenarios.json",
        help="arquivo JSON de cenários",
    )
    parser.add_argument(
        "--historico", type=Path, default=raiz / "dados" / "historico_eolico.json",
        help="arquivo JSON do histórico eólico",
    )
    args = parser.parse_args(argv)

    from src.dados import carregar_cenarios, carregar_historico

    try:
        cenarios = carregar_cenarios(args.cenarios)
    except (OSError, ValueError) as erro:
        print(formatar_resultado({"erro": f"Não foi possível carregar cenários: {erro}"}))
        return 1

    if args.listar:
        for cenario in cenarios:
            print(cenario["id"])
        return 0

    cenario = next((item for item in cenarios if item["id"] == args.cenario), None)
    if cenario is None:
        print(formatar_resultado({"erro": f"Cenário inexistente: {args.cenario}. Use --listar."}))
        return 1

    erro_historico = None
    try:
        historico = carregar_historico(args.historico)
    except (OSError, ValueError) as erro:
        historico = None
        erro_historico = f"Não foi possível carregar histórico eólico: {erro}"

    from src.sistema import executar_cenario

    resultado = executar_cenario(cenario, historico)
    if erro_historico and not resultado["erro"]:
        resultado["erro_previsao"] = erro_historico
    print(formatar_resultado(resultado))
    return 1 if resultado["erro"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
