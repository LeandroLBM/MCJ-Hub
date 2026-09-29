import os
import sys
import shutil

from pathlib import Path
from datetime import datetime

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
            restaurar_backup()
            break

        else:
            print("Opção inválida.")
            input("\nPressione ENTER para continuar")

def realizar_backup():
    os.system("cls")

    appdata = os.getenv("APPDATA")

    if not appdata:
        print("Não foi possível localizar a pasta AppData.")
        return[]

    pasta_minecraft = Path(appdata) / ".minecraft"
    
    if not pasta_minecraft.is_dir():
        print("A pasta .Minecraft não foi encontrada.")
        return[]

    pasta_mundos = pasta_minecraft / "saves"

    if not pasta_mundos.is_dir():
        print("A pasta saves não foi encontrada.")
        return[]

    mundos = [
        pasta
        for pasta in pasta_mundos.iterdir()
        if pasta.is_dir()
    ]

    if not mundos:
        print("nenhum mundo encontrado.")
        return[]

    print("mundos encontrados:\n")

    print("0.Voltar")

    for indice, mundo in enumerate(mundos, start=1):
        tamanho = calcular_tamanho(mundo)
        tamanho_formatado = formatar_tamanho(tamanho)

        print(f"{indice}.{mundo.name} - {tamanho_formatado}")
    

    while True:
        opcao = input("\nEscolha um mundo: ")

        if opcao == "0":
            return

        if not opcao.isdigit():
            print("\nOpção inválida. Por favor, tente novamente.")
            continue

        indice = int(opcao)

        if not 1 <= indice <= len(mundos):
            print("\nOpção inválida. Por favor, tente novamente.")
            continue

        mundo_escolhido = mundos[indice - 1]

        print(f"\nMundo selecionado: {mundo_escolhido.name}")

        pasta_destino = input(
            "\nInforme o caminho da pasta para salvar o backup: "
        )

        pasta_destino = Path(pasta_destino)

        if not pasta_destino.is_dir():
            print("\nA pasta informada não existe.")
            input("\nPressione ENTER para continuar.")
            continue

        data_backup = datetime.now().strftime("%d_%m_%Y")

        nome_backup = f"{mundo_escolhido.name} ({data_backup})"

        destino_backup = pasta_destino / nome_backup

        while True:
            try:
                print("\nRealizando backup...")

                shutil.copytree(
                    mundo_escolhido,
                    destino_backup
                )
                tamanho_original = calcular_tamanho(mundo_escolhido)
                tamanho_backup = calcular_tamanho(destino_backup)

                print("\n========== BACKUP CONCLUÍDO ==========")
                print(f"Mapa Original: {mundo_escolhido.name}")
                print(f"Tamanho: {formatar_tamanho(tamanho_original)}")
                print(f"Backup: {destino_backup.name}")
                print(f"Tamanho: {formatar_tamanho(tamanho_backup)}")
                print(f"Local: {destino_backup}")

                input("\nPressione ENTER para continuar.")
                return

            except Exception as erro:
                print("\nERRO AO REALIZAR O BACKUP!")
                print(f"Detalhes: {erro}")

                while True:
                    print("\n1. Tentar novamente")
                    print("2. Cancelar operação")

                    opcao_erro = input("\nEscolha uma opção: ")

                    if opcao_erro == "1":
                        break

                    elif opcao_erro == "2":
                        return

                    else:
                        print("\nOpção inválida.")

def restaurar_backup():
    print("restaurar menu")


def calcular_tamanho(pasta):
    tamanho = 0    

    for arquivo in pasta.rglob("*"):
        if arquivo.is_file():
            tamanho += arquivo.stat().st_size
    return tamanho

def formatar_tamanho(tamanho):
    tamanho_gb = tamanho / (1024 ** 3)
    
    return f"({tamanho_gb:.2f} GB) - [{tamanho:,} bytes]"

if __name__ == "__main__":
    menu_backup()