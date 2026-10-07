import os

from .backup import realizar_backup
from .restauracao import realizar_restauracao
from PresetsCode.acoes import registrar_acao

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

            if gravar_preset:
                registrar_acao(
                    acoes_preset,
                    "menu",
                    {
                        "menu": "Gerenciamento de mundos",
                        "opcao": "0",
                        "descrição": "Voltar para o menu principal"                    
                    }
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
                 gravar_preset=gravar_preset
            )
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
            break

        else:
            os.system("cls")
            print("Opção inválida.")
            input("\nPressione ENTER para continuar")
