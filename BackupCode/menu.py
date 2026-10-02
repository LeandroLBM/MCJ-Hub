import os

from .backup import realizar_backup
from .restauracao import realizar_restauracao

def menu_backup(gravar_preset=False, acoes_preset=None):

    if acoes_preset is None:
        acoes_preset = []

    while True:
        os.system("cls")

        print("========== MENU BACKUP ==========\n")
        print("0. Voltar para o menu principal")
        print("1. Realizar backup do mundo")
        print("2. Restaurar backup do mundo")
        
        opcao = input("\nEscolha uma opção: ")

        if gravar_preset and opcao.casefold() == "terminar":
                    return

        if opcao == "0":
            return

        elif opcao == "1":

            if gravar_preset:
                acoes_preset.append("Backup")
            
            realizar_backup()
            break

        elif opcao == "2":

            if gravar_preset:
                acoes_preset.append("Restauração")
            
            realizar_restauracao()
            break

        else:
            os.system("cls")
            print("Opção inválida.")
            input("\nPressione ENTER para continuar")
