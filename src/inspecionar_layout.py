import os 
from collections import Counter

BASES = [
    ("ORIGINAL", "data/original"),
    ("NOVOS", "data/novos_valores"),
]

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def ler_linhas_raw(caminho):
    with open(caminho, encoding="latin1", errors="replace") as f:
        for n, linha in enumerate(f, start=1):
            linha = linha.rstrip("\n")
            if not linha.strip():
                continue
            yield n, linha

def inspecionar_arquivo(caminho):
    cont_cols = Counter()
    tipos = Counter()
    min_cols = 10**9
    max_cols = 0

    exemplos_ruins = []
    total_linhas = 0

    for n, linha in ler_linhas_raw(caminho):
        total_linhas += 1

        #tenta separar por ; (SIOPE usa)
        cols =linha.split(";")
        k = len(cols)

        cont_cols[k] += 1
        min_cols = min(min_cols, k)
        max_cols = max(max_cols, k)

        #tipo = primeira coluna
        tipo = cols[0].strip() if k > 0 else ""
        if tipo:
            tipos[tipo] += 1

        #registra exemplos suspeitos (muito poucas colunas)
        if k < 4 and len(exemplos_ruins) < 5:
            exemplos_ruins.append((n,k,linha[:200]))

        # "layout esperado" = quantidade de colunas mais frequentes (modo)
        expected_cols = cont_cols.most_common(1)[0][0] if cont_cols else 0

    return {
        "total_linhas": total_linhas,
        "expected_cols": expected_cols,
        "min_cols": min_cols if total_linhas else 0,
        "max_cols": max_cols,
        "dist_cols": dict(cont_cols),
        "tipos": dict(tipos),
        "exemplos_ruins": exemplos_ruins,
    }

def main():
    relatorio_csv = os.path.join(LOG_DIR, "relatorio_layout.csv")
    relatorio_txt = os.path.join(LOG_DIR, "relatorio_layout_detalhado.txt")

    with open(relatorio_csv, "w", encoding="utf-8", newline="") as out_csv, \
            open(relatorio_txt, "w", encoding="utf-8", newline="") as out_txt:
        
        out_csv.write("grupo;arquivo;total_linhas;expected_cols;min_cols;max_cols;tipos\n")

        for grupo, pasta in BASES:
            if not os.path.isdir(pasta):
                continue
            for nome in os.listdir(pasta):
                if not nome.lower().endswith(".csv"):
                    continue


                caminho = os.path.join(pasta, nome)
                info = inspecionar_arquivo(caminho)

                tipos_str = ",".join([f"{k}:{v}" for k, v in sorted(info["tipos"].items())])
                out_csv.write(f"{grupo};{nome};{info['total_linhas']};{info['expected_cols']};{info['min_cols']};{info['max_cols']};{tipos_str}\n")

                out_txt.write(f"\n=== {grupo} / {nome} ===\n")
                out_txt.write(f"Total linhas: {info['total_linhas']}\n")
                out_txt.write(f"Colunas (modo/esperado): {info['expected_cols']}\n")
                out_txt.write(f"Min colunas: {info['min_cols']} | Max colunas: {info['max_cols']}\n")
                out_txt.write(f"Distribuição colunas: {info['dist_cols']}\n")
                out_txt.write(f"Tipos: {info['tipos']}\n")
                if info["exemplos_ruins"]:
                    out_txt.write("Exemplos suspeitos (linha, colunas, trecho):\n")
                    for n, k, trecho in info["exemplos_ruins"]:
                        out_txt.write(f" - L{n} ({k} cols): {trecho}\n")

    print("OK! Relatórios gerados em:")
    print(" - logs/relatorio_layout.csv")
    print(" - logs/relatorio_layout_detalhado.txt")

if __name__ == "__main__":
    main() 