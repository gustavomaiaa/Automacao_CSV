import csv
from config.siope_layout import *
from src.escritor_csv import escrever_linha

def float_to_br(v: float) -> str:
    # mantém compatibilidade simples com SIOPE
    s = f"{float(v):.2f}".replace(".", ",")
    # tira ,00 se quiser (opcional)
    if s.endswith(",00"):
        return s[:-3]
    return s

def atualizar_receita_total(cols, receitas_map, auditor_writer):
    # planilha 1
    if cols[COL_PLANILHA] != "1":
        return False
    cod = cols[COL_CODIGO]
    if cod not in receitas_map:
        return False

    orcada, ate_mes = receitas_map[cod]

    antes_prev = cols[COL_PREV_ATUAL]
    antes_real = cols[COL_REALIZADA]

    cols[COL_PREV_ATUAL] = float_to_br(orcada)
    cols[COL_REALIZADA] = float_to_br(ate_mes)

    mudou = (cols[COL_PREV_ATUAL] != antes_prev) or (cols[COL_REALIZADA] != antes_real)
    if mudou:
        auditor_writer.writerow([cod, antes_prev, cols[COL_PREV_ATUAL], antes_real, cols[COL_REALIZADA]])
    return mudou

def atualizar_despesa_2384(cols, despesa_map, auditor_writer):
    if cols[COL_PLANILHA] != "2384":
        return False
    cod = cols[COL_CODIGO]
    if cod not in despesa_map:
        return False

    dot, emp, liq, pag = despesa_map[cod]
    a_dot, a_emp, a_liq, a_pag = cols[COL_DOT_ATUAL], cols[COL_EMPENHADO], cols[COL_LIQUIDADO], cols[COL_PAGO]

    cols[COL_DOT_ATUAL] = float_to_br(dot)
    cols[COL_EMPENHADO] = float_to_br(emp)
    cols[COL_LIQUIDADO] = float_to_br(liq)
    cols[COL_PAGO] = float_to_br(pag)

    mudou = (cols[COL_DOT_ATUAL], cols[COL_EMPENHADO], cols[COL_LIQUIDADO], cols[COL_PAGO]) != (a_dot, a_emp, a_liq, a_pag)
    if mudou:
        auditor_writer.writerow([cod, a_dot, cols[COL_DOT_ATUAL], a_emp, cols[COL_EMPENHADO], a_liq, cols[COL_LIQUIDADO], a_pag, cols[COL_PAGO]])
    return mudou