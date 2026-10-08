import os

from .criação import criacao_preset
from .exclussao import exclucao_preset


def preset_menu(menu):

    while True:

        os.system("cls")

        print("========== PRESETS MENU ==========\n")
        print("0. Voltar para o menu principal")
        print("1. Criar um novo preset")
        print("2. Excluir preset")
        print()

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "0":

            return

        elif opcao == "1":

            criacao_preset(menu)

        elif opcao == "2":

            exclucao_preset()

        else:

            os.system("cls")

            print("Opção inválida.")

            input("\nPressione ENTER para continuar.")