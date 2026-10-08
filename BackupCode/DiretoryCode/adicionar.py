import os
import json

from pathlib import Path


def adicionar_diretorio():

    pasta_presets = Path("MJH_Presets")
    pasta_diretorios = pasta_presets / "Diretórios"

    pasta_diretorios.mkdir(
        parents=True,
        exist_ok=True
    )

    os.system("cls")

    print("========== ADICIONAR DIRETÓRIO ==========\n")

    nome = input(
        "Digite um nome para o diretório (opcional): "
    ).strip()

    caminho = input(
        "\nInforme o caminho do diretório: "
    ).strip()

    if not caminho:

        print("\nO caminho não pode estar vazio.")

        input("\nPressione ENTER para continuar.")

        return

    pasta = Path(caminho)

    if not pasta.is_dir():

        print("\nO diretório informado não existe.")

        input("\nPressione ENTER para continuar.")

        return

    if not nome:

        numero = 1

        while True:

            nome_gerado = f"Diretorio_{numero}"

            arquivo_diretorio = (
                pasta_diretorios /
                f"{nome_gerado}.json"
            )

            if not arquivo_diretorio.exists():

                nome = nome_gerado

                break

            numero += 1

    else:

        arquivo_diretorio = (
            pasta_diretorios /
            f"{nome}.json"
        )

        if arquivo_diretorio.exists():

            print(
                "\nJá existe um diretório salvo "
                f"com o nome '{nome}'."
            )

            input("\nPressione ENTER para continuar.")

            return

    dados_diretorio = {
        "nome": nome,
        "caminho": str(pasta)
    }

    try:

        with open(
            arquivo_diretorio,
            "w",
            encoding="utf-8"
        ) as arquivo:

            json.dump(
                dados_diretorio,
                arquivo,
                ensure_ascii=False,
                indent=4
            )

        print("\nDiretório adicionado com sucesso!")

        print(f"\nNome: {nome}")
        print(f"Caminho: {pasta}")

    except Exception as erro:

        print("\nNão foi possível salvar o diretório.")
        print(f"Detalhes: {erro}")

    input("\nPressione ENTER para continuar.")