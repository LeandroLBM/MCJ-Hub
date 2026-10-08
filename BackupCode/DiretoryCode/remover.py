import os
import json

from pathlib import Path


def remover_diretorio():

    pasta_diretorios = Path("MJH_Presets") / "Diretórios"

    if not pasta_diretorios.is_dir():

        print("\nNenhum diretório salvo foi encontrado.")

        input("\nPressione ENTER para continuar.")

        return

    diretorios = sorted(
        arquivo
        for arquivo in pasta_diretorios.iterdir()
        if arquivo.is_file()
        and arquivo.suffix.lower() == ".json"
    )

    if not diretorios:

        print("\nNenhum diretório salvo foi encontrado.")

        input("\nPressione ENTER para continuar.")

        return

    while True:

        os.system("cls")

        print("========== REMOVER DIRETÓRIO ==========\n")
        print("0. Voltar\n")

        for indice, arquivo in enumerate(diretorios, start=1):

            try:

                with open(
                    arquivo,
                    "r",
                    encoding="utf-8"
                ) as json_file:

                    dados = json.load(json_file)

                nome = dados.get(
                    "nome",
                    arquivo.stem
                )

                caminho = dados.get(
                    "caminho",
                    "Caminho não informado"
                )

                print(
                    f"{indice}. {nome} - {caminho}"
                )

            except Exception:

                print(
                    f"{indice}. {arquivo.stem}"
                )

        opcao = input(
            "\nEscolha um diretório: "
        ).strip()

        if opcao == "0":

            return

        if not opcao.isdigit():

            print("\nOpção inválida.")

            input("\nPressione ENTER para continuar.")

            continue

        indice = int(opcao)

        if not 1 <= indice <= len(diretorios):

            print("\nOpção inválida.")

            input("\nPressione ENTER para continuar.")

            continue

        arquivo_escolhido = diretorios[indice - 1]

        try:

            with open(
                arquivo_escolhido,
                "r",
                encoding="utf-8"
            ) as json_file:

                dados = json.load(json_file)

            nome = dados.get(
                "nome",
                arquivo_escolhido.stem
            )

            caminho = dados.get(
                "caminho",
                "Caminho não informado"
            )

        except Exception:

            nome = arquivo_escolhido.stem
            caminho = "Caminho não informado"

        os.system("cls")

        print("========== REMOVER DIRETÓRIO ==========\n")

        print(f"Nome: {nome}")
        print(f"Caminho: {caminho}")

        confirmacao = input(
            "\nDeseja realmente remover este diretório? (s/n): "
        ).strip().lower()

        if confirmacao == "s":

            try:

                arquivo_escolhido.unlink()

                print("\nDiretório removido com sucesso!")

                diretorios.remove(arquivo_escolhido)

                input("\nPressione ENTER para continuar.")

                if not diretorios:

                    return

            except Exception as erro:

                print(
                    "\nNão foi possível remover o diretório."
                )

                print(f"Detalhes: {erro}")

                input("\nPressione ENTER para continuar.")

        elif confirmacao == "n":

            print("\nOperação cancelada.")

            input("\nPressione ENTER para continuar.")

        else:

            print("\nOpção inválida.")

            input("\nPressione ENTER para continuar.")