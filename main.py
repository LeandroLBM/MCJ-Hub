import os
import sys
import json

from pathlib import Path
from textwrap import dedent

from BackupCode.menu import menu_backup
from ModificationsCode.update_modifications import menu_update_modifications
from PresetsCode.menu import preset_menu
from PresetsCode.acoes import registrar_acao


def carregar_presets():

    pasta_presets = Path("MJH_Presets")

    if not pasta_presets.is_dir():
        return []

    presets = [
        arquivo.stem
        for arquivo in pasta_presets.iterdir()
        if arquivo.is_file()
        and arquivo.suffix.lower() == ".json"
    ]

    return sorted(presets)


def executar_preset(nome_preset):

    pasta_presets = Path("MJH_Presets")
    arquivo_preset = pasta_presets / f"{nome_preset}.json"

    if not arquivo_preset.is_file():

        print(
            f"\nO preset '{nome_preset}' não foi encontrado."
        )

        input("\nPressione ENTER para continuar.")

        return

    try:

        with open(
            arquivo_preset,
            "r",
            encoding="utf-8"
        ) as arquivo:

            dados_preset = json.load(arquivo)

        os.system("cls")

        print("========== EXECUTANDO PRESET ==========\n")

        print(
            f"Preset: "
            f"{dados_preset.get('nome', nome_preset)}"
        )

        print()

        acoes = dados_preset.get("acoes", [])

        if not acoes:

            print("Este preset não possui ações registradas.")

            input("\nPressione ENTER para continuar.")

            return

        print(f"Ações encontradas: {len(acoes)}")
        print()

        # O executor das ações será implementado aqui.
        #
        # futuramente:
        #
        # executar_acoes(acoes)

        print("Preset carregado com sucesso.")

        input("\nPressione ENTER para continuar.")

    except json.JSONDecodeError:

        print(
            "\nO arquivo do preset possui "
            "um JSON inválido."
        )

        input("\nPressione ENTER para continuar.")

    except Exception as erro:

        print("\nNão foi possível carregar o preset.")
        print(f"Detalhes: {erro}")

        input("\nPressione ENTER para continuar.")


def menu(gravar_preset=False, acoes_preset=None):

    if acoes_preset is None:
        acoes_preset = []

    while True:

        os.system("cls")

        print("================================")
        print(" Bem vindo ao MinecraftJava-Hub ")
        print("================================")
        print()

        print(
            "Selecione a aplicação que deseja utilizar"
        )

        print(dedent("""
            Você pode escolher com base nos numéricos do
            seu teclado ou executar um preset pelo nome.
            """))

        print()

        print("0 - Sair")
        print("1 - Gerenciamento de mundos")
        print("2 - Atualizar minhas modificações")
        print("3 - Gerenciar presets")

        print()

        print("========== PRESETS DISPONÍVEIS ==========")

        presets = carregar_presets()

        if presets:

            for preset in presets:
                print(f"- {preset}")

        else:

            print("Nenhum preset disponível.")

        print()

        option = input(
            "Escolha uma opção ou digite o nome do preset: "
        ).strip()

        # ========================================
        # FINALIZAR GRAVAÇÃO
        # ========================================

        if gravar_preset and option.casefold() == "terminar":

            return

        # ========================================
        # SAIR
        # ========================================

        if option == "0":

            if gravar_preset:

                print(
                    "\nDurante a criação de um preset,"
                )

                print(
                    "utilize 'terminar' para finalizar "
                    "a gravação."
                )

                input(
                    "\nPressione ENTER para continuar."
                )

                continue

            os.system("cls")

            print("Obrigado por usar MCJ-Hub")

            sys.exit()

        # ========================================
        # GERENCIAMENTO DE MUNDOS
        # ========================================

        elif option == "1":

            if gravar_preset:

                registrar_acao(
                    acoes_preset,
                    "menu",
                    {
                        "menu": "Menu principal",
                        "opcao": "1",
                        "descricao": "Gerenciamento de mundos"
                    }
                )

            menu_backup(
                gravar_preset=gravar_preset,
                acoes_preset=acoes_preset
            )

        # ========================================
        # ATUALIZAR MODIFICAÇÕES
        # ========================================

        elif option == "2":

            if gravar_preset:

                registrar_acao(
                    acoes_preset,
                    "menu",
                    {
                        "menu": "Menu principal",
                        "opcao": "2",
                        "descricao": "Atualizar minhas modificações"
                    }
                )

            menu_update_modifications(
                gravar_preset=gravar_preset,
                acoes_preset=acoes_preset
            )

        # ========================================
        # GERENCIAR PRESETS
        # ========================================

        elif option == "3":

            if gravar_preset:

                print(
                    "\nO gerenciamento de presets "
                    "não pode ser acessado durante "
                    "uma gravação."
                )

                input(
                    "\nPressione ENTER para continuar."
                )

                continue

            preset_menu(menu)

        # ========================================
        # EXECUTAR PRESET
        # ========================================

        elif option in presets:

            if gravar_preset:

                print(
                    "\nNão é possível executar um preset "
                    "durante a criação de outro preset."
                )

                input(
                    "\nPressione ENTER para continuar."
                )

                continue

            executar_preset(option)

        # ========================================
        # OPÇÃO INVÁLIDA
        # ========================================

        else:

            os.system("cls")

            print("Operação inválida.")

            input(
                "\nPressione ENTER para continuar."
            )


if __name__ == "__main__":
    menu()