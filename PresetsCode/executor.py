import json
import os

from pathlib import Path


def carregar_preset(nome_preset):

    pasta_presets = Path("MJH_Presets")
    arquivo_preset = pasta_presets / f"{nome_preset}.json"

    if not arquivo_preset.is_file():

        print(
            f"\nO preset '{nome_preset}' não foi encontrado."
        )

        return None

    try:

        with open(
            arquivo_preset,
            "r",
            encoding="utf-8"
        ) as arquivo:

            dados_preset = json.load(arquivo)

        return dados_preset

    except json.JSONDecodeError as erro:

        print("\nNão foi possível ler o preset.")
        print("O arquivo possui um JSON inválido.")
        print(f"Detalhes: {erro}")

        return None

    except Exception as erro:

        print("\nNão foi possível carregar o preset.")
        print(f"Detalhes: {erro}")

        return None


def executar_preset(nome_preset):

    dados_preset = carregar_preset(nome_preset)

    if dados_preset is None:

        input("\nPressione ENTER para continuar.")
        return

    nome = dados_preset.get(
        "nome",
        nome_preset
    )

    acoes = dados_preset.get(
        "acoes",
        []
    )

    if not isinstance(acoes, list):

        print("\nO campo 'acoes' do preset é inválido.")

        input("\nPressione ENTER para continuar.")

        return

    if not acoes:

        print("\nEste preset não possui ações registradas.")

        input("\nPressione ENTER para continuar.")

        return

    os.system("cls")

    print("================================")
    print("       EXECUTANDO PRESET")
    print("================================")
    print()
    print(f"Preset: {nome}")
    print(f"Ações registradas: {len(acoes)}")
    print()

    input("Pressione ENTER para iniciar...")

    # Importação aqui evita importação circular
    from main import menu

    acoes_execucao = iter(acoes)

    menu(
        modo_execucao=True,
        acoes_execucao=acoes_execucao
    )


if __name__ == "__main__":

    nome_preset = input(
        "Digite o nome do preset: "
    ).strip()

    if nome_preset:

        executar_preset(nome_preset)

    else:

        print("\nNome do preset não informado.")