import os
import sys

from .criação import criacao_preset
from .edicao import edicao_preset
from .exclussao import exclucao_preset


def preset_menu(menu):
    while True:
        os.system("cls")

        print("========== PRESETS MENU ==========\n")
        print("0. Voltar para o menu principal")
        print("1. Criar um novo preset")
        print("2. Editar preset")
        print("3. Excluir preset")

        opcao = input("\nEscolha uma opção: ")

        if opcao == "0":
            return
        
        elif opcao == "1":
            criacao_preset(menu)

        elif opcao == "2":
            edicao_preset(menu)

        elif opcao == "3":
            exclucao_preset(menu)

        else:
            os.system("cls")
            print("Opção inválida.")
            input("\nPressione ENTER para continuar")