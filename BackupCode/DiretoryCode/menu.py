import os

from .adicionar import adicionar_diretorio
from .remover import remover_diretorio


def menu_diretorios():

    while True:

        os.system("cls")

        print("========== GERENCIAR DIRETÓRIOS ==========\n")
        print("0. Voltar")
        print("1. Adicionar diretório")
        print("2. Remover diretório")

        opcao = input(
            "\nEscolha uma opção: "
        ).strip()

        if opcao == "0":

            return

        elif opcao == "1":

            adicionar_diretorio()

        elif opcao == "2":

            remover_diretorio()

        else:

            print("\nOpção inválida.")

            input("\nPressione ENTER para continuar.")