import os

from .backup import realizar_backup
from .restauracao import realizar_restauracao
from .DiretoryCode.menu import menu_diretorios
from PresetsCode.acoes import registrar_acao


def menu_backup(
    gravar_preset=False,
    acoes_preset=None,
    modo_execucao=False,
    acoes_execucao=None
):

    if acoes_preset is None:
        acoes_preset = []

    if acoes_execucao is None:
        acoes_execucao = iter([])

    while True:

        os.system("cls")

        print("========== MENU BACKUP ==========\n")
        print("0. Voltar para o menu principal")
        print("1. Realizar backup do mundo")
        print("2. Restaurar backup do mundo")
        print("3. Gerenciar diretórios")

        if modo_execucao:

            try:

                acao = next(acoes_execucao)

            except StopIteration:

                print("\nO preset terminou antes de concluir o menu.")

                input("\nPressione ENTER para continuar.")

                return

            if acao.get("tipo") == "voltar":

                return

            if acao.get("tipo") != "menu":

                print("\nErro no preset.")

                input("\nPressione ENTER para continuar.")

                return

            dados = acao.get("dados", {})

            opcao = dados.get("opcao")

            if opcao == "3":

                print(
                    "\nO gerenciamento de diretórios "
                    "não pode ser executado por um preset."
                )

                input("\nPressione ENTER para continuar.")

                return

            print(f"\nEscolha uma opção: {opcao}")

        else:

            opcao = input(
                "\nEscolha uma opção: "
            ).strip()

        if gravar_preset and opcao.casefold() == "terminar":

            return

        if opcao == "0":

            if gravar_preset:

                registrar_acao(
                    acoes_preset,
                    "voltar"
                )

            return

        elif opcao == "1":

            if gravar_preset:

                registrar_acao(
                    acoes_preset,
                    "menu",
                    {
                        "menu": "Gerenciamento de mundos",
                        "opcao": "1",
                        "descricao": "Realizar backup do mundo"
                    }
                )

            realizar_backup(
                acoes_preset=acoes_preset,
                gravar_preset=gravar_preset,
                modo_execucao=modo_execucao,
                acoes_execucao=acoes_execucao
            )

            if modo_execucao:

                return

            break

        elif opcao == "2":

            if gravar_preset:

                registrar_acao(
                    acoes_preset,
                    "menu",
                    {
                        "menu": "Gerenciamento de mundos",
                        "opcao": "2",
                        "descricao": "Restaurar backup do mundo"
                    }
                )

            realizar_restauracao(
                acoes_preset=acoes_preset,
                gravar_preset=gravar_preset
            )

            if modo_execucao:

                return

            break

        elif opcao == "3":

            if gravar_preset:

                print(
                    "\nO gerenciamento de diretórios "
                    "não pode ser acessado durante "
                    "a criação de um preset."
                )

                input("\nPressione ENTER para continuar.")

                continue

            menu_diretorios()

        else:

            os.system("cls")

            print("Opção inválida.")

            input("\nPressione ENTER para continuar.")