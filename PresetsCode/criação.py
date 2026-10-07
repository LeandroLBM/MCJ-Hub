import json
from pathlib import Path


def criacao_preset(menu):

    pasta_presets = Path("MJH_Presets")

    pasta_presets.mkdir(exist_ok=True)

    acoes_preset = []

    menu(
        gravar_preset=True,
        acoes_preset=acoes_preset
    )

    print("\nAções registradas:")

    for acao in acoes_preset:
        print(acao)

    nome_preset = input(
        "\nDigite o nome do preset: "
    ).strip()

    if not nome_preset:
        print("\nO nome do preset não pode estar vazio.")
        input("\nPressione ENTER para continuar.")
        return

    nome_arquivo = pasta_presets / f"{nome_preset}.json"

    dados_preset = {
        "nome": nome_preset,
        "acoes": acoes_preset
    }

    try:

        with open(
            nome_arquivo,
            "w",
            encoding="utf-8"
        ) as arquivo:

            json.dump(
                dados_preset,
                arquivo,
                ensure_ascii=False,
                indent=4
            )

        print("\nPreset criado com sucesso!")
        print(f"Nome: {nome_preset}")
        print(f"Local: {nome_arquivo}")

    except Exception as erro:

        print("\nNão foi possível salvar o preset.")
        print(f"Detalhes: {erro}")

    input("\nPressione ENTER para continuar.")