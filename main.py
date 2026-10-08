import os
import sys

from pathlib import Path
from textwrap import dedent

from BackupCode.menu import menu_backup
from ModificationsCode.update_modifications import menu_update_modifications
from PresetsCode.menu import preset_menu
from PresetsCode.acoes import registrar_acao
from PresetsCode.executor import executar_preset


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


def menu(
    gravar_preset=False,
    acoes_preset=None,
    modo_execucao=False,
    acoes_execucao=None
):

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

        if modo_execucao:

            try:

                acao = next(acoes_execucao)

            except StopIteration:

                print(
                    "\nO preset terminou antes "
                    "de concluir o menu principal."
                )

                input(
                    "\nPressione ENTER para continuar."
                )

                return

            if acao.get("tipo") != "menu":

                print("\nErro no preset.")

                input(
                    "\nPressione ENTER para continuar."
                )

                return

            dados = acao.get("dados", {})

            menu_nome = dados.get("menu")
            option = dados.get("opcao")

            print(
                f"Escolha uma opção: {option}"
            )

            print()

        else:

            option = input(
                "Escolha uma opção ou digite o nome do preset: "
            ).strip()

        if gravar_preset and option.casefold() == "terminar":

            return

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
                acoes_preset=acoes_preset,
                modo_execucao=modo_execucao,
                acoes_execucao=acoes_execucao
            )

            if modo_execucao:
                return

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

            if modo_execucao:
                return

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

            if modo_execucao:

                print(
                    "\nO gerenciamento de presets "
                    "não pode ser executado por um preset."
                )

                input(
                    "\nPressione ENTER para continuar."
                )

                return

            preset_menu(menu)

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

        else:

            os.system("cls")

            print("Operação inválida.")

            input(
                "\nPressione ENTER para continuar."
            )


if __name__ == "__main__":
    menu()