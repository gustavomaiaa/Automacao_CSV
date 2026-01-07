from config.siope_layout import COL_TIPO, COL_PLANILHA

def listar_planilhas_por_header(caminho_csv, ler_linhas):
    vistos = set()
    for _, cols in ler_linhas(caminho_csv):
        if len(cols) <= COL_PLANILHA:
            continue
        if cols[COL_TIPO] == "T":
            pid = cols[COL_PLANILHA]
            if pid not in vistos:
                vistos.add(pid)
                yield pid, cols