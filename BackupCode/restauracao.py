import os
import shutil
from pathlib import Path

from .validacoes import calcular_tamanho
from .validacoes import formatar_tamanho
from .validacoes import progresso
from .validacoes import mostrar_alerta


def realizar_restauracao():
    os.system("cls")

    appdata = os.getenv("APPDATA")

    if not appdata:
        print("\nNão foi possível localizar a pasta AppData.")
        input("\nPressione ENTER para continuar.")
        return

    pasta_minecraft = Path(appdata) / ".minecraft"

    if not pasta_minecraft.is_dir():
        print("\nNão foi possível localizar a pasta .minecraft.")
        input("\nPressione ENTER para continuar.")
        return

    pasta_saves = pasta_minecraft / "saves"

    if not pasta_saves.is_dir():
        print("\nA pasta saves não foi encontrada.")
        input("\nPressione ENTER para continuar.")
        return

    os.system("cls")

    mundos = [
        pasta
        for pasta in pasta_saves.iterdir()
        if pasta.is_dir()
    ]

    print("========== RESTAURAR BACKUP ==========\n")

    print("Mundos disponíveis no minecraft:")
    print("0. Voltar ao Menu")
    print()

    if mundos:
        for mundo in mundos:
            print(f"{mundo.name}")
    else:
        print("Nenhum mundo disponível no minecraft.")

    print("\n--------------------------------------\n")

    pasta_backup = input(
        "Informe o caminho da pasta onde estão os backups: "
    ).strip()

    if pasta_backup == "0":
        return

    if not pasta_backup:
        print("\nÉ obrigatório informar uma pasta.")
        input("\nPressione ENTER para continuar.")
        return

    pasta_backup = Path(pasta_backup)

    if not pasta_backup.is_dir():
        print("\nA pasta informada não foi encontrada.")
        input("\nPressione ENTER para continuar.")
        return

    backups = [
        pasta
        for pasta in pasta_backup.iterdir()
        if pasta.is_dir()
    ]

    os.system("cls")

    print("========== BACKUPS DISPONÍVEIS ==========\n")
    print("0. Voltar\n")

    if not backups:
        print("Nenhum backup encontrado na pasta informada.")
        input("\nPressione ENTER para continuar.")
        return

    for indice, backup in enumerate(backups, start=1):
        print(f"{indice}. {backup.name}")

    while True:
        opcao = input("\nEscolha um backup: ").strip()

        if opcao == "0":
            return

        if not opcao.isdigit():
            print("\nOpção inválida. Digite apenas um número.")
            input("\nPressione ENTER para continuar.")
            continue

        indice = int(opcao)

        if not 1 <= indice <= len(backups):
            print("\nOpção inválida. Escolha um número da lista.")
            input("\nPressione ENTER para continuar.")
            continue

        backup_escolhido = backups[indice - 1]

        break

    os.system("cls")

    nome_backup = backup_escolhido.name

    if " (" in nome_backup:
        nome_mundo = nome_backup.rsplit(" (", 1)[0]
    else:
        nome_mundo = nome_backup

    mundo_existente = pasta_saves / nome_mundo

    print("========== BACKUP SELECIONADO ==========\n")
    print(f"Backup selecionado: {nome_backup}")
    print(f"Nome do mundo: {nome_mundo}")

    print()

    if mundo_existente.is_dir():

        tamanho_backup = calcular_tamanho(backup_escolhido)
        tamanho_mundo = calcular_tamanho(mundo_existente)

        print("⚠️ JÁ EXISTE UM MUNDO COM ESTE NOME!\n")

        print(f"Mundo existente:")
        print(f"  {mundo_existente.name}")
        print(f"  Tamanho: {formatar_tamanho(tamanho_mundo)}")

        print()

        print(f"Backup:")
        print(f"  {backup_escolhido.name}")
        print(f"  Tamanho: {formatar_tamanho(tamanho_backup)}")

        print("\n--------------------------------------")

        # Compara os tamanhos antes da exclusão
        if tamanho_mundo != tamanho_backup:
            mostrar_alerta(
                "O tamanho do mundo existente é diferente "
                "do tamanho do backup."
            )

            print(
                "\n⚠️ Os tamanhos do mundo existente e do backup "
                "são diferentes."
            )

        else:
            print(
                "\nOs tamanhos do mundo existente e do backup "
                "são iguais."
            )

        print()
        print("Deseja EXCLUIR o mundo atual e copiar o backup?")
        print("(s/n)")

        while True:
            opcao_existente = input("\nEscolha uma opção: ").strip().lower()

            if opcao_existente == "s":

                try:
                    shutil.rmtree(mundo_existente)

                    print("\nMundo existente excluído.")
                    print("O backup poderá ser restaurado.")

                    break

                except Exception as erro:
                    print(
                        "\nNão foi possível excluir "
                        "o mundo existente."
                    )
                    print(f"Detalhes: {erro}")

                    input("\nPressione ENTER para continuar.")
                    return

            elif opcao_existente == "n":

                print("\nOperação cancelada.")
                input("\nPressione ENTER para continuar.")
                return

            else:
                print("\nOpção inválida. Escolha s ou n.")

    else:

        tamanho_backup = calcular_tamanho(backup_escolhido)

        print("Nenhum mundo com este nome foi encontrado.")
        print("O mundo poderá ser restaurado.")

        print()
        print(f"Tamanho do backup: {formatar_tamanho(tamanho_backup)}")

    while True:

        print("\nDeseja restaurar este mundo? (s/n)")

        opcao_restaurar = input("\nEscolha uma opção: ").strip().lower()

        if opcao_restaurar == "s":

            try:
                os.system("cls")

                print("========== RESTAURANDO BACKUP ==========\n")
                print(f"Mundo: {nome_mundo}")
                print(f"Backup: {backup_escolhido.name}")
                print()

                tamanho_backup = calcular_tamanho(backup_escolhido)

                print(
                    f"Tamanho do backup: "
                    f"{formatar_tamanho(tamanho_backup)}"
                )

                print()

                progresso(
                    backup_escolhido,
                    mundo_existente
                )


                tamanho_restaurado = calcular_tamanho(
                    mundo_existente
                )

                print("\n")
                print("========== VALIDANDO RESTAURAÇÃO ==========\n")

                print(
                    f"Tamanho do backup:     "
                    f"{formatar_tamanho(tamanho_backup)}"
                )

                print(
                    f"Tamanho restaurado:    "
                    f"{formatar_tamanho(tamanho_restaurado)}"
                )

                if tamanho_backup == tamanho_restaurado:

                    print("\n✓ Validação concluída.")
                    print("✓ Os tamanhos são iguais.")

                    print(
                        "\n========== RESTAURAÇÃO CONCLUÍDA =========="
                    )

                    print(f"Mundo restaurado: {nome_mundo}")
                    print(f"Local: {mundo_existente}")

                else:

                    mostrar_alerta(
                        "O tamanho do backup é diferente "
                        "do tamanho do mundo restaurado."
                    )

                    print(
                        "\n⚠️ ATENÇÃO: A restauração apresentou "
                        "diferença de tamanho!"
                    )

                    print(
                        f"\nBackup:     "
                        f"{formatar_tamanho(tamanho_backup)}"
                    )

                    print(
                        f"Restaurado: "
                        f"{formatar_tamanho(tamanho_restaurado)}"
                    )

                    print(
                        "\nA restauração pode não ter sido concluída "
                        "corretamente."
                    )

                input("\nPressione ENTER para continuar.")
                return

            except Exception as erro:

                print("\nERRO AO RESTAURAR O MUNDO!")
                print(f"Detalhes: {erro}")

                input("\nPressione ENTER para continuar.")
                return

        elif opcao_restaurar == "n":

            print("\nOperação cancelada.")
            input("\nPressione ENTER para continuar.")
            return

        else:

            print("\nOpção inválida. Escolha s ou n.")