import os

from .backup import realizar_backup
from .restauracao import realizar_restauracao

def menu_backup():
    while True:
        os.system("cls")

        print("========== MENU BACKUP ==========\n")
        print("0. Voltar para o menu principal")
        print("1. Realizar backup do mundo")
        print("2. Restaurar backup do mundo")

        opcao = input("\nEscolha uma opção: ")

        if opcao == "0":
            return

        elif opcao == "1":
            realizar_backup()
            break

        elif opcao == "2":
            realizar_restauracao()
            break

        else:
            os.system("cls")
            print("Opção inválida.")
            input("\nPressione ENTER para continuar")

if __name__ == "__main__":
    menu_backup()