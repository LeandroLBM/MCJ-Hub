import os
import shutil
import json

from pathlib import Path
from datetime import datetime

from .validacoes import (
    calcular_tamanho,
    formatar_tamanho,
    progresso
)
from PresetsCode.acoes import registrar_acao


def carregar_diretorios():

    pasta_diretorios = (
        Path("MJH_Presets") /
        "Diretórios"
    )

    if not pasta_diretorios.is_dir():

        return []

    diretorios = []

    arquivos = sorted(
        arquivo
        for arquivo in pasta_diretorios.iterdir()
        if arquivo.is_file()
        and arquivo.suffix.lower() == ".json"
    )

    for arquivo in arquivos:

        try:

            with open(
                arquivo,
                "r",
                encoding="utf-8"
            ) as json_file:

                dados = json.load(json_file)

            nome = dados.get("nome")
            caminho = dados.get("caminho")

            if caminho:

                if not nome:

                    nome = arquivo.stem

                diretorios.append(
                    {
                        "nome": nome,
                        "caminho": caminho
                    }
                )

        except Exception:

            continue

    return diretorios


def realizar_backup(
    gravar_preset=False,
    acoes_preset=None,
    modo_execucao=False,
    acoes_execucao=None
):

    if acoes_preset is None:

        acoes_preset = []

    if acoes_execucao is None:

        acoes_execucao = iter([])

    appdata = os.getenv("APPDATA")

    if not appdata:

        print("\nNão foi possível localizar a pasta AppData.")

        input("\nPressione ENTER para continuar.")

        return

    pasta_minecraft = Path(appdata) / ".minecraft"
    pasta_mundos = pasta_minecraft / "saves"

    if not pasta_minecraft.is_dir():

        print("\nA pasta .minecraft não foi encontrada.")

        input("\nPressione ENTER para continuar.")

        return

    if not pasta_mundos.is_dir():

        print("\nA pasta de mundos não foi encontrada.")

        input("\nPressione ENTER para continuar.")

        return

    mundos = [
        pasta
        for pasta in pasta_mundos.iterdir()
        if pasta.is_dir()
    ]

    if not mundos:

        print("\nNenhum mundo encontrado.")

        input("\nPressione ENTER para continuar.")

        return

    while True:

        os.system("cls")

        print("========== MUNDOS ENCONTRADOS ==========\n")
        print("0. Voltar")

        for indice, mundo in enumerate(
            mundos,
            start=1
        ):

            tamanho = calcular_tamanho(mundo)

            print(
                f"{indice}. "
                f"{mundo.name} - "
                f"{formatar_tamanho(tamanho)}"
            )

        if modo_execucao:

            try:

                acao = next(
                    acoes_execucao
                )

            except StopIteration:

                print(
                    "\nO preset terminou antes "
                    "de selecionar o mundo."
                )

                input(
                    "\nPressione ENTER para continuar."
                )

                return

            if acao.get("tipo") == "voltar":

                return

            if acao.get(
                "tipo"
            ) != "selecao_mundo":

                print("\nErro no preset.")

                input(
                    "\nPressione ENTER para continuar."
                )

                return

            dados = acao.get(
                "dados",
                {}
            )

            nome_mundo = dados.get(
                "mundo"
            )

            mundo_escolhido = next(
                (
                    mundo
                    for mundo in mundos
                    if mundo.name == nome_mundo
                ),
                None
            )

            if mundo_escolhido is None:

                print(
                    f"\nO mundo '{nome_mundo}' "
                    "não foi encontrado."
                )

                input(
                    "\nPressione ENTER para continuar."
                )

                return

            print(
                f"\nEscolha uma opção: "
                f"{mundos.index(mundo_escolhido) + 1}"
            )

        else:

            opcao = input(
                "\nEscolha uma opção: "
            ).strip()

            if opcao == "0":

                if gravar_preset:

                    registrar_acao(
                        acoes_preset,
                        "voltar"
                    )

                return

            if not opcao.isdigit():

                print("\nOpção inválida.")

                input(
                    "\nPressione ENTER para continuar."
                )

                continue

            indice = int(opcao)

            if not 1 <= indice <= len(mundos):

                print("\nOpção inválida.")

                input(
                    "\nPressione ENTER para continuar."
                )

                continue

            mundo_escolhido = mundos[
                indice - 1
            ]

            if gravar_preset:

                registrar_acao(
                    acoes_preset,
                    "selecao_mundo",
                    {
                        "mundo": mundo_escolhido.name
                    }
                )

        print(
            f"\nMundo selecionado: "
            f"{mundo_escolhido.name}"
        )

        break

    # ==================================================
    # SELEÇÃO DO DESTINO
    # ==================================================

    if modo_execucao:

        try:

            acao = next(
                acoes_execucao
            )

        except StopIteration:

            print(
                "\nO preset terminou antes "
                "de informar o destino."
            )

            input(
                "\nPressione ENTER para continuar."
            )

            return

        if acao.get(
            "tipo"
        ) != "destino":

            print("\nErro no preset.")

            input(
                "\nPressione ENTER para continuar."
            )

            return

        dados = acao.get(
            "dados",
            {}
        )

        caminho_destino = dados.get(
            "caminho"
        )

        if not caminho_destino:

            print(
                "\nO preset não possui um caminho "
                "de destino válido."
            )

            input(
                "\nPressione ENTER para continuar."
            )

            return

        pasta_destino = Path(
            caminho_destino
        )

        print(
            f"\nDestino selecionado: "
            f"{caminho_destino}"
        )

    else:

        diretorios = carregar_diretorios()

        while True:

            os.system("cls")

            print(
                "========== DESTINO DO BACKUP ==========\n"
            )

            if diretorios:

                print("Diretórios salvos:\n")

                for indice, diretorio in enumerate(
                    diretorios,
                    start=1
                ):

                    print(
                        f"{indice}. "
                        f"{diretorio['nome']} - "
                        f"{diretorio['caminho']}"
                    )

            else:

                print(
                    "Nenhum diretório salvo."
                )

            print("\n0. Voltar")

            entrada = input(
                "\nInforme o número do diretório "
                "ou digite um novo caminho: "
            ).strip()

            # VOLTAR
            if entrada == "0":

                if gravar_preset:

                    registrar_acao(
                        acoes_preset,
                        "voltar"
                    )

                return

            # NÚMERO = DIRETÓRIO SALVO
            if entrada.isdigit():

                indice = int(entrada)

                if not 1 <= indice <= len(
                    diretorios
                ):

                    print(
                        "\nDiretório inválido."
                    )

                    input(
                        "\nPressione ENTER para continuar."
                    )

                    continue

                diretorio_escolhido = (
                    diretorios[indice - 1]
                )

                caminho_destino = (
                    diretorio_escolhido[
                        "caminho"
                    ]
                )

                pasta_destino = Path(
                    caminho_destino
                )

                print(
                    f"\nDiretório selecionado: "
                    f"{diretorio_escolhido['nome']}"
                )

                break

            # TEXTO = CAMINHO INFORMADO MANUALMENTE
            caminho_destino = entrada

            if not caminho_destino:

                print(
                    "\nO caminho não pode estar vazio."
                )

                input(
                    "\nPressione ENTER para continuar."
                )

                continue

            pasta_destino = Path(
                caminho_destino
            )

            if not pasta_destino.is_dir():

                print(
                    "\nO diretório informado "
                    "não existe."
                )

                input(
                    "\nPressione ENTER para continuar."
                )

                continue

            break

        if gravar_preset:

            registrar_acao(
                acoes_preset,
                "destino",
                {
                    "caminho": caminho_destino
                }
            )

    if not pasta_destino.is_dir():

        print(
            "\nA pasta de destino não existe."
        )

        input(
            "\nPressione ENTER para continuar."
        )

        return

    data_backup = datetime.now().strftime(
        "%d_%m_%Y"
    )

    nome_backup = (
        f"{mundo_escolhido.name} "
        f"({data_backup})"
    )

    destino_backup = (
        pasta_destino /
        nome_backup
    )

    backups_existentes = [
        pasta
        for pasta in pasta_destino.iterdir()
        if pasta.is_dir()
        and pasta.name.startswith(
            f"{mundo_escolhido.name} ("
        )
    ]

    if backups_existentes:

        print(
            "\nBackups existentes encontrados:\n"
        )

        for backup in backups_existentes:

            print(
                f"- {backup.name}"
            )

        if modo_execucao:

            try:

                acao = next(
                    acoes_execucao
                )

            except StopIteration:

                print(
                    "\nO preset não possui confirmação "
                    "para os backups existentes."
                )

                input(
                    "\nPressione ENTER para continuar."
                )

                return

            if acao.get(
                "tipo"
            ) != "confirmacao_backups_existentes":

                print(
                    "\nErro no preset."
                )

                input(
                    "\nPressione ENTER para continuar."
                )

                return

            dados = acao.get(
                "dados",
                {}
            )

            confirmacao = dados.get(
                "resposta"
            )

            print(
                "\nDeseja excluir os backups existentes "
                "e criar um novo? (n/s): "
                f"{confirmacao}"
            )

        else:

            confirmacao = input(
                "\nDeseja excluir os backups existentes "
                "e criar um novo? (n/s): "
            ).strip().lower()

            if gravar_preset:

                registrar_acao(
                    acoes_preset,
                    "confirmacao_backups_existentes",
                    {
                        "resposta": confirmacao
                    }
                )

        if confirmacao == "s":

            try:

                for backup in backups_existentes:

                    shutil.rmtree(
                        backup
                    )

            except Exception as erro:

                print(
                    "\nNão foi possível excluir "
                    "os backups existentes."
                )

                print(
                    f"Detalhes: {erro}"
                )

                input(
                    "\nPressione ENTER para continuar."
                )

                return

        elif confirmacao == "n":

            print(
                "\nOperação cancelada."
            )

            input(
                "\nPressione ENTER para continuar."
            )

            return

        else:

            print(
                "\nOpção inválida."
            )

            input(
                "\nPressione ENTER para continuar."
            )

            return

    try:

        print(
            "\nIniciando backup...\n"
        )

        progresso(
            mundo_escolhido,
            destino_backup
        )

        tamanho_original = calcular_tamanho(
            mundo_escolhido
        )

        tamanho_backup = calcular_tamanho(
            destino_backup
        )

        if tamanho_original != tamanho_backup:

            print(
                "\nO backup foi concluído, mas os tamanhos"
            )

            print(
                "dos arquivos não são iguais."
            )

            print(
                f"\nOriginal: "
                f"{formatar_tamanho(tamanho_original)}"
            )

            print(
                f"Backup: "
                f"{formatar_tamanho(tamanho_backup)}"
            )

            if modo_execucao:

                try:

                    acao = next(
                        acoes_execucao
                    )

                except StopIteration:

                    return

                if acao.get(
                    "tipo"
                ) == "erro_backup":

                    resposta = acao.get(
                        "dados",
                        {}
                    ).get(
                        "resposta"
                    )

                    if resposta == "Tentar novamente":

                        return realizar_backup(
                            gravar_preset=gravar_preset,
                            acoes_preset=acoes_preset,
                            modo_execucao=True,
                            acoes_execucao=acoes_execucao
                        )

                    return

            return

        print(
            "\n================================"
        )

        print(
            "       BACKUP CONCLUÍDO"
        )

        print(
            "================================"
        )

        print(
            f"\nMundo original: "
            f"{mundo_escolhido.name}"
        )

        print(
            f"Tamanho original: "
            f"{formatar_tamanho(tamanho_original)}"
        )

        print(
            f"\nBackup criado: "
            f"{destino_backup.name}"
        )

        print(
            f"Tamanho do backup: "
            f"{formatar_tamanho(tamanho_backup)}"
        )

        print(
            f"\nLocal: "
            f"{destino_backup}"
        )

    except Exception as erro:

        print(
            "\nNão foi possível realizar o backup."
        )

        print(
            f"Detalhes: {erro}"
        )

        if modo_execucao:

            try:

                acao = next(
                    acoes_execucao
                )

            except StopIteration:

                input(
                    "\nPressione ENTER para continuar."
                )

                return

            if acao.get(
                "tipo"
            ) == "erro_backup":

                resposta = acao.get(
                    "dados",
                    {}
                ).get(
                    "resposta"
                )

                if resposta == "Tentar novamente":

                    return realizar_backup(
                        gravar_preset=gravar_preset,
                        acoes_preset=acoes_preset,
                        modo_execucao=True,
                        acoes_execucao=acoes_execucao
                    )

                return

        else:

            print(
                "\n1. Tentar novamente"
            )

            print(
                "2. Cancelar operação"
            )

            opcao = input(
                "\nEscolha uma opção: "
            ).strip()

            if opcao == "1":

                return realizar_backup(
                    gravar_preset=gravar_preset,
                    acoes_preset=acoes_preset
                )

            return

    input(
        "\nPressione ENTER para continuar."
    )