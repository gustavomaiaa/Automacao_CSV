# src/auditoria.py
from config.siope_layout import (
    COL_CODIGO, COL_BIMESTRE,
    COL_PREVISAO, COL_REALIZADA, COL_DED_FUNDEB, COL_OUTRAS_DED, COL_INTRA
)

CAMPOS_VALORES = [
    ("previsao", COL_PREVISAO),
    ("realizada", COL_REALIZADA),
    ("ded_fundeb", COL_DED_FUNDEB),
    ("outras_ded", COL_OUTRAS_DED),
    ("intra", COL_INTRA),
]

def diff_valores(cols_antiga, cols_nova):
    diffs = []
    for nome, idx in CAMPOS_VALORES:
        a = cols_antiga[idx] if idx < len(cols_antiga) else ""
        b = cols_nova[idx] if idx < len(cols_nova) else ""
        if a != b:
            diffs.append((nome, a, b))
    return diffs

def escrever_cabecalho_auditoria(arq):
    arq.write("arquivo;linha;codigo;bimestre;campo;antes;depois\n")

def registrar_auditoria(arq, nome_arquivo, numero_linha, cols_antiga, cols_nova):
    codigo = cols_antiga[COL_CODIGO]
    bimestre = cols_antiga[COL_BIMESTRE]
    for campo, antes, depois in diff_valores(cols_antiga, cols_nova):
        arq.write(f"{nome_arquivo};{numero_linha};{codigo};{bimestre};{campo};{antes};{depois}\n")