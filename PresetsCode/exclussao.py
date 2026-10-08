import os
import json

from pathlib import Path


def exclucao_preset():

    pasta_presets = Path("MJH_Presets")

    if not pasta_presets.is_dir():
        print("\nNenhum preset foi encontrado.")
        input("\nPressione ENTER para continuar.")
        return

    presets = sorted(
        arquivo
        for arquivo in pasta_presets.iterdir()
        if arquivo.is_file()
        and arquivo.suffix == ".json"
    )

    if not presets:
        print("\nNenhum preset foi encontrado.")
        input("\nPressione ENTER para continuar.")
        return

    while True:

        os.system("cls")

        print("========== EXCLUIR PRESET ==========\n")
        print("0. Voltar\n")

        for indice, preset in enumerate(presets, start=1):
            print(f"{indice}. {preset.stem}")

        opcao = input("\nEscolha um preset: ").strip()

        if opcao == "0":
            return

        if not opcao.isdigit():
            print("\nOpção inválida.")
            input("\nPressione ENTER para continuar.")
            continue

        indice = int(opcao)

        if not 1 <= indice <= len(presets):
            print("\nOpção inválida.")
            input("\nPressione ENTER para continuar.")
            continue

        preset_escolhido = presets[indice - 1]

        os.system("cls")

        print("========== EXCLUIR PRESET ==========\n")
        print(f"Preset selecionado: {preset_escolhido.stem}")

        confirmacao = input(
            "\nDeseja realmente excluir este preset? (s/n): "
        ).strip().lower()

        if confirmacao == "s":

            try:

                preset_escolhido.unlink()

                print("\nPreset excluído com sucesso!")

                input("\nPressione ENTER para continuar.")

                presets.remove(preset_escolhido)

                if not presets:
                    return

            except Exception as erro:

                print("\nNão foi possível excluir o preset.")
                print(f"Detalhes: {erro}")

                input("\nPressione ENTER para continuar.")

        elif confirmacao == "n":

            print("\nOperação cancelada.")
            input("\nPressione ENTER para continuar.")

        else:

            print("\nOpção inválida.")
            input("\nPressione ENTER para continuar.")