def ler_linhas(caminho):
    with open(caminho, encoding="latin1", errors="replace") as f:
        for numero, linha in enumerate(f, start=1):
            linha = linha.strip()
            if not linha:
                continue
            yield numero, linha.split(";")