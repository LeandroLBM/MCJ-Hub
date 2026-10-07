
def registrar_acao(acoes_preset, tipo, dados=None):

    passo = {
        "tipo": tipo,
        "dados": dados
    }

    acoes_preset.append(passo)