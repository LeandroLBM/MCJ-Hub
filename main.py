import os
import sys
from textwrap import dedent

from BackupCode.menu import menu_backup
from ModificationsCode.update_modifications import menu_update_modifications
from PresetsCode.menu import preset_menu

def menu(gravar_preset=False, acoes_preset=None):

    if acoes_preset is None:
        acoes_preset = []

    while True:
        os.system("cls")
        print("================================")
        print(" Bem vindo ao MinecraftJava-Hub ")
        print("================================")
        print()
        print("Selecione a aplicação que deseja utilizar")
        print(dedent("""
            Você pode escolher com base nos numéricos do 
            seu teclado
            """))
        print()
        print("0 - Sair")
        print("1 - Gerenciamento de mundos")
        print("2 - Atualizar minhas modificações")
        print("3 - Presets menu")
        print()

        option = input("Escolha uma opção: ")

        if gravar_preset and option.casefold() == "terminar":
            return

        if option == "0":

            if gravar_preset:
                print("\nDurante a criação de um preset,")
                print("utilize 'terminar' para finalizar a gravação.")
                input("\nPressione ENTER para continuar.")
                continue

            os.system("cls")
            print("Obrigado por usar MCJ-Hub")
            sys.exit()

        elif option == "1":
            if gravar_preset:
                acoes_preset.append("Gerenciamento de mundos")

            menu_backup(
                gravar_preset=gravar_preset,
                acoes_preset=acoes_preset
                )
        
        elif option == "2":
            if gravar_preset:
                acoes_preset.append("Atualizar minhas modificações")

            menu_update_modifications(
                gravar_preset=gravar_preset,
                acoes_preset=acoes_preset
            )

        elif option == "3":
            if gravar_preset:
                print("\nO menu de presets não pode ser acessado durante uma gravação.")
                input("\nPressione ENTER para continuar.")
                continue

            preset_menu(menu)
        
        else:
            os.system("cls")
            print("Operação Invalida!")
            input("\nPressione ENTER para continuar.")

if __name__ == "__main__":
    menu()