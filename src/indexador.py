from config.siope_layout import COL_TIPO, COL_CODIGO, COL_BIMESTRE

def indexar_novos(caminho_csv):
    index = {}

    from src.leitor_stream import ler_linhas

    for _, cols in ler_linhas(caminho_csv):
        if cols[COL_TIPO] != "D":
            continue

        codigo = cols[COL_CODIGO]
        bimestre = cols[COL_BIMESTRE]

        index[(codigo, bimestre)] = cols

    return index
