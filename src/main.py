import os
from datetime import datetime

from config.regras import *
from config.siope_layout import COL_TIPO
from src.leitor_stream import ler_linhas
from src.escritor_csv import escrever_linha
from src.siope_utils import log
from src.updaters import atualizar_receita_total, atualizar_despesa_2384

from src.fontes.receita_balanco_pdf import extrair_receita_balanco
from src.fontes.despesa_educacao_pdf import extrair_despesa_educacao

def pegar_primeiro_csv(pasta):
    arqs = [f for f in os.listdir(pasta) if f.lower().endswith(".csv")]
    if not arqs:
        raise RuntimeError(f"Nenhum CSV em {pasta}/")
    return os.path.join(pasta, arqs[0])

def achar_pdf(pasta, termo):
    termo = termo.lower()
    pdfs = [f for f in os.listdir(pasta) if f.lower().endswith(".pdf") and termo in f.lower()]
    return os.path.join(pasta, pdfs[0]) if pdfs else None

def main():
    os.makedirs("data/output", exist_ok=True)
    os.makedirs("logs", exist_ok=True)

    csv_alvo = pegar_primeiro_csv("data/original")
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    saida = os.path.join("data/output", os.path.basename(csv_alvo).replace(".csv", f"_ATUALIZADO_{ts}.csv"))

    # Carregar fontes opcionais
    receitas_map = {}
    despesa_map = {}

    if ATIVAR_RECEITA_TOTAL:
        pdf_receita = achar_pdf("data/pdf", "balanco") or achar_pdf("data/pdf", "consolid")
        if pdf_receita and os.path.exists(pdf_receita):
            log(f"Fonte Receita (PDF): {pdf_receita}")
            receitas_map = extrair_receita_balanco(pdf_receita)
            log(f"Códigos de receita extraídos: {len(receitas_map)}")
        else:
            msg = "Faltou PDF de receita (balanço). Receita Total não será atualizada."
            log(msg)
            if FALTA_FONTE == "error":
                raise RuntimeError(msg)

    if ATIVAR_DESPESA_2384:
        pdf_despesa = achar_pdf("data/pdf", "despesa")
        if pdf_despesa and os.path.exists(pdf_despesa):
            log(f"Fonte Despesa (PDF): {pdf_despesa}")
            despesa_map = extrair_despesa_educacao(pdf_despesa)
            log(f"Códigos de despesa extraídos: {len(despesa_map)}")
        else:
            msg = "Faltou PDF de despesa. Despesa 2384 não será atualizada."
            log(msg)
            if FALTA_FONTE == "error":
                raise RuntimeError(msg)

    # Auditorias
    aud_receita_path = "logs/auditoria_receita.csv"
    aud_despesa_path = "logs/auditoria_despesa.csv"

    import csv as _csv
    with open(aud_receita_path, "w", encoding="utf-8", newline="") as ar, \
         open(aud_despesa_path, "w", encoding="utf-8", newline="") as ad:

        wr = _csv.writer(ar, delimiter=";")
        wd = _csv.writer(ad, delimiter=";")
        wr.writerow(["codigo", "prev_antes", "prev_depois", "real_antes", "real_depois"])
        wd.writerow(["codigo", "dot_antes", "dot_depois", "emp_antes", "emp_depois", "liq_antes", "liq_depois", "pag_antes", "pag_depois"])

        subs_r = 0
        subs_d = 0

        log("Aplicando alterações (streaming)...")
        with open(saida, "w", encoding="latin1", newline="") as out:
            for _, cols in ler_linhas(csv_alvo):
                if cols[COL_TIPO] == "V":
                    if receitas_map:
                        if atualizar_receita_total(cols, receitas_map, wr):
                            subs_r += 1
                    if despesa_map:
                        if atualizar_despesa_2384(cols, despesa_map, wd):
                            subs_d += 1

                escrever_linha(out, cols)

    log(f"OK. Substituições Receita: {subs_r} | Substituições Despesa 2384: {subs_d}")
    log(f"Saída: {saida}")
    log(f"Auditorias: {aud_receita_path} | {aud_despesa_path}")

if __name__ == "__main__":
    main()