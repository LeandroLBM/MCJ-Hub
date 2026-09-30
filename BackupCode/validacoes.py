import shutil

def progresso(origem, destino):
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


def calcular_tamanho(pasta):
    tamanho = 0

    for arquivo in pasta.rglob("*"):
        if arquivo.is_file():
            tamanho += arquivo.stat().st_size
    return tamanho

def formatar_tamanho(tamanho):
    tamanho_gb = tamanho / (1024 ** 3)
    
    return f"({tamanho_gb:.2f} GB) - [{tamanho:,} bytes]"

def mostrar_alerta():
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