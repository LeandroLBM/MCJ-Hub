import os
import sys

from pathlib import Path


def criacao_preset(menu):

    pasta_presets = Path("MJH_Presest")

    pasta_presets.mkdir(exist_ok=True)

    menu(
        gravar_preset=True,
        acoes_preset=acoes_preset
    )

    print("\nAções registradas:")

    for acao in acoes_preset:
            print(acao)

    input("\nENTER para continuar.")

acoes_preset = []
