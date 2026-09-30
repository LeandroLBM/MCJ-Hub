import os
import sys
from textwrap import dedent

from BackupCode.backup import menu_backup
from ModificationsCode.update_modifications import menu_update_modifications

def menu():
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
        print()

        option = input("Escolha uma opção: ")

        if option == "0":
            os.system("cls")
            print("Obrigado por usar MCJ-Hub")
            sys.exit()

        elif option == "1":
            menu_backup()
        
        elif option == "2":
            menu_update_modifications()
        
        else:
            os.system("cls")
            print("Operação Invalida!")
            input("\nPressione ENTER para continuar.")

if __name__ == "__main__":
    menu()
