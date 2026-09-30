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
            os.system("cls")
            print("Opção inválida.")
            input("\nPressione ENTER para continuar")

def copiar_com_progresso(origem, destino):
    arquivos = []

    for arquivo in origem.rglob("*"):
        if arquivo.is_file():
            arquivos.append(arquivo)

    tamanho_total = sum(
        arquivo.stat().st_size
        for arquivo in arquivos
    )

    tamanho_copiado = 0

    destino.mkdir(parents=True, exist_ok=True)

    total_arquivos = len(arquivos)

    print(f"Arquivos encontrados: {total_arquivos}")
    print(f"Tamanho total: {formatar_tamanho(tamanho_total)}")
    print()

    for numero, arquivo in enumerate(arquivos, start=1):

        caminho_relativo = arquivo.relative_to(origem)

        destino_arquivo = destino / caminho_relativo

        destino_arquivo.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        shutil.copy2(
            arquivo,
            destino_arquivo
        )

        tamanho_arquivo = arquivo.stat().st_size

        tamanho_copiado += tamanho_arquivo

        porcentagem = (
            tamanho_copiado / tamanho_total * 100
            if tamanho_total > 0
            else 100
        )

        barra_tamanho = 30

        preenchido = int(
            barra_tamanho * porcentagem / 100
        )

        barra = (
            "█" * preenchido
            + "░" * (barra_tamanho - preenchido)
        )

        tamanho_atual_gb = (
            tamanho_copiado / (1024 ** 3)
        )

        tamanho_total_gb = (
            tamanho_total / (1024 ** 3)
        )

        print(
            f"\r[{barra}] "
            f"{porcentagem:6.2f}% "
            f"{tamanho_atual_gb:.2f} GB / "
            f"{tamanho_total_gb:.2f} GB "
            f"({numero}/{total_arquivos})",
            end="",
            flush=True
        )

    print()

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
    
    while True:
        os.system("cls")

        print("========== MUNDOS ENCONTRADOS ==========\n")
        print("0.Voltar")

        for indice, mundo in enumerate(mundos, start=1):
            tamanho = calcular_tamanho(mundo)
            tamanho_formatado = formatar_tamanho(tamanho)
        
            print(f"{indice}.{mundo.name} - {tamanho_formatado}")

        opcao = input("\nEscolha uma opção: ")

        if opcao == "0":
            return

        if not opcao.isdigit():
            os.system("cls")
            print("\nOpção inválida. Por favor, tente novamente.")
            input("\nPressione ENTER para continuar.")
            
            continue

        indice = int(opcao)

        if not 1 <= indice <= len(mundos):
            os.system("cls")
            print("\nOpção inválida. Por favor, tente novamente.")
            input("\nPressione ENTER para continuar.")
            
            continue

        os.system("cls")
        mundo_escolhido = mundos[indice - 1]

        print(f"\nMundo selecionado: {mundo_escolhido.name}")

        pasta_destino = input(
            "\nInforme o caminho da pasta para salvar o backup: "
        ).strip()

        os.system("cls")
        if not pasta_destino:
            print("\nÉ obrigatório informar uma pasta de destino.")
            input("\nPressione ENTER para continuar.")
            continue

        os.system("cls")
        pasta_destino = Path(pasta_destino)

        if not pasta_destino.is_dir():
            print("\nA pasta informada não foi encontrada.")
            input("\nPressione ENTER para continuar.")
            continue

        data_backup = datetime.now().strftime("%d_%m_%Y")
        nome_mundo = mundo_escolhido.name

        backup_existentes = [
            pasta
            for pasta in pasta_destino.iterdir()
            if pasta.is_dir()
            and pasta.name.startswith(f"{nome_mundo} (")
        ]

        cancelar_backup = False

        if backup_existentes:
            print("\nJá existem backups deste mundo:")

            for backup in backup_existentes:
                print(f"- {backup.name}")

            while True:
                opcao_backup = input(
                    "\nDeseja excluir os backups existentes e criar um novo? (n/s): "
                ).strip().lower()
            
                if opcao_backup == "s":
                    for backup in backup_existentes:
                        shutil.rmtree(backup)
                
                    print("\nBackups anteriores excluídos.")
                    break

                elif opcao_backup == "n":
                    print("\nOperação cancelada.")
                    print("\nPressione ENTER para continuar.")
                    cancelar_backup = True
                    break

                else:
                    print("\nOpção inválida. Digite (s) ou (n).")

        if cancelar_backup:
            continue

        nome_backup = f"{mundo_escolhido.name} ({data_backup})"
        destino_backup = pasta_destino / nome_backup

        nova_tentativa = False

        while True:
            try:
                if nova_tentativa and destino_backup.exists():
                    shutil.rmtree(destino_backup)

                nova_tentativa = False

                os.system("cls")
                print("\nRealizando backup...")

                copiar_com_progresso(
                    mundo_escolhido,
                    destino_backup
                )

                tamanho_original = calcular_tamanho(mundo_escolhido)
                tamanho_backup = calcular_tamanho(destino_backup)

                os.system("cls")

                if tamanho_original != tamanho_backup:
                    mostar_alerta()
                    print("\n========== ALERTA DE BACKUP ==========")
                    print("\nO backup foi concluído, mas os tamanhos")
                    print("dos mundos não são iguais!")
                    print()
                    print(f"Mundo Original: {mundo_escolhido.name}")
                    print(
                        f"Tamanho Original: "
                        f"{formatar_tamanho(tamanho_original)}"
                    )
                    print()
                    print(f"Backup: {destino_backup.name}")
                    print(
                        f"Tamanho do Backup: "
                        f"{formatar_tamanho(tamanho_backup)}"
                    )
                    print()
                    print("O backup pode estar incompleto ou corrompido.")

                    while True:
                        print("\n1. Tentar novamente")
                        print("2. Cancelar operação")

                        opcao_erro = input("\nEscolha uma opção: ")
                        
                        if opcao_erro == "1":
                            nova_tentativa = True
                            break

                        elif opcao_erro == "2":
                            return

                        else:
                            print("\nOpção inválida.")

                    continue

                print("\n========== BACKUP CONCLUÍDO ==========")
                print(f"Mapa Original: {mundo_escolhido.name}")
                print(f"Tamanho: {formatar_tamanho(tamanho_original)}")
                print(f"Backup: {destino_backup.name}")
                print(f"Tamanho: {formatar_tamanho(tamanho_backup)}")
                print()
                print(f"Local: {destino_backup}")

                input("\nPressione ENTER para continuar.")

                break

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

def mostar_alerta():
    print(r"""
                          ████████                          
                        ██        ██                        
                      ██            ██                      
                      ██            ██                      
                    ██    ████████    ██                    
                  ██    ████████████    ██                  
                  ██    ████████████    ██                  
                ██      ████████████      ██                
              ██          ████████          ██              
              ██          ████████          ██              
            ██            ████████            ██            
          ██                ████                ██          
          ██                ████                ██          
        ██                                        ██        
      ██                    ████                    ██      
      ██                  ████████                  ██      
    ██                  ████████████                  ██    
  ██                    ████████████                    ██  
  ██                      ████████                      ██  
  ██                        ████                        ██  
    ██                                                ██    
      ████████████████████████████████████████████████   
""")

if __name__ == "__main__":
    menu_backup()